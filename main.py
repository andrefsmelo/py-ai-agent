import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("content", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.content)])]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info,
                               schema_get_file_content,
                               schema_run_python_file,
                               schema_write_file])
    
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if response.usage_metadata is None:
                raise RuntimeError("API request has failed.")

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            
            function_call  = response.function_calls
            if function_call == None and len(response.text) > 0:
                print(f"{response.text}")
                break

            if args.verbose:
                print(f"User prompt: {args.content}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            result_list = []
            for function_call_part in function_call:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                function_call_result = call_function(function_call_part)

                if not function_call_result.parts[0].function_response.response:
                    raise RuntimeError(f"Failed to obtain function results from {function_call_part.name}")
        
                result_list.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=[types.Part(text=str(result_list))]))

        except Exception as e:
            print(f"Error: {e}") 

if __name__ == "__main__":
    main()

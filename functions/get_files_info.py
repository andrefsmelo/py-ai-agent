import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{full_path}" is not a directory'
    
    try:
        entries = []
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            entries.append(f"  - {file}: file_size={size} bytes, is_dir={is_dir}")    
    
        header = "Result for current directory:" if directory in [".", "", None] else f'Result for directory "{directory}":'
        return "\n".join([header] + entries)

    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself using .",
            ),
        },
    ),
)
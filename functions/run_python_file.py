import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    result = ""

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not os.path.abspath(full_path).endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python", full_path] + args, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if completed_process.stdout:
            result += f"STDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            result += " " if len(result) > 0 else ""
            result += f"STDERR: {completed_process.stderr}"
        if completed_process.returncode != 0:
            result += " " if len(result) > 0 else ""
            result += f"Process exited with code {completed_process.returncode}"
        if len(result) == 0:
            result += "No output produced"

    except Exception as e:
        return f"Error: executing Python file: {e}"

    return result

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory. Maximum execution time is 30 seconds.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file.",
            ),
        }
    ),
)
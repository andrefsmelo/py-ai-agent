import os
import subprocess

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
        completed_process = subprocess.run(f"python {full_path}", args=args, capture_output=True, timeout=30, stdout=True, stderr=True)
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

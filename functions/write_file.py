import os 

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(full_path, "w") as f:
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
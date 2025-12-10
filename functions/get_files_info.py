import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{full_path}" is not a directory'
    
    try:
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            print(f"{file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
    
    except Exception as e:
        return f"Error: {e}"
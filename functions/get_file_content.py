import os
from utils.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Safety checks
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        is_file = os.path.isfile(target_file)

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not is_file:
            return f'Error: File not found or is not a regular file: "{target_file}"'
        
        
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

    except Exception as e:
        return f"Error: Failed to get file info: {e}"
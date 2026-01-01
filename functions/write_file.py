import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file specified relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Safety checks
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        is_existing_dir = os.path.isdir(target_file)

        if not valid_target_dir:
            return f'Error: Cannot write to "{target_file}" as it is outside the permitted working directory'
        if is_existing_dir:
            return f'Error: Cannot write to "{target_file}" as it is a directory'
        
        file_path_list = target_file.split("/")
        dir_path = "/".join(file_path_list[:-1])
        os.makedirs(dir_path, exist_ok=True)
            
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{target_file}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: Failed to write to {file_path}. {e}"
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Safety checks
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        is_dir = os.path.isdir(target_dir)

        if not valid_target_dir:
            return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
        if not is_dir:
            return f'Error: "{target_dir}" is not a directory'
    
        files = os.listdir(target_dir)
        file_info_list = []
        for file in files:
            file_path = f"{target_dir}/{file}"
            size = os.path.getsize(file_path)
            is_directory = os.path.isdir(file_path)
            file_info = f"  - {file}: file_size={size} bytes, is_dir={is_directory}"
            file_info_list.append(file_info)
        return f"Results for '{directory}' dir:\n" + "\n".join(file_info_list)
    except Exception as e:
        return f"Error: Failed to get directory info: {e}"

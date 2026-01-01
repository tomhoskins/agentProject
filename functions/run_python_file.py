import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file specified relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments for the function to be run.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Safety checks
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        file_exists = os.path.isfile(target_file)
        is_python_script = file_path[-3:] == ".py"

        if  not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not file_exists:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not is_python_script:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        
        completed_process = subprocess.run(command, capture_output=True, text=True, cwd=working_dir_abs, timeout=30)

        output_str = ""
        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}\n"
        if (not completed_process.stdout) and (not completed_process.stderr):
            output_str += "No output produced\n"
        if not output_str:
            output_str += f"STDOUT:\n{completed_process.stdout}\n"
            output_str += f"STDERR:\n{completed_process.stderr}\n"
        return output_str
    
    except Exception as e:
        return f"Error: executing python file: {e}"
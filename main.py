import os
import sys
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils.prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("gemini api key not found")

    client = genai.Client(api_key=api_key)
    current_prompt = args.user_prompt
    messages = []
    for _ in range(20):
        # call the model, handle responses, etc.
        messages.append(types.Content(role="user", parts=[types.Part(text=current_prompt)]))
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                ),
            )

        if response.usage_metadata == None:
            raise RuntimeError("API call error")
        if args.verbose:
            print(f"User prompt:\n{messages}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Add response candidates to message history
        candidates = response.candidates
        if candidates:
            for candidate in candidates:
                messages.append(candidate.content)
        
        function_calls = response.function_calls
        if function_calls:
            function_results = []
            for function_call in function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception(f"function_call_result of func \'{function_call.name}\' does not contain a parts list.")
                if function_call_result.parts[0].function_response == None:
                    raise Exception(f"function_response of func \'{function_call.name}\' is None.")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception(f"function_response.response of func \'{function_call.name}\' is None.")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            # Add function calls to message history
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(f"Final Response:\n{response.text}")
            return
        
    print("Maximum iterations reached. Exiting program.")
    sys.exit(1)

if __name__ == "__main__":
    main()

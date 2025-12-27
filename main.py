import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils.prompts import system_prompt

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    load_dotenv()
    #prompt = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("gemini api key not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
    
    if response.usage_metadata == None:
        raise RuntimeError("API call error")
    if args.verbose:
        print(f"User prompt:\n{messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()

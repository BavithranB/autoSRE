import os
import sys
from openai import OpenAI

def summarize_file(file_path: str) -> None:
    """
    Read the file at ⁠ file_path ⁠, send its contents to GPT-4.1-mini for summarization
    using the OpenAI Python SDK v1.x interface, and print the result. If the text
    defines a function, the AI will also describe its input and output parameters.
    """
    # 1. Read file contents
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}")
        return
    except PermissionError:
        print(f"Error: permission denied when accessing: {file_path}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading {file_path!r}: {e}")
        return

    # 2. Instantiate OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # or OpenAI() if env var is set

    # 3. Build messages for Chat Completion
    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Please provide a clear, concise summary of the user‐supplied text. "
            "If the text defines a program function, also describe that function’s inputs and outputs."
        )
    }
    user_msg = {"role": "user", "content": content}

    # 4. Make the API call using the new client interface
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[system_msg, user_msg],
            temperature=0.2,
            max_tokens=500,
        )
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return

    # 5. Print the AI-generated summary
    summary = resp.choices[0].message.content.strip()
    print(summary)


if _name_ == "_main_":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <path/to/yourfile.ext>")
    else:
        summarize_file(sys.argv[1])
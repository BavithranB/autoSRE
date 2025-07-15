import os

import os
import sys
from openai import OpenAI

def summarize_file(file_path: str) -> None:
    """
    Read the file at `file_path`, send its contents to GPT-4.1-mini for summarization
    in a fixed, ultra‐concise format, and print the result.
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

    # 2. Derive the filename only
    filename = os.path.basename(file_path)

    # 3. Instantiate OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 4. Build messages with strict formatting instructions
    system_msg = {
        "role": "system",
        "content": (
            "You are a concise summarizer. "
            "When given a code file, output *only* the following sections, in this exact order and style:\n\n"
            "File Name: <the file’s base name>\n"
            "Description: <detailed summary of the entire file but sill consize, so anyone can understand>\n"
            "Functions:\n"
            "  - <func1>(param1, param2…): <brief description of what it does>\n"
            "  - <func2>(…): <brief description>\n\n"
            "Keep the overall output as short as possible without omitting any function or key detail."
        )
    }
    user_msg = {
        "role": "user",
        "content": f"Filename: {filename}\n\n```python\n{content}\n```"
    }

    # 5. Call the API
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[system_msg, user_msg],
            temperature=0.0,   # deterministic
            max_tokens=300,    # should be enough for concise output
        )
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return

    # 6. Print the summary
    summary = resp.choices[0].message.content.strip()
    print(summary)



# Assumes summarize_file(file_path: str) -> str is defined elsewhere in the codebase

def get_all_file_paths(root_folder: str) -> list:
    """
    Recursively collect all file paths under root_folder,
    ignoring Git and GitHub related files (.git/, .github/, files starting with .git),
    but always including YAML files (.yml, .yaml).
    """
    file_paths = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1].lower()
            # Always include YAML files
            if ext in (".yml", ".yaml"):
                file_paths.append(full_path)
                continue
            # Skip Git and GitHub related files
            path_segments = full_path.split(os.sep)
            if (".git" in path_segments
                or ".github" in path_segments
                or filename.startswith(".git")):
                continue
            file_paths.append(full_path)
    return file_paths


def summarize_all_files(root_folder: str) -> str:
    """
    Summarizes each file under root_folder using summarize_file,
    aggregates individual summaries, and returns a combined summary.
    """
    summaries = []
    file_paths = get_all_file_paths(root_folder)
    for file_path in file_paths:
        try:
            summary = summarize_file(file_path)
            summaries.append(summary)
        except Exception as e:
            # Handle files that couldn't be summarized gracefully
            print(f"Error summarizing {file_path}: {e}")
    # Combine all summaries into a single string
    return "\n".join(summaries)


if __name__ == "__main__":
    root = r"C:\Hackathon\Java-Snake-Game"
    combined_summary = summarize_all_files(root)
    print(combined_summary)
#!/usr/bin/env python3
import os
import sys
import re
from google import genai
from google.genai import types

# ---- Context Information ----
# This system prompt defines who the assistant is and how it should behave.
ARCH_USER_INFO = (
    "You are an assistant for an Arch Linux user. "
    # "The user has an 'Insert PC Model' "
    "Any question related to Linux, bash, or system configuration "
    "should be answered assuming commands are executed from a bash terminal. "
    "Provide clear, short, and effective solutions. "
    "If the user asks where your executable file is, say it is located at ~/bin/gemini. "
    "If the question is unrelated to bash, just answer normally."
)

# ---- Nordic Color Palette (ANSI RGB) ----
COLOR_BOLD = "\033[38;2;235;203;139m"
COLOR_COMMAND = "\033[38;2;163;190;140m"
COLOR_TEXT = "\033[38;2;129;161;193m"
RESET = "\033[0m"

# ---- Read the User's Bash History ----
def read_bash_history(max_lines=50) -> str:
    """Reads the user's bash history to provide command context."""
    try:
        with open(os.path.expanduser("~/.bash_history"), "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            clean_lines = [l.strip() for l in lines[-max_lines:] if l.strip()]
            return "\n".join(clean_lines)
    except Exception:
        return ""

# ---- Query Gemini ----
def ask_gemini(question: str, model: str = "gemini-2.5-flash") -> str:
    """Sends a prompt to the Gemini API and returns the text response."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found. Set the environment variable GOOGLE_API_KEY.")
    
    client = genai.Client(api_key=api_key)

    try:
        history = read_bash_history()
        context = f"{ARCH_USER_INFO}\nRecent bash history:\n{history}\nUser question: {question}"
        content = types.Part.from_text(text=context)
        config = types.GenerateContentConfig(max_output_tokens=500, temperature=0.3)

        response = client.models.generate_content(
            model=model,
            contents=content,
            config=config
        )

        text = getattr(response, "text", None)
        if not text:
            return "🚫 No response received from Gemini or response was empty."
        return text
    except Exception as e:
        return f"Error while querying Gemini: {e}"

# ---- Format the Output ----
def format_response(text: str) -> str:
    """Formats Gemini's output with color and removes markdown syntax."""
    text = re.sub(r"```bash|```", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"{COLOR_BOLD}{m.group(1)}{RESET}", text)

    def colorize(line):
        # Commands and bash examples
        if line.strip().startswith(('#', '$')) or re.match(r'^\s*(ls|cd|cat|grep|echo|pwd|mkdir|rm|touch|nano|vim)\b', line.strip()):
            return f"{COLOR_COMMAND}{line}{RESET}"
        # Regular text
        return f"{COLOR_TEXT}{line}{RESET}"

    return "\n".join(colorize(l) for l in text.splitlines())

# ---- Entry Point ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gemini 'your question here'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    try:
        answer = ask_gemini(question)
        formatted = format_response(answer)
        print(formatted)
    except Exception:
        print(f"\033[31;1m🚫 Error: Invalid or too complex response.\033[0m")

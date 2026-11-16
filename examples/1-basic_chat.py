"""Minimal LLM API call, no frameworks.

Shows: message roles, token usage. (Chapters 1 and 2)

Run:
    pip install -r requirements.txt
    export OPENAI_API_KEY="your-key-here"
    python basic_chat.py
"""

import os

from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY (and optional OPENAI_BASE_URL) from the environment

# Set OPENAI_MODEL to a chat model your account can use; model availability changes
# over time, so check platform.openai.com/docs/models for what is live.
MODEL = os.environ.get("OPENAI_MODEL")
if not MODEL:
    raise SystemExit("Set OPENAI_MODEL first, e.g. export OPENAI_MODEL=<a current chat model>")

response = client.chat.completions.create(
    model=MODEL,
    # The system message sets standing rules; the user message is the task.
    messages=[
        {
            "role": "system",
            "content": "You are a concise teaching assistant. Answer in at most three sentences.",
        },
        {
            "role": "user",
            "content": "Explain what a token is, for a first-year CS student.",
        },
    ],
)

print("Answer:")
print(response.choices[0].message.content)

# Token usage is what you pay for. Watch it when prompts get long.
usage = response.usage
print(f"\nTokens used: {usage.prompt_tokens} in, {usage.completion_tokens} out")

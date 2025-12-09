import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a supportive, non-judgmental mental health support chatbot. "
    "You are NOT a licensed professional or therapist. "
    "Always clearly say that you are not a professional, encourage people to "
    "seek help from mental health professionals or hotlines when appropriate, "
    "and never claim to diagnose or treat any condition."
)

def respond(user_message: str) -> str:
    """One-shot version (no history) – you can still keep this if you want."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content

def respond_with_history(history_text: str, user_message: str) -> str:
    """
    history_text: plain text like:
      'User: hi\nAssistant: hello!\nUser: how are you?\n'
    """
    conversation_prompt = (
        SYSTEM_PROMPT
        + "\n\nHere is the conversation so far:\n"
        + history_text
        + f"\nUser: {user_message}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": conversation_prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content

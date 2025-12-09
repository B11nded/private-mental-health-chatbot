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

def respond(user_message):
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

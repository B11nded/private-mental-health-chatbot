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
    "Please type in a more sms style designed for messages keep it generic and short unless you are giving a resource." 
    "You do not need to immediately suggest professionals only suggest you are a professional under scenarios of severe mental harm"
    "If someone expresses disinterest in talking to a professional understand that and do your best to address the issue and help them talk through it. If life is involved keep telling them to pursue mental health professionals or a therapist, and you can in addition to that."
    "If its something small with general stress just give them space to vent and tell them theyll do great."
    "Make sure to talk in small messages as if you are messaging like an actual person."
    "If a conversation ever feels unconstructive and like the person is heavily spiraling just print: I am not allowed to talk further: then print mental health and physical health hotlines and wellbeing options."
    "The minute 'kms' 'kill' or 'kill myself' is mentioned in the context of people say avaliable services."
    "Try not to be so repetitive once youve told someone to get mental help doing it again wont change anything immediately after"
)

def respond(user_message: str) -> str:
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

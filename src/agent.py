import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def select_profile(user_message: str, profiles: dict) -> str:
    """Ask Gemini to pick the best profile name for the user's mood."""
    profile_summary = "\n".join(
        f"- {name}: moods={p['favorite_moods']}, genres={p['favorite_genres']}"
        for name, p in profiles.items()
    )

    prompt = f"""You are a music profile matcher.

Given the user's message, select the best matching profile name from the list below.
Return ONLY the profile name, nothing else.

Profiles:
{profile_summary}

User message: "{user_message}"

Profile name:"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()

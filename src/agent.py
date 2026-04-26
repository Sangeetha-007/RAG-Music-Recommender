import os
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

load_dotenv()

from recommender import load_songs, recommend_songs

_client = None

def _get_client():
    # _get_client() creates a new client on every call, and the previous one gets closed. 
    # Fix: cache it so it's only created once.
    global _client
    if _client is None:
        try:
            import streamlit as st
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = os.getenv("GEMINI_API_KEY", "")
        _client = genai.Client(api_key=api_key)
    return _client


def _call_gemini(prompt: str) -> str:
    global _client
    try:
        return _get_client().models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        ).text.strip()
    except genai_errors.ClientError as e:
        code = getattr(e, "status_code", 0)
        if code == 429:
            raise RuntimeError("Gemini quota exceeded. Please try again later.")
        elif code in (401, 403):
            raise RuntimeError("Invalid API key. Check your GEMINI_API_KEY.")
        elif code == 404:
            raise RuntimeError("Gemini model not found. Check the model name in agent.py.")
        raise RuntimeError(f"Gemini API error ({code}): {e}")
    except Exception as e:
        if "client has been closed" in str(e).lower():
            _client = None
            raise RuntimeError("Connection was reset. Please try again.")
        raise RuntimeError(f"Unexpected error: {e}")


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

    return _call_gemini(prompt)


def get_recommendations(
    profile_name: str,
    profiles: dict,
    songs_path: str,
    k: int = 5
) -> Tuple[str, List[Tuple[Dict, float, str]]]:
    """Look up the selected profile and return top-k recommended songs."""
    profile = profiles[profile_name]
    songs = load_songs(songs_path)
    results = recommend_songs(profile, songs, k=k)
    return profile_name, results


def format_response(
    user_message: str,
    profile_name: str,
    results: List[Tuple[Dict, float, str]]
) -> str:
    """Ask Gemini to turn the top-k results into a natural language recommendation."""
    song_list = "\n".join(
        f"{i+1}. '{s['title']}' by {s['artist']} (genre: {s['genre']}, mood: {s['mood']}, score: {score:.2f})"
        for i, (s, score, _) in enumerate(results)
    )

    prompt = f"""You are a friendly music assistant.

The user said: "{user_message}"
You matched them to the '{profile_name}' listening profile.
Here are their top song recommendations:

{song_list}

Write a short, friendly response (3-5 sentences) recommending these songs and explaining why they fit the user's mood.
Do not add any songs that are not in the list above."""

    return _call_gemini(prompt)

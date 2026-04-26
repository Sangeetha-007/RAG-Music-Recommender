import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from main import PROFILES
from agent import select_profile, get_recommendations, format_response

SONGS_PATH = os.path.join(os.path.dirname(__file__), "../data/songs.csv")

st.set_page_config(
    page_title="Vinyl Vibes — Music Recommender",
    page_icon="🎵",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Special+Elite&display=swap');

.stApp {
    background-color: #0d0804;
    background-image:
        radial-gradient(ellipse at 20% 50%, #1f0e06 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, #1a0c05 0%, transparent 50%);
    color: #f5e6c8;
    font-family: 'Special Elite', monospace;
}

#MainMenu, footer, header { visibility: hidden; }

.vintage-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #d4a017;
    text-align: center;
    letter-spacing: 0.05em;
    text-shadow: 0 0 30px rgba(212, 160, 23, 0.4);
    margin-bottom: 0;
}

.vintage-subtitle {
    font-family: 'Special Elite', monospace;
    font-size: 0.85rem;
    color: #8b6914;
    text-align: center;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.divider {
    border: none;
    border-top: 1px solid #3d2314;
    margin: 1.5rem 0;
}

.stTextInput > div > div > input {
    background-color: #1a0f08 !important;
    border: 1px solid #5a3a1a !important;
    border-radius: 2px !important;
    color: #f5e6c8 !important;
    font-family: 'Special Elite', monospace !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.5) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #d4a017 !important;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.5), 0 0 8px rgba(212,160,23,0.2) !important;
}

.stTextInput label {
    color: #c8a060 !important;
    font-family: 'Special Elite', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
}

.stButton > button {
    background: linear-gradient(180deg, #8b4513 0%, #5c2d0a 100%) !important;
    border: 1px solid #d4a017 !important;
    border-radius: 2px !important;
    color: #f5e6c8 !important;
    font-family: 'Special Elite', monospace !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(180deg, #a0521a 0%, #7a3d10 100%) !important;
    box-shadow: 0 0 12px rgba(212, 160, 23, 0.3) !important;
}

.profile-badge {
    background: linear-gradient(135deg, #2a1a0e, #1a0f08);
    border: 1px solid #d4a017;
    border-radius: 2px;
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    text-align: center;
}

.profile-label {
    font-family: 'Special Elite', monospace;
    font-size: 0.7rem;
    color: #8b6914;
    letter-spacing: 0.3em;
    text-transform: uppercase;
}

.profile-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #d4a017;
    margin-top: 0.25rem;
}

.song-card {
    background: linear-gradient(135deg, #1f1008, #160c05);
    border: 1px solid #3d2314;
    border-left: 3px solid #d4a017;
    border-radius: 2px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.track-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #5a3a1a;
    min-width: 2rem;
    text-align: center;
}

.song-info { flex: 1; }

.song-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #f5e6c8;
    font-weight: 700;
}

.song-artist {
    font-family: 'Special Elite', monospace;
    font-size: 0.8rem;
    color: #a07840;
    margin-top: 0.1rem;
}

.song-meta {
    font-family: 'Special Elite', monospace;
    font-size: 0.7rem;
    color: #5a3a1a;
    margin-top: 0.3rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.song-score {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #d4a017;
    text-align: right;
}

.response-text {
    font-family: 'Special Elite', monospace;
    font-size: 0.95rem;
    color: #c8a060;
    line-height: 1.7;
    border-left: 2px solid #5a3a1a;
    padding-left: 1rem;
    margin: 1.5rem 0;
}

.error-box {
    background: #1a0808;
    border: 1px solid #8b1a1a;
    border-radius: 2px;
    padding: 1rem;
    color: #c87070;
    font-family: 'Special Elite', monospace;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="vintage-title">◈ Vinyl Vibes ◈</div>', unsafe_allow_html=True)
st.markdown('<div class="vintage-subtitle">— A.I. powered music recommender —</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
user_message = st.text_input(
    "How are you feeling?",
    placeholder="e.g. I'm feeling really stressed after work...",
)

submitted = st.button("Drop the Needle")

# ── Processing ────────────────────────────────────────────────────────────────
if submitted and user_message.strip():
    try:
        with st.spinner("Reading the room..."):
            profile_name = select_profile(user_message, PROFILES)

        if profile_name not in PROFILES:
            st.markdown(f'<div class="error-box">Could not match a profile. Got: "{profile_name}"</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="profile-badge">
                <div class="profile-label">Matched Profile</div>
                <div class="profile-name">{profile_name.replace("_", " ").title()}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Pulling records from the archive..."):
                _, results = get_recommendations(profile_name, PROFILES, SONGS_PATH)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            for i, (song, score, _) in enumerate(results, start=1):
                st.markdown(f"""
                <div class="song-card">
                    <div class="track-num">{i}</div>
                    <div class="song-info">
                        <div class="song-title">{song['title']}</div>
                        <div class="song-artist">{song['artist']}</div>
                        <div class="song-meta">{song['genre']} · {song['mood']}</div>
                    </div>
                    <div class="song-score">{score:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            with st.spinner("Composing your message..."):
                response = format_response(user_message, profile_name, results)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown(f'<div class="response-text">{response}</div>', unsafe_allow_html=True)

    except Exception as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            st.markdown('<div class="error-box">Gemini API quota exceeded. Please try again later or enable billing at ai.google.dev.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">Error: {err}</div>', unsafe_allow_html=True)

elif submitted and not user_message.strip():
    st.markdown('<div class="error-box">Please describe how you\'re feeling first.</div>', unsafe_allow_html=True)

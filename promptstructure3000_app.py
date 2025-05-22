# promptstructure3000_app.py — v4
# ---------------------------------------------
# Fixes:
#   • Copy Prompt now copies reliably using JS and shows a small temporary label instead of an alert popup.
#   • Everything else unchanged (responsive UI, tooltips, sentence connectors).

import streamlit as st
import pandas as pd
import random, json, time

st.set_page_config(page_title="PromptStructure3000", page_icon="🪄", layout="wide")

# ---------- Load token buckets ----------
@st.cache_data
def load_tokens():
    df = pd.read_csv("prompt_token_library_wide_v2.csv")
    return {col: df[col].dropna().tolist() for col in df.columns}

buckets = load_tokens()

# ---------- Global style ----------
st.markdown(
    '''
    <style>
    :root {
        --primary-blue: #0A62C1;
        --light-grey: #F4F6F8;
    }
    body, .stTextInput>div>div>input, .stTextArea textarea {
        background-color: var(--light-grey);
    }
    .stButton>button {
        background-color: var(--primary-blue);
        color: white;
    }
    .stButton>button:hover {
        filter: brightness(115%);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.title("PromptStructure3000")

# ---------- Free-text inputs ----------
subject = st.text_input("Subject", placeholder="e.g., a vintage camera on a wooden desk", help="Who or what the image depicts. Include any action.")
extra_notes = st.text_area("Extra notes (optional)", help="Additional descriptors you want in the prompt.")

# ---------- Multiselect buckets ----------
selections = {}
left, right = st.columns(2)

bucket_order = [
    "Materials & Textures",
    "Composition & Framing",
    "Lighting",
    "Style & Realism",
    "Atmosphere / Extras",
    "FX & Details / Overlays / Imperfections",
    "Shot Type & Angle",
    "Aesthetics",
    "Technical / Output"
]

helpers = {
    "Materials & Textures": "Surface finish, physical makeup.",
    "Composition & Framing": "Camera angle, crop, perspective.",
    "Lighting": "Source, direction, mood.",
    "Style & Realism": "Overall photographic style.",
    "Atmosphere / Extras": "Effects, ambience, imperfections.",
    "FX & Details / Overlays / Imperfections": "Post‑process or shader effects.",
    "Shot Type & Angle": "Formal shot classifications.",
    "Aesthetics": "Visual subculture vibe.",
    "Technical / Output": "Aspect ratio."
}

for i, bucket in enumerate(bucket_order):
    col = left if i % 2 == 0 else right
    with col:
        selections[bucket] = st.multiselect(bucket, buckets.get(bucket, []), help=helpers.get(bucket, ""))

# ---------- Actions row ----------
a1, a2, a3 = st.columns(3)

with a1:
    if st.button("Random Fill Empty Buckets"):
        for bucket, tokens in buckets.items():
            if not selections[bucket] and tokens:
                choice = random.choice(tokens)
                selections[bucket].append(choice)
                st.session_state[bucket] = selections[bucket]

with a2:
    if st.button("Clear All"):
        for bucket in bucket_order:
            st.session_state[bucket] = []
        if 'copied_flag' in st.session_state:
            del st.session_state['copied_flag']
        st.experimental_rerun()

# ---------- Build prompt ----------
parts = []
if subject:
    parts.append(subject)

connector_map = {
    "Materials & Textures": "featuring",
    "Composition & Framing": "shot as",
    "Lighting": "lit by",
    "Style & Realism": "in the style of",
    "Atmosphere / Extras": "with",
    "FX & Details / Overlays / Imperfections": "using",
    "Shot Type & Angle": "framed as",
    "Aesthetics": "evoking",
    "Technical / Output": "with an aspect ratio of"
}

for bucket in bucket_order:
    tokens = selections.get(bucket, [])
    if tokens:
        parts.append(f"{connector_map[bucket]} {', '.join(tokens)}")

if extra_notes:
    parts.append(extra_notes)

prompt = ", ".join(parts) + "."

st.markdown("### Final Prompt")
st.code(prompt if prompt.strip() != "." else "(Prompt will appear here)")

# ---------- Copy Prompt button ----------
with a3:
    if st.button("Copy Prompt"):
        copy_js = f"navigator.clipboard.writeText({json.dumps(prompt)})"
        st.components.v1.html(f'<script>{copy_js}</script>', height=0)
        st.session_state['copied_flag'] = True

# ephemeral copied label
if st.session_state.get('copied_flag'):
    copied_placeholder = st.empty()
    copied_placeholder.markdown("<span style='color:var(--primary-blue); font-weight:bold;'>Prompt copied!</span>", unsafe_allow_html=True)
    time.sleep(2)
    copied_placeholder.empty()
    st.session_state['copied_flag'] = False

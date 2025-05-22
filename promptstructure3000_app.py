
import streamlit as st
import pandas as pd
import random, json

st.set_page_config(page_title="PromptStructure3000", page_icon="🪄", layout="centered")

@st.cache_data
def load_tokens():
    df = pd.read_csv("prompt_token_library_wide_v2.csv")
    return {col: df[col].dropna().tolist() for col in df.columns}

buckets = load_tokens()

st.title("PromptStructure3000")

# Free-text inputs
subject = st.text_input("Subject", placeholder="e.g., vintage camera on wooden desk")
extra_notes = st.text_area("Extra notes (optional)")

# Multiselect buckets
selections = {}
cols = st.columns(2)
for i, (bucket, tokens) in enumerate(buckets.items()):
    with cols[i % 2]:
        selections[bucket] = st.multiselect(bucket, tokens, key=bucket)

# Sidebar token definition
def define(token):
    return f"A concise description of '{token}' for creative prompting."

with st.sidebar:
    st.header("Token helper")
    if 'last_token' in st.session_state:
        tk = st.session_state['last_token']
        st.write(f"**{tk}**")
        st.caption(define(tk))
    else:
        st.write("Select a token to see its description.")

# Update last_token on multiselect changes
for bucket, selected in selections.items():
    if selected:
        st.session_state['last_token'] = selected[-1]

# Random fill empty buckets
if st.button("Random Fill Empty Buckets"):
    for bucket, tokens in buckets.items():
        if not selections[bucket] and tokens:
            choice = random.choice(tokens)
            selections[bucket].append(choice)
            st.session_state[bucket] = selections[bucket]

# Clear all
if st.button("Clear All"):
    for bucket in buckets:
        st.session_state[bucket] = []
    st.experimental_rerun()

# Build final prompt
order = ["Subject", "Materials & Textures", "Composition & Framing", "Lighting",
         "Style & Realism", "Atmosphere / Extras",
         "FX & Details / Overlays / Imperfections", "Shot Type & Angle",
         "Aesthetics", "Technical / Output"]

parts = [subject] if subject else []
parts += [extra_notes] if extra_notes else []
for bucket in order[1:]:
    tokens = selections.get(bucket, [])
    if tokens:
        parts.append(", ".join(tokens))
prompt = ", ".join(parts)

st.markdown("### Final Prompt")
st.code(prompt or "(Prompt will appear here)", language="text")

# Copy to clipboard
if st.button("Copy Prompt"):
    copy_js = f"navigator.clipboard.writeText({json.dumps(prompt)}); alert('Prompt copied! Go Create!');"
    st.components.v1.html(f'<script>{copy_js}</script>', height=0)

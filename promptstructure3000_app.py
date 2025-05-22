import streamlit as st, pandas as pd, json, random, re

# --- PAGE CONFIG ---
st.set_page_config(page_title="PromptStructure3000", page_icon="🪄", layout="wide")

# --- HARD CSS: FORCED BLUE, SHARP CORNERS ---
st.markdown('''
<style>
button, .stButton > button {
    background-color:#0051FF !important;
    border-radius:0px !important;
    color:white !important;
}
.stMultiSelect > div, input, textarea, .stSelectbox > div, .stSelectbox label {
    border-radius:0px !important;
}
</style>
''', unsafe_allow_html=True)

# --- EXPLAINER + EXAMPLE ---
st.markdown("""
# PromptStructure3000

PromptStructure3000 lets you build advanced, highly-structured image prompts using blueprints from the professional PDF prompt packs below. This tool lets you mix and match options, load preset templates, and copy the final output for use in Midjourney, Sora, Stable Diffusion, Firefly, and more.

### Example (from the PDF prompt packs):

> **A dynamic, high-impact photograph capturing an adventure sport athlete in mid-action, in a sun-drenched desert, featuring matte carbon fiber, shot as a low-angle fisheye, lit by golden-hour glow, in the style of cinematic, with motion blur, using film grain overlays, framed as Extreme Wide Shot (EWS), with an aspect ratio of 16:9.**

_This is the output you'll get — but with your custom subjects, modifiers, and styles._
""")

# --- PRESETS ---
with open('presets.json') as f:
    presets = json.load(f)

preset_names = ["(none)"] + sorted(presets.keys())

col_engine, col_preset = st.columns(2)
with col_engine:
    engine = st.selectbox("Gen‑AI Engine", ["Plain text","Midjourney (MJ)","Stable Diffusion"], index=0)
with col_preset:
    chosen_preset = st.selectbox("Load preset", preset_names)

# --- FORM SLOTS ---
subject = st.text_input("Main subject", "")
action = st.text_input("Peak action / verb", "")
env_desc = st.text_input("Environmental element", "")
narrative_extra = st.text_area("Extra cinematic detail", "")

# --- AESTHETICS with HEADERS ---
aesthetics_options = [
    "— Classic Styles —",
    "Cinematic", "Photorealistic", "Editorial", "Fine Art", "High Fashion", "Concept Art", "3D Render",
    "— Modern Styles —",
    "Y2K", "Vaporwave", "Cyberpunk", "Steampunk", "Retro Futurism", "Noir", "Vintage / Retro", "Pastel", "Brutalist", "Modern", "Surrealist", "Abstract", "Glitch", "Polaroid", "Analog", "Matte", "Lo-Fi / Grainy", "HDR", "Long Exposure", "Color Pop / Vibrant", "Moody / Dark",
    "— Art Movements —",
    "Pop Art", "Art Deco", "Bauhaus", "Expressionist", "Sculptural", "Watercolor", "Sketch / Ink"
]
def is_header(item):
    return item.startswith("—")

aesthetics_sel = st.multiselect(
    "Aesthetics (curated, with category headers)",
    options=aesthetics_options,
    help="Widely used and recognized visual styles. Section headers are not selectable."
)
# Remove any headers if selected by accident
aesthetics_sel = [x for x in aesthetics_sel if not is_header(x)]

# --- Random Fill/ Clear All ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Random Fill"):
        # Randomly pick a single aesthetic style (never a header)
        choices = [x for x in aesthetics_options if not is_header(x)]
        aesthetics_sel = [random.choice(choices)]
        st.session_state['Aesthetics'] = aesthetics_sel
        st.experimental_rerun()
with col2:
    if st.button("Clear All"):
        st.session_state['Aesthetics'] = []
        st.experimental_rerun()

# --- PROMPT OUTPUT ---
parts = []
if subject: parts.append(subject)
if action: parts.append(action)
if env_desc: parts.append(env_desc)
if aesthetics_sel: parts.append("in the style of " + ", ".join(aesthetics_sel))
if narrative_extra: parts.append(narrative_extra)
prompt = ", ".join(parts).strip()
if prompt and not prompt.endswith('.'): prompt += '.'

st.subheader("Final Prompt")
st.code(prompt if prompt else "(Prompt will appear here)", language="text")

if st.button("Copy Prompt"):
    st.write(":blue[Copied to clipboard!]")  # Streamlit's copy-to-clipboard is handled by browser.

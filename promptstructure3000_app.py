import streamlit as st
import json

st.set_page_config(page_title="PromptStructure3000", page_icon="🪄", layout="wide")

# --- FORCE BLUE UI, SHARP CORNERS ---
st.markdown("""
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
""", unsafe_allow_html=True)

# --- TOP EXPLAINER & EXAMPLE ---
st.markdown(""
# PromptStructure3000

PromptStructure3000 lets you build advanced, structured image prompts using the blueprints from the PDF prompt packs. Load a preset, edit, and copy for Midjourney, Sora, or any AI image tool.

**Example prompt:**
> A dynamic, high-impact photograph capturing an adventure sport athlete in mid-action, in a sun-drenched desert, featuring matte carbon fiber, shot as a low-angle fisheye, lit by golden-hour glow, in the st

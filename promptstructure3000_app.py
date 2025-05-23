import streamlit as st
import json
import random

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

# --- EXPLAINER & EXAMPLE ---
st.markdown("""
# PromptStructure3000

PromptStructure3000 builds advanced, highly-structured image prompts using the exact blueprint found in the premium PDF packs below. Every field and dropdown matches the categories used in professional Midjourney/Sora/SD/Firebase workflows.

**Example:**
> A dynamic, high-impact photograph capturing an adventure sport athlete in mid-action, in a sun-drenched desert, featuring matte carbon fiber, shot as a low-angle fisheye, lit by golden-hour glow, in the style of cinematic, with motion blur, using film grain overlays, framed as Extreme Wide Shot (EWS), with an aspect ratio of 16:9.
""")

# --- PRESET LOADING ---
try:
    with open("presets.json") as f:
        presets = json.load(f)
except Exception:
    presets = {}

preset_names = ["(none)"] + sorted(list(presets.keys()))
col_engine, col_preset = st.columns(2)
with col_engine:
    engine = st.selectbox("Gen‑AI Engine", ["Plain text", "Midjourney (MJ)", "Stable Diffusion"], index=0)
with col_preset:
    chosen_preset = st.selectbox("Load preset", preset_names)

# ---- DROPDOWN CATEGORY OPTIONS ----
aesthetics_options = [
    "— Classic Styles —", "Cinematic", "Photorealistic", "Editorial", "Fine Art", "High Fashion", "Concept Art", "3D Render",
    "— Modern Styles —", "Y2K", "Vaporwave", "Cyberpunk", "Steampunk", "Retro Futurism", "Noir", "Vintage / Retro", "Pastel", "Brutalist", "Modern", "Surrealist", "Abstract", "Glitch", "Polaroid", "Analog", "Matte", "Lo-Fi / Grainy", "HDR", "Long Exposure", "Color Pop / Vibrant", "Moody / Dark",
    "— Art Movements —", "Pop Art", "Art Deco", "Bauhaus", "Expressionist", "Sculptural", "Watercolor", "Sketch / Ink"
]
lighting_options = [
    "— Natural Light —", "Golden-hour glow", "Blue-hour", "Sunrise", "Sunset", "Overcast", "Backlit", "Window light",
    "— Studio Light —", "Softbox", "Ringlight", "Beauty dish", "Spotlight", "Colored gel", "Hard flash", "Rembrandt", "Butterfly", "Strobe",
    "— Mixed/Other —", "Neon", "Candlelight", "Practical light"
]
materials_options = [
    "— Metals —", "Polished chrome", "Brushed steel", "Matte aluminum", "Gold", "Copper",
    "— Glass/Ceramics —", "Frosted glass", "Translucent glass", "Glossy ceramic", "Porcelain",
    "— Natural —", "Wood", "Stone", "Concrete", "Marble", "Sand", "Bamboo",
    "— Fabric/Textile —", "Linen", "Velvet", "Canvas", "Wool", "Denim", "Silk",
    "— Plastic/Synthetics —", "Acrylic", "Matte plastic", "Glossy plastic", "Rubber"
]
shot_options = [
    "— Wide/Full —", "Extreme Wide Shot (EWS)", "Full Shot (FS)", "Wide Shot (WS)",
    "— Medium —", "Medium Wide Shot (MWS)", "Medium Shot (MS)", "Medium Close-Up (MCU)",
    "— Close/Extreme Close —", "Close-Up (CU)", "Extreme Close-Up (ECU)",
    "— Special/POV —", "Over-the-Shoulder", "POV", "Bird's-eye view", "Low angle", "High angle", "Dutch angle"
]
atmosphere_options = [
    "Soft bloom", "Dust motes", "Light leaks", "Haze", "Bokeh", "Glow", "Fog", "Mist", "Cinematic grain", "Lens flare", "Sunbeams", "Rain", "Snow", "Smoke", "Shadow play"
]
fx_options = [
    "Film grain", "VHS overlay", "Halftone dots", "Noise", "Scratch", "Glitch FX", "Bloom", "Chromatic aberration", "Double exposure", "Color fringing"
]
technical_options = [
    "Aspect 16:9", "Aspect 1:1", "Aspect 4:3", "Aspect 3:2", "Aspect 9:16", "Ultra High Resolution", "Low Resolution", "Alpha Channel"
]

def is_header(x): return x.startswith("—")

# --- FIELD GETTERS FOR PRESET ---
def get_from_preset(field, fallback=[]):
    if chosen_preset and chosen_preset != "(none)" and field in presets[chosen_preset]:
        val = presets[chosen_preset][field]
        if isinstance(val, str):
            if val and "," in val:
                return [v.strip() for v in val.split(",")]
            return [val] if val else []
        if isinstance(val, list):
            return val
    return fallback.copy()

def get_text_from_preset(field):
    if chosen_preset and chosen_preset != "(none)" and field in presets[chosen_preset]:
        val = presets[chosen_preset][field]
        if isinstance(val, str):
            return val
        elif isinstance(val, list) and len(val) > 0:
            return ", ".join(val)
    return ""

# ---- MAIN FORM INPUTS ----
subject = st.text_input("Main subject", value=get_text_from_preset("Main subject"))
action = st.text_input("Peak action / verb", value=get_text_from_preset("Peak action / verb"))
env_desc = st.text_input("Environmental element", value=get_text_from_preset("Environmental element"))
narrative_extra = st.text_area("Extra cinematic detail", value=get_text_from_preset("Extra cinematic detail"))

materials_sel = st.multiselect(
    "Materials & Textures",
    options=materials_options,
    default=[m for m in get_from_preset("Materials & Textures") if m in materials_options],
    help="Section headers are not selectable."
)
materials_sel = [x for x in materials_sel if not is_header(x)]

lighting_sel = st.multiselect(
    "Lighting",
    options=lighting_options,
    default=[l for l in get_from_preset("Lighting") if l in lighting_options],
    help="Section headers are not selectable."
)
lighting_sel = [x for x in lighting_sel if not is_header(x)]

aesthetics_sel = st.multiselect(
    "Aesthetics",
    options=aesthetics_options,
    default=[a for a in get_from_preset("Aesthetics") if a in aesthetics_options],
    help="Section headers are not selectable."
)
aesthetics_sel = [x for x in aesthetics_sel if not is_header(x)]

shot_sel = st.multiselect(
    "Shot Type & Angle",
    options=shot_options,
    default=[s for s in get_from_preset("Shot Type & Angle") if s in shot_options],
    help="Section headers are not selectable."
)
shot_sel = [x for x in shot_sel if not is_header(x)]

atmosphere_sel = st.multiselect(
    "Atmosphere / Extras",
    options=atmosphere_options,
    default=[a for a in get_from_preset("Atmosphere / Extras") if a in atmosphere_options]
)
fx_sel = st.multiselect(
    "FX & Details / Overlays / Imperfections",
    options=fx_options,
    default=[f for f in get_from_preset("FX & Details / Overlays / Imperfections") if f in fx_options]
)
technical_sel = st.multiselect(
    "Technical / Output",
    options=technical_options,
    default=[t for t in get_from_preset("Technical / Output") if t in technical_options]
)

# ---- MIDJOURNEY PARAMS PANEL ----
mj_params = {}
if engine == "Midjourney (MJ)":
    st.markdown("#### Midjourney Parameters")
    colmj1, colmj2, colmj3 = st.columns(3)
    with colmj1:
        mj_params["--ar"] = st.text_input("--ar (aspect)", value=get_text_from_preset("--ar"))
        mj_params["--stylize"] = st.text_input("--stylize", value=get_text_from_preset("--stylize"))
        mj_params["--quality"] = st.text_input("--quality", value=get_text_from_preset("--quality"))
    with colmj2:
        mj_params["--seed"] = st.text_input("--seed", value=get_text_from_preset("--seed"))
        mj_params["--chaos"] = st.text_input("--chaos", value=get_text_from_preset("--chaos"))
        mj_params["--style"] = st.text_input("--style", value=get_text_from_preset("--style"))
    with colmj3:
        mj_params["--no"] = st.text_input("--no (negative prompt)", value=get_text_from_preset("--no"))
        mj_params["--tile"] = st.text_input("--tile", value=get_text_from_preset("--tile"))
        mj_params["--stop"] = st.text_input("--stop", value=get_text_from_preset("--stop"))

# ---- RANDOM FILL / CLEAR ALL ----
col1, col2 = st.columns(2)
with col1:
    if st.button("Random Fill"):
        rand = lambda opts: random.choice([x for x in opts if not is_header(x)])
        st.session_state['Materials & Textures'] = [rand(materials_options)]
        st.session_state['Lighting'] = [rand(lighting_options)]
        st.session_state['Aesthetics'] = [rand(aesthetics_options)]
        st.session_state['Shot Type & Angle'] = [rand(shot_options)]
        st.session_state['Atmosphere / Extras'] = [rand(atmosphere_options)]
        st.session_state['FX & Details / Overlays / Imperfections'] = [rand(fx_options)]
        st.session_state['Technical / Output'] = [rand(technical_options)]
        st.experimental_rerun()
with col2:
    if st.button("Clear All"):
        for field in ['Materials & Textures', 'Lighting', 'Aesthetics', 'Shot Type & Angle', 'Atmosphere / Extras', 'FX & Details / Overlays / Imperfections', 'Technical / Output']:
            st.session_state[field] = []
        st.experimental_rerun()

# ---- FINAL PROMPT ASSEMBLY ----
parts = []
if subject: parts.append(subject)
if action: parts.append(action)
if env_desc: parts.append(env_desc)
if materials_sel: parts.append("featuring " + ", ".join(materials_sel))
if lighting_sel: parts.append("lit by " + ", ".join(lighting_sel))
if aesthetics_sel: parts.append("in the style of " + ", ".join(aesthetics_sel))
if shot_sel: parts.append("shot as " + ", ".join(shot_sel))
if atmosphere_sel: parts.append("with " + ", ".join(atmosphere_sel))
if fx_sel: parts.append("using " + ", ".join(fx_sel))
if technical_sel: parts.append("with " + ", ".join(technical_sel))
if narrative_extra: parts.append(narrative_extra)

prompt = ", ".join(parts).strip()
if prompt and not prompt.endswith('.'): prompt += '.'
if engine == "Midjourney (MJ)":
    param_str = " ".join([f"{k} {v}" for k, v in mj_params.items() if v and v.strip()])
    prompt = f"{prompt} {param_str}".strip()

st.subheader("Final Prompt")
st.code(prompt if prompt else "(Prompt will appear here)", language="text")

if st.button("Copy Prompt"):
    st.write(":blue[Copied to clipboard!]")

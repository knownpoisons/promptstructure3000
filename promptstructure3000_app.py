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
st.markdown("""
# PromptStructure3000

PromptStructure3000 lets you build advanced, structured image prompts using blueprints from the PDF prompt packs. Load a preset, edit, and copy for Midjourney, Sora, or any AI image tool.

**Example prompt:**
> A dynamic, high-impact photograph capturing an adventure sport athlete in mid-action, in a sun-drenched desert, featuring matte carbon fiber, shot as a low-angle fisheye, lit by golden-hour glow, in the style of cinematic, with motion blur, using film grain overlays, framed as Extreme Wide Shot (EWS), with an aspect ratio of 16:9.
""")

# --- PRESETS LOADING ---
try:
    with open('presets.json') as f:
        presets = json.load(f)
except Exception:
    presets = {}

preset_names = ["(none)"] + sorted(list(presets.keys()))

col_engine, col_preset = st.columns(2)
with col_engine:
    engine = st.selectbox("Gen‑AI Engine", ["Plain text", "Midjourney (MJ)", "Stable Diffusion"], index=0)
with col_preset:
    chosen_preset = st.selectbox("Load preset", preset_names)

def get_from_preset(field):
    if chosen_preset and chosen_preset != "(none)" and field in presets[chosen_preset]:
        val = presets[chosen_preset][field]
        if isinstance(val, list):
            return val
        return val
    return ""

# --- FORM INPUTS ---
subject = st.text_input("Main subject", value=get_from_preset("Main subject"))
action = st.text_input("Peak action / verb", value=get_from_preset("Peak action / verb"))
env_desc = st.text_input("Environmental element", value=get_from_preset("Environmental element"))
narrative_extra = st.text_area("Extra cinematic detail", value=get_from_preset("Extra cinematic detail"))

# --- AESTHETICS WITH SECTION HEADERS ---
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

default_aesthetics = get_from_preset("Aesthetics")
if isinstance(default_aesthetics, str):
    default_aesthetics = [default_aesthetics]
aesthetics_sel = st.multiselect(
    "Aesthetics (curated, sectioned)",
    options=aesthetics_options,
    default=[a for a in default_aesthetics if a in aesthetics_options],
    help="Widely used and recognized visual styles. Section headers are not selectable."
)
aesthetics_sel = [x for x in aesthetics_sel if not is_header(x)]

# --- LIGHTING (with headers) ---
lighting_options = [
    "— Natural Light —",
    "Golden-hour glow", "Blue-hour", "Sunrise", "Sunset", "Overcast", "Backlit", "Window light",
    "— Studio Light —",
    "Softbox", "Ringlight", "Beauty dish", "Spotlight", "Colored gel", "Hard flash", "Rembrandt", "Butterfly", "Strobe",
    "— Mixed/Other —",
    "Neon", "Candlelight", "Practical light"
]
default_lighting = get_from_preset("Lighting")
if isinstance(default_lighting, str):
    default_lighting = [default_lighting]
lighting_sel = st.multiselect(
    "Lighting (sectioned)",
    options=lighting_options,
    default=[l for l in default_lighting if l in lighting_options],
    help="Section headers are not selectable."
)
lighting_sel = [x for x in lighting_sel if not is_header(x)]

# --- MATERIALS (with headers) ---
materials_options = [
    "— Metals —",
    "Polished chrome", "Brushed steel", "Matte aluminum", "Gold", "Copper",
    "— Glass/Ceramics —",
    "Frosted glass", "Translucent glass", "Glossy ceramic", "Porcelain",
    "— Natural —",
    "Wood", "Stone", "Concrete", "Marble", "Sand", "Bamboo",
    "— Fabric/Textile —",
    "Linen", "Velvet", "Canvas", "Wool", "Denim", "Silk",
    "— Plastic/Synthetics —",
    "Acrylic", "Matte plastic", "Glossy plastic", "Rubber"
]
default_materials = get_from_preset("Materials & Textures")
if isinstance(default_materials, str):
    default_materials = [default_materials]
materials_sel = st.multiselect(
    "Materials & Textures (sectioned)",
    options=materials_options,
    default=[m for m in default_materials if m in materials_options],
    help="Section headers are not selectable."
)
materials_sel = [x for x in materials_sel if not is_header(x)]

# --- SHOT TYPE & ANGLE (with headers) ---
shot_options = [
    "— Wide/Full —",
    "Extreme Wide Shot (EWS)", "Full Shot (FS)", "Wide Shot (WS)",
    "— Medium —",
    "Medium Wide Shot (MWS)", "Medium Shot (MS)", "Medium Close-Up (MCU)",
    "— Close/Extreme Close —",
    "Close-Up (CU)", "Extreme Close-Up (ECU)",
    "— Special/POV —",
    "Over-the-Shoulder", "POV", "Bird's-eye view", "Low angle", "High angle", "Dutch angle"
]
default_shot = get_from_preset("Shot Type & Angle")
if isinstance(default_shot, str):
    default_shot = [default_shot]
shot_sel = st.multiselect(
    "Shot Type & Angle (sectioned)",
    options=shot_options,
    default=[s for s in default_shot if s in shot_options],
    help="Section headers are not selectable."
)
shot_sel = [x for x in shot_sel if not is_header(x)]

# --- ATMOSPHERE / EXTRAS ---
atmosphere_options = [
    "Soft bloom", "Dust motes", "Light leaks", "Haze", "Bokeh", "Glow", "Fog", "Mist",
    "Cinematic grain", "Lens flare", "Sunbeams", "Rain", "Snow", "Smoke", "Shadow play"
]
default_atmo = get_from_preset("Atmosphere / Extras")
if isinstance(default_atmo, str):
    default_atmo = [default_atmo]
atmosphere_sel = st.multiselect(
    "Atmosphere / Extras",
    options=atmosphere_options,
    default=[a for a in default_atmo if a in atmosphere_options]
)

# --- FINAL PROMPT ASSEMBLY ---
parts = []
if subject: parts.append(subject)
if action: parts.append(action)
if env_desc: parts.append(env_desc)
if materials_sel: parts.append("featuring " + ", ".join(materials_sel))
if lighting_sel: parts.append("lit by " + ", ".join(lighting_sel))
if shot_sel: parts.append("shot as " + ", ".join(shot_sel))
if aesthetics_sel: parts.append("in the style of " + ", ".join(aesthetics_sel))
if atmosphere_sel: parts.append("with " + ", ".join(atmosphere_sel))
if narrative_extra: parts.append(narrative_extra)
prompt = ", ".join(parts).strip()
if prompt and not prompt.endswith('.'): prompt += '.'

st.subheader("Final Prompt")
st.code(prompt if prompt else "(Prompt will appear here)", language="text")

if st.button("Copy Prompt"):
    st.write(":blue[Copied to clipboard!]")

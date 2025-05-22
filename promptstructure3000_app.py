
import streamlit as st, pandas as pd, random, json, re

st.set_page_config(theme={'primaryColor':'#0051FF','base':'light'}, page_title="PromptStructure3000", page_icon="🪄", layout="wide")

# ------------ Load tokens & presets ------------
@st.cache_data
def load_tokens():
    df = pd.read_csv("prompt_token_library_wide_v2.csv")
    return {col: df[col].dropna().tolist() for col in df.columns}

@st.cache_data
def load_presets():
    import json, pathlib
    with open('presets.json') as f:
        return json.load(f)

buckets = load_tokens()
presets = load_presets()

# add Setting bucket
buckets["Setting / Environment"] = [
    "misty mountain range","stormy sea cliff","urban alley at night","sun‑drenched desert",
    "dense rainforest canopy","snow‑covered peak","city rooftop at dawn","neon‑lit street",
    "abandoned warehouse","foggy lake shore","tropical beach","subway tunnel",
    "moon‑lit highway","lush valley","infinite white studio sweep"
]

# ------------ UI theme ------------
st.markdown("""<style>
:root{--primary-blue:#0051FF;--light-grey:#F4F6F8;}
body{background-color:var(--light-grey);}
button[kind=primary]{background-color:var(--primary-blue);color:white;border-radius:0;}
button[kind=primary]:hover{filter:brightness(115%);}
div[data-baseweb="select"]>div{border-radius:0;}
textarea, input{border-radius:0;}
label{font-weight:bold;}
label span.helper{font-weight:normal;font-style:italic;}
</style>""",unsafe_allow_html=True)

# ------------ Engine selector ------------
engine = st.selectbox("Gen‑AI Engine", ["Plain text","Midjourney (MJ)","Stable Diffusion"], index=0)

mj_params = {}
if engine == "Midjourney (MJ)":
    st.markdown("**Midjourney parameters**")
    cols = st.columns(3)
    with cols[0]:
        mj_params["--ar"] = st.text_input("--ar (aspect)", placeholder="16:9")
        mj_params["--stylize"] = st.text_input("--stylize", placeholder="250")
        mj_params["--quality"] = st.text_input("--quality", placeholder="2")
    with cols[1]:
        mj_params["--seed"] = st.text_input("--seed", placeholder="42")
        mj_params["--chaos"] = st.text_input("--chaos", placeholder="0")
        mj_params["--style"] = st.text_input("--style", placeholder="raw")
    with cols[2]:
        mj_params["--no"] = st.text_input("--no (negative)", placeholder="text, logo")
        mj_params["--tile"] = st.text_input("--tile", placeholder="true/false")
        mj_params["--stop"] = st.text_input("--stop", placeholder="80")

# ------------ Preset loader ------------
preset_names = ["(none)"] + list(presets.keys())
chosen_preset = st.selectbox("Load preset", preset_names)

# ------------ Subject builder ------------
st.subheader("Core narrative")
subject = st.text_input("Main subject")
action = st.text_input("Peak action / verb")
env_desc = st.text_input("Environmental element")
narrative_extra = st.text_area("Extra cinematic detail", height=80)

# ------------ Buckets ------------
helpers = {
    "Materials & Textures":"surface finish, physical makeup",
    "Composition & Framing":"camera angle, crop, perspective",
    "Lighting":"source, direction, mood",
    "Style & Realism":"overall photographic style",
    "Atmosphere / Extras":"effects, ambience, imperfections",
    "FX & Details / Overlays / Imperfections":"post‑process or shader effects",
    "Shot Type & Angle":"formal shot classifications",
    "Aesthetics":"visual subculture vibe",
    "Technical / Output":"aspect ratio",
    "Setting / Environment":"location, background, time‑of‑day"
}

bucket_order = ["Setting / Environment","Materials & Textures","Composition & Framing","Shot Type & Angle",
"Lighting","Style & Realism","Atmosphere / Extras","FX & Details / Overlays / Imperfections","Aesthetics","Technical / Output"]

selections={b:[] for b in bucket_order}

# apply preset
if chosen_preset != "(none)":
    pre = presets[chosen_preset]
    subject = pre.get("Main subject","")
    action = pre.get("Peak action / verb","")
    env_desc = pre.get("Environmental element","")
    narrative_extra = pre.get("Extra cinematic detail","")
    for b in bucket_order:
        selections[b] = pre.get(b, [])
        st.session_state[b] = selections[b]

left,right = st.columns(2)
for i,bucket in enumerate(bucket_order):
    col=left if i%2==0 else right
    with col:
        selections[bucket] = st.multiselect(f"{bucket} ({helpers[bucket]})", buckets[bucket], key=bucket, default=selections[bucket])

# ------------ Actions ------------
a1,a2,a3 = st.columns(3)
with a1:
    if st.button("Random Fill"):
        for b in bucket_order:
            if not selections[b]:
                choice=random.choice(buckets[b])
                selections[b].append(choice)
                st.session_state[b]=selections[b]
        st.experimental_rerun()
with a2:
    if st.button("Clear All"):
        for b in bucket_order:
            st.session_state[b]=[]
        st.experimental_rerun()

# ------------ Prompt builder ------------
connector_map = {
    "Setting / Environment":"in",
    "Materials & Textures":"featuring",
    "Composition & Framing":"shot as",
    "Shot Type & Angle":"framed as",
    "Lighting":"lit by",
    "Style & Realism":"in the style of",
    "Atmosphere / Extras":"with",
    "FX & Details / Overlays / Imperfections":"using",
    "Aesthetics":"evoking",
    "Technical / Output":"with an aspect ratio of"
}

parts=[]
if subject: parts.append(subject)
if action: parts.append(action)
if env_desc: parts.append(env_desc)
for b in bucket_order:
    if selections[b]:
        parts.append(f"{connector_map[b]} {', '.join(selections[b])}")
if narrative_extra: parts.append(narrative_extra)

prompt = ", ".join(parts).strip()
if prompt and not prompt.endswith('.'): prompt+='.'

# append MJ params
if engine == "Midjourney (MJ)":
    param_str = " ".join([f"{k} {v}" for k,v in mj_params.items() if v.strip()])
    prompt = f"{prompt} {param_str}".strip()

prompt = re.sub(r'\s{2,}',' ',prompt)

st.subheader("Final Prompt")
st.code(prompt or "(Prompt will appear here)", language="text")

copy_holder = st.empty()
if st.button("Copy Prompt"):
    js=f"""<script>
    navigator.clipboard.writeText({json.dumps(prompt)});
    const note=window.parent.document.getElementById('copy-note'); if(note){{note.style.display='inline'; setTimeout(()=>{{note.style.display='none'}},1500);}}
    </script>"""
    st.components.v1.html(js,height=0)
    copy_holder.markdown("<span id='copy-note' style='color:var(--primary-blue);font-weight:bold;'>Copied!</span>",unsafe_allow_html=True)

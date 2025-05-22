
import streamlit as st
import pandas as pd
import random, json, re

st.set_page_config(page_title="PromptStructure3000", page_icon="🪄", layout="wide")

@st.cache_data
def load_tokens():
    df = pd.read_csv("prompt_token_library_wide_v2.csv")
    return {col: df[col].dropna().tolist() for col in df.columns}

# ---------- Tokens ----------
buckets = load_tokens()
buckets["Setting / Environment"] = [
    "misty mountain range","stormy sea cliff","urban alley at night","sun‑drenched desert",
    "dense rainforest canopy","snow‑covered peak","city rooftop at dawn","neon‑lit street",
    "abandoned warehouse","foggy lake shore","tropical beach","subway tunnel",
    "moon‑lit highway","lush valley","infinite white studio sweep"
]

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
                "Lighting","Style & Realism","Atmosphere / Extras",
                "FX & Details / Overlays / Imperfections","Aesthetics","Technical / Output"]

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

# ---------- Global Style ----------
st.markdown("""<style>
/* color scheme */
:root{--primary-blue:#0051FF;--light-grey:#F4F6F8;}
body{background-color:var(--light-grey);}
input,textarea,select,div[data-baseweb="select"] > div{border-radius:0!important;}
button[kind=primary]{background-color:var(--primary-blue);color:white;border-radius:0!important;}
button[kind=primary]:hover{filter:brightness(115%);}
label{font-weight:bold;}
label span.helper{font-weight:normal;font-style:italic;}
.stMultiSelect>div{border-radius:0!important;}
</style>""", unsafe_allow_html=True)

st.title("PromptStructure3000")

# ---------- Multi-slot Subject Builder ----------
st.subheader("Core narrative")
col1,col2 = st.columns(2)
with col1:
    subject = st.text_input("Main subject", placeholder="e.g., adventure sport athlete")
with col2:
    action = st.text_input("Peak action / verb", placeholder="e.g., carving through a wave")

env_desc = st.text_input("Environmental element", placeholder="e.g., roaring spray of water")
narrative_extra = st.text_area("Extra cinematic detail", height=60, placeholder="e.g., tension visible in muscles, droplets frozen mid‑air")

# ---------- Dropdowns ----------
st.subheader("Creative modifiers")

selections={}
left,right = st.columns(2)
for i,bucket in enumerate(bucket_order):
    col = left if i%2==0 else right
    label = f"{bucket} ( {helpers[bucket]} )"  # helper in brackets
    with col:
        selections[bucket] = st.multiselect(label, buckets[bucket], key=bucket, placeholder="Select...")

# ---------- Actions ----------
c1,c2,c3 = st.columns(3)
with c1:
    if st.button("Random Fill"):
        for bucket in bucket_order:
            if not selections[bucket]:
                choice = random.choice(buckets[bucket])
                selections[bucket].append(choice)
                st.session_state[bucket] = selections[bucket]
        st.experimental_rerun()  # ensure UI updates
with c2:
    if st.button("Clear All"):
        for bucket in bucket_order:
            st.session_state[bucket] = []
        for key in ["Main subject","Peak action / verb","Environmental element","Extra cinematic detail"]:
            if key in st.session_state: del st.session_state[key]
        st.experimental_rerun()

# ---------- Build prompt ----------
parts=[]
if subject: parts.append(subject)
if action: parts.append(action)
if env_desc: parts.append(env_desc)

for bucket in bucket_order:
    toks = selections[bucket]
    if toks:
        parts.append(f"{connector_map[bucket]} {', '.join(toks)}")

if narrative_extra: parts.append(narrative_extra)

prompt = ", ".join(parts).strip()
prompt = re.sub(r'\s+,', ',', prompt)
if prompt and not prompt.endswith('.'): prompt+='.'

st.subheader("Final Prompt")
st.code(prompt or "(Prompt will appear here)", language="text")

copied_holder = st.empty()
def copy(text):
    js = f"""<script>
    navigator.clipboard.writeText({json.dumps(text)});
    const el = window.parent.document.getElementById('copy-note');
    if(el){{el.style.display='inline'; setTimeout(()=>{{el.style.display='none'}},1500);}}
    </script>"""
    st.components.v1.html(js,height=0)

if st.button("Copy Prompt"):
    copy(prompt)
    copied_holder.markdown("<span id='copy-note' style='color:var(--primary-blue);font-weight:bold;'>Copied!</span>", unsafe_allow_html=True)

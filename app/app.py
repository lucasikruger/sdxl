import streamlit as st
from PIL import Image
from datetime import datetime
from src.functions import load_model

st.image(Image.open("media/logo.webp"))
st.title("Stable Diffusion XL")
st.sidebar.title("Parameters")
n_steps = st.sidebar.slider("Number of Inference Steps", min_value=1, max_value=100, value=40, step=1, key="n_steps")
num_images_per_prompt = st.sidebar.slider("Number of Images per Prompt", min_value=1, max_value=8, value=1, step=1, key="num_images_per_prompt")


set_seed = st.sidebar.checkbox("Set seed", value=False, key="set_seed")
if set_seed:
    seed = st.sidebar.text_input("Seed", value="42", key="seed")
    seed = int(seed)
else:
    seed = None

mem_offload = st.sidebar.checkbox("Memory Offload", value=False, key="mem_offload")

use_refiner = st.sidebar.checkbox("Use Refiner", value=False, key="use_refiner")
if use_refiner:
    high_noise_frac = st.sidebar.slider("High Noise Fraction", min_value=0.0, max_value=1.0, value=0.8, step=0.1, key="high_noise_frac")
    high_noise_frac = float(high_noise_frac)
else:
    high_noise_frac = None
    
prompt = st.text_input("Prompt", value= "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k", key="prompt")
negative_prompt= st.text_input("Negative Prompt", value="", key="negative_prompt")

if st.button("Generate"):
    with st.spinner("Generating..."):
        st.text (str(prompt))
        model = load_model(use_refiner=use_refiner, mem_offload=mem_offload)
        seed = None
        images = model.infer(
            prompt=str(prompt),
            negative_prompt=str(negative_prompt),
            num_images_per_prompt=int(num_images_per_prompt),
            seed=seed,
            n_steps=int(n_steps),
            use_refiner=use_refiner,
            high_noise_frac=high_noise_frac,
            )
        for image in images:
            st.image(image, width=512)
            image.save(f"output/{prompt}-{negative_prompt}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
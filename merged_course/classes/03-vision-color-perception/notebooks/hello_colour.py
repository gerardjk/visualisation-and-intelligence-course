import streamlit as st

st.title("My first colour app")
wavelength = st.slider("Wavelength (nm)", 380, 700, 550)
st.write("Selected wavelength:", wavelength, "nm")
st.caption("Moving the slider reruns this script from top to bottom.")

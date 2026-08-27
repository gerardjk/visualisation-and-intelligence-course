from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Color and Perception", page_icon="👁️", layout="wide")

DATA_FILE = Path(__file__).parent / "data" / "CIE_xyz_1931_2deg.csv"


@st.cache_data
def load_cie():
    return pd.read_csv(
        DATA_FILE,
        header=None,
        names=["wavelength", "xbar", "ybar", "zbar"],
    ).query("380 <= wavelength <= 700")


def gaussian(x, centre, width):
    return np.exp(-0.5 * ((x - centre) / width) ** 2)


def cone_sensitivities(wavelengths):
    """Schematic curves: useful for the model, not physiological reference data."""
    return np.column_stack([
        gaussian(wavelengths, 445, 32),
        gaussian(wavelengths, 535, 43),
        gaussian(wavelengths, 565, 48),
    ])


st.title("Color and Perception")
st.caption("Change a physical spectrum; inspect what survives each representation.")

st.sidebar.header("Light source")
centre = st.sidebar.slider("Peak wavelength (nm)", 400, 680, 540, 1)
width = st.sidebar.slider("Spectral width (nm)", 2, 100, 28, 1)
second_peak = st.sidebar.checkbox("Add a second peak")
second_centre = st.sidebar.slider("Second peak (nm)", 400, 680, 620, 1, disabled=not second_peak)

wavelengths = np.arange(380, 701)
spectrum = gaussian(wavelengths, centre, width)
if second_peak:
    spectrum = spectrum + 0.65 * gaussian(wavelengths, second_centre, width)

cones = cone_sensitivities(wavelengths)
responses = np.trapezoid(spectrum[:, None] * cones, wavelengths, axis=0)
responses = responses / responses.max()

cie = load_cie()
sampled_spectrum = np.interp(cie["wavelength"], wavelengths, spectrum)
XYZ = cie[["xbar", "ybar", "zbar"]].to_numpy().T @ sampled_spectrum
xy = XYZ[:2] / XYZ.sum()

world_tab, eye_tab, map_tab = st.tabs(["1 · Spectrum", "2 · Eye", "3 · Chromaticity"])

with world_tab:
    st.subheader("The physical input is a spectrum")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(wavelengths, spectrum, color="#0F4BEB", lw=3)
    ax.fill_between(wavelengths, spectrum, color="#00B7E0", alpha=.18)
    ax.set(xlabel="wavelength (nm)", ylabel="relative power", xlim=(380, 700))
    st.pyplot(fig, clear_figure=True)
    st.info("The peak wavelength is one property of this light. The full curve is the input.")

with eye_tab:
    st.subheader("The model compresses the spectrum to three responses")
    columns = st.columns(3)
    for column, label, value in zip(columns, ["S", "M", "L"], responses):
        column.metric(f"{label}-cone response", f"{value:.3f}")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for label, curve, colour in zip(["S", "M", "L"], cones.T, ["#5B4BCE", "#00A878", "#E44B35"]):
        ax.plot(wavelengths, curve, lw=2.5, label=label, color=colour)
    ax.set(xlabel="wavelength (nm)", ylabel="schematic sensitivity", xlim=(380, 700), ylim=(0, 1.05))
    ax.legend()
    st.pyplot(fig, clear_figure=True)
    st.warning("These are schematic cone curves. Colour appearance also depends on adaptation, context and later neural processing.")

with map_tab:
    st.subheader("CIE xy keeps chromaticity and leaves out overall scale")
    xyz = cie[["xbar", "ybar", "zbar"]].to_numpy()
    locus = xyz[:, :2] / xyz.sum(axis=1)[:, None]
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.plot(np.r_[locus[:, 0], locus[0, 0]], np.r_[locus[:, 1], locus[0, 1]], color="#111", lw=2)
    ax.scatter([xy[0]], [xy[1]], s=130, color="#FF2305", edgecolor="white", linewidth=1.5, zorder=3)
    ax.set(xlim=(0, .8), ylim=(0, .9), xlabel="x", ylabel="y")
    ax.set_aspect("equal", adjustable="box")
    st.pyplot(fig, clear_figure=True)
    st.metric("Current chromaticity", f"x={xy[0]:.3f}, y={xy[1]:.3f}")
    st.caption("An xy point is not a spectrum and not a complete colour appearance.")

st.divider()
st.subheader("Your extension")
st.write("Add an intensity slider that multiplies the entire spectrum. Cone-response magnitudes should change; x and y should remain almost unchanged.")

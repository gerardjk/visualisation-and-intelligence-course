"""Build figures, notebook and Streamlit app for Color and Perception."""

from __future__ import annotations

import ast
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import nbformat as nbf
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "beamer" / "figs"
NOTEBOOKS = ROOT / "notebooks"
DATA = NOTEBOOKS / "data" / "CIE_xyz_1931_2deg.csv"
FIGS.mkdir(parents=True, exist_ok=True)

INK = "#111111"
BLUE = "#0F4BEB"
RED = "#FF2305"
CYAN = "#00B7E0"
GREY = "#5A5F63"
S_COLOUR = "#5B4BCE"
M_COLOUR = "#00A878"
L_COLOUR = "#E44B35"

plt.rcParams.update(
    {
        "font.family": "Arial",
        "font.size": 12,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIGS / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def gaussian(x: np.ndarray, centre: float, width: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - centre) / width) ** 2)


def wavelength_rgb(wavelength: float) -> tuple[float, float, float]:
    """Approximate a wavelength with display RGB; for annotation only."""
    w = float(wavelength)
    if 380 <= w < 440:
        rgb = (-(w - 440) / 60, 0, 1)
    elif w < 490:
        rgb = (0, (w - 440) / 50, 1)
    elif w < 510:
        rgb = (0, 1, -(w - 510) / 20)
    elif w < 580:
        rgb = ((w - 510) / 70, 1, 0)
    elif w < 645:
        rgb = (1, -(w - 645) / 65, 0)
    elif w <= 780:
        rgb = (1, 0, 0)
    else:
        rgb = (0, 0, 0)
    return tuple(float(np.clip(channel, 0, 1)) for channel in rgb)


def planck(wavelength_nm: np.ndarray, temperature: float) -> np.ndarray:
    wavelength_m = wavelength_nm * 1e-9
    c2 = 1.438776877e-2
    values = 1 / (wavelength_m**5 * np.expm1(c2 / (wavelength_m * temperature)))
    return values / values.max()


def cone_sensitivities(wavelengths: np.ndarray) -> np.ndarray:
    """Schematic overlapping S, M and L sensitivities for teaching."""
    return np.column_stack(
        [
            gaussian(wavelengths, 445, 32),
            gaussian(wavelengths, 535, 43),
            gaussian(wavelengths, 565, 48),
        ]
    )


def make_figures() -> None:
    wavelengths = np.arange(380, 781)

    # Visible interval and three broad spectral recipes.
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    for w in range(380, 780, 2):
        ax.axvspan(w, w + 2, color=wavelength_rgb(w), alpha=0.17, lw=0)
    daylight = planck(wavelengths, 5800)
    candle = planck(wavelengths, 1800)
    # White-LED LCD shape: the backlight's blue LED spike, then phosphor
    # light through the green and red filters.
    pixel = gaussian(wavelengths, 450, 9) + 0.58 * gaussian(wavelengths, 535, 30) + 0.65 * gaussian(wavelengths, 612, 25)
    pixel /= pixel.max()
    ax.plot(wavelengths, daylight, color=INK, lw=2.8, label="daylight-like source")
    ax.plot(wavelengths, candle, color="#D97904", lw=2.8, label="candle-like source")
    ax.plot(wavelengths, pixel, color=BLUE, lw=2.8, label="LCD display (white-LED backlight)")
    ax.set(xlabel="wavelength (nm)", ylabel="relative spectral power", xlim=(380, 780), ylim=(0, 1.08))
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    ax.set_title("A light is a distribution of power across wavelengths")
    save(fig, "fig-spectral-recipes.png")

    # Illumination multiplied by reflectance.
    illuminant = planck(wavelengths, 5200)
    reflectance = 0.06 + 0.80 / (1 + np.exp(-(wavelengths - 585) / 13))
    reflected = illuminant * reflectance
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.7), sharex=True, sharey=True)
    items = [
        (illuminant, "illumination", BLUE),
        (reflectance, "surface reflectance", GREY),
        (reflected, "light reaching the eye", RED),
    ]
    for ax, (values, title, colour) in zip(axes, items):
        ax.plot(wavelengths, values, color=colour, lw=3)
        ax.fill_between(wavelengths, values, color=colour, alpha=0.15)
        ax.set_title(title)
        ax.set_xlim(380, 780)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("wavelength (nm)")
    axes[0].set_ylabel("relative amount")
    fig.text(0.34, 0.52, r"$\times$", fontsize=30, ha="center", va="center")
    fig.text(0.665, 0.52, r"$=$", fontsize=30, ha="center", va="center")
    fig.suptitle("For an ordinary surface: illumination × reflectance = received spectrum", y=1.04, fontweight="bold")
    save(fig, "fig-illumination-reflectance.png")

    # Additive and subtractive operations.
    size = 500
    yy, xx = np.ogrid[:size, :size]
    masks = [
        (xx - 185) ** 2 + (yy - 175) ** 2 < 135**2,
        (xx - 315) ** 2 + (yy - 175) ** 2 < 135**2,
        (xx - 250) ** 2 + (yy - 300) ** 2 < 135**2,
    ]
    additive = np.zeros((size, size, 3))
    for mask, primary in zip(masks, np.eye(3)):
        additive[mask] += primary
    additive = np.clip(additive, 0, 1)
    subtractive = np.ones((size, size, 3))
    subtractive[~np.logical_or.reduce(masks)] = 0.96
    for mask, filter_rgb in zip(masks, [(0, 1, 1), (1, 0, 1), (1, 1, 0)]):
        subtractive[mask] *= filter_rgb
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.8))
    axes[0].imshow(additive)
    axes[0].set_title("Add light: channel powers add")
    axes[1].imshow(subtractive)
    axes[1].set_title("Stack ideal filters: transmissions multiply")
    for ax in axes:
        ax.set_axis_off()
    save(fig, "fig-additive-subtractive.png")

    # Schematic cone sensitivities.
    cones = cone_sensitivities(wavelengths)
    fig, ax = plt.subplots(figsize=(10.7, 4.7))
    for index, (label, colour) in enumerate(zip(("S", "M", "L"), (S_COLOUR, M_COLOUR, L_COLOUR))):
        ax.plot(wavelengths, cones[:, index], lw=3, color=colour, label=f"{label}-cone")
        ax.fill_between(wavelengths, cones[:, index], color=colour, alpha=0.10)
    ax.set(xlabel="wavelength (nm)", ylabel="relative sensitivity", xlim=(380, 780), ylim=(0, 1.08))
    ax.legend(frameon=False, ncol=3, loc="upper right")
    ax.set_title("Three cone classes sample broad, overlapping wavelength ranges")
    ax.text(383, 0.04, "schematic curves", color=GREY, fontsize=10)
    save(fig, "fig-cone-sensitivities.png")

    # Spectrum compressed to three responses.
    spectrum = 0.65 * gaussian(wavelengths, 455, 13) + 0.95 * gaussian(wavelengths, 545, 30) + 0.45 * gaussian(wavelengths, 625, 22)
    response = np.trapezoid(spectrum[:, None] * cones, wavelengths, axis=0)
    response /= response.max()
    fig = plt.figure(figsize=(11.2, 4.4))
    left = fig.add_axes([0.07, 0.17, 0.56, 0.70])
    right = fig.add_axes([0.75, 0.20, 0.20, 0.62])
    left.plot(wavelengths, spectrum, color=INK, lw=3)
    left.fill_between(wavelengths, spectrum, color=CYAN, alpha=0.16)
    left.set(xlabel="wavelength (nm)", ylabel="relative spectral power", xlim=(380, 780), title="many wavelength values")
    right.bar(["S", "M", "L"], response, color=[S_COLOUR, M_COLOUR, L_COLOUR])
    right.set(ylim=(0, 1.08), ylabel="relative response", title="three responses")
    fig.text(0.69, 0.52, "→", fontsize=34, color=RED, ha="center", va="center")
    fig.suptitle("The first retinal encoding is a severe compression", y=0.99, fontweight="bold")
    save(fig, "fig-spectrum-to-cones.png")

    # Same centre patch in different surrounds.
    context = np.ones((260, 720, 3))
    context[:, :360] = 0.10
    context[:, 360:] = 0.88
    centre = np.array([0.38, 0.52, 0.68])
    context[78:182, 118:242] = centre
    context[78:182, 478:602] = centre
    fig, ax = plt.subplots(figsize=(10.8, 4.1))
    ax.imshow(context)
    ax.set_axis_off()
    ax.set_title("The two centre patches contain identical RGB values")
    save(fig, "fig-context.png")

    # CIE data and chromaticity figures.
    cmf = pd.read_csv(DATA, header=None, names=["wavelength", "xbar", "ybar", "zbar"])
    cmf = cmf.query("380 <= wavelength <= 700").copy()
    wave = cmf["wavelength"].to_numpy()
    xyz = cmf[["xbar", "ybar", "zbar"]].to_numpy()
    totals = xyz.sum(axis=1)
    xy = xyz[:, :2] / totals[:, None]

    fig, ax = plt.subplots(figsize=(10.7, 4.6))
    for label, colour, values in zip((r"$\bar{x}$", r"$\bar{y}$", r"$\bar{z}$"), (RED, M_COLOUR, S_COLOUR), xyz.T):
        ax.plot(wave, values, lw=2.7, color=colour, label=label)
    ax.set(xlabel="wavelength (nm)", ylabel="matching function", xlim=(380, 700), ylim=(0, None))
    ax.legend(frameon=False, ncol=3)
    ax.set_title("CIE 1931 colour-matching functions: wavelength → X, Y, Z contributions")
    save(fig, "fig-cie-matching-functions.png")

    # Exact metameric pair relative to the sampled CIE matching functions.
    response_matrix = xyz.T
    candidate = np.sin(np.linspace(0, 10 * np.pi, len(wave))) + 0.35 * np.cos(np.linspace(0, 3 * np.pi, len(wave)))
    invisible = candidate - response_matrix.T @ np.linalg.solve(
        response_matrix @ response_matrix.T, response_matrix @ candidate
    )
    invisible /= np.max(np.abs(invisible))
    spectrum_a = 0.55 + 0.28 * invisible
    spectrum_b = 0.55 - 0.28 * invisible
    response_a = response_matrix @ spectrum_a
    response_b = response_matrix @ spectrum_b
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.2))
    axes[0].plot(wave, spectrum_a, lw=2.5, color=BLUE, label="spectrum A")
    axes[0].plot(wave, spectrum_b, lw=2.5, color=RED, label="spectrum B")
    axes[0].set(xlabel="wavelength (nm)", ylabel="relative power", title="different spectral recipes")
    axes[0].legend(frameon=False)
    norm_a = response_a / response_a.sum()
    norm_b = response_b / response_b.sum()
    positions = np.arange(3)
    axes[1].bar(positions - 0.17, norm_a, width=0.34, color=BLUE, label="A")
    axes[1].bar(positions + 0.17, norm_b, width=0.34, color=RED, alpha=0.70, label="B")
    axes[1].set_xticks(positions, ["X", "Y", "Z"])
    axes[1].set(ylabel="normalised tristimulus value", title="the same three-number match")
    axes[1].legend(frameon=False)
    fig.suptitle("Metamers: the spectrum is different; the colour match is the same", y=1.02, fontweight="bold")
    save(fig, "fig-metamers.png")

    gamuts = {
        "sRGB": (np.array([[0.640, 0.330], [0.300, 0.600], [0.150, 0.060]]), BLUE),
        "Display P3": (np.array([[0.680, 0.320], [0.265, 0.690], [0.150, 0.060]]), RED),
        "Rec.2020": (np.array([[0.708, 0.292], [0.170, 0.797], [0.131, 0.046]]), M_COLOUR),
    }
    fig, ax = plt.subplots(figsize=(7.4, 6.5))
    ax.plot(np.r_[xy[:, 0], xy[0, 0]], np.r_[xy[:, 1], xy[0, 1]], color=INK, lw=2.4)
    for name, (triangle, colour) in gamuts.items():
        closed = np.vstack([triangle, triangle[0]])
        ax.plot(closed[:, 0], closed[:, 1], lw=2.2, marker="o", ms=5, color=colour, label=name)
    for wavelength in (420, 460, 500, 540, 580, 620, 680):
        index = int(np.argmin(np.abs(wave - wavelength)))
        ax.annotate(str(wavelength), xy[index], xytext=(5, 4), textcoords="offset points", fontsize=8)
    ax.set(xlim=(0, 0.8), ylim=(0, 0.9), xlabel="x", ylabel="y", title="CIE 1931 xy: spectral locus and device gamuts")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(frameon=False, loc="upper right")
    save(fig, "fig-chromaticity-gamuts.png")

    # Mixtures land on a straight line in chromaticity.
    a = xy[np.argmin(np.abs(wave - 460))]
    b = xy[np.argmin(np.abs(wave - 610))]
    weights = np.linspace(0, 1, 9)
    mixtures = weights[:, None] * a + (1 - weights[:, None]) * b
    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    ax.plot(np.r_[xy[:, 0], xy[0, 0]], np.r_[xy[:, 1], xy[0, 1]], color="#9A9A9A", lw=1.8)
    ax.plot(mixtures[:, 0], mixtures[:, 1], color=INK, lw=2.5)
    ax.scatter(mixtures[:, 0], mixtures[:, 1], c=weights, cmap="coolwarm", s=75, edgecolor="white", zorder=3)
    ax.annotate("460 nm", a, xytext=(-35, 8), textcoords="offset points", fontweight="bold")
    ax.annotate("610 nm", b, xytext=(8, 4), textcoords="offset points", fontweight="bold")
    ax.set(xlim=(0, 0.8), ylim=(0, 0.9), xlabel="x", ylabel="y", title="Add two lights: chromaticity follows the line between them")
    ax.set_aspect("equal", adjustable="box")
    save(fig, "fig-mixture-line.png")


APP_SOURCE = r'''from pathlib import Path

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
'''


HELLO_APP = r'''import streamlit as st

st.title("My first colour app")
wavelength = st.slider("Wavelength (nm)", 380, 700, 550)
st.write("Selected wavelength:", wavelength, "nm")
st.caption("Moving the slider reruns this script from top to bottom.")
'''


def md(source: str):
    return nbf.v4.new_markdown_cell(textwrap.dedent(source).strip() + "\n")


def code(source: str):
    return nbf.v4.new_code_cell(textwrap.dedent(source).strip() + "\n")


def build_notebook() -> None:
    cells = [
        md(
            """
            # Color and Perception
            ## From light to an interactive Streamlit explanation

            A colour is not stored in a wavelength, an object, an eye or a hexadecimal code. This lab follows the translations between them:

            > **light source → spectrum → surface → spectrum reaching the eye → cone responses → neural processing → appearance → colour coordinates → display signal → new light**

            We will build each link, identify what it preserves, and identify what it discards. The final section turns the model into a small Streamlit app.
            """
        ),
        md(
            """
            ## What you will be able to explain

            By the end of the lab you should be able to:

            1. distinguish a wavelength from a spectral power distribution;
            2. explain why three cone classes compress a spectrum to three responses;
            3. explain metamerism without claiming that a display reproduces the original light;
            4. construct the CIE 1931 spectral locus from the official colour-matching table;
            5. interpret a gamut triangle and the line of purples; and
            6. turn a Python calculation into a Streamlit app with widgets, charts and explanatory text.
            """
        ),
        md(
            """
            ## Setup

            Install the packages once from a terminal:

            ```bash
            python -m pip install numpy pandas matplotlib streamlit jupyter
            ```

            Keep this notebook inside its supplied folder. The official CIE table is stored at `data/CIE_xyz_1931_2deg.csv`; no internet connection is needed during the lab.
            """
        ),
        code(
            """
            from pathlib import Path
            import importlib.util

            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd

            plt.rcParams.update({
                "figure.figsize": (9, 4.6),
                "axes.spines.top": False,
                "axes.spines.right": False,
                "axes.titleweight": "bold",
            })

            DATA_FILE = Path("data/CIE_xyz_1931_2deg.csv")
            print("CIE table:", "found" if DATA_FILE.exists() else "NOT FOUND")
            print("Streamlit:", "installed" if importlib.util.find_spec("streamlit") else "install before the app section")
            """
        ),
        md(
            r"""
            # 1 · What light is

            Light is electromagnetic radiation. A wavelength describes one repeating spatial period of that radiation; wavelength is measured here in nanometres (nm). Human vision responds to only a limited interval of the electromagnetic spectrum, conventionally approximated as 380–780 nm.

            A real light source usually emits many wavelengths at once. Its **spectral power distribution** (SPD) records how much power is present at each wavelength. It is a curve, not a single colour name:

            \[
            P(\lambda) = \text{power at wavelength }\lambda.
            \]

            Sunlight, a candle and a display pixel can look pale or white while having quite different SPDs. Calling the light “white” reports an appearance under particular conditions; it does not specify the physical recipe.
            """
        ),
        code(
            """
            def gaussian(x, centre, width):
                return np.exp(-0.5 * ((x - centre) / width) ** 2)

            def planck(wavelength_nm, temperature):
                wavelength_m = wavelength_nm * 1e-9
                c2 = 1.438776877e-2
                values = 1 / (wavelength_m**5 * np.expm1(c2 / (wavelength_m * temperature)))
                return values / values.max()

            wavelengths = np.arange(380, 781)
            spectra = {
                "daylight-like source": planck(wavelengths, 5800),
                "candle-like source": planck(wavelengths, 1800),
                "LCD display (white-LED backlight)": (
                    gaussian(wavelengths, 450, 9)
                    + 0.58 * gaussian(wavelengths, 535, 30)
                    + 0.65 * gaussian(wavelengths, 612, 25)
                ),
            }
            spectra["LCD display (white-LED backlight)"] /= spectra["LCD display (white-LED backlight)"].max()

            fig, ax = plt.subplots()
            for label, spectrum in spectra.items():
                ax.plot(wavelengths, spectrum, lw=2.5, label=label)
            ax.set(xlabel="wavelength (nm)", ylabel="relative spectral power",
                   xlim=(380, 780), title="Different physical recipes")
            ax.legend()
            plt.show()
            """
        ),
        md(
            r"""
            ## Light from an object is a product

            An ordinary surface does not contain a fixed colour signal. The spectrum reaching the eye depends on both the illumination and the surface:

            \[
            P_{\text{eye}}(\lambda)
            = P_{\text{illuminant}}(\lambda)\,R_{\text{surface}}(\lambda).
            \]

            `R_surface` is the fraction reflected at each wavelength. Change the lamp and the same surface sends a different spectrum to the eye. This is why colour management needs viewing conditions, not only object labels.
            """
        ),
        code(
            """
            illuminant = planck(wavelengths, 5200)
            reflectance = 0.06 + 0.80 / (1 + np.exp(-(wavelengths - 585) / 13))
            received = illuminant * reflectance

            fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharex=True, sharey=True)
            for ax, values, title in zip(
                axes,
                [illuminant, reflectance, received],
                ["illumination", "surface reflectance", "spectrum reaching the eye"],
            ):
                ax.plot(wavelengths, values, lw=2.5)
                ax.fill_between(wavelengths, values, alpha=.15)
                ax.set(title=title, xlabel="wavelength (nm)", xlim=(380, 780), ylim=(0, 1.05))
            axes[0].set_ylabel("relative amount")
            plt.show()
            """
        ),
        md(
            r"""
            # 2 · What the eye does with light

            Human daylight colour vision begins with three cone classes: S, M and L. Their labels mean **short-, middle- and long-wavelength sensitive**. They should not be renamed blue, green and red receptors: all three have broad, overlapping sensitivities, and two classes can respond strongly to the same wavelength.

            For a teaching model, the response of cone class (i) is:

            \[
            q_i = \int P_{\text{eye}}(\lambda)s_i(\lambda)\,d\lambda,
            \]

            where (P_{\text{eye}}) is the incoming spectrum and (s_i) is that cone class's sensitivity curve. Multiply wavelength by wavelength, then add. One complete spectrum becomes three response values.

            The “three buckets” analogy is useful if used carefully: each bucket has a different spectral filter, and its output is only a total. A single cone cannot report which wavelength caused its response. This is the **principle of univariance**.
            """
        ),
        code(
            """
            def cone_sensitivities(wavelengths):
                # Schematic teaching curves, not physiological reference data.
                return np.column_stack([
                    gaussian(wavelengths, 445, 32),
                    gaussian(wavelengths, 535, 43),
                    gaussian(wavelengths, 565, 48),
                ])

            cones = cone_sensitivities(wavelengths)
            fig, ax = plt.subplots()
            for label, curve, colour in zip(
                ["S", "M", "L"], cones.T, ["#5B4BCE", "#00A878", "#E44B35"]
            ):
                ax.plot(wavelengths, curve, lw=2.8, label=label, color=colour)
            ax.set(xlabel="wavelength (nm)", ylabel="relative sensitivity",
                   xlim=(380, 780), ylim=(0, 1.05),
                   title="Schematic cone sensitivities overlap")
            ax.legend()
            plt.show()
            """
        ),
        code(
            """
            def cone_response(spectrum):
                return np.trapezoid(spectrum[:, None] * cones, wavelengths, axis=0)

            response_rows = []
            for label, spectrum in spectra.items():
                response = cone_response(spectrum)
                response_rows.append([label, *response])

            responses = pd.DataFrame(response_rows, columns=["light", "S", "M", "L"])
            responses[["S", "M", "L"]] = responses[["S", "M", "L"]].div(
                responses[["S", "M", "L"]].max(axis=1), axis=0
            )
            responses.round(3)
            """
        ),
        md(
            """
            ## What three cone responses explain—and what they do not

            Three-channel sampling explains **colour matching**. If two spectra produce the same three responses for an observer under fixed conditions, the observer cannot distinguish them by colour in that matching task. Such spectra are **metamers**.

            This is why a display can match the appearance of a spectral yellow using red and green primaries. The display does not recreate the original spectrum. It creates another spectrum that produces the required match.

            Trichromacy does not explain everything about appearance. After the cones, the visual system compares signals across space and time, forms opponent channels, adapts to illumination and uses surrounding context. The same retinal input can therefore contribute to different appearances in different scenes.
            """
        ),
        md(
            """
            # 3 · Metamerism: what a display exploits

            The next calculation constructs two different, non-negative spectra with the same response under the CIE 1931 standard observer. The linear algebra is supplied; concentrate on the result.
            """
        ),
        code(
            """
            cie = pd.read_csv(
                DATA_FILE,
                header=None,
                names=["wavelength", "xbar", "ybar", "zbar"],
            ).query("380 <= wavelength <= 700").copy()

            cie_wavelengths = cie["wavelength"].to_numpy()
            cie_xyz = cie[["xbar", "ybar", "zbar"]].to_numpy()
            response_matrix = cie_xyz.T

            candidate = (
                np.sin(np.linspace(0, 10 * np.pi, len(cie)))
                + 0.35 * np.cos(np.linspace(0, 3 * np.pi, len(cie)))
            )
            invisible_component = candidate - response_matrix.T @ np.linalg.solve(
                response_matrix @ response_matrix.T,
                response_matrix @ candidate,
            )
            invisible_component /= np.max(np.abs(invisible_component))

            spectrum_a = 0.55 + 0.28 * invisible_component
            spectrum_b = 0.55 - 0.28 * invisible_component
            XYZ_a = response_matrix @ spectrum_a
            XYZ_b = response_matrix @ spectrum_b

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(cie_wavelengths, spectrum_a, lw=2.5, label="spectrum A")
            ax.plot(cie_wavelengths, spectrum_b, lw=2.5, label="spectrum B")
            ax.set(xlabel="wavelength (nm)", ylabel="relative power",
                   title="Different spectra")
            ax.legend()
            plt.show()

            comparison = pd.DataFrame(
                [XYZ_a / XYZ_a.sum(), XYZ_b / XYZ_b.sum()],
                index=["A", "B"], columns=["X proportion", "Y proportion", "Z proportion"]
            )
            display(comparison.round(9))
            print("Largest difference in unnormalised XYZ:", np.max(np.abs(XYZ_a - XYZ_b)))
            """
        ),
        md(
            """
            # 4 · Context enters after the first three responses

            Both centre patches below have exactly the same RGB values. If they appear different, the pixel did not change. The surround changed the visual system's comparison.

            This matters for visualisation: a palette is never perceived as a list of isolated hexadecimal codes. Every colour is seen against neighbours, backgrounds and display conditions.
            """
        ),
        code(
            """
            image = np.ones((220, 620, 3))
            image[:, :310] = 0.10
            image[:, 310:] = 0.88
            centre = np.array([0.38, 0.52, 0.68])
            image[65:155, 100:210] = centre
            image[65:155, 410:520] = centre

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.imshow(image)
            ax.set_axis_off()
            ax.set_title("Identical centre RGB: [0.38, 0.52, 0.68]")
            plt.show()
            """
        ),
        md(
            """
            # 5 · A short history of different questions

            Colour theory did not advance by everybody answering one question more accurately. Different systems were built for different objects and tasks.

            | Work | Object being studied | Question |
            |---|---|---|
            | Newton, *Opticks* (1704) | rays transformed by prisms | How does white light separate and recombine? |
            | Goethe, *Theory of Colours* (1810) | colour as experienced | How do shadows, boundaries, afterimages and context affect appearance? |
            | Maxwell, 1850s–60s | three-primary matches | How can one light be matched by mixtures of three others? |
            | Munsell, *A Color Notation* (1905) | ordered surface samples | How can hue, value and chroma support practical comparison? |
            | CIE, 1931 | average matching behaviour | How can laboratories and industries report compatible colour matches? |

            Newton's optics and Goethe's observations of appearance operate at different points in the chain. Munsell is a system for ordering surface-colour samples. CIE XYZ is a mathematical system for recording standardised colour matches. Treating all four as rival versions of one colour wheel erases the problem each was designed to solve.
            """
        ),
        md(
            r"""
            # 6 · From matching experiments to CIE XYZ

            Colour measurement did not begin by placing sensors directly inside an eye. Observers adjusted three primary lights until one half of a small field matched a test light in the other half.

            With the real primaries used in the 1931 RGB experiments, some test wavelengths could not be matched using positive amounts of all three primaries. The experimenter moved one primary to the test side. Algebra records that operation as a negative amount on the matching side.

            The CIE then transformed those RGB matching results into the mathematical coordinates **X, Y and Z**. They are not three cone outputs and not three physical lamps. The transform was chosen so that:

            - the standard colour-matching functions are non-negative;
            - (Y) carries the standard photopic luminance quantity; and
            - ordinary colour matching can be calculated with linear algebra.

            For a spectrum (P(\lambda)):

            \[
            X=\int P(\lambda)\bar{x}(\lambda)d\lambda,\quad
            Y=\int P(\lambda)\bar{y}(\lambda)d\lambda,\quad
            Z=\int P(\lambda)\bar{z}(\lambda)d\lambda.
            \]
            """
        ),
        code(
            """
            fig, ax = plt.subplots()
            for column, label, colour in [
                ("xbar", "x̄", "#E44B35"),
                ("ybar", "ȳ", "#00A878"),
                ("zbar", "z̄", "#5B4BCE"),
            ]:
                ax.plot(cie["wavelength"], cie[column], lw=2.5, label=label, color=colour)
            ax.set(xlabel="wavelength (nm)", ylabel="matching function",
                   title="Official CIE 1931 2° colour-matching functions")
            ax.legend()
            plt.show()
            """
        ),
        md(
            r"""
            # 7 · Removing overall scale: chromaticity

            Multiplying a spectrum by two multiplies X, Y and Z by two. Its relative three-way balance is unchanged. Chromaticity coordinates keep that balance:

            \[
            x=\frac{X}{X+Y+Z},\qquad
            y=\frac{Y}{X+Y+Z},\qquad
            z=\frac{Z}{X+Y+Z}=1-x-y.
            \]

            Only two coordinates are needed because the three proportions sum to one. An xy point therefore omits the overall tristimulus scale; it is **not** a complete description of brightness or colour appearance.

            To draw the spectral locus, take one monochromatic wavelength at a time. Read its \(\bar{x},\bar{y},\bar{z}\) values, divide by their sum and plot \((x,y)\). Repeating this over the visible interval traces the curved boundary.
            """
        ),
        code(
            """
            totals = cie_xyz.sum(axis=1)
            spectral_xy = cie_xyz[:, :2] / totals[:, None]

            fig, ax = plt.subplots(figsize=(7, 6))
            ax.plot(spectral_xy[:, 0], spectral_xy[:, 1], color="black", lw=2.2,
                    label="spectral locus")
            ax.plot([spectral_xy[-1, 0], spectral_xy[0, 0]],
                    [spectral_xy[-1, 1], spectral_xy[0, 1]],
                    color="#9475CD", lw=2.2, label="line of purples")
            for wavelength in [420, 460, 500, 540, 580, 620, 680]:
                row = np.argmin(np.abs(cie_wavelengths - wavelength))
                ax.annotate(str(wavelength), spectral_xy[row], xytext=(5, 4),
                            textcoords="offset points", fontsize=8)
            ax.set(xlim=(0, .8), ylim=(0, .9), xlabel="x", ylabel="y",
                   title="CIE 1931 xy chromaticity diagram")
            ax.set_aspect("equal", adjustable="box")
            ax.legend()
            plt.show()
            """
        ),
        md(
            """
            ## Why mixtures lie inside

            Adding two lights adds their spectra. Because XYZ is linear, their XYZ values add too. After normalisation to xy, the mixture lies on the straight segment joining the two chromaticities. Its position depends on the relative amounts.

            A general spectrum is a non-negative mixture of wavelength components, so its chromaticity lies in the convex region bounded by the spectral locus and the straight **line of purples**. Purple is on that closure because it mixes light from opposite ends of the visible spectrum; it is not a single spectral wavelength.
            """
        ),
        code(
            """
            blue = spectral_xy[np.argmin(np.abs(cie_wavelengths - 460))]
            red = spectral_xy[np.argmin(np.abs(cie_wavelengths - 610))]
            amounts = np.linspace(0, 1, 9)
            mixtures = amounts[:, None] * blue + (1 - amounts[:, None]) * red

            fig, ax = plt.subplots(figsize=(7, 6))
            ax.plot(np.r_[spectral_xy[:, 0], spectral_xy[0, 0]],
                    np.r_[spectral_xy[:, 1], spectral_xy[0, 1]], color="#999", lw=1.5)
            ax.plot(mixtures[:, 0], mixtures[:, 1], color="black", lw=2)
            ax.scatter(mixtures[:, 0], mixtures[:, 1], c=amounts,
                       cmap="coolwarm", s=75, edgecolor="white")
            ax.set(xlim=(0, .8), ylim=(0, .9), xlabel="x", ylabel="y",
                   title="Mixtures fall on the line between two lights")
            ax.set_aspect("equal", adjustable="box")
            plt.show()
            """
        ),
        md(
            """
            # 8 · A display gamut is a triangle, not the horseshoe

            A display has three physical primaries. Positive mixtures of those primaries produce chromaticities inside the triangle joining their coordinates. A wider triangle reaches more chromaticities, but no three real primaries cover the entire spectral locus.

            The diagram is not a screenshot of all visible colours. Your notebook itself is displayed through your monitor's gamut, so colours outside that gamut cannot be shown faithfully even if their coordinates can be drawn.
            """
        ),
        code(
            """
            GAMUTS = {
                "sRGB / Rec.709": np.array([[0.640, 0.330], [0.300, 0.600], [0.150, 0.060]]),
                "Display P3": np.array([[0.680, 0.320], [0.265, 0.690], [0.150, 0.060]]),
                "Rec.2020": np.array([[0.708, 0.292], [0.170, 0.797], [0.131, 0.046]]),
            }

            fig, ax = plt.subplots(figsize=(7, 6))
            ax.plot(np.r_[spectral_xy[:, 0], spectral_xy[0, 0]],
                    np.r_[spectral_xy[:, 1], spectral_xy[0, 1]], color="black", lw=2)
            for name, triangle in GAMUTS.items():
                closed = np.vstack([triangle, triangle[0]])
                ax.plot(closed[:, 0], closed[:, 1], marker="o", lw=2, label=name)
            ax.set(xlim=(0, .8), ylim=(0, .9), xlabel="x", ylabel="y",
                   title="Three display primaries define a triangular gamut")
            ax.set_aspect("equal", adjustable="box")
            ax.legend()
            plt.show()
            """
        ),
        md(
            """
            # 9 · What this means for data visualisation

            Colour is a useful but conditional encoding channel.

            - **Hue** is effective for distinguishing a modest number of categories; it does not supply a natural numerical order.
            - **Lightness** can carry order when it changes monotonically.
            - **Chroma** changes emphasis but supports only coarse comparisons.
            - Equal steps in RGB or HSL are not equal perceptual steps.
            - A palette must be tested against its actual background, at its actual mark size, and under relevant colour-vision differences.
            - Important distinctions need a redundant cue such as position, direct labelling, shape or line style.

            The screen receives codes. The viewer experiences comparisons in context. Designing only the codes ignores the middle of the chain.
            """
        ),
        md(
            """
            # 10 · Streamlit: turn the calculation into an explanatory interface

            A notebook runs cells when you ask. A Streamlit app is an ordinary Python script that **reruns from top to bottom whenever a widget changes**.

            The basic pattern is:

            ```text
            widget produces a Python value
                         ↓
            ordinary Python transforms that value
                         ↓
            st.* commands draw the new result
            ```

            Common translations:

            | Notebook or script | Streamlit app |
            |---|---|
            | fixed value `wavelength = 550` | widget `wavelength = st.slider(...)` |
            | `print(value)` | `st.write(value)` or `st.metric(...)` |
            | `display(df)` | `st.dataframe(df)` or `st.table(df)` |
            | `plt.show()` | `st.pyplot(fig)` |
            | headings in Markdown cells | `st.title()`, `st.header()`, `st.markdown()` |

            Start with the smallest possible app.
            """
        ),
        code(
            f"""
            from pathlib import Path

            HELLO_APP = {HELLO_APP!r}
            hello_path = Path("hello_colour.py")
            hello_path.write_text(HELLO_APP, encoding="utf-8")
            print(f"Wrote {{hello_path.resolve()}}")
            print("Run: python -m streamlit run hello_colour.py")
            """
        ),
        md(
            """
            Open a terminal in this notebook folder and run:

            ```bash
            python -m streamlit run hello_colour.py
            ```

            Streamlit opens a local page, normally at `http://localhost:8501`. Move the slider and watch the printed wavelength update. Nothing calls a special event handler: the new widget value is assigned and the whole script reruns.

            Stop the server with `Ctrl+C` when finished.
            """
        ),
        md(
            """
            ## Build the complete spectrum explorer

            The next cell writes a complete app. Read it in this order:

            1. imports and page configuration;
            2. functions that contain the model;
            3. sidebar widgets that create the current input values;
            4. calculations derived from those values; and
            5. tabs that present three different representations.

            The app uses `@st.cache_data` only for the fixed CIE table. The spectrum and plots must recompute when a widget changes.
            """
        ),
        code(
            f"""
            APP_SOURCE = {APP_SOURCE!r}
            app_path = Path("vision_colour_app.py")
            app_path.write_text(APP_SOURCE, encoding="utf-8")
            compile(APP_SOURCE, str(app_path), "exec")
            print(f"Wrote {{app_path.resolve()}} ({{len(APP_SOURCE.splitlines())}} lines)")
            print("Run: python -m streamlit run vision_colour_app.py")
            """
        ),
        md(
            """
            ## Your extension: separate intensity from chromaticity

            Add an `Intensity` slider to the sidebar and multiply the entire spectrum by its value.

            **Prediction before coding:** Which outputs should change? Which should remain stable?

            **Definition of done:**

            - the spectrum height changes;
            - the unnormalised S, M and L responses change;
            - the chromaticity point remains in the same place, apart from rounding;
            - the app includes one sentence explaining why.

            This is a better test than “the app runs”: it checks whether the interface preserves the distinction between amount of light and its chromaticity.
            """
        ),
        code(
            """
            # Record your intended edit or paste the revised block here.
            # Then make the same change in vision_colour_app.py and test it in the browser.

            my_change = ""
            print(my_change or "Describe your change before editing the app.")
            """
        ),
        md(
            """
            ## Review the app as a visual explanation

            Exchange screens with another student. Ask them to answer without seeing the code:

            1. What is the physical input?
            2. Where is that input reduced to three numbers?
            3. What does the xy point preserve and omit?
            4. Which curves are official data and which are schematic?
            5. What claim would be wrong to make from this app?

            Revise one label, caption or arrangement based on where they hesitate.
            """
        ),
        md(
            """
            # Sources

            - CIE, [CIE 1931 2° colour-matching functions](https://cie.co.at/datatable/cie-1931-colour-matching-functions-2-degree-observer), DOI `10.25039/CIE.DS.xvudnb9b`.
            - Kalloniatis and Luu, [The Perception of Color](https://www.ncbi.nlm.nih.gov/books/NBK11538/), *Webvision*.
            - Isaac Newton, [*Opticks* (1704)](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00034).
            - J. W. von Goethe, [*Theory of Colours* (1810)](https://www.gutenberg.org/ebooks/50572).
            - A. H. Munsell, [*A Color Notation* (1905)](https://www.gutenberg.org/ebooks/26054).
            - W3C, [CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/).
            - Streamlit, [Basic concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts).

            **Model boundaries:** the cone curves and wavelength-to-display approximations in this lesson are schematic. CIE data are standard-observer colour-matching functions, not measured cone sensitivities. The app does not model adaptation, spatial context, individual observer variation, fluorescence or device calibration.
            """
        ),
    ]

    notebook = nbf.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
    )
    notebook_path = NOTEBOOKS / "vision_color_perception_lab.ipynb"
    nbf.write(notebook, notebook_path)
    (NOTEBOOKS / "vision_colour_app.py").write_text(APP_SOURCE, encoding="utf-8")
    (NOTEBOOKS / "hello_colour.py").write_text(HELLO_APP, encoding="utf-8")

    for cell in notebook.cells:
        if cell.cell_type == "code":
            ast.parse(cell.source)
    ast.parse(APP_SOURCE)
    ast.parse(HELLO_APP)
    print(f"Wrote {notebook_path}")


if __name__ == "__main__":
    make_figures()
    build_notebook()

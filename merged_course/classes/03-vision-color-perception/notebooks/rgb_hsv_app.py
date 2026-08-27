"""Two slider sets, one colour space. Run with:
python -m streamlit run rgb_hsv_app.py
"""
import colorsys

import streamlit as st

st.set_page_config(page_title="RGB and HSV", page_icon="🎚️", layout="wide")
st.title("RGB and HSV")
st.caption("The same colours, described on two sets of axes.")


def swatch(hexcode):
    st.markdown(
        f'<div style="height:130px;border-radius:10px;border:1px solid #ccc;'
        f'background:{hexcode}"></div>',
        unsafe_allow_html=True,
    )
    st.code(hexcode)


left, right = st.columns(2, gap="large")

with left:
    st.subheader("RGB: three lamp intensities")
    r = st.slider("R", 0, 255, 230)
    g = st.slider("G", 0, 255, 60)
    b = st.slider("B", 0, 255, 200)
    swatch(f"#{r:02X}{g:02X}{b:02X}")
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    st.write(
        f"The same colour in HSV: hue {h*360:.0f}°, "
        f"saturation {s*100:.0f}%, value {v*100:.0f}%."
    )

with right:
    st.subheader("HSV: the same cube on cylinder axes")
    hh = st.slider("Hue (degrees around the wheel)", 0, 360, 210)
    st.markdown(
        '<div style="height:10px;border-radius:5px;background:linear-gradient('
        "90deg,#f00,#ff0,#0f0,#0ff,#00f,#f0f,#f00)\"></div>",
        unsafe_allow_html=True,
    )
    ss = st.slider("Saturation (distance from grey)", 0, 100, 85)
    vv = st.slider("Value (brightness of the strongest channel)", 0, 100, 90)
    r2, g2, b2 = (
        round(c * 255) for c in colorsys.hsv_to_rgb(hh / 360, ss / 100, vv / 100)
    )
    swatch(f"#{r2:02X}{g2:02X}{b2:02X}")
    st.write(f"The same colour in RGB: R {r2}, G {g2}, B {b2}.")

st.divider()
st.markdown(
    """
**How HSV relates to RGB.** HSV adds no new colours; it re-describes the
same 16,777,216 RGB codes on axes that match how people think about colour.

- **Value** is the largest of the three channels. Turn all three lamps down
  together and value falls.
- **Saturation** measures how far the smallest channel sits below the
  largest. Equal channels give grey (saturation 0); one channel at zero
  gives a fully saturated colour.
- **Hue** records which channel leads and by how much, wrapped onto a
  0-360° wheel: red at 0°, yellow 60°, green 120°, cyan 180°, blue 240°,
  magenta 300°.

Set saturation to 0 and hue stops mattering: the wheel collapses to the
grey axis. That is why hue is meaningless for near-grey colours.
"""
)

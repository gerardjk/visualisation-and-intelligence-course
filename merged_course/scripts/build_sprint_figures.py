"""Regenerate the Seeing Data claim-sprint figures with large axis fonts.

Two kinds of figure:
- canonical forms (Gaussian, log-normal, power law, species abundance,
  S-curve, violin): code lifted from the course figure library, re-rendered
  with bigger fonts;
- real measurements (Ngram, sea ice, cherry blossom, market candlesticks,
  GW150914, sunspots): fetched from the public source at build time and
  cached under data/, so the charts are real, not representative.

Writes PNGs into classes/01-seeing-data/beamer/figs/.
"""

import io
import json
import re
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT.parent / "quarto-book" / "atlas.qmd"
OUT = ROOT / "classes" / "01-seeing-data" / "beamer" / "figs"
CACHE = ROOT / "shared" / "data"
CACHE.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 15,
    "axes.labelsize": 17,
    "axes.titlesize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
})

UA = {"User-Agent": "Mozilla/5.0 (course-build)"}


def fetch(url, dest, binary=False):
    dest = CACHE / dest
    if not dest.exists():
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=60).read()
        dest.write_bytes(data)
    return dest.read_bytes() if binary else dest.read_text(errors="replace")


def save(name):
    plt.gcf().savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close("all")
    print("built", name)


# ---------------- canonical forms, from the course figure code ----------------
FORM_BLOCKS = ["gaussian", "lognormal", "powerlaw", "sad", "logistic", "violin"]


def atlas_code(label):
    text = ATLAS.read_text()
    m = re.search(r"```\{python\}\n#\| label: fig-" + label + r"\n(.*?)```",
                  text, re.S)
    assert m, f"fig-{label} not found in atlas.qmd"
    return "\n".join(l for l in m.group(1).split("\n")
                     if not l.startswith("#|"))


def build_forms():
    for label in FORM_BLOCKS:
        code = atlas_code(label)
        exec(code, {"np": np, "plt": plt, "pd": pd})
        suffix = "output-2" if label == "lognormal" else "output-1"
        save(f"fig-{label}-{suffix}.png")


# ---------------- real measurements ----------------

def build_ngram():
    url = ("https://books.google.com/ngrams/json?content="
           "telegraph,telephone,internet&year_start=1850&year_end=2019"
           "&corpus=en&smoothing=3")
    data = json.loads(fetch(url, "ngram_telegraph_telephone_internet.json"))
    fig, ax = plt.subplots(figsize=(8, 4.4))
    years = np.arange(1850, 2020)
    for series in data:
        ax.plot(years, series["timeseries"], lw=2.2,
                label=series["ngram"].split(" (")[0])
    ax.set_xlabel("year")
    ax.set_ylabel("relative frequency in books")
    ax.set_title("Google Books Ngram: three technologies", fontsize=16)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save("fig-ngram-output-1.png")


def build_seaice():
    url = ("https://noaadata.apps.nsidc.org/NOAA/G02135/north/daily/data/"
           "N_seaice_extent_daily_v4.0.csv")
    raw = fetch(url, "nsidc_seaice_daily.csv")
    df = pd.read_csv(io.StringIO(raw), skiprows=[1])
    df.columns = [c.strip() for c in df.columns]
    df = df[["Year", "Month", "Day", "Extent"]].astype(float)
    monthly = df.groupby(["Year", "Month"])["Extent"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4.4))
    years = sorted(monthly["Year"].unique())
    cmap = plt.cm.viridis
    for y in years:
        g = monthly[monthly["Year"] == y]
        if len(g) < 12:
            continue
        ax.plot(g["Month"], g["Extent"], color=cmap((y - years[0]) / (years[-1] - years[0])),
                lw=1.1, alpha=0.85)
    sm = plt.cm.ScalarMappable(cmap=cmap,
                               norm=plt.Normalize(years[0], years[-1]))
    fig.colorbar(sm, ax=ax, label="year")
    ax.set_xlabel("month")
    ax.set_ylabel("extent (million km²)")
    ax.set_title("Arctic sea-ice extent, NSIDC Sea Ice Index", fontsize=16)
    plt.tight_layout()
    save("fig-seaice-output-1.png")


def build_cherry():
    # Aono & Kazui Kyoto full-flowering series, from the authoritative source.
    url = ("https://www.ncei.noaa.gov/pub/data/paleo/historical/"
           "phenology/japan/LatestVersion/KyotoFullFlower7.xls")
    data = fetch(url, "KyotoFullFlower7.xls", binary=True)
    df = pd.read_excel(io.BytesIO(data), header=None)
    # locate the data block: first column AD year, second full-flowering DOY
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df[[0, 1]].dropna()
    df.columns = ["year", "doy"]
    df = df[(df["year"] >= 800) & (df["doy"] > 50) & (df["doy"] < 150)]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.scatter(df["year"], df["doy"], s=8, alpha=0.4, color="#c76b8e")
    roll = df.set_index("year")["doy"].rolling(30, min_periods=10).mean()
    ax.plot(roll.index, roll.values, color="#7a1f42", lw=2.2,
            label="30-year rolling mean")
    ax.set_xlabel("year")
    ax.set_ylabel("full-bloom day of year")
    ax.set_title("Kyoto cherry full-bloom dates (Aono & Kazui)", fontsize=16)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save("fig-cherry-output-1.png")


def build_candlestick():
    # ASX 200 daily OHLC from the Yahoo Finance chart API (no key needed).
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/%5EAXJO"
           "?range=3mo&interval=1d")
    data = json.loads(fetch(url, "axjo_daily.json"))
    r = data["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    import datetime
    rows = [(datetime.datetime.fromtimestamp(t).date(), o, h, l, c)
            for t, o, h, l, c in zip(r["timestamp"], q["open"], q["high"],
                                     q["low"], q["close"])
            if None not in (o, h, l, c)][-30:]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    for i, (d, o, h, l, c) in enumerate(rows):
        up = c >= o
        color = "#2e8b57" if up else "#c0392b"
        ax.plot([i, i], [l, h], color=color, lw=1.4)
        ax.add_patch(plt.Rectangle((i - 0.32, min(o, c)), 0.64,
                                   abs(c - o) or 0.5, color=color))
    ax.set_xlabel("trading session")
    ax.set_ylabel("ASX 200 index level")
    ax.set_title(f"ASX 200, last 30 sessions to {rows[-1][0]}", fontsize=16)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save("fig-candlestick-output-1.png")


def build_ligo():
    # The observed H1 strain behind Fig. 1 of the GW150914 discovery paper.
    url = "https://gwosc.org/GW150914data/P150914/fig1-observed-H.txt"
    raw = fetch(url, "gw150914_fig1_observed_H.txt")
    rows = [l.split() for l in raw.splitlines()
            if l.strip() and not l.startswith("#")]
    arr = np.array(rows, dtype=float)
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(arr[:, 0], arr[:, 1], color="#b03a2e", lw=1.4)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("strain (×10⁻²¹)")
    ax.set_title("GW150914: observed strain, LIGO Hanford", fontsize=16)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save("fig-ligo-output-1.png")


def build_sunspots():
    # SILSO monthly mean sunspot number (the longest-running experiment).
    raw = fetch("https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.csv",
                "silso_sunspots_monthly.csv")
    df = pd.read_csv(io.StringIO(raw), sep=";", header=None,
                     names=["year", "month", "frac_year", "sn", "sd", "nobs",
                            "provisional"])
    df = df[df["sn"] >= 0]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(df["frac_year"], df["sn"], lw=0.8, color="#b8860b")
    ax.set_xlabel("year")
    ax.set_ylabel("monthly mean sunspot number")
    ax.set_title("Sunspots since 1749, SILSO", fontsize=16)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    save("sprint-sunspots.png")


if __name__ == "__main__":
    build_forms()
    build_ngram()
    build_seaice()
    build_cherry()
    build_candlestick()
    build_ligo()
    build_sunspots()

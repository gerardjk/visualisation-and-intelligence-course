"""Build the twelve-entry A1 artefact pool. This script never uploads to Canvas."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import subprocess
import tempfile
import zipfile
from collections import Counter, defaultdict, deque
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
A1 = ROOT / "assessments/A1-critique-and-repair"
POOL = A1 / "pool"
ATLAS_FIGS = REPO / "quarto-book/_book/atlas_files/figure-html"


def spec(n, category, title, publisher, page, chart, data, mode, fields, **extra):
    return dict(id=f"POOL-{n:02d}", category=category, title=title,
                publisher=publisher, page=page, chart=chart, data=data,
                mode=mode, fields=fields, **extra)


SPECS = [
    spec(1, "Deviation", "Global mean temperature anomaly", "NASA Goddard Institute for Space Studies",
         "https://data.giss.nasa.gov/gistemp/graphs_v4/",
         "https://data.giss.nasa.gov/gistemp/graphs_v4/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.png",
         "https://data.giss.nasa.gov/gistemp/graphs_v4/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.csv", "giss",
         {"year": "Calendar year.", "anomaly_c": "Annual global mean surface temperature anomaly, °C relative to the 1951–1980 baseline.", "lowess_c": "Lowess-smoothed (5-year) anomaly, °C.", "uncertainty_95_c": "Published 95% uncertainty half-width, °C; available through 2018.", "uncertainty_low_c": "Annual anomaly minus the published 95% uncertainty half-width, °C.", "uncertainty_high_c": "Annual anomaly plus the published 95% uncertainty half-width, °C."},
         uncertainty_data="https://data.giss.nasa.gov/gistemp/uncertainty/v1.2.1/totalCI_ERA.csv",
         matching_note="Annual mean and LOWESS values come from the chart CSV. The published NASA 95% uncertainty series is merged through 2018; NASA's downloadable historical interval ends there, so later interval fields are blank.",
         publication="Updated annually", licence="NASA; US government work, public domain."),
    spec(2, "Correlation", "Life expectancy vs health expenditure", "Our World in Data",
         "https://ourworldindata.org/grapher/life-expectancy-vs-health-expenditure",
         "https://ourworldindata.org/grapher/life-expectancy-vs-health-expenditure.png",
         "https://ourworldindata.org/grapher/life-expectancy-vs-health-expenditure.csv", "owid_health",
         {"country": "Country or territory.", "code": "ISO 3166-1 alpha-3 code.", "year": "Year of observation.", "life_expectancy_years": "Period life expectancy at birth, years.", "health_exp_per_capita_usd": "Health expenditure per capita, international dollars.", "region": "World region according to OWID."},
         publication="Updated annually", licence="CC BY 4.0."),
    spec(3, "Correlation", "Hubble's 1929 distance–velocity relation", "Proceedings of the National Academy of Sciences",
         "https://pmc.ncbi.nlm.nih.gov/articles/PMC522427/", "local:hubble-1929.png",
         "https://apod.nasa.gov/diamond_jubilee/1996/hub_1929.html", "hubble",
         {"record_type": "Individual nebula observation or the reference mean shown as a cross.", "object": "Object name from Hubble's Table 1, or the reference-mean label.", "distance_mpc": "Distance in megaparsecs as tabulated by Hubble.", "velocity_km_s": "Measured radial velocity in kilometres per second; the reference-mean row is the corrected value printed in the paper.", "individual_fit_slope": "Published K coefficient for the 24-object solution, km/s/Mpc.", "group_fit_slope": "Published K coefficient for the nine-group solution, km/s/Mpc."},
         matching_note="The CSV now includes object labels, both published line slopes and the reference mean shown as a cross. Hubble did not tabulate the solar-motion-corrected individual velocities or the nine grouped plotting coordinates, so those parts of the historical figure cannot be reconstructed exactly from the paper's tables.",
         publication="1929", licence="Public-domain historical figure and tabulated observations."),
    spec(4, "Ranking", "Country rankings by life evaluation, 2021–2023", "World Happiness Report",
         "https://worldhappiness.report/ed/2024/", "pdf:https://files.worldhappiness.report/WHR24.pdf#page=17",
         "https://files.worldhappiness.report/WHR24_Data_Figure_2.1.xls", "happiness",
         {"rank": "Rank by mean life evaluation.", "country": "Country or territory.", "life_evaluation": "Mean Cantril Ladder score, 0–10.", "score_ci_low": "Lower endpoint of the score's 95% confidence interval.", "score_ci_high": "Upper endpoint of the score's 95% confidence interval."},
         matching_note="The supplied image is the first page of the multi-page Figure 2.1 and shows ranks 1–48. The complete 143-country Figure 2.1 table and score confidence intervals are supplied in the CSV. The simultaneous confidence intervals for rank printed as text beside the original bars are not included in the downloadable workbook.",
         publication="2024", licence="World Happiness Report supporting data; report reproduction terms apply."),
    spec(5, "Distribution", "Lorenz curves for US family income", "OpenStax",
         "https://openstax.org/books/principles-economics-3e/pages/15-4-income-inequality-measurement-and-causes",
         "https://openstax.org/apps/archive/20260604.144757/resources/7173a2545e7c437dcbd9f62692b185b1d9718eb8",
         "https://openstax.org/books/principles-economics-3e/pages/15-4-income-inequality-measurement-and-causes", "lorenz",
         {"population_share": "Cumulative share of families.", "income_share_1980": "Cumulative family-income share in 1980.", "income_share_2020": "Cumulative family-income share in 2020."},
         publication="2022", licence="CC BY 4.0."),
    spec(6, "Flow", "Estimated US energy consumption, 2023", "Lawrence Livermore National Laboratory / US Department of Energy",
         "https://flowcharts.llnl.gov/commodities/energy",
         "https://flowcharts.llnl.gov/sites/flowcharts/files/2024-12/energy-2023-united-states.png",
         "https://flowcharts.llnl.gov/commodities/energy", "llnl_energy",
         {"source": "Node the energy flows out of.", "target": "Node the energy flows into.", "quads": "Energy flow in quadrillion BTU (quads), as printed on the published diagram."},
         matching_note="Every CSV flow value reproduces a number printed on the published diagram (source: DOE/EIA SEDS via LLNL), rather than a width digitised from pixels. The published diagram is internally non-additive beyond what its displayed precision can explain: terminal components sum to 32.38 quads of Energy Services and 61.12 quads of Rejected Energy, while the aggregate nodes are labelled 32.1 and 61.5. Industrial labelled outputs sum to 26.4 against a 26.1 node; Transportation labelled outputs sum to 27.57 against a 28 node. Treat this as a documented source limitation, not a student calculation error.",
         publication="2023 data; diagram released October 2024", licence="Credit to Lawrence Livermore National Laboratory and the Department of Energy is required for reproduction."),
    spec(7, "Change over time", "Measures of underlying inflation", "Reserve Bank of Australia",
         "https://www.rba.gov.au/chart-pack/aus-inflation.html",
         "https://www.rba.gov.au/chart-pack/images/aus-inflation/underlying-inflation.svg",
         "https://www.rba.gov.au/statistics/tables/csv/g1-data.csv", "rba_g1",
         {"quarter": "Quarter end date (ISO).", "cpi_excl_volatile_pct": "Year-ended CPI inflation excluding volatile items, interest charges and tax changes, per cent.", "weighted_median_pct": "Year-ended weighted median inflation, per cent.", "trimmed_mean_pct": "Year-ended trimmed mean inflation, per cent."},
         publication="Updated monthly (Chart Pack); table G1 quarterly", licence="© Reserve Bank of Australia; reproduction with attribution permitted."),
    spec(8, "Correlation", "Lynx–hare phase portrait (Hudson Bay pelt records)", "San Diego State University (J. M. Mahaffy)",
         "https://jmahaffy.sdsu.edu/courses/f09/math636/lectures/lotka/qualde2.html",
         "https://jmahaffy.sdsu.edu/courses/f09/math636/lectures/lotka/images/phaselyhar.jpg",
         "https://jmahaffy.sdsu.edu/courses/f09/math636/lectures/lotka/qualde2.html", "lynxhare",
         {"year": "Trapping year.", "hares_thousands": "Snowshoe hare pelts traded, thousands.", "lynx_thousands": "Canada lynx pelts traded, thousands."},
         matching_note="These are the 21 observations for 1900–1920 printed on the same source page as the phase portrait, replacing the previously supplied and non-matching 1845–1935 series.",
         publication="Course publication; chart data 1900–1920", licence="Educational criticism and review with attribution; historical data public domain."),
    spec(9, "Magnitude", "Cosmic abundance of the elements", "NASA Imagine the Universe / HEASARC",
         "https://imagine.gsfc.nasa.gov/educators/elements/imagine/cosmic_abundances.html",
         "https://imagine.gsfc.nasa.gov/Images/educators/posters/elements/booklet/solar_abundances_big.jpg",
         "https://chem.libretexts.org/Bookshelves/General_Chemistry/Interactive_Chemistry_(Moore_Zhou_and_Garand)/06%3A_Appendix/6.02%3A_Elemental_Abundances", "abundance",
         {"atomic_number": "Atomic number.", "element": "Chemical symbol.", "atoms_per_1e12_H": "Solar-system abundance scaled to one trillion hydrogen atoms.", "log10_atoms_per_1e12_H": "Base-10 logarithm of atoms_per_1e12_H, matching the chart's H=12 scale."},
         matching_note="The full available Anders–Grevesse solar-system table is supplied through uranium (atomic number 92), normalised to one trillion hydrogen atoms. Elements without a stable natural abundance are absent rather than assigned invented zeroes.",
         publication="NASA educational poster; abundance table accessed 2026", licence="NASA media usage guidelines; data table CC BY-NC-SA 4.0."),
    spec(10, "Part-to-whole", "Sources of US electricity generation", "US Energy Information Administration",
         "https://www.eia.gov/energyexplained/electricity/electricity-in-the-us.php",
         "https://www.eia.gov/energyexplained/electricity/images/outlet-graph-large.jpg",
         "https://www.eia.gov/energyexplained/electricity/electricity-in-the-us.php", "eia_mix",
         {"energy_source": "Fuel or generation source as named in the chart.", "parent_source": "Parent category for renewable subtypes; blank for major sources.", "level": "Major source or renewable subtype.", "share_pct": "Publisher-labelled share of 2025 utility-scale generation, per cent.", "approx_billion_kwh": "Approximate billion kWh derived from the rounded share and EIA's 4.43-trillion-kWh total.", "display_order": "Order used in the published graphic."},
         matching_note="The CSV uses the percentages printed in the supplied 2025 EIA graphic and page. Approximate generation amounts are derived from EIA's stated 4.43-trillion-kWh total and should not be treated as unrounded source measurements. Independently rounded shares sum to 99.9% for the major sources and 24.2% for the renewable subtypes, while the displayed renewable total is 24.1%.",
         publication="2025 data; page updated 2026", licence="US Energy Information Administration; US government work, public domain."),
    spec(11, "Spatial", "Seismicity of the Earth 1900–2007", "US Geological Survey",
         "https://pubs.usgs.gov/sim/3064/",
         "pdf:https://pubs.usgs.gov/sim/3064/pdf/SIM3064.pdf#page=1",
         "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=1900-01-01&endtime=2008-01-01&minmagnitude=7.3&orderby=time", "quakes",
         {"date": "Origin date (UTC).", "latitude": "Epicentre latitude, degrees.", "longitude": "Epicentre longitude, degrees.", "depth_km": "Hypocentre depth, kilometres.", "magnitude": "Moment magnitude.", "place": "USGS region description."},
         matching_note="The catalogue extract covers the map's own 1900–2007 window, filtered to magnitude 7.3 and above so the file stays beginner-sized. The published map plots smaller events too, so it shows many more points than the extract; early decades are also sparser in the instrumental catalogue.",
         publication="2010 (map); catalogue extract 1900–2007, M ≥ 7.3", licence="US Geological Survey; US government work, public domain.", dpi=30),
    spec(12, "Flow", "Worldwide airline route network", "OpenFlights",
         "https://openflights.org/data.php", "https://openflights.org/demo/openflights-routedb-2048.png",
         "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat", "routes",
         {"airport_a_iata": "IATA code for the alphabetically first endpoint of an undirected airport pair.", "airport_a_city": "City for endpoint A.", "airport_a_lat": "Latitude of endpoint A.", "airport_a_lon": "Longitude of endpoint A.", "airport_b_iata": "IATA code for the alphabetically second endpoint of an undirected airport pair.", "airport_b_city": "City for endpoint B.", "airport_b_lat": "Latitude of endpoint B.", "airport_b_lon": "Longitude of endpoint B.", "airline_record_count": "Number of historical OpenFlights airline-route records aggregated across both directions for the airport pair; not passenger, flight or seat volume."},
         matching_note="A beginner-sized curated extract: the 250 undirected airport pairs with the largest historical airline-record counts, aggregated across airlines and both directions. Endpoint A/B labels do not encode travel direction, and airline-record count is not passenger or flight volume. The published image draws the full route database (about 19,000 unique pairs), so the extract reproduces major corridors rather than its full density; the complete database remains available at the source-data link.",
         publication="OpenFlights route database snapshot (historical, June 2014)", licence="Open Database License; image attribution per OpenFlights."),
]

# Canonical values copied verbatim into each pool provenance sheet and META_n.
# Several entries intentionally share a domain so the three-domain selection
# rule is meaningful rather than a free-text exercise.
POOL_DOMAINS = {
    "POOL-01": "climate science",
    "POOL-02": "public health",
    "POOL-03": "astronomy",
    "POOL-04": "wellbeing",
    "POOL-05": "economics",
    "POOL-06": "energy",
    "POOL-07": "economics",
    "POOL-08": "ecology",
    "POOL-09": "astronomy",
    "POOL-10": "energy",
    "POOL-11": "geophysics",
    "POOL-12": "transportation",
}
for pool_spec in SPECS:
    pool_spec["domain"] = POOL_DOMAINS[pool_spec["id"]]


def fetch(url: str) -> bytes:
    cache = Path("/tmp/a1-source-cache") / sha(url.encode())
    if cache.exists() and cache.stat().st_size:
        return cache.read_bytes()
    cache.parent.mkdir(parents=True, exist_ok=True)
    run = subprocess.run(["curl", "-fsSL", "--max-time", "45", url], capture_output=True)
    if run.returncode:
        raise RuntimeError(f"download failed: {url}: {run.stderr.decode()[-300:]}")
    cache.write_bytes(run.stdout)
    return run.stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def xlsx_sheet(raw: bytes, wanted: str | None = None) -> list[list[object]]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships", "p": "http://schemas.openxmlformats.org/package/2006/relationships"}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", ns)) for si in root.findall("m:si", ns)]
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall("p:Relationship", ns)}
        sheets = wb.findall("m:sheets/m:sheet", ns)
        sheet = next((s for s in sheets if s.attrib.get("name") == wanted), sheets[0])
        target = targets[sheet.attrib[f"{{{ns['r']}}}id"]].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        root = ET.fromstring(z.read(target))
        out = []
        for row in root.findall(".//m:sheetData/m:row", ns):
            vals = {}
            for cell in row.findall("m:c", ns):
                ref = cell.attrib["r"]
                col = 0
                for ch in re.match(r"[A-Z]+", ref).group():
                    col = col * 26 + ord(ch) - 64
                typ = cell.attrib.get("t")
                node = cell.find("m:v", ns)
                if typ == "inlineStr":
                    value = "".join(t.text or "" for t in cell.findall(".//m:t", ns))
                elif node is None:
                    value = None
                elif typ == "s":
                    value = shared[int(node.text)]
                else:
                    value = node.text
                    try: value = float(value)
                    except (TypeError, ValueError): pass
                vals[col - 1] = value
            width = max(vals, default=-1) + 1
            out.append([vals.get(i) for i in range(width)])
        return out


def chart_bytes(s):
    if s["chart"].endswith(".svg"):
        raw = fetch(s["chart"])
        with tempfile.TemporaryDirectory(prefix="a1-svg-") as td:
            src = Path(td) / "chart.svg"
            src.write_bytes(raw)
            subprocess.run(["soffice", f"-env:UserInstallation=file://{td}/profile",
                            "--headless", "--convert-to", "png", "--outdir", td, str(src)],
                           check=True, capture_output=True)
            return (Path(td) / "chart.png").read_bytes(), ".png"
    if s["chart"].startswith("local:"):
        name = s["chart"].split(":", 1)[1]
        p = ROOT / "shared/assets/originals" / name
        if not p.exists(): p = ATLAS_FIGS / name
        return p.read_bytes(), p.suffix
    if s["chart"].startswith("pdf:"):
        url, page = s["chart"][4:].split("#page=")
        saved = Path("/tmp/whr24.pdf")
        raw = saved.read_bytes() if saved.exists() and url.endswith("WHR24.pdf") else fetch(url)
        dpi = str(s.get("dpi", 160))
        with tempfile.TemporaryDirectory(prefix="a1-pdf-") as td:
            src, base = Path(td) / "source.pdf", Path(td) / "page"
            src.write_bytes(raw)
            subprocess.run(["pdftoppm", "-f", page, "-l", page, "-png", "-singlefile", "-r", dpi, str(src), str(base)], check=True, capture_output=True)
            return (base.with_suffix(".png")).read_bytes(), ".png"
    raw = fetch(s["chart"])
    return raw, ".jpg" if raw[:2] == b"\xff\xd8" else ".png"


def dihedral(a, b, c, d):
    b0, b1, b2 = -(b-a), c-b, d-c
    b1 = b1 / np.linalg.norm(b1)
    v, w = b0 - np.dot(b0, b1)*b1, b2 - np.dot(b2, b1)*b1
    return math.degrees(math.atan2(np.dot(np.cross(b1, v), w), np.dot(v, w)))


def extract_data(s, raw):
    mode = s["mode"]
    if mode == "csv":
        return pd.read_csv(io.BytesIO(raw)).dropna()
    if mode == "llnl_energy":
        flows = [
            ("Solar", "Electricity Generation", 0.56), ("Solar", "Residential", 0.24),
            ("Solar", "Commercial", 0.07), ("Solar", "Industrial", 0.02),
            ("Nuclear", "Electricity Generation", 8.1),
            ("Hydro", "Electricity Generation", 0.81), ("Hydro", "Industrial", 0.01),
            ("Wind", "Electricity Generation", 1.5),
            ("Geothermal", "Electricity Generation", 0.06), ("Geothermal", "Residential", 0.04),
            ("Geothermal", "Commercial", 0.02),
            ("Natural Gas", "Electricity Generation", 13.3), ("Natural Gas", "Residential", 4.64),
            ("Natural Gas", "Commercial", 3.43), ("Natural Gas", "Industrial", 10.9),
            ("Natural Gas", "Transportation", 1.32),
            ("Coal", "Electricity Generation", 7.24), ("Coal", "Commercial", 0.01),
            ("Coal", "Industrial", 0.91),
            ("Biomass", "Electricity Generation", 0.33), ("Biomass", "Residential", 0.45),
            ("Biomass", "Commercial", 0.19), ("Biomass", "Industrial", 2.23),
            ("Biomass", "Transportation", 1.79),
            ("Petroleum", "Electricity Generation", 0.17), ("Petroleum", "Residential", 0.97),
            ("Petroleum", "Commercial", 0.94), ("Petroleum", "Industrial", 8.53),
            ("Petroleum", "Transportation", 24.8),
            ("Net Electricity Imports", "Electricity Generation", 0.07),
            ("Electricity Generation", "Residential", 4.96),
            ("Electricity Generation", "Commercial", 4.69),
            ("Electricity Generation", "Industrial", 3.5),
            ("Electricity Generation", "Transportation", 0.02),
            ("Electricity Generation", "Rejected Energy", 18.9),
            ("Residential", "Energy Services", 7.34), ("Residential", "Rejected Energy", 3.95),
            ("Commercial", "Energy Services", 6.07), ("Commercial", "Rejected Energy", 3.27),
            ("Industrial", "Energy Services", 13.1), ("Industrial", "Rejected Energy", 13.3),
            ("Transportation", "Energy Services", 5.87), ("Transportation", "Rejected Energy", 21.7),
        ]
        return pd.DataFrame(flows, columns=["source", "target", "quads"])
    if mode == "giss":
        text = raw.decode()
        start = next(i for i, line in enumerate(text.splitlines()) if line.startswith("Year,"))
        df = pd.read_csv(io.StringIO("\n".join(text.splitlines()[start:])))
        df.columns = ["year", "anomaly_c", "lowess_c"]
        uncertainty = pd.read_csv(io.BytesIO(fetch(s["uncertainty_data"])))
        uncertainty = uncertainty.rename(columns={"ci95": "uncertainty_95_c"})[
            ["year", "uncertainty_95_c"]
        ]
        df = df.merge(uncertainty, on="year", how="left")
        df["uncertainty_low_c"] = df["anomaly_c"] - df["uncertainty_95_c"]
        df["uncertainty_high_c"] = df["anomaly_c"] + df["uncertainty_95_c"]
        return df.dropna(subset=["year", "anomaly_c", "lowess_c"])
    if mode == "owid_health":
        df = pd.read_csv(io.BytesIO(raw))
        df.columns = ["country", "code", "year", "life_expectancy_years",
                      "health_exp_per_capita_usd", "region"]
        df = df[df["code"].notna() & ~df["code"].str.startswith("OWID")
                & df["life_expectancy_years"].notna()
                & df["health_exp_per_capita_usd"].notna()]
        year = max(y for y, g in df.groupby("year") if len(g) >= 50)
        out = df[df["year"] == year].copy()
        out["region"] = out["region"].fillna("Unclassified")
        return out.reset_index(drop=True)
    if mode == "rba_g1":
        rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
        series_row = next(r for r in rows if r and r[0] == "Series ID")
        idx = {name: series_row.index(sid) for name, sid in
               [("cpi_excl_volatile_pct", "GCPIXVIYP"),
                ("weighted_median_pct", "GCPIOCPMWMYP"),
                ("trimmed_mean_pct", "GCPIOCPMTMYP")]}
        out = []
        for r in rows:
            if not (r and re.match(r"\d{2}/\d{2}/\d{4}$", r[0])):
                continue
            try:
                vals = [float(r[i]) for i in idx.values()]
            except (ValueError, IndexError):
                continue
            day, month, year = r[0].split("/")
            out.append([f"{year}-{month}-{day}"] + vals)
        return pd.DataFrame(out, columns=["quarter"] + list(idx))
    if mode == "lynxhare":
        table = pd.read_html(io.BytesIO(raw))[1]
        left = table.iloc[1:, :3].copy()
        right = table.iloc[1:, 3:6].copy()
        left.columns = right.columns = ["year", "hares_thousands", "lynx_thousands"]
        df = pd.concat([left, right], ignore_index=True).apply(pd.to_numeric, errors="coerce")
        df = df.dropna().sort_values("year").reset_index(drop=True)
        df["year"] = df["year"].astype(int)
        return df
    if mode == "eia_mix":
        values = [
            ("Natural gas", "", "major", 40.8),
            ("Coal", "", "major", 16.6),
            ("Nuclear", "", "major", 17.7),
            ("Renewables", "", "major", 24.1),
            ("Petroleum and other", "", "major", 0.7),
            ("Wind", "Renewables", "renewable subtype", 10.5),
            ("Hydropower", "Renewables", "renewable subtype", 5.6),
            ("Solar", "Renewables", "renewable subtype", 6.7),
            ("Biomass", "Renewables", "renewable subtype", 1.0),
            ("Geothermal", "Renewables", "renewable subtype", 0.4),
        ]
        df = pd.DataFrame(values, columns=["energy_source", "parent_source", "level", "share_pct"])
        df["approx_billion_kwh"] = (df["share_pct"] * 44.3).round(1)
        df["display_order"] = range(1, len(df) + 1)
        return df
    if mode == "quakes":
        df = pd.read_csv(io.BytesIO(raw))
        out = pd.DataFrame({
            "date": pd.to_datetime(df["time"]).dt.date.astype(str),
            "latitude": df["latitude"], "longitude": df["longitude"],
            "depth_km": df["depth"], "magnitude": df["mag"], "place": df["place"],
        })
        return out.dropna().reset_index(drop=True)
    if mode == "owid_world":
        df = pd.read_csv(io.BytesIO(raw))
        return df[df["Code"].eq("OWID_WRL")].dropna(axis=1, how="all").tail(240)
    if mode == "kleiber":
        rows = xlsx_sheet(raw, "B-MetabolicRateDryMass")
        vals = [[r[0], r[1]] for r in rows[1:84] if len(r) > 1 and isinstance(r[0], (int, float)) and isinstance(r[1], (int, float))]
        return pd.DataFrame(vals, columns=["metabolic_rate_uW", "dry_mass_mg"])
    if mode == "hubble":
        objects = ["S. Mag.", "L. Mag.", "NGC 6822", "NGC 598", "NGC 221", "NGC 224",
                   "NGC 5457", "NGC 4736", "NGC 5194", "NGC 4449", "NGC 4214", "NGC 3031",
                   "NGC 3627", "NGC 4826", "NGC 5236", "NGC 1068", "NGC 5055", "NGC 7331",
                   "NGC 4258", "NGC 4151", "NGC 4382", "NGC 4472", "NGC 4486", "NGC 4649"]
        d = [0.032,0.034,0.214,0.263,0.275,0.275,0.45,0.5,0.5,0.63,0.8,0.9,0.9,0.9,0.9,1.0,1.1,1.1,1.4,1.7,2.0,2.0,2.0,2.0]
        v = [170,290,-130,-70,-185,-220,200,290,270,200,300,-30,650,150,500,920,450,500,500,960,500,850,800,1090]
        df = pd.DataFrame({"record_type": "individual", "object": objects,
                           "distance_mpc": d, "velocity_km_s": v})
        mean_row = pd.DataFrame([{"record_type": "reference mean", "object": "Mean of 22 nebulae",
                                  "distance_mpc": 1.4, "velocity_km_s": 745}])
        df = pd.concat([df, mean_row], ignore_index=True)
        df["individual_fit_slope"] = 465
        df["group_fit_slope"] = 513
        return df
    if mode == "happiness":
        source = pd.read_excel(io.BytesIO(raw))
        out = source[["Country name", "Ladder score", "lowerwhisker", "upperwhisker"]].copy()
        out.columns = ["country", "life_evaluation", "score_ci_low", "score_ci_high"]
        out.insert(0, "rank", range(1, len(out) + 1))
        return out.dropna().reset_index(drop=True)
    if mode == "lorenz":
        return pd.DataFrame({"population_share":[0,.2,.4,.6,.8,1], "income_share_1980":[0,.043,.146,.315,.563,1], "income_share_2020":[0,.030,.112,.258,.480,1]})
    if mode == "pdb":
        residues = []
        atoms = defaultdict(dict)
        names = {}
        for line in raw.decode().splitlines():
            if line.startswith("ATOM") and line[12:16].strip() in {"N","CA","C"} and line[16] in {" ","A"}:
                key=(line[21].strip() or "_", int(line[22:26])); names[key]=line[17:20].strip()
                atoms[key][line[12:16].strip()] = np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])])
        keys=sorted(atoms)
        for i in range(1,len(keys)-1):
            prev, key, nxt=keys[i-1],keys[i],keys[i+1]
            if prev[0]!=key[0] or nxt[0]!=key[0] or not all(set(atoms[k])=={"N","CA","C"} for k in (prev,key,nxt)): continue
            phi=dihedral(atoms[prev]["C"],atoms[key]["N"],atoms[key]["CA"],atoms[key]["C"])
            psi=dihedral(atoms[key]["N"],atoms[key]["CA"],atoms[key]["C"],atoms[nxt]["N"])
            omega=dihedral(atoms[prev]["CA"],atoms[prev]["C"],atoms[key]["N"],atoms[key]["CA"])
            if names[key] == "GLY": rama_class = "Glycine"
            elif names[key] == "PRO": rama_class = "Cis proline" if abs(omega) < 30 else "Trans proline"
            elif names[nxt] == "PRO": rama_class = "Pre-proline"
            elif names[key] in {"ILE", "VAL"}: rama_class = "Isoleucine and valine"
            else: rama_class = "General case"
            residues.append((key[0],key[1],names[key],phi,psi,omega,rama_class))
        return pd.DataFrame(residues,columns=["chain","residue","amino_acid","phi_deg","psi_deg","omega_deg","rama_class"])
    if mode == "abundance":
        table = pd.read_html(io.BytesIO(raw))[0]
        table = table.rename(columns={"Atom": "element", "Atomic No.": "atomic_number",
                                      "Log(abund)": "log_abundance_per_1e6_si"})
        table = table[["atomic_number", "element", "log_abundance_per_1e6_si"]]
        table = table[pd.to_numeric(table["atomic_number"], errors="coerce").between(1, 92)]
        table["log_abundance_per_1e6_si"] = pd.to_numeric(table["log_abundance_per_1e6_si"], errors="coerce")
        table = table.dropna().copy()
        hydrogen_log = float(table.loc[table["atomic_number"].eq(1), "log_abundance_per_1e6_si"].iloc[0])
        table["log10_atoms_per_1e12_H"] = table["log_abundance_per_1e6_si"] - hydrogen_log + 12
        table["atoms_per_1e12_H"] = 10 ** table["log10_atoms_per_1e12_H"]
        return table[["atomic_number", "element", "atoms_per_1e12_H", "log10_atoms_per_1e12_H"]].reset_index(drop=True)
    if mode == "carbon":
        rows=xlsx_sheet(raw,"Global Carbon Budget")
        header_i=next(i for i,r in enumerate(rows) if any(str(x).strip()=="Year" for x in r))
        header=[str(x or "").strip() for x in rows[header_i]]
        def idx(words): return next(i for i,h in enumerate(header) if all(w in h.lower() for w in words))
        iy=idx(["year"]); cols=[idx(["fossil"]),idx(["land-use"]),idx(["atmospheric"]),idx(["ocean"]),idx(["land sink"])]
        out=[]
        for r in rows[header_i+1:]:
            if len(r)<=max(cols+[iy]): continue
            try: year=int(float(r[iy]))
            except (TypeError,ValueError): continue
            if 2015<=year<=2024: out.append([year]+[r[i] for i in cols])
        return pd.DataFrame(out,columns=["year","fossil_emissions","land_use_change","atmospheric_growth","ocean_sink","land_sink"])
    if mode == "gerrymander":
        magenta={(r,c) for r in (2,3,6,7) for c in range(2,8)} | {(r,c) for r in (4,5) for c in (2,3,6,7)}
        blocked=set()
        def block(a,b): blocked.add(tuple(sorted((a,b))))
        for r in [1]: block((r,4),(r,5))
        for c in [3,4]: block((1,c),(2,c))
        for r in [2,3]: block((r,2),(r,3))
        for c in range(3,9): block((3,c),(4,c))
        block((3,1),(4,1))
        for r in range(4,8): block((r,1),(r,2)); block((r,3),(r,4))
        for c in [2,3,5,6]: block((7,c),(8,c))
        for r in [4,5]: block((r,5),(r,6))
        block((5,5),(6,5))
        for r in [6,7]: block((r,4),(r,5))
        block((8,6),(8,7))
        comp={}; cid=0
        for start in [(r,c) for r in range(1,9) for c in range(1,9)]:
            if start in comp: continue
            cid+=1; comp[start]=cid; q=deque([start])
            while q:
                r,c=q.popleft()
                for nb in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                    if not (1<=nb[0]<=8 and 1<=nb[1]<=8) or tuple(sorted(((r,c),nb))) in blocked or nb in comp: continue
                    comp[nb]=cid; q.append(nb)
        out=[]
        for r in range(1,9):
            for c in range(1,9): out.append((r,c,"magenta" if (r,c) in magenta else "green",1+(r>4)*2+(c>4),comp[(r,c)]))
        return pd.DataFrame(out,columns=["row","column","party","compact_district","gerrymandered_district"])
    if mode == "routes":
        airports=fetch("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat")
        amap={}
        for r in csv.reader(io.StringIO(airports.decode(errors="replace"))):
            if len(r)>7:
                try: amap[r[0]]=(r[4],r[2],float(r[6]),float(r[7]))
                except ValueError: pass
        counts=Counter()
        for r in csv.reader(io.StringIO(raw.decode(errors="replace"))):
            if len(r)>5 and r[3] in amap and r[5] in amap and r[3]!=r[5]: counts[tuple(sorted((r[3],r[5])))] += 1
        out=[]
        for (a,b),n in counts.most_common(250):
            endpoint_a, endpoint_b = sorted((amap[a], amap[b]), key=lambda airport: airport[0])
            out.append((*endpoint_a, *endpoint_b, n))
        return pd.DataFrame(out,columns=["airport_a_iata","airport_a_city","airport_a_lat","airport_a_lon","airport_b_iata","airport_b_city","airport_b_lat","airport_b_lon","airline_record_count"])
    raise ValueError(mode)


def main_deck_hashes():
    decks=[ROOT/"classes/01-seeing-data/beamer/seeing-data.pdf",ROOT/"classes/02-visual-forms/Choosing-Visual-Forms.pdf"]
    hashes=set()
    with tempfile.TemporaryDirectory(prefix="a1-decks-") as td:
        for i,pdf in enumerate(decks):
            if not pdf.exists(): continue
            subprocess.run(["pdfimages","-all",str(pdf),str(Path(td)/f"d{i}")],check=True,capture_output=True)
        for p in Path(td).iterdir():
            try: hashes.add(sha(p.read_bytes()))
            except OSError: pass
    return hashes


def build(selected_ids: set[str] | None = None):
    deck_hashes=main_deck_hashes(); results=[]
    targets = [s for s in SPECS if selected_ids is None or s["id"] in selected_ids]
    unknown = (selected_ids or set()) - {s["id"] for s in SPECS}
    if unknown:
        raise ValueError(f"unknown pool IDs: {', '.join(sorted(unknown))}")
    for s in targets:
        d=POOL/s["id"]; d.mkdir(parents=True,exist_ok=True)
        for p in d.iterdir():
            if p.is_file(): p.unlink()
        chart,ext=chart_bytes(s)
        try: Image.open(io.BytesIO(chart)).verify()
        except Exception as e: raise RuntimeError(f"{s['id']} invalid chart image: {e}")
        if ext!=".png":
            # students submit original_chart_n.png; normalise every original to real PNG
            buf=io.BytesIO(); Image.open(io.BytesIO(chart)).convert("RGB").save(buf,"PNG")
            chart,ext=buf.getvalue(),".png"
        raw=fetch(s["data"]) if s["mode"] not in {"hubble","lorenz","gerrymander"} else fetch(s["data"])
        df=extract_data(s,raw)
        if not (6<=len(df)<=100000 and 2<=df.shape[1]<=12): raise RuntimeError(f"{s['id']} unsuitable data shape {df.shape}")
        (d/f"original_chart{ext}").write_bytes(chart); df.to_csv(d/"source_data.csv",index=False)
        metadata={"id":s["id"],"domain":s["domain"],"category":s["category"],"title":s["title"],"publisher":s["publisher"],"chart_page":s["page"],"chart_asset":s["chart"],"source_data":s["data"],"publication":s["publication"],"downloaded":date.today().isoformat(),"chart_sha256":sha(chart),"source_sha256":sha(raw)}
        if s.get("uncertainty_data"):
            supplementary = fetch(s["uncertainty_data"])
            metadata["supplementary_source_data"] = s["uncertainty_data"]
            metadata["supplementary_source_sha256"] = sha(supplementary)
        (d/"source_metadata.json").write_text(json.dumps(metadata,indent=2)+"\n")
        fields="\n".join(f"| `{c}` | {s['fields'].get(c,'Source field used by the published chart.')} |" for c in df.columns)
        (d/"data_dictionary.md").write_text(f"# Data dictionary: {s['id']}\n\n| Field | Meaning |\n|---|---|\n{fields}\n\nThe supplied CSV is a documented extract of the linked source data; no values were digitised from chart pixels.\n")
        supplementary_line = f"- Supplementary source data: {s['uncertainty_data']}\n" if s.get("uncertainty_data") else ""
        provenance=f"# {s['id']}: {s['title']}\n\n- Domain (copy exactly into `META_n`): {s['domain']}\n- FT Visual Vocabulary category: {s['category']}\n- Publisher: {s['publisher']}\n- Publication date (copy exactly into `META_n`): {s['publication']}\n- Access date: {date.today().isoformat()}\n- Published chart and context: {s['page']}\n- Chart asset: {s['chart']}\n- Source data: {s['data']}\n{supplementary_line}- Data supplied: {len(df)} rows × {df.shape[1]} columns\n- Licence/use note: {s['licence']}\n- Chart–data match: {s.get('matching_note', 'Publisher/source data were filtered or transformed into a beginner-sized CSV; no chart-image digitisation was used.')}\n"
        (d/"provenance.md").write_text(provenance); (d/"entry.md").write_text(provenance)
        check={"id":s["id"],"domain":s["domain"],"category":s["category"],"publisher":s["publisher"],"rows":len(df),"columns":df.shape[1],"chart_sha256":sha(chart),"student_csv_sha256":sha((d/"source_data.csv").read_bytes()),"source_sha256":sha(raw),"exact_match_in_published_week_1_or_2_decks":sha(chart) in deck_hashes,"chart_card_exception_allowed":s["id"] in {"POOL-03","POOL-05","POOL-06","POOL-12"}}
        if check["exact_match_in_published_week_1_or_2_decks"]: raise RuntimeError(f"{s['id']} duplicates a published teaching deck")
        (d/"checks.json").write_text(json.dumps(check,indent=2)+"\n"); results.append(check)
    if selected_ids is not None:
        print(f"built {len(targets)} selected entries; manifest and ZIP left unchanged")
        return
    package_existing()
    counts=Counter(s["category"] for s in SPECS)
    print(f"built {len(SPECS)} entries; {dict(counts)}")


def package_existing():
    """Package only the four files students actually use."""
    student_files = ("original_chart.png", "source_data.csv",
                     "data_dictionary.md", "provenance.md")
    with zipfile.ZipFile(A1/"A1_artefact_pool.zip","w",zipfile.ZIP_DEFLATED) as z:
        for s in SPECS:
            entry = POOL / s["id"]
            missing = [name for name in student_files if not (entry / name).is_file()]
            if missing:
                raise RuntimeError(f"{s['id']} missing student files: {', '.join(missing)}")
            for name in student_files:
                p = entry / name
                z.write(p, p.relative_to(A1))
    print(f"packaged {len(SPECS)} entries; four student files per entry")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="+", metavar="POOL-ID",
                        help="Rebuild only these entries; leave the shared manifest and ZIP unchanged.")
    parser.add_argument("--package-only", action="store_true",
                        help="Rebuild the manifest and ZIP from existing entry directories.")
    args = parser.parse_args()
    if args.package_only and args.only:
        parser.error("--package-only and --only cannot be used together")
    if args.package_only:
        package_existing()
    else:
        build(set(args.only) if args.only else None)

from __future__ import annotations

from pathlib import Path
import math
import random
import pandas as pd

random.seed(42)

regions = {
    "Inner Sydney": (-33.8688, 151.2093),
    "Western Sydney": (-33.8150, 150.9980),
    "Northern Beaches": (-33.7140, 151.2970),
    "Central Coast": (-33.4250, 151.3420),
    "Newcastle": (-32.9283, 151.7817),
    "Illawarra": (-34.4278, 150.8931),
}

modes = ["Train", "Bus", "Ferry", "Light rail"]
dates = pd.date_range("2019-01-01", "2025-12-01", freq="MS")

base_by_mode = {"Train": 1000000, "Bus": 700000, "Ferry": 90000, "Light rail": 120000}
region_factor = {
    "Inner Sydney": 1.3,
    "Western Sydney": 1.1,
    "Northern Beaches": 0.55,
    "Central Coast": 0.45,
    "Newcastle": 0.5,
    "Illawarra": 0.42,
}

rows = []
for region, (lat, lon) in regions.items():
    for mode in modes:
        base = base_by_mode[mode] * region_factor[region]
        for date in dates:
            # seasonal pattern
            month = date.month
            season = 1 + 0.08 * math.sin((month - 1) / 12 * 2 * math.pi)
            # COVID-like drop and recovery
            if date.year == 2020 and date.month >= 3:
                recovery = 0.35
            elif date.year == 2021:
                recovery = 0.55
            elif date.year == 2022:
                recovery = 0.72
            elif date.year == 2023:
                recovery = 0.84
            elif date.year == 2024:
                recovery = 0.90
            elif date.year == 2025:
                recovery = 0.96
            else:
                recovery = 1.0
            # synthetic methodology-like discontinuity from July 2024
            methodology_note = "stable"
            method_factor = 1.0
            if date >= pd.Timestamp("2024-07-01") and mode in {"Bus", "Light rail"}:
                method_factor = 1.08
                methodology_note = "synthetic allocation change from July 2024"
            noise = random.uniform(0.94, 1.06)
            trips = int(base * season * recovery * method_factor * noise)
            rows.append({
                "date": date.strftime("%Y-%m-%d"),
                "region": region,
                "mode": mode,
                "trips": trips,
                "lat": lat,
                "lon": lon,
                "methodology_note": methodology_note,
            })

df = pd.DataFrame(rows)
baseline = (
    df[pd.to_datetime(df["date"]).dt.year == 2019]
    .groupby(["region", "mode"], as_index=False)["trips"]
    .mean()
    .rename(columns={"trips": "baseline_2019"})
)
df = df.merge(baseline, on=["region", "mode"], how="left")
df["index_2019"] = (df["trips"] / df["baseline_2019"] * 100).round(1)

out = Path(__file__).resolve().parents[1] / "starter_app" / "data" / "sample_public_transport.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(f"Wrote {len(df):,} rows to {out}")

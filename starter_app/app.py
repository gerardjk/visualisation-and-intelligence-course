from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Public Transport Recovery Explorer",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "sample_public_transport.csv"
REQUIRED_COLUMNS = {
    "date",
    "region",
    "mode",
    "trips",
    "index_2019",
    "lat",
    "lon",
    "methodology_note",
}


@st.cache_data(ttl=3600)
def load_and_prepare_data(path: Path) -> pd.DataFrame:
    """Load and prepare data for the app.

    Streamlit reruns the script after widget interactions. Caching data loading and
    stable transformations makes the app feel responsive and avoids repeated parsing.
    """
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"The dataset is missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["date"])
    after = len(df)
    if after == 0:
        raise ValueError("No valid dates remained after parsing the date column.")
    df.attrs["dropped_invalid_dates"] = before - after
    return df


try:
    with st.spinner("Loading and preparing data..."):
        df = load_and_prepare_data(DATA_PATH)
except Exception as exc:  # user-facing error state
    st.error(f"The app could not load the dataset: {exc}")
    st.stop()

st.title("Public Transport Recovery Explorer")
st.markdown(
    """
    This teaching app shows how an interactive visual data product can combine
    user stories, the FT Visual Vocabulary, data loading, caching, empty-state
    handling, and a clear **Data and AI Disclosure**.

    **Important:** the dataset is synthetic. Replace it with an approved public
    dataset for assessment.
    """
)

with st.expander("User stories supported by this app", expanded=False):
    st.markdown(
        """
        1. **As a transport analyst**, I want to compare patronage recovery by mode
           since 2019, so that I can identify which modes remain below baseline.
        2. **As a policy adviser**, I want to identify which modes are weakest in
           the latest month, so that I can prioritise follow-up analysis.
        3. **As a reviewer**, I want to see the data source and limitations, so that
           I can judge whether the app is appropriate for my use.
        """
    )

st.sidebar.header("Controls")
regions = sorted(df["region"].dropna().unique())
modes = sorted(df["mode"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Regions",
    options=regions,
    default=regions[:3],
)

selected_modes = st.sidebar.multiselect(
    "Modes",
    options=modes,
    default=modes,
)

metric = st.sidebar.selectbox(
    "Metric",
    options=["index_2019", "trips"],
    format_func=lambda value: "Index to 2019 baseline" if value == "index_2019" else "Trips",
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()
selected_date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

start_date = pd.Timestamp(selected_date_range[0])
end_date = pd.Timestamp(selected_date_range[1])

filtered = df[
    df["region"].isin(selected_regions)
    & df["mode"].isin(selected_modes)
    & (df["date"] >= start_date)
    & (df["date"] <= end_date)
].copy()

if filtered.empty:
    st.warning("No data is available for the selected filters. Change the region, mode, or date selection.")
    st.stop()

methodology_rows = filtered[filtered["methodology_note"] != "stable"]
if not methodology_rows.empty:
    st.info(
        "This synthetic dataset includes a methodology-like discontinuity from July 2024 "
        "for selected modes. A real project should mark and explain provider methodology changes."
    )

summary_left, summary_middle, summary_right = st.columns(3)
with summary_left:
    st.metric("Rows after filtering", f"{len(filtered):,}")
with summary_middle:
    st.metric("Regions selected", len(selected_regions))
with summary_right:
    st.metric("Modes selected", len(selected_modes))

tab_trends, tab_compare, tab_spatial, tab_data = st.tabs(
    ["Trends", "Compare", "Spatial overview", "Data and disclosure"]
)

with tab_trends:
    st.subheader("Change over time")
    st.caption("FT Visual Vocabulary category: Change over time")

    line_chart = (
        alt.Chart(filtered)
        .mark_line(point=False)
        .encode(
            x=alt.X("date:T", title="Month"),
            y=alt.Y(f"{metric}:Q", title="Index to 2019" if metric == "index_2019" else "Trips"),
            color=alt.Color("mode:N", title="Mode"),
            strokeDash=alt.StrokeDash("region:N", title="Region"),
            tooltip=["date:T", "region:N", "mode:N", "trips:Q", "index_2019:Q", "methodology_note:N"],
        )
        .properties(height=380)
    )
    st.altair_chart(line_chart, use_container_width=True)

    st.markdown(
        """
        **Interpretation prompt:** This chart supports a change-over-time task.
        Ask whether the trend is stable, whether the comparison period is justified,
        and whether methodology changes affect the story.
        """
    )

with tab_compare:
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Latest ranking")
        st.caption("FT Visual Vocabulary category: Ranking")
        latest_date = filtered["date"].max()
        latest = filtered[filtered["date"] == latest_date].sort_values(metric, ascending=False)

        bar_chart = (
            alt.Chart(latest)
            .mark_bar()
            .encode(
                x=alt.X(f"{metric}:Q", title="Index to 2019" if metric == "index_2019" else "Trips"),
                y=alt.Y("mode:N", sort="-x", title="Mode"),
                color=alt.Color("region:N", title="Region"),
                tooltip=["region:N", "mode:N", "trips:Q", "index_2019:Q"],
            )
            .properties(height=360)
        )
        st.altair_chart(bar_chart, use_container_width=True)

    with right:
        st.subheader("Distribution of selected values")
        st.caption("FT Visual Vocabulary category: Distribution")
        dist_chart = (
            alt.Chart(filtered)
            .mark_bar()
            .encode(
                x=alt.X(f"{metric}:Q", bin=alt.Bin(maxbins=20), title="Index to 2019" if metric == "index_2019" else "Trips"),
                y=alt.Y("count():Q", title="Number of months"),
                color=alt.Color("mode:N", title="Mode"),
                tooltip=["mode:N", "count():Q"],
            )
            .properties(height=360)
        )
        st.altair_chart(dist_chart, use_container_width=True)

with tab_spatial:
    st.subheader("Spatial overview")
    st.caption("FT Visual Vocabulary category: Spatial + magnitude")
    latest_date = filtered["date"].max()
    latest_spatial = (
        filtered[filtered["date"] == latest_date]
        .groupby(["region", "lat", "lon"], as_index=False)[metric]
        .mean()
    )

    spatial_chart = (
        alt.Chart(latest_spatial)
        .mark_circle(opacity=0.75)
        .encode(
            x=alt.X("lon:Q", title="Longitude", scale=alt.Scale(zero=False)),
            y=alt.Y("lat:Q", title="Latitude", scale=alt.Scale(zero=False)),
            size=alt.Size(f"{metric}:Q", title="Mean selected value"),
            tooltip=["region:N", f"{metric}:Q"],
        )
        .properties(height=380)
    )
    st.altair_chart(spatial_chart, use_container_width=True)
    st.caption(
        "This is a lightweight spatial sketch rather than a full geographic map. "
        "A real spatial app should consider projections, boundaries, normalisation, and geographic inference risks."
    )

with tab_data:
    st.subheader("Data preview")
    st.dataframe(filtered, use_container_width=True)

    st.subheader("User story acceptance test")
    acceptance = pd.DataFrame(
        [
            {
                "User story": "Compare recovery by mode since 2019",
                "Feature": "Mode and region filters + indexed line chart",
                "Visual Vocabulary": "Change over time",
                "Potential failure": "Methodology change makes comparison unstable",
            },
            {
                "User story": "Identify weakest latest-month recovery",
                "Feature": "Latest ranking bar chart",
                "Visual Vocabulary": "Ranking",
                "Potential failure": "Latest month may be atypical",
            },
            {
                "User story": "Judge whether the app is appropriate to use",
                "Feature": "Data and AI Disclosure",
                "Visual Vocabulary": "Documentation/trust",
                "Potential failure": "Disclosure too vague",
            },
        ]
    )
    st.dataframe(acceptance, use_container_width=True)

    with st.expander("About the data and AI use", expanded=False):
        st.markdown(
            """
            **Data source:**  
            Synthetic teaching dataset generated for this course package. Replace with an approved public dataset.

            **Time period:**  
            Monthly data from 2019 to 2025.

            **Unit of analysis:**  
            One row represents one month, one region, and one transport mode.

            **What the data includes:**  
            Date, region, mode, trips, latitude, longitude, a methodology note, and an index relative to a 2019 baseline.

            **What the data excludes:**  
            Real service disruptions, true provider methodology notes, demographic variables, and real operational data.

            **Cleaning and transformations:**  
            Dates are parsed, rows with invalid dates are dropped, filters are applied, latest-month rankings are calculated, and values are indexed to a 2019 baseline.

            **Primary visual task:**  
            Show change over time and compare recovery by mode.

            **FT Visual Vocabulary category:**  
            Change over time; ranking; distribution; spatial.

            **Known limitations:**  
            The data is synthetic. It should not be used for real-world policy conclusions. The spatial view is approximate and does not use true geographic boundaries.

            **AI assistance used:**  
            Replace this with project-specific intelligent-tool use. The starter code includes an example provenance file.

            **Human verification performed:**  
            Replace this with project-specific verification. At minimum, verify row counts, data source, chart mappings, and generated code.

            **Appropriate use:**  
            Learning app structure, interaction, caching, Visual Vocabulary classification, and disclosure.

            **Inappropriate use:**  
            Drawing real conclusions about public transport recovery.
            """
        )

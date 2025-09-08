import streamlit as st
import plotly.express as px
import geopandas as gpd
import pandas as pd

# -------------------------------
# Load data
# -------------------------------
cities = pd.read_csv("languageCities.csv", encoding="utf-8")
cities_geo = gpd.GeoDataFrame(
    cities, geometry=gpd.points_from_xy(cities["latitude"], cities["longitude"])
)

display_data = pd.read_csv("display_data.csv")

# Group by treatment, create ranges
treatment_range = (
    display_data.groupby("treatment")["number"].agg(["min", "max"]).reset_index()
)

treatment_dict = {}
for _, row in treatment_range.iterrows():
    key = row["treatment"]
    if row["min"] == row["max"]:
        string = str(int(row["min"])).zfill(3) + " " + key
    else:
        string = (
            str(int(row["min"])).zfill(3)
            + "-"
            + str(int(row["max"])).zfill(3)
            + " "
            + key
        )
    treatment_dict[key] = string

display_data["treatment"] = display_data["treatment"].map(treatment_dict)

# Normalize & color
display_data["sonority_scaled"] = (
    display_data["sonority_avg"] - display_data["sonority_avg"].min()
) / (display_data["sonority_avg"].max() - display_data["sonority_avg"].min())
display_data["place_scaled"] = (
    display_data["place_avg"] - display_data["place_avg"].min()
) / (display_data["place_avg"].max() - display_data["place_avg"].min())


def blend_colors(r, g, b):
    return f"rgb({int(r * 255)}, {int(g)}, {int(b * 255)})"


display_data["color"] = [
    blend_colors(r, g, b)
    for r, g, b in zip(
        display_data["sonority_scaled"],
        display_data["voice_avg"],
        display_data["place_scaled"],
    )
]

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Digitally Mapping Romance Phonetic Outcomes")
st.write("A visual presentation of the modern pronunciation of Latin consonants across the Romance languages, inspired by the L'Atlas Linguistique Roman (ALiR) 1987")

# Dropdowns
treatment = st.selectbox(
    "Treatment",
    options=display_data.sort_values(by="number")["treatment"].unique().tolist(),
    index=0,
)

environ_list = display_data[display_data["treatment"] == treatment][
    "environment"
].unique().tolist()
environment = st.selectbox("Environment", options=environ_list)

versions_list = (
    display_data[
        (display_data["treatment"] == treatment)
        & (display_data["environment"] == environment)
    ]["version"]
    .sort_values()
    .unique()
    .tolist()
)
version = st.selectbox("Version", options=versions_list, index=0)

# -------------------------------
# Build filtered dataset
# -------------------------------
latin_to_rom_sub = display_data[
    (display_data["treatment"] == treatment) & (display_data["environment"] == environment)
]

grouped = latin_to_rom_sub.groupby("language")
version_tables = []
for language, df in grouped:
    if version in df["version"].unique().tolist():
        select_version = version
    else:
        select_version = "a"
    version_tables.append(df[df["version"] == select_version])

if version_tables:
    version_sub = pd.concat(version_tables, axis=0)
else:
    version_sub = pd.DataFrame(columns=display_data.columns)

city_context = pd.merge(
    cities_geo, version_sub, left_on="language_code", right_on="language"
).dropna(subset=["display"])

# -------------------------------
# Map
# -------------------------------
fig = px.scatter_geo(
    city_context,
    lat=city_context.geometry.x,
    lon=city_context.geometry.y,
    text="display",
    hover_name="Language Variety",
    hover_data=["sonority_avg", "place_avg"],
    color=city_context["color"],
    color_discrete_map="identity",
)

fig.update_layout(
    geo=dict(projection_scale=8, center=dict(lat=45.76, lon=4.84)),
    margin=dict(t=10, l=10, b=10, r=10),
)
fig.update_traces(
    textfont=dict(family="Arial", size=16, color="black"),
    marker=dict(size=30, opacity=0.4),
)
fig.update_geos(showcountries=True)

st.plotly_chart(fig, width='stretch')

# -------------------------------
# Side tables
# -------------------------------
version_sub = pd.merge(
    cities_geo, version_sub, left_on="language_code", right_on="language"
).sort_values("longitude")
version_sub = version_sub[["language", "display"]]

mid = len(version_sub) // 2 if len(version_sub) > 16 else len(version_sub)
col1_data = version_sub.iloc[:mid]
col2_data = version_sub.iloc[mid:] if len(version_sub) > 16 else pd.DataFrame()

col1, col2 = st.columns(2)
with col1:
    st.dataframe(col1_data, use_container_width=True, hide_index=True)
with col2:
    if not col2_data.empty:
        st.dataframe(col2_data, use_container_width=True, hide_index=True)


st.write('Data compiled digitally by Tim Bertucci (tbertucci@luc.edu), app created by Leigha DeRango (lderango@luc.edu), in collaboration with Loyola University Chicago Center for Data Science and Consulting (data@luc.edu)')

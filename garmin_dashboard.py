# Garmin online dashboard pro sledování sportovních aktivit
# Autor: Ondřej Klubal

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from garminconnect import Garmin
import folium
from streamlit_folium import st_folium

SPORT_GROUPS = {
    "Běh": ["running", "treadmill_running"],
    "Cyklistika": ["cycling", "indoor_cycling"],
    "Plavání": ["swimming", "pool_swimming", "open_water_swimming", "lap_swimming"],
    "Silový trénink": ["strength_training", "weight_training"],
    "Běžky": ["cross_country_skiing", "nordic_skiing"],
    "Turistika/Chůze": ["hiking", "walking", "trail_walking", "casual_walking"]
}

def map_sport_group(type_key):
    for group, keys in SPORT_GROUPS.items():
        if type_key in keys:
            return group
    return "Jiné"

def format_tempo(speed_m_s):
    if speed_m_s <= 0:
        return "-"
    pace_min_per_km = 1000 / speed_m_s / 60
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}:{seconds:02d} min/km"

def format_duration(seconds):
    return str(timedelta(seconds=int(seconds)))

def plot_activity_map(activity_detail):
    if "geoPolylineDTO" in activity_detail and activity_detail["geoPolylineDTO"]:
        polyline_data = activity_detail["geoPolylineDTO"].get("polyline", [])
        if isinstance(polyline_data, list) and isinstance(polyline_data[0], dict):
            latlngs = [(point["lat"], point["lon"]) for point in polyline_data if point.get("lat") and point.get("lon")]
        else:
            latlngs = polyline_data  # fallback
        if not latlngs:
            return None
        m = folium.Map(location=latlngs[0], zoom_start=13)
        folium.PolyLine(latlngs, color="blue", weight=5).add_to(m)
        return m
    else:
        return None

mail = "ondra.klubal@gmail.com"
pwd = "&zVd#Ec%u?V0"

@st.cache_resource(show_spinner="🔐 Přihlašuji se ke Garminu...")
def connect_to_garmin():
    try:
        client = Garmin(email=mail, password=pwd)
        client.login()
        return client
    except Exception as e:
        st.error(f"Chyba při přihlašování: {e}")
        st.stop()

client = connect_to_garmin()

@st.cache_data(show_spinner="📥 Načítám aktivity z Garminu...")
def load_all_activities():
    activities = client.get_activities(0, 1000)
    df = pd.DataFrame(activities)

    df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"])
    df["distance"] = df["distance"].astype(float)
    df["duration"] = df["duration"].astype(float)
    df["sport"] = df["activityType"].apply(lambda x: x["typeKey"])
    df["sport_group"] = df["sport"].apply(map_sport_group)

    return df

df = load_all_activities()

# --- Layout filtrů nahoře v jednom řádku
st.title("📊 Garmin dashboard")

col1, col2, col3 = st.columns([1, 2, 3])

with col1:
    available_sports = sorted(df["sport_group"].unique())
    selected_sport = st.selectbox("Vyber sport", available_sports)

with col2:
    min_date = df["startTimeLocal"].min().date()
    max_date = df["startTimeLocal"].max().date()
    start_date = st.date_input("Od", min_value=min_date, max_value=max_date, value=max_date - timedelta(days=30))
    end_date = st.date_input("Do", min_value=min_date, max_value=max_date, value=max_date)

# Filtrování dat podle výběru
df_filtered = df[
    (df["sport_group"] == selected_sport) &
    (df["startTimeLocal"].dt.date >= start_date) &
    (df["startTimeLocal"].dt.date <= end_date)
]

# Výběr aktivity pro mapu
with col3:
    activity_options = df_filtered.apply(
        lambda row: f"{row['startTimeLocal'].strftime('%Y-%m-%d %H:%M')} – {row['activityName']}", axis=1
    ).tolist()
    if activity_options:
        selected_activity_str = st.selectbox("Vyber aktivitu pro mapu", activity_options)
        selected_index = activity_options.index(selected_activity_str)
        selected_activity_id = df_filtered.iloc[selected_index]["activityId"]
    else:
        selected_activity_id = None

# --- Výsledky pod filtry, roztáhnuté na celou šířku
st.markdown("---")

if df_filtered.empty:
    st.warning("Žádné aktivity pro vybrané období.")
    st.stop()

total_distance_km = df_filtered["distance"].sum() / 1000
total_duration_h = df_filtered["duration"].sum() / 3600
total_calories = df_filtered["calories"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Celková vzdálenost", f"{total_distance_km:.1f} km")
c2.metric("Celkový čas", f"{total_duration_h:.1f} h")
c3.metric("Spálené kalorie", f"{int(total_calories):,} kcal")

st.subheader("📋 Aktivity")
df_display = df_filtered.copy()

df_display["Vzdálenost (km)"] = df_display["distance"] / 1000
df_display["Tempo (min/km)"] = df_display["averageSpeed"].apply(format_tempo)
df_display["Doba trvání"] = df_display["duration"].apply(format_duration)
df_display["Průměrná tepová frekvence"] = df_display.get("averageHR", pd.Series([None]*len(df_display)))
df_display["Kadence"] = df_display.get("averageCadence", pd.Series([None]*len(df_display)))

st.dataframe(
    df_display[[
        "startTimeLocal", "activityName", "Vzdálenost (km)", "Doba trvání", "Tempo (min/km)",
        "Průměrná tepová frekvence", "Kadence", "calories"
    ]].rename(columns={
        "startTimeLocal": "Datum",
        "activityName": "Název",
        "calories": "Kalorie"
    }),
    use_container_width=True
)

st.subheader("🗺️ Mapa vybrané aktivity")

if selected_activity_id is None:
    st.info("Žádné aktivity k zobrazení mapy.")
else:
    st.write(f"Zobrazujeme aktivitu: {selected_activity_str}")
    try:
        detail = client.get_activity_details(selected_activity_id)
        m = plot_activity_map(detail)
        if m is not None:
            st_folium(m, width=900, height=600)
        else:
            st.info("Vybraná aktivita nemá GPS data vhodná pro mapu.")
    except Exception as e:
        st.warning(f"Nepodařilo se načíst detaily aktivity: {e}")

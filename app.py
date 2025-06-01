import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
from folium.plugins import BeautifyIcon
import requests
from datetime import datetime, date, timedelta

# CONFIGURACIÓN GENERAL
st.set_page_config(page_title="Planificador de Excursiones", layout="wide")
st.title("🚌 Planificador de Excursiones por España")

# DESTINOS DISPONIBLES
locations = {
    "Málaga": (36.7213, -4.4214), "Marbella": (36.5101, -4.8825),
    "Puerto Banús": (36.4828, -4.9529), "Torremolinos": (36.6256, -4.4998),
    "Benalmádena": (36.5953, -4.5696), "Nerja": (36.7461, -3.8809),
    "Caminito del Rey": (36.9103, -4.7595), "Mijas Pueblo": (36.5964, -4.6373),
    "Ronda": (36.7423, -5.1671), "Sevilla": (37.3891, -5.9845),
    "Granada": (37.1773, -3.5986), "Córdoba": (37.8882, -4.7794),
    "Cádiz": (36.5163, -6.2994), "Almería": (36.8340, -2.4637),
    "Madrid": (40.4168, -3.7038), "Barcelona": (41.3874, 2.1686),
    "Valencia": (39.4699, -0.3763), "Bilbao": (43.2630, -2.9350),
    "San Sebastián": (43.3183, -1.9812), "Santiago de Compostela": (42.8804, -8.5463),
    "Zaragoza": (41.6488, -0.8891), "Toledo": (39.8628, -4.0273)
}

# PRECIOS FIJOS
excursion_prices = {
    "Marbella": 160, "Puerto Banús": 160, "Torremolinos": 140,
    "Benalmádena": 140, "Nerja": 180, "Caminito del Rey": 200,
    "Mijas Pueblo": 150, "Ronda": 210, "Sevilla": 320,
    "Granada": 280, "Córdoba": 300, "Cádiz": 340, "Almería": 310,
}

# CONSTANTES
PRICE_PER_KM_PRIVATE = 1.2
PRICE_SHUTTLE = 15
GUIDE_PRICE = 120
PEOPLE_PER_GUIDE = 30
PEOPLE_PER_BUS = 54
BUS_COST = 350

# SIDEBAR FORMULARIO
with st.sidebar.form("config"):
    st.header("🎯 Configura tu Viaje")
    origin = st.selectbox("📍 Origen:", list(locations.keys()), index=0)
    selected_destinations = st.multiselect("📌 Destinos:", [k for k in locations if k != origin], default=["Granada", "Sevilla"])
    num_passengers = st.slider("👥 N° de pasajeros:", 1, 300, 100)
    fecha_viaje = st.date_input("📅 Fecha (máx. 7 días)", min_value=date.today(), max_value=date.today() + timedelta(days=7), help="Elige una fecha para el viaje")
    submitted = st.form_submit_button("✅ Confirmar presupuesto")

# FUNCIÓN CLIMA
def obtener_clima(lat, lon, fecha):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Europe/Madrid"
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "Error al obtener datos del clima"}
        data = response.json()
        fechas = data["daily"]["time"]
        idx = fechas.index(fecha.strftime("%Y-%m-%d"))
        return {
            "min": data["daily"]["temperature_2m_min"][idx],
            "max": data["daily"]["temperature_2m_max"][idx],
            "codigo": data["daily"]["weathercode"][idx]
        }
    except Exception as e:
        return {"error": f"Error de conexión: {e}"}

# PANEL CLIMA
st.sidebar.markdown("---")
st.sidebar.subheader("🌤️ Pronóstico del clima")
lat, lon = locations[origin]
clima = obtener_clima(lat, lon, fecha_viaje)
if "error" in clima:
    st.sidebar.warning(clima["error"])
else:
    st.sidebar.success(f"{fecha_viaje.strftime('%A %d/%m/%Y')}")
    st.sidebar.markdown(f"🌡️ Mín: {clima['min']}°C | Máx: {clima['max']}°C")

# MAPA Y PRESUPUESTO
if submitted and selected_destinations:
    origin_coords = locations[origin]
    m = folium.Map(location=origin_coords, zoom_start=6, control_scale=True, tiles="CartoDB Positron")
    folium.Marker(origin_coords, tooltip="Origen", icon=BeautifyIcon(icon="bus", background_color="blue", text_color="white")).add_to(m)

    total_private_cost = 0
    trip_details = []
    for destino in selected_destinations:
        dest_coords = locations[destino]
        dist = round(geodesic(origin_coords, dest_coords).km, 2)
        buses = (num_passengers + PEOPLE_PER_BUS - 1) // PEOPLE_PER_BUS
        cost = dist * PRICE_PER_KM_PRIVATE * buses
        total_private_cost += cost
        folium.Marker(dest_coords, tooltip=destino, icon=BeautifyIcon(icon="star", border_color="green")).add_to(m)
        folium.PolyLine([origin_coords, dest_coords], color="green", weight=2).add_to(m)
        trip_details.append((destino, dist, cost))

    st.subheader("🗺️ Mapa Interactivo")
    st_folium(m, width=1000, height=600)

    # Cálculos
    guides = (num_passengers + PEOPLE_PER_GUIDE - 1) // PEOPLE_PER_GUIDE
    buses = (num_passengers + PEOPLE_PER_BUS - 1) // PEOPLE_PER_BUS
    total_cost = total_private_cost + (guides * GUIDE_PRICE) + (buses * BUS_COST) + (num_passengers * PRICE_SHUTTLE)
    cost_per_passenger = total_cost / num_passengers
    cost_per_bus = total_private_cost / buses

    st.subheader("📦 Presupuesto Detallado")
    st.markdown(f"- 🚌 Autobuses necesarios: **{buses}** (€{bus_total := buses * BUS_COST:.2f})")
    st.markdown(f"- 👨‍🏫 Guías necesarios: **{guides}** (€{guide_total := guides * GUIDE_PRICE:.2f})")
    st.markdown(f"- 🚐 Shuttle total: **€{shuttle_total := num_passengers * PRICE_SHUTTLE:.2f}**")
    st.markdown(f"- 🚚 Traslados privados: **€{total_private_cost:.2f}**")

    st.subheader("👤 Costo por Pasajero")
    st.markdown(f"### 🔢 €{cost_per_passenger:.2f} por persona")
    st.markdown(f"### 🚌 €{cost_per_bus:.2f} por autobús (viaje privado)")

    st.subheader("📍 Detalles por Destino")
    st.table([
        {"Destino": d, "Distancia (km)": f"{dist:.1f}", "Costo (€)": f"{cost:.2f}"}
        for d, dist, cost in trip_details
    ])

    st.subheader("🎫 Precios Fijos desde Málaga")
    st.table([
        {"Destino": d, "Precio fijo (€)": f"{p:.2f}"}
        for d, p in excursion_prices.items()
    ])

    st.caption("🔹 Costos estimados sujetos a variación estacional o por proveedor.")

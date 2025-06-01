# 🚌🇪🇸 Planificador de Excursiones por España

**Planificador de Excursiones por España** es una plataforma interactiva desarrollada con [Streamlit](https://streamlit.io/) que facilita la organización de excursiones turísticas grupales por todo el territorio español, con un enfoque especial en la región de **Andalucía**.

💡 Ideal para **ayuntamientos, centros educativos, organizaciones culturales y empresas turísticas**, esta herramienta proporciona información detallada sobre rutas, costos, logística, y pronóstico climático para tomar decisiones eficientes y sostenibles.

---

## 🎯 Características Destacadas

| Funcionalidad | Descripción |
|---------------|-------------|
| 🧭 **Selección Dinámica de Rutas** | Escoge un punto de origen y múltiples destinos turísticos en España. |
| 🌦️ **Clima Integrado (OpenWeather API)** | Obtén el pronóstico detallado para la fecha del viaje. |
| 💶 **Presupuesto Automatizado** | Cálculo instantáneo del costo por pasajero, bus, guía y traslado. |
| 🗺️ **Mapa Interactivo** | Visualiza el recorrido y los puntos clave de tu excursión. |
| 🚌 **Logística Inteligente** | Asignación automática de guías y buses según la cantidad de pasajeros. |
| 📊 **Precios Fijos por Destino** | Tarifas establecidas para excursiones frecuentes desde Málaga. |

---

## 🌐 Vista previa de la aplicación

![preview](https://user-images.githubusercontent.com/your_image.png)

---

## 🛠️ Tecnologías Utilizadas

- **🧠 Python 3.9+** – Lenguaje principal
- **🎨 Streamlit** – Framework web para dashboards
- **🗺️ Folium + Leaflet.js** – Mapas interactivos y rutas
- **📍 Geopy** – Cálculo preciso de distancias geográficas
- **🌤️ OpenWeatherMap API** – Pronóstico meteorológico
- **📦 Docker (opcional)** – Para despliegue profesional

---

## 📦 Instalación Local

### ⚙️ Requisitos

- Python 3.9 o superior
- Cuenta gratuita en [OpenWeatherMap](https://openweathermap.org/api) para obtener tu clave API

### 🧪 Paso a paso

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu_usuario/planificador-excursiones.git
cd planificador-excursiones

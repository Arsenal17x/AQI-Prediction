import streamlit as st
import pandas as pd
import joblib
from analysis import data_analysis_page
from realtime import get_aqi
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
st.set_page_config(page_title="Air Quality Index Prediction", layout="wide", page_icon="🌍")
# Load the model
model = joblib.load('RFregressor.joblib')

st.markdown("""
    <style>
        /* Sidebar Customization */
        .css-1d391kg {background-color: #0e1e34; padding: 30px; border-radius: 12px; box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.1);}
        .css-1d391kg .sidebar .sidebar-content {color: white;}
        .sidebar .sidebar-content h1 {color: #FFCC00; font-size: 28px; font-weight: bold; margin-bottom: 15px; text-align: center;}

        /* Sidebar Titles */
        .sidebar h2 {font-size: 24px; font-weight: bold; color: #FFCC00; margin-top: 20px; margin-bottom: 10px;}
        .sidebar h3 {color: #FFFF99; font-size: 18px; margin-top: 10px; text-align: left;}

        /* Sidebar Navigation Links */
        .sidebar .stRadio {background-color: transparent; border: none;}
        .sidebar .stRadio label {font-size: 18px; color: #FFCC00; font-weight: bold; padding: 5px 0;}
        .sidebar .stRadio input[type="radio"]:checked+label {background-color: #FFCC00; color: #333; border-radius: 5px; padding: 6px 8px;}

        /* Button Styling */
        .stButton>button {
            background-color: #FFCC00;
            color: #333;
            border-radius: 10px;
            border: 2px solid #FFCC00;
            font-weight: bold;
            padding: 12px;
            font-size: 18px;
            width: 100%;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        /* Hover effect for buttons */
        .stButton>button:hover {
            background-color: #FF6600;
            color: white;
            transform: translateY(-3px);
        }

        /* Page Title Styling */
        h1, h2 {text-align: center; color: #FFCC00; margin-top: 20px;}

        /* Content Styling */
        .stTextInput>div>input {font-size: 16px; padding: 8px;}
    </style>
""", unsafe_allow_html=True)


# Create a sidebar menu with different options
with st.sidebar:
    page = option_menu(
        'Air Quality Prediction System',
        ['Introduction', 'AQI Prediction', 'Seasonal Trend Analysis','Real-Time Weather'],
        menu_icon='hospital-fill',  # Icon for the menu
        icons=['house', 'cloud-sun', 'bar-chart'],  # Icons for each section
        default_index=0  # Default selected index
    )
if page == "Introduction":
    st.title("Air Quality Index (AQI) Prediction Project")
    st.markdown("""
    ### Objective
    The primary goal of this project is to forecast the concentration of PM2.5 (particulate matter) and calculate the corresponding AQI. This will help users understand current air pollution levels and take necessary precautions.

    ### Key Features
    - *PM2.5 Prediction:* The model predicts PM2.5 levels using input features like wind speed, temperature, humidity, and aerosol optical depth.
    - *AQI Calculation:* The predicted PM2.5 is converted into an AQI value based on standard breakpoints defined by environmental agencies.
    - *Health Recommendations:* The tool provides personalized health advice based on the AQI category to help users mitigate risks associated with poor air quality.
    - Seasonal Trend Analysis:Analyze air quality patterns over different seasons to identify trends and variations, helping in better understanding of pollution dynamics and planning preventive measures.
    - Real-Time Weather Integration:Seamlessly incorporates real-time weather data, including temperature, humidity, and wind speed, to provide more accurate and context-aware air quality predictions.
    - Alerts and Warnings:Generates timely alerts and warnings when pollutant levels exceed safe limits, enabling quick actions to minimize health risks and improve public safety.

    ### Technologies Used
    - *Machine Learning:* A Random Forest Regressor model is used for predicting PM2.5 levels.
    - Python:Used for data analysis, preprocessing, and implementing machine learning models for air quality prediction.
    - Streamlit:A Python-based framework for building an interactive and user-friendly web application for visualizing air quality data.
    - Pandas and NumPy:Utilized for efficient data manipulation and numerical computations.
    - Matplotlib and Seaborn:Used for creating insightful visualizations and trend analysis charts.
    - Scikit-learn:Employed for implementing machine learning models and performing model evaluation.
    ### Why This Project Matters
    Monitoring and predicting air quality is critical for public health. Poor air quality can cause respiratory issues, cardiovascular problems, and other health complications. This project empowers users to make informed decisions by providing real-time predictions and insights into air pollution levels.

    ### Target Users
    - *General Public:* Individuals seeking to monitor air quality in their local environment.
    - *Health Enthusiasts:* People concerned about air quality’s impact on health.
    - *Environmental Agencies:* Organizations tracking air pollution for research and policy-making.
    """)

# Page 2: AQI Prediction
elif page == "AQI Prediction":
    st.title("Predict AQI")

    # Input fields
    ws = st.number_input("Wind Speed (ws)", value=0.0, format="%.10f")
    wd = st.number_input("Wind Direction (wd)", value=0.0, format="%.10f")
    temp = st.number_input("Temperature (temp)", value=0.0, format="%.10f")
    rh = st.number_input("Relative Humidity (rh)", value=0.0, format="%.10f")
    dew_temp = st.number_input("Dew Temperature (dew_temp)", value=0.0, format="%.10f")
    precipitation = st.number_input("Precipitation (precipitation)", value=0.0, format="%.10f")
    pressure = st.number_input("Pressure (pressure)", value=1013.25, format="%.10f")
    wv = st.number_input("Water Vapor (wv)", value=0.0, format="%.10f")
    blh = st.number_input("Boundary Layer Height (blh)", value=0.0, format="%.10f")
    bcaod550 = st.number_input("BC Aerosol Optical Depth at 550nm (bcaod550)", value=0.0, format="%.10f")
    duaod550 = st.number_input("DU Aerosol Optical Depth at 550nm (duaod550)", value=0.0, format="%.10f")
    omaod550 = st.number_input("Oma Aerosol Optical Depth at 550nm (omaod550)", value=0.0, format="%.10f")
    ssaod550 = st.number_input("SSA Aerosol Optical Depth at 550nm (ssaod550)", value=0.0, format="%.10f")
    suaod550 = st.number_input("SUA Aerosol Optical Depth at 550nm (suaod550)", value=0.0, format="%.10f")
    aod469 = st.number_input("Aerosol Optical Depth at 469nm (aod469)", value=0.0, format="%.10f")
    aod550 = st.number_input("Aerosol Optical Depth at 550nm (aod550)", value=0.0, format="%.10f")
    aod670 = st.number_input("Aerosol Optical Depth at 670nm (aod670)", value=0.0, format="%.10f")
    aod865 = st.number_input("Aerosol Optical Depth at 865nm (aod865)", value=0.0, format="%.10f")
    aod1240 = st.number_input("Aerosol Optical Depth at 1240nm (aod1240)", value=0.0, format="%.10f")

    if st.button("Predict"):
        input_data = pd.DataFrame({
            'ws': [ws], 'wd': [wd], 'temp': [temp], 'rh': [rh],
            'dew_temp': [dew_temp], 'precipitation': [precipitation], 'pressure': [pressure],
            'wv': [wv], 'blh': [blh], 'bcaod550': [bcaod550], 'duaod550': [duaod550],
            'omaod550': [omaod550], 'ssaod550': [ssaod550], 'suaod550': [suaod550],
            'aod469': [aod469], 'aod550': [aod550], 'aod670': [aod670], 'aod865': [aod865], 'aod1240': [aod1240]
        })

        predicted_pm25 = model.predict(input_data)


        def calculate_aqi(pm25):
            breakpoints = [
                (0, 12, 0, 50), (12.1, 35.4, 51, 100),
                (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200),
                (150.5, 250.4, 201, 300), (250.5, 500, 301, 500)
            ]
            for (low, high, low_aqi, high_aqi) in breakpoints:
                if low <= pm25 <= high:
                    return int(((pm25 - low) / (high - low)) * (high_aqi - low_aqi) + low_aqi)
            return None


        aqi = calculate_aqi(predicted_pm25[0])


        def early_warning_system(aqi):
            if aqi >= 150:
                return "⚠ *Early Warning!* AQI is high. Take necessary precautions to avoid health issues.", "red"
            elif aqi >= 100:
                return "⚠ *Warning:* Air quality is moderate. Sensitive individuals should limit outdoor activities.", "orange"
            elif aqi >= 50:
                return "✅ *Air Quality is Good.* No immediate health concerns.", "yellow"
            else:
                return "✅ *Excellent Air Quality.* No health risks.", "green"


        # Get the warning message and color
        warning_message, color = early_warning_system(aqi)

        # Display the warning with dynamic color
        st.markdown(
            f"<div style='background-color: {color}; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center;'>{warning_message}</div>",
            unsafe_allow_html=True
        )


        def get_health_recommendation(aqi):
            if aqi <= 50:
                return (
                    """Good: Air quality is satisfactory, and air pollution poses little or no risk.

        Causes:
        1. Minimal emissions from vehicles and industries.
        2. Low levels of natural air pollutants.
        3. Clean energy sources being used widely.
        4. Favorable weather conditions dispersing pollutants.
        5. Low urban traffic congestion.

        Prevention:
        1. Continue using clean energy sources.
        2. Maintain low emissions from vehicles and industries.
        3. Encourage walking and biking to reduce traffic.
        4. Support policies for reducing air pollution.
        5. Promote awareness of air quality benefits."""
                )
            elif aqi <= 100:
                return (
                    """Moderate: Air quality is acceptable; however, some pollutants may be a concern for sensitive individuals.

        Causes:
        1. Slight increase in vehicle emissions.
        2. Higher industrial activity producing moderate pollutants.
        3. Pollutants from household activities, such as heating.
        4. Weather conditions allowing pollutants to accumulate.
        5. Occasional high traffic congestion.

        Prevention:
        1. Limit outdoor activities for sensitive individuals.
        2. Use eco-friendly transport options like carpooling.
        3. Reduce household emissions (e.g., using cleaner fuels).
        4. Maintain proper ventilation indoors.
        5. Encourage the use of public transportation."""
                )
            elif aqi <= 150:
                return (
                    """Unhealthy for Sensitive Groups: Members of sensitive groups may experience health effects.

        Causes:
        1. Higher levels of pollutants like PM2.5 and ozone.
        2. Emissions from vehicles and factories in urban areas.
        3. Weather conditions like temperature inversions trapping pollutants.
        4. Dust storms or wildfires contributing to particulate matter.
        5. Industrial waste or agricultural activity releasing pollutants.

        Prevention:
        1. Sensitive individuals should limit outdoor activities.
        2. Install air purifiers indoors.
        3. Reduce vehicle usage, especially in peak hours.
        4. Encourage urban green spaces to improve air quality.
        5. Stay hydrated and wear protective masks outdoors."""
                )
            elif aqi <= 200:
                return (
                    """Unhealthy: Everyone may experience health effects; sensitive groups may experience more serious effects.

        Causes:
        1. High levels of pollution from industrial emissions.
        2. Traffic congestion in densely populated areas.
        3. Seasonal smog or haze affecting air quality.
        4. Burning of fossil fuels contributing to elevated emissions.
        5. Climatic conditions limiting the dispersal of pollutants.

        Prevention:
        1. Avoid prolonged outdoor activities.
        2. Wear protective masks, especially for children and elderly.
        3. Use air purifiers indoors to reduce pollution exposure.
        4. Limit industrial and vehicular emissions.
        5. Follow health advisories issued by local authorities."""
                )
            elif aqi <= 300:
                return (
                    """Very Unhealthy: Health alert—everyone may experience more serious health effects.

        Causes:
        1. Extreme pollution from uncontrolled industrial activities.
        2. High levels of particulate matter from wildfire smoke.
        3. Vehicle emissions in high-density urban areas.
        4. Seasonal weather patterns trapping air pollutants.
        5. Air pollution from both local and distant sources.

        Prevention:
        1. Avoid all outdoor activities.
        2. Keep windows and doors closed to limit outdoor air infiltration.
        3. Use high-efficiency air filters indoors.
        4. Follow health guidelines from local health authorities.
        5. Use air quality apps to stay updated and reduce exposure."""
                )
            else:
                return (
                    """Hazardous: Health warnings of emergency conditions. The entire population is more likely to be affected.

        Causes:
        1. Severe pollution from wildfires, industrial disasters, or major accidents.
        2. Large-scale emissions from factories, power plants, and refineries.
        3. Persistent weather conditions causing pollutant buildup.
        4. High concentrations of toxic air pollutants like sulfur dioxide.
        5. Extreme weather conditions like heat waves worsening air quality.

        Prevention:
        1. Remain indoors and avoid all outdoor activities.
        2. Keep windows closed and use air conditioning with proper filtration.
        3. Follow emergency measures from local health and government agencies.
        4. Use N95 masks for added protection when going outdoors.
        5. Stay updated with local air quality warnings and alerts."""
                )

        recommendation = get_health_recommendation(aqi)

        # Display results
        st.subheader("Results")
        st.write(f"Predicted PM2.5: {predicted_pm25[0]:.2f} µg/m³")
        st.write(f"AQI: {aqi}")
        st.markdown(f"Health Recommendation:<br>{recommendation}", unsafe_allow_html=True)


# Page 3: Future Features
elif page == "Seasonal Trend Analysis":
    data_analysis_page()

elif page == "Real-Time Weather":

    st.title("Real-Time Weather Condition")

    # Input fields for latitude, longitude, and API key
    longitude = st.text_input("Enter longitude of the place:")
    latitude = st.text_input("Enter latitude of the place:")

    # Button to trigger AQI data retrieval
    if st.button("Get Real-Time Weather"):
        # Check if both latitude and longitude are provided
        if longitude and latitude:
            try:
                # Convert input values to float
                longitude = float(longitude)
                latitude = float(latitude)

                # Use your OpenWeatherMap API key here
                api_key = "13c0e92df4c25cb3a7b65377e97183da"

                # Get AQI data for the provided coordinates
                response_data = get_aqi(longitude, latitude, api_key)

                if response_data is not None:
                    # Extracting the data
                    weather_condition = response_data["weather"][0]["description"]
                    temperature = response_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
                    humidity = response_data["main"]["humidity"]
                    wind_speed = response_data["wind"]["speed"]
                    wind_direction = response_data["wind"]["deg"]
                    sunrise_timestamp = response_data["sys"]["sunrise"]
                    sunset_timestamp = response_data["sys"]["sunset"]
                    location = response_data["name"]
                    visibility = response_data["visibility"]


                    def convert_to_ist(timestamp):
                        # Convert the timestamp to a UTC datetime object
                        utc_time = datetime.utcfromtimestamp(timestamp)

                        # IST is UTC + 5 hours and 30 minutes
                        ist_offset = timedelta(hours=5, minutes=30)
                        ist_time = utc_time + ist_offset

                        # Return IST time in a readable format
                        return ist_time.strftime("%Y-%m-%d %H:%M:%S")


                    # Convert sunrise and sunset timestamps to IST
                    sunrise_time_ist = convert_to_ist(sunrise_timestamp)
                    sunset_time_ist = convert_to_ist(sunset_timestamp)

                    # Display the extracted information
                    st.write(f"*Weather in {location}:* {weather_condition}")
                    st.write(f"*Temperature:* {temperature:.2f} °C")
                    st.write(f"*Humidity:* {humidity}%")
                    st.write(f"*Wind Speed:* {wind_speed} m/s")
                    st.write(f"*Wind Direction:* {wind_direction}°")
                    st.write(f"*Visibility:* {visibility} meters")
                    st.write(f"*Sunrise:* {sunrise_time_ist}")
                    st.write(f"*Sunset:* {sunset_time_ist}")
                else:
                    st.write("Failed to retrieve AQI data. Please check the coordinates or API key.")
            except ValueError:
                st.write("Please enter valid numeric values for latitude and longitude.")
        else:
            st.write("Please enter both latitude and longitude.")


# import joblib
#
# model = joblib.load('model/RFregressor.joblib')
# input_features = [
#     1.024499178 ,   297.0213013,    27.93826294,    19.90987083,    2.834838867 ,   0.000426138,    1005.254456,    9.298650742,
#     1027.545044  ,  0.003951926 ,   0.002403036 ,   0.054809123 ,   0.001572877  ,  0.017226346 ,   0.099897027 ,   0.079970568,
#     0.059608743   , 0.039478689  ,  0.021583095
#
# ]
# output = model.predict([input_features])
#
# print(f"Model Output: {output[0]}")
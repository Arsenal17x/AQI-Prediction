import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_analysis_page():
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

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

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['Year'] = df['datetime'].dt.year
        df['Month'] = df['datetime'].dt.month
        df = df.sort_values(by='datetime')
        df['AQI'] = df['pm2p5'].apply(calculate_aqi)

        st.write("Transformed Data Preview:")
        st.dataframe(df)

        st.subheader("AQI by Year")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Year', y='AQI', data=df)
        st.pyplot(plt)

        st.subheader("AQI Trend Over Months")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Month', y='AQI', data=df, marker='o')
        st.pyplot(plt)


        st.subheader("Monthly Analysis")
        # Select only numeric columns again to avoid issues with non-numeric columns
        numerical_cols = ['ws', 'pm2p5', 'temp', 'rh','bcaod550','omaod550','ssaod550']

        # Extract month and convert to string for consistent grouping
        df['Month'] = df['datetime'].dt.to_period('M').astype(str)

        # Handle NaN values by filling or ignoring them (choose based on need)
        monthly_data = df.groupby('Month', as_index=False)[numerical_cols].mean(numeric_only=True)

        # Plotting
        plt.figure(figsize=(20, 12))
        for col in numerical_cols:
            plt.plot(monthly_data['Month'], monthly_data[col], label=col)

        plt.xlabel('Months')
        plt.ylabel('Mean Values per month')
        plt.title('Changes by month')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(plt)

        st.subheader("Monthly and Annual Average AQI ")
        df['Month'] = df['datetime'].dt.to_period('M')
        df['Year'] = df['datetime'].dt.year

        monthly_aqi = df.groupby('Month')['AQI'].mean()

        annual_aqi_mean = df.groupby('Year')['AQI'].mean()

        plt.figure(figsize=(20, 12), dpi=300)

        plt.plot(monthly_aqi.index.astype(str), monthly_aqi, color='blue', label='Monthly AQI Average')

        plt.axhline(y=annual_aqi_mean.mean(), linestyle='--', color='red', label='Annual AQI Average')

        plt.xlabel('Month')
        plt.ylabel('AQI')
        plt.title('Monthly and Annual Average AQI')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(plt)



    else:
        st.warning("Please upload an Excel file to continue.")
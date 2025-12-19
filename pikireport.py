# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 01:29:43 2024

@author: USER
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from math import radians, sin, cos, sqrt, atan2
import folium
from folium.plugins import HeatMap


st.set_page_config(page_title="Piki Report", page_icon="📋", layout="wide")

# Function to apply custom CSS styling


def set_style():
    st.markdown(
        """
        <style>
        /* Main page background */
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://unsplash.com/photos/aJTiW00qqtI/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8N3x8YmFja2dyb3VuZCUyMGNvdmVyc3xlbnwwfHx8fDE3MDcxNTg0NDB8MA&force=true");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
        }
        .main {
            max-width: 800px;
            padding: 20px;
            background-color: rgba(244, 244, 244, 0.85); /* Transparent box for readability */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
            overflow-y: auto;
        }
        .main:hover {
            transform: scale(1.02);
        }

        /* Sidebar customization */
        [data-testid="stSidebar"] {
            background-color: #f4f4f4; /* Light background color */
            background-attachment: fixed;
            padding: 20px;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
            border-left: 2px solid #007bff; /* Blue border on the left */
        }

        /* Radio button styling */
        [data-testid="stSidebar"] .css-1vhn7lj {
            font-size: 22px;  /* Font size for radio button text */
            font-weight: bold; /* Make text bold */
            color: #333;       /* Text color */
            margin: 10px 0;   /* Margin for spacing */
            padding: 10px;     /* Padding for better click area */
            border-radius: 5px; /* Rounded corners */
            background-color: #e9ecef; /* Light gray background for each button */
            transition: background-color 0.3s ease; /* Smooth background transition */
        }

        /* Change background on hover */
        [data-testid="stSidebar"] .css-1vhn7lj:hover {
            background-color: #d6d8db; /* Darker gray on hover */
        }

        /* Title and header customization */
        .title {
            font-size: 32px;
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }

        .subheader {
            font-size: 24px;
            text-align: center;
            margin-bottom: 10px;
            color: #555;
        }

        .emoji {
            font-size: 40px;
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the CSS styles
set_style()


st.sidebar.markdown(
    """
    <style>
    .circular-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        height: 150px;
        border-radius: 50%;  /* Circular frame */
        object-fit: cover;   /* Ensure the image fills the circle */
        border: 2px solid #f4f4f4;  /* Optional border for decoration */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);  /* Optional shadow effect */
    }
    </style>
    <img class="circular-image" src="https://unsplash.com/photos/5E7sHzeIHN8/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTN8fGRvd24lMjBhcnJvd3xlbnwwfHx8fDE3MjkxNjQ2MDd8MA&force=true" alt="Piki Logo">
    """,
    unsafe_allow_html=True
)



# Main function
def main():
    set_style()

    # App content
    st.title("DAILY REPORT ")
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Data analysis for daily operation 📊</div>", unsafe_allow_html=True)
    
    
   
    # Navigation sidebar
    nav_page = st.sidebar.radio("Navigation", ["Data Analysis📈📉", "Delivery Time⏰","drivers analysis🚴","rejected orders"])
    
    if nav_page == "Data Analysis📈📉":
        data_analysis()
    elif nav_page == "Delivery Time⏰":
        delivery_time()
    elif nav_page == "drivers analysis🚴":
        drivers_analysis()        
    elif nav_page == "rejected orders":
        rejected_orders()
        
    st.sidebar.image(
        "https://unsplash.com/photos/50yZdrpM_ec/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8N3x8ZGVsaXZlcnklMjBtb3RvcnxlbnwwfHx8fDE3MzA3MTMxNDd8MA&force=true",
        #"https://media.istockphoto.com/id/1296986175/photo/young-man-working-for-a-food-delivery-service-checking-with-road-motorcycle-in-the-city.jpg?s=2048x2048&w=is&k=20&c=Jg03jmHONRuVF_LJSxC1Y87-6DXzc930GzJVI1wUMWU=", 
        use_column_width=True, 
        caption="Piki Delivery",
    )

    

# At the start of the app
if 'df' not in st.session_state:
    st.session_state.df = None

def load_data():
    uploaded_files = st.file_uploader(
        "Upload Your Dataset (CSV or Excel)",
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        try:
            dataframes = []

            for file in uploaded_files:
                if file.name.endswith(".xlsx"):
                    df = pd.read_excel(file, engine="openpyxl")
                else:
                    df = pd.read_csv(file)

                dataframes.append(df)

            # Combine all files (row-wise)
            combined_df = pd.concat(dataframes, ignore_index=True)

            st.session_state.df = combined_df
            st.success(f"{len(uploaded_files)} file(s) uploaded and combined successfully")

        except Exception as e:
            st.error(f"Error loading files: {e}")


    
    
# Updated download function to accept filename as an argument
def download_excel(dataframe, filename="download.xlsx"):
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)    


def data_analysis():
    st.title("DATA SUMMARY")

    load_data()

    if st.session_state.df is not None:
        df = st.session_state.df

        st.write("Preview of Combined Data")
        st.dataframe(df.head())

        st.write("Dataset Shape:", df.shape)

        # Example: Download cleaned dataset
        download_excel(df, "combined_dataset.xlsx")




    
        # Convert DELIVERY TIME to datetime and extract hour
        df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'], errors='coerce')
        df['HOURS'] = df['DELIVERY TIME'].dt.hour

        # Filter data based on selected hours
        hours_range = st.slider("Select Hours Range:", min_value=0, max_value=23, value=(0, 23))
        selected_hours = list(range(hours_range[0], hours_range[1] + 1))
        filtered_df = df[df['HOURS'].isin(selected_hours)]




        # ---- Summary Table for Order Status ----
        state_summary = filtered_df['STATE'].value_counts().reset_index()
        state_summary.columns = ['STATE', 'Count']
        total_orders = filtered_df.shape[0]
        total_row = pd.DataFrame({'STATE': ['TOTAL ORDERS'], 'Count': [total_orders]})
        state_summary = pd.concat([total_row, state_summary], ignore_index=True)
        
        st.markdown("### Summary Table for Order Status")
        st.table(state_summary)
        
        # Download Button for Order Status Summary
        if st.button("Download Order Status Summary"):
            download_excel(state_summary, "order_status_summary.xlsx")
        
        # ---- Driver Location Analysis and Checklist ----
        st.markdown("### Driver Location Analysis and Checklist")
        
        # Define the regional cities
        regional_cities = ['Mwanza', 'Zanzibar', 'Arusha', 'Dodoma']
        
        # Classify drivers into Dar es Salaam or Regional
        df['Driver Location'] = df['BUSINESS CITY'].apply(
            lambda x: 'Regional' if x in regional_cities else 'Dar es Salaam'
        )
        
        # Calculate total drivers by location
        driver_location_summary = df.groupby('Driver Location')['DRIVER ID'].nunique().reset_index()
        driver_location_summary.rename(columns={'DRIVER ID': 'Total Number of Drivers'}, inplace=True)
        
        # Add placeholders for the checklist columns
        driver_location_summary['Is Driver Sufficient?'] = ''
        driver_location_summary['Explain any challenge you faced that need improvement'] = ''
        driver_location_summary['What are your suggestions?'] = ''
        
        # Calculate total number of drivers across locations
        total_drivers = df['DRIVER ID'].nunique()
        
        # Add a "Total" row at the bottom
        total_row = pd.DataFrame({
            'Driver Location': ['Total'],
            'Total Number of Drivers': [total_drivers],
            'Is Driver Sufficient?': [''],
            'Explain any challenge you faced that need improvement': [''],
            'What are your suggestions?': ['']
        })
        
        # Append the "Total" row to the driver_location_summary DataFrame
        driver_location_summary = pd.concat([driver_location_summary, total_row], ignore_index=True)
        
        # Display the driver location analysis and checklist
        st.table(driver_location_summary)
        
        # Download Button for Driver Location Analysis
        if st.button("Download Driver Location Analysis and Checklist"):
            download_excel(driver_location_summary, "driver_location_analysis_checklist.xlsx")
        
        
        

        # ---- Custom Analysis for Business City and Order Status ----
        # Map specific states to new columns using multiple conditions
        df['ORDER STATUS'] = np.where(
            df['STATE'].isin(['Delivery Completed By Driver']),
            'DELIVERY COMPLETED BY DRIVER',
            np.where(
                df['STATE'].isin(['Rejected', 'Rejected by Driver', 'Rejected by Business']),
                'REJECTED',
                np.where(
                    df['STATE'].isin(['Completed', 'Pickup completed by customer']),
                    'PICKUP ORDERS',
                    np.where(
                        df['STATE'].isin(['Delivery Failed By Driver', 'Not picked by customer', 'Pickup Failed By Driver']),
                        'DELIVERY FAILED BY DRIVER',
                        np.nan
                    )
                )
            )
        )

        # Filter data to include only rows with mapped order statuses
        df_filtered = df.dropna(subset=['ORDER STATUS'])

        # Create pivot table
        order_status_summary = df_filtered.pivot_table(
            index='BUSINESS CITY',
            columns='ORDER STATUS',
            values='ID',
            aggfunc='count',
            margins=False
        ).fillna(0).astype(int)
        
        # Add total orders per city
        order_status_summary['TOTAL_ORDERS'] = order_status_summary.sum(axis=1)
        
        # Ensure expected columns exist
        expected_cols = [
            'DELIVERY COMPLETED BY DRIVER',
            'REJECTED',
            'PICKUP ORDERS',
            'DELIVERY FAILED BY DRIVER'
        ]
        
        for col in expected_cols:
            if col not in order_status_summary.columns:
                order_status_summary[col] = 0
        
        # Vendor count
        restaurant_counts = df[['BUSINESS NAME', 'BUSINESS CITY']].drop_duplicates() \
            .groupby('BUSINESS CITY').size().reset_index(name='NUMBER OF RESTAURANTS')
        
        # Merge restaurant data
        order_status_summary = order_status_summary.reset_index().merge(
            restaurant_counts,
            on='BUSINESS CITY',
            how='left'
        )
        
        order_status_summary['NUMBER OF RESTAURANTS'] = order_status_summary['NUMBER OF RESTAURANTS'].fillna(0).astype(int)
        
        # Percentage contribution
        total_company_orders = order_status_summary['TOTAL_ORDERS'].sum()
        
        order_status_summary['PERCENTAGE CONTRIBUTION'] = (
            (order_status_summary['TOTAL_ORDERS'] / total_company_orders) * 100
        ).round(1).astype(str) + '%'
        
        # Sort by highest orders
        order_status_summary = order_status_summary.sort_values(by='TOTAL_ORDERS', ascending=False)
        
        # Add Total row
        total_row = pd.DataFrame({
            'BUSINESS CITY': ['TOTAL'],
            'DELIVERY COMPLETED BY DRIVER': [order_status_summary['DELIVERY COMPLETED BY DRIVER'].sum()],
            'REJECTED': [order_status_summary['REJECTED'].sum()],
            'PICKUP ORDERS': [order_status_summary['PICKUP ORDERS'].sum()],
            'DELIVERY FAILED BY DRIVER': [order_status_summary['DELIVERY FAILED BY DRIVER'].sum()],
            'TOTAL_ORDERS': [order_status_summary['TOTAL_ORDERS'].sum()],
            'NUMBER OF RESTAURANTS': [order_status_summary['NUMBER OF RESTAURANTS'].sum()],
            'PERCENTAGE CONTRIBUTION': ['100%']
        })
        
        order_status_summary = pd.concat([order_status_summary, total_row], ignore_index=True)
        
        # FINAL COLUMN ORDER
        final_cols = [
            'BUSINESS CITY',
            'NUMBER OF RESTAURANTS',
            'DELIVERY COMPLETED BY DRIVER',
            'REJECTED',
            'PICKUP ORDERS',
            'DELIVERY FAILED BY DRIVER',
            'TOTAL_ORDERS',
            'PERCENTAGE CONTRIBUTION'
        ]
        
        order_status_summary = order_status_summary[final_cols]
        
        # Display table
        st.markdown("### Order Status by Business City")
        st.table(order_status_summary)
        
        # Download file
        if st.button("Download Order Status by Business City"):
            download_excel(order_status_summary, "order_status_by_city.xlsx")

            
            

        # ---- Customer Ordering Platform Distribution ----
        platform_counts = df['CREATE_FROM'].value_counts().reset_index()
        platform_counts.columns = ['Platform', 'Count']

        st.markdown("### Customer Ordering Platform Distribution")
        st.table(platform_counts)

        plt.figure(figsize=(8, 8))
        plt.pie(platform_counts['Count'], labels=platform_counts['Platform'],
                autopct='%1.1f%%', startangle=140)
        plt.title("Customer Ordering Platform Distribution")
        plt.tight_layout()
        st.pyplot(plt)
        




# Function to categorize issues for orders
def categorize_issues(row):
    issues = []
    if row['Accepted by Business'] < 0 or row['Accepted by Business'] > 30:
        issues.append("Accepted by Business Out of Range")
    if row['Assigned Time'] < 0 or row['Assigned Time'] > 30:
        issues.append("Assigned Time Out of Range")
    if row['Accepted by Driver'] < 0 or row['Accepted by Driver'] > 45:
        issues.append("Accepted by Driver Out of Range")
    if row['Driver to Business'] < 0 or row['Driver to Business'] > 45:
        issues.append("Driver to Business Out of Range")
    if row['Driver in Business'] < 0 or row['Driver in Business'] > 90:
        issues.append("Driver in Business Out of Range")
    if row['Pickup to Customer'] < 0 or row['Pickup to Customer'] > 45:
        issues.append("Pickup to Customer Out of Range")
    if row['Average Delivery Time'] < 0 or row['Average Delivery Time'] > 100:
        issues.append("Average Delivery Time Out of Range")
    return ", ".join(issues)


    
# Haversine formula to calculate distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Calculate distances and categorize them
def calculate_distances(df):
    distances = []

    # Loop through each row to compute the distance
    for _, row in df.iterrows():
        distance = haversine(
            row['CUSTOMER LATITUDE'],
            row['CUSTOMER LONGITUDE'],
            row['BUSINESS LATITUDE'],
            row['BUSINESS LONGITUDE']
        )
        distances.append(distance)

    # Add the 'Distance (km)' column to the DataFrame
    df['DISTANCE (km)'] = distances

    # Define distance bins and labels
    bins = [0, 2, 3, 4, 5, 7, float('inf')]
    labels = ['0-2 km', '2-3 km', '3-4 km', '4-5 km', '5-7 km', '7+ km']


    # Create the 'Distance Category' column
    df['Distance Category'] = pd.cut(df['DISTANCE (km)'], bins=bins, labels=labels)

    return df

        
def calculate_order_timing(df):
    # Sort by driver name and delivery time to maintain order
    df = df.sort_values(by=['DRIVER NAME', 'DELIVERY TIME'])

    # Add Current Order Time column
    df['Current Order Time'] = df['DELIVERY TIME']

    # Add Last Order Delivery Time column
    df['Last Order Delivery Time'] = df.groupby('DRIVER NAME')['DELIVERY HOUR'].shift(1)

    # Calculate Time Difference in minutes before another order
    df['Time Difference (mins)'] = (df['DELIVERY TIME'] - df['Last Order Delivery Time']).dt.total_seconds() / 60
    df['Time Difference (mins)'] = df['Time Difference (mins)'].fillna(0)  # Fill NaN with 0 for first order

    return df



# Main delivery time function
def delivery_time():
    st.title("Delivery Time Report")

    if st.session_state.df is None:
        st.warning("Please upload data first in Data Analysis tab.")
        return
    
    df = st.session_state.df.copy()  # consistently use df
    
    # Filter completed deliveries
    df = df[df['STATE'] == 'Delivery Completed By Driver'].copy()
    
    # Convert relevant columns to datetime
    datetime_cols = [
        'DELIVERY TIME', 'ACCEPTED BUSINESS HOUR', 'ASSIGNED HOUR', 
        'ACCEPTED DRIVER HOUR', 'IN BUSINESS HOUR', 'PICKUP HOUR', 'DELIVERY HOUR'
    ]
    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime)
    
    
    # Calculate time differences in minutes
    df['Accepted by Business'] = (df['ACCEPTED BUSINESS HOUR'] - df['DELIVERY TIME']).dt.total_seconds() / 60
    df['Accepted by Business'] = df['Accepted by Business'].mask(df['Accepted by Business'] < 0, 0)
    
    df['Assigned Time'] = (df['ASSIGNED HOUR'] - df['ACCEPTED BUSINESS HOUR']).dt.total_seconds() / 60
    df['Assigned Time'] = df['Assigned Time'].mask(df['Assigned Time'] < 0, 3)
    
    df['Accepted by Driver'] = (df['ACCEPTED DRIVER HOUR'] - df['ASSIGNED HOUR']).dt.total_seconds() / 60
    df['Accepted by Driver'] = df['Accepted by Driver'].mask(df['Accepted by Driver'] < 0, 3)
    
    df['Driver to Business'] = (df['IN BUSINESS HOUR'] - df['ACCEPTED DRIVER HOUR']).dt.total_seconds() / 60
    df['Driver to Business'] = df['Driver to Business'].mask(df['Driver to Business'] < 0, 7)
    
    df['Driver in Business'] = (df['PICKUP HOUR'] - df['IN BUSINESS HOUR']).dt.total_seconds() / 60
    df['Driver in Business'] = df['Driver in Business'].mask(df['Driver in Business'] < 0, 15)
    
    df['Pickup to Customer'] = (df['DELIVERY HOUR'] - df['PICKUP HOUR']).dt.total_seconds() / 60
    df['Pickup to Customer'] = df['Pickup to Customer'].mask(df['Pickup to Customer'] < 0, 15)          
    
    # Step 2: Calculate Average Delivery Time and Handle Cross-Day Deliveries
    df['Average Delivery Time'] = (df['DELIVERY HOUR'] - df['DELIVERY TIME']).dt.total_seconds() / 60
    df['Average Delivery Time'] = df['Average Delivery Time'].mask(df['Average Delivery Time'] < 0,
        (df['DELIVERY HOUR'] - df['ACCEPTED BUSINESS HOUR']).dt.total_seconds() / 60)
    df['Average Delivery Time'] = df['Average Delivery Time'].mask(df['Average Delivery Time'] < 0, 40)
              
        
        

    df = calculate_distances(df)
    
    # Add 'Cause for the delay' column from 'MESSAGES'
    df['Cause for the delay'] = df['MESSAGES']

    # Identify and categorize issues
    df['Issues'] = df.apply(categorize_issues, axis=1)
    orders_with_issues = df[df['Issues'] != ""]
    non_issue_orders = df[df['Issues'] == ""]

    # Orders with Issues: Pivot Table
    st.write("### Orders with Issues")
    issues_pivot = orders_with_issues[[
        'ID', 'BUSINESS NAME', 'BUSINESS CITY', 'DRIVER NAME', 'DISTANCE (km)', 'SUBTOTAL',
        'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
        'Driver to Business', 'Driver in Business', 'Pickup to Customer',
        'Average Delivery Time', 'Issues', 'Cause for the delay'
    ]].round(1)

    total_rows = len(issues_pivot)
    st.write(issues_pivot)
    st.write(f"Total Rows: {total_rows}")
    download_excel(issues_pivot, "orders_with_issues.xlsx")

   
    
    
    # Actual Delivery Time Analysis for Non-Issue Orders
    st.write("### Actual Delivery Time Analysis")
    non_issue_orders['HOURS'] = non_issue_orders['DELIVERY TIME'].dt.hour
    
    non_issue_pivot = non_issue_orders.pivot_table(
        index='BUSINESS CITY',
        values=[ 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
                'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
        aggfunc={
            #'STATE': 'count',
            #'DRIVER ID': 'nunique',
            'Accepted by Business': 'mean',
            'Assigned Time': 'mean',
            'Accepted by Driver': 'mean',
            'Driver to Business': 'mean',
            'Driver in Business': 'mean',
            'Pickup to Customer': 'mean',
            'Average Delivery Time': 'mean'
        },
        margins=True
    ).round(1)
    
    #non_issue_pivot.rename(columns={'STATE': 'Total Orders', 'DRIVER ID': 'Total Drivers'}, inplace=True)
    column_order = [
        'Accepted by Business', 'Assigned Time',
        'Accepted by Driver', 'Driver to Business', 'Driver in Business',
        'Pickup to Customer', 'Average Delivery Time'
    ]
    non_issue_pivot = non_issue_pivot[column_order]
    non_issue_pivot.reset_index(inplace=True)
    
    # Exclude 'Total Orders' and 'Total Drivers' from the display and downloadable file
    #non_issue_pivot_display = non_issue_pivot.drop(columns=['Total Orders', 'Total Drivers'])
    
    # Display and download the modified table
    st.write(non_issue_pivot)
    download_excel(non_issue_pivot, "actual_delivery_time_analysis.xlsx")
    
                
    
          
    
    
    # Identify and categorize issues
    df['Issues'] = df.apply(categorize_issues, axis=1)

    # Pivot Table for Total Delivery Time (Including Issue and Non-Issue Orders)
    #st.write("### Total Delivery Time (Including Issue and Non-Issue Orders)")
    total_delivery_pivot = df.pivot_table(
        index='BUSINESS CITY',
        values=[
            'STATE', 'DRIVER ID', 'Accepted by Business', 'Assigned Time',
            'Accepted by Driver', 'Driver to Business', 'Driver in Business',
            'Pickup to Customer', 'Average Delivery Time'
        ],
        aggfunc={
            'STATE': 'count',  # Total Orders
            'DRIVER ID': 'nunique',  # Total Drivers
            'Accepted by Business': 'mean',
            'Assigned Time': 'mean',
            'Accepted by Driver': 'mean',
            'Driver to Business': 'mean',
            'Driver in Business': 'mean',
            'Pickup to Customer': 'mean',
            'Average Delivery Time': 'mean'
        },
        margins=True
    ).round(1)

    # Rename columns and arrange in the desired order
    total_delivery_pivot.rename(columns={'STATE': 'Total Orders', 'DRIVER ID': 'Total Drivers'}, inplace=True)

    column_order = [
        'Total Orders', 'Total Drivers', 'Accepted by Business', 'Assigned Time',
        'Accepted by Driver', 'Driver to Business', 'Driver in Business',
        'Pickup to Customer', 'Average Delivery Time'
    ]

    total_delivery_pivot = total_delivery_pivot[column_order]

    # Reset index to include 'BUSINESS CITY' as a column in the Excel output
    total_delivery_pivot.reset_index(inplace=True)

    #st.write(total_delivery_pivot)
    #download_excel(total_delivery_pivot, "total_delivery_time.xlsx")
    
    
    
    # Identify excluded/problematic orders
    df['Issues'] = df.apply(categorize_issues, axis=1)
    df['Excluded Orders'] = df['Issues'].apply(lambda x: 1 if x != "" else 0)
    
    # Pivot table
    actual_pivot = df.pivot_table(
        index='BUSINESS CITY',
        values=['Excluded Orders', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
                'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
        aggfunc={'Excluded Orders':'sum','Accepted by Business':'mean','Assigned Time':'mean',
                 'Accepted by Driver':'mean','Driver to Business':'mean','Driver in Business':'mean',
                 'Pickup to Customer':'mean','Average Delivery Time':'mean'}
    ).round(1).reset_index()
    
    # Ensure column order
    actual_pivot = actual_pivot[['BUSINESS CITY','Excluded Orders','Accepted by Business','Assigned Time',
                                 'Accepted by Driver','Driver to Business','Driver in Business',
                                 'Pickup to Customer','Average Delivery Time']]
    
    # Sort only if numeric column is valid
    if pd.api.types.is_numeric_dtype(actual_pivot['Average Delivery Time']):
        actual_pivot = actual_pivot.sort_values(by='Average Delivery Time', ascending=True)
    
    st.write("### Actual Delivery Time Analysis (with number of problematic orders)")
    st.table(actual_pivot)
    download_excel(actual_pivot, "actual_delivery_time_analysis.xlsx")


    

    #PRE ORDER ANALYSIS
    # Ensure datetime columns are in the correct format
    df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'])  # Expected time (target time)
    df['DELIVERY HOUR'] = pd.to_datetime(df['DELIVERY HOUR'])  # Actual delivery time
    df['ACCEPTED BUSINESS HOUR'] = pd.to_datetime(df['ACCEPTED BUSINESS HOUR'])

    # Step 1: Identify Pre-orders (using the existing condition)
    df['PRE ORDERS'] = df['ACCEPTED BUSINESS HOUR'] < df['DELIVERY TIME']

    # Step 2: Calculate In Progress Time (difference between delivery hour and accepted business hour)
    df['IN PROGRESS TIME'] = (df['DELIVERY HOUR'] - df['ACCEPTED BUSINESS HOUR']).dt.total_seconds() / 60  # Time in minutes

    # Step 3: Calculate Time Difference (actual delivery vs scheduled delivery)
    df['TIME DIFFERENCE'] = (df['DELIVERY HOUR'] - df['DELIVERY TIME']).dt.total_seconds() / 60  # Time in minutes

    # Step 4: Calculate Time Deviation (absolute value of time difference)
    df['TIME DEVIATION'] = df['TIME DIFFERENCE'].abs()

    # Step 5: Add a Comment Column based on the deviation
    conditions = [
        (df['TIME DEVIATION'] <= 10),  # Within ±10 minutes
        (df['TIME DIFFERENCE'] < -10), # Early by more than 10 minutes
        (df['TIME DIFFERENCE'] > 10)   # Late by more than 10 minutes
    ]
    comments = ['On Time', 'Early', 'Late']
    df['COMMENT'] = np.select(conditions, comments, default='Unknown')

    # Step 6: Filter the DataFrame for pre-orders only
    pre_orders_df = df[df['PRE ORDERS'] == True]

    # Step 7: Rename columns with professional names
    pre_orders_df = pre_orders_df.rename(columns={
        'DELIVERY TIME': 'Expected Time',          # Time customer expects to receive the order
        'DELIVERY HOUR': 'Actual Delivery Time',   # Time when order was actually delivered
        'TIME DIFFERENCE': 'Time Difference',
        'TIME DEVIATION': 'Time Deviation'
    })

    # Convert 'Actual Delivery Time' to show only time (no date)
    pre_orders_df['Actual Delivery Time'] = pre_orders_df['Actual Delivery Time'].dt.time
    pre_orders_df['Expected Time'] = pre_orders_df['Expected Time'].dt.time

    # Step 8: Create a pivot table with the specified columns
    pivot_table = pre_orders_df.pivot_table(
        index='ID',
        values=['BUSINESS NAME', 'Expected Time', 'Actual Delivery Time', 'IN PROGRESS TIME', 'Time Difference', 'Time Deviation', 'COMMENT'],
        aggfunc='first'
    )


    # Step 10: Rearrange the columns in the specified order
    pivot_table = pivot_table[['BUSINESS NAME', 'Expected Time', 'Actual Delivery Time', 'IN PROGRESS TIME', 'Time Difference', 'Time Deviation', 'COMMENT']]

    # Step 11: Format numeric columns to one decimal place
    numeric_columns = ['IN PROGRESS TIME', 'Time Difference', 'Time Deviation']
    pivot_table[numeric_columns] = pivot_table[numeric_columns].round(1)

    # Display the pivot table
    st.write("### Pre-orders Analysis")
    st.write(pivot_table)

    # Step 12: Provide download button for the pivot table
    download_excel(pivot_table.reset_index(), "Pre_Orders_Analysis.xlsx")
                  
    
    
    
    
    # Make sure distances are calculated
    df = calculate_distances(df)
    
    # Drop rows with missing coordinates (optional)
    df_coords = df.dropna(subset=['CUSTOMER LATITUDE', 'CUSTOMER LONGITUDE'])
    
    # Let user select any business city
    business_cities = sorted(df['BUSINESS CITY'].unique())
    selected_city = st.selectbox("Select Business City for Detailed Analysis", business_cities)
    
    # Filter data for selected city
    city_data = df_coords[df_coords['BUSINESS CITY'] == selected_city]
    
    # Customer Heatmap
    st.write(f"### Customer Location Heatmap for {selected_city}")
    city_map = folium.Map(location=[-6.8018, 39.2801], zoom_start=14)
    HeatMap(city_data[['CUSTOMER LATITUDE', 'CUSTOMER LONGITUDE']].values.tolist(),
            radius=15, blur=10).add_to(city_map)
    st.components.v1.html(city_map._repr_html_(), height=600)
    
    # Pivot table for delivery analysis by distance with count of orders
    city_pivot = city_data.pivot_table(
        index='Distance Category',
        values=['Average Delivery Time','Accepted by Business','Assigned Time','Accepted by Driver',
                'Driver to Business','Driver in Business','Pickup to Customer'],
        aggfunc='mean'
    ).round(1)
    
    # Add Count of Orders column
    order_counts = city_data.groupby('Distance Category')['ID'].count()
    city_pivot['Number of Orders'] = order_counts
    
    # Display pivot table
    st.write(f"### Delivery Analysis Pivot Table for {selected_city}")
    st.table(city_pivot)
    
        
    # Average Delivery Time vs Distance Chart
    st.write(f"### Average Delivery Time vs Distance for {selected_city}")
    st.bar_chart(city_pivot['Average Delivery Time'])
    
        
    

  
    st.write("Delivery Time Categorization:")
    #st.subheader(f"--- Delivery Time Categorizatio ---")
    # Delivery Time Categorization
    explode = (0.1, 0, 0, 0, 0, 0)
    bins = [0, 40, 45, 60, 90, 119, float('inf')]
    labels = ['Excellent', 'Ideal', 'Average', 'Delayed', 'Bad', 'Worse']
    colors = sns.color_palette("deep", len(labels))
    
    # Add a new column with the delivery time categories
    df['Delivery Time Category'] = pd.cut(df['Average Delivery Time'], bins=bins, labels=labels)
    
    # Count the number of orders in each category
    category_counts = df['Delivery Time Category'].value_counts()
    
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
           startangle=140, explode=explode, colors=colors)
    ax.set_title('Distribution of Delivery Time Categories')
    plt.axis('equal')
    
    # Dynamic legend generation
    legend_labels = [f'{label} ({start}-{end} mins)' for label, start, end in zip(labels, bins[:-1], bins[1:])]
    ax.legend(legend_labels, title='Categories in minutes', loc='upper right', bbox_to_anchor=(1.5, 1))
    
    st.pyplot(fig)
    
    
    
    # Table for Delivery Categories
    results = pd.DataFrame({
        'Category': labels,
        'Range of Classification': [f'{start} - {end}' for start, end in zip(bins[:-1], bins[1:])],
    })

    # Add a column for the number of orders in each category
    results['Number of Orders'] = [category_counts.get(label, 0) for label in labels]

    # Calculate the percentage of the number of orders
    total_orders = results['Number of Orders'].sum()
    results['Percentage %'] = ((results['Number of Orders'] / total_orders) * 100).round(1)

    # Display the table of results
    st.write("Table of Delivery Time Categories:")
    st.write(results)

    # Display the download button for the delivery categories
    if st.button("Download Delivery Time Categories"):
        download_excel(results, "Delivery_Time_Categories.xlsx")
        
            
        




                
def drivers_analysis():
    st.title("Drivers Analysis 🚴")

    # Sub-navigation for daily and weekly report
    sub_nav = st.radio("Select Report Type", ["Daily Report", "Weekly Report"])

    if sub_nav == "Daily Report":
        daily_report()
    elif sub_nav == "Weekly Report":
        weekly_report()


# Daily Report Function
def daily_report():
    st.markdown("### Daily Report for Drivers")
    
    
    if st.session_state.df is None:
        st.warning("Please upload data first in Data Analysis tab.")
        return
    
    df = st.session_state.df.copy()  # consistently use df
    


    # Filter relevant rows
    df = df[df['STATE'] == 'Delivery Completed By Driver'].copy()      

    # Convert time columns to datetime
    datetime_cols = [
        'DELIVERY TIME', 'ACCEPTED BUSINESS HOUR', 'ASSIGNED HOUR',
        'ACCEPTED DRIVER HOUR', 'IN BUSINESS HOUR', 'PICKUP HOUR', 'DELIVERY HOUR'
    ]
    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime)

    # Calculate various time metrics
    time_calculations = [
        ('Accepted by Business', 'ACCEPTED BUSINESS HOUR', 'DELIVERY TIME', 0),
        ('Assigned Time', 'ASSIGNED HOUR', 'ACCEPTED BUSINESS HOUR', 3),
        ('Accepted by Driver', 'ACCEPTED DRIVER HOUR', 'ASSIGNED HOUR', 3),
        ('Driver to Business', 'IN BUSINESS HOUR', 'ACCEPTED DRIVER HOUR', 7),
        ('Driver in Business', 'PICKUP HOUR', 'IN BUSINESS HOUR', 15),
        ('Pickup to Customer', 'DELIVERY HOUR', 'PICKUP HOUR', 15),
        ('Average Delivery Time', 'DELIVERY HOUR', 'DELIVERY TIME', 40)
    ]
    for name, end, start, default in time_calculations:
        df[name] = (df[end] - df[start]).dt.total_seconds() / 60
        df[name] = df[name].mask(df[name] < 0, default)



    # 1. Number of Drivers in Each Business City
   
    total_drivers_all = df['DRIVER ID'].nunique()
    st.write("TOTAL NUMBER OF DRIVERS (All Shifts): ", total_drivers_all)

    # Extract the hour part of the timestamp
    df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'])
    df['HOURS'] = df['DELIVERY TIME'].dt.hour

    # Filter data based on selected hours
    hours_range = st.slider("Select Hours Range:", min_value=0, max_value=23, value=(0, 23))
    selected_hours = list(range(hours_range[0], hours_range[1] + 1))
    filtered_df = df[df['HOURS'].isin(selected_hours)]  # Filtered DataFrame based on selected hours
    
    # Multiselect filter for selecting business cities
    all_cities = df['BUSINESS CITY'].unique()
    selected_cities = st.multiselect('Filter by Business City:', all_cities, default=all_cities)
    
    # Apply the city filter if any city is selected
    if selected_cities:
        filtered_df = filtered_df[filtered_df['BUSINESS CITY'].isin(selected_cities)]
    
    # Calculate the total number of drivers from the filtered data
    total_drivers_filtered = filtered_df['DRIVER ID'].nunique()
    
    # Display the total number of drivers from filtered data
    st.write(f"Total Number of Drivers in Filtered Data: {total_drivers_filtered}")
    
    # Define conditions for morning and evening shifts
    morning_shift_condition = (filtered_df['HOURS'] >= 7) & (filtered_df['HOURS'] <= 15)
    evening_shift_condition = (filtered_df['HOURS'].isin([16, 17, 18, 19, 20, 21, 22, 23, 24, 1, 2]))
    
    # Create DataFrames for morning and evening shifts
    morning_shift_df = filtered_df[morning_shift_condition].copy()
    evening_shift_df = filtered_df[evening_shift_condition].copy()
    
    # Total number of drivers for morning shift
    total_drivers_morning = morning_shift_df['DRIVER ID'].nunique()
    st.write("\nTOTAL NUMBER OF DRIVERS (Morning Shift): ", total_drivers_morning)
    
    # Total number of drivers for evening shift
    total_drivers_evening = evening_shift_df['DRIVER ID'].nunique()
    st.write("TOTAL NUMBER OF DRIVERS (Evening Shift): ", total_drivers_evening)
    
    # Calculate the number of drivers and orders for each business city
    drivers_summary = filtered_df.groupby('BUSINESS CITY').agg({'DRIVER ID': 'nunique', 'ID': 'count'}).reset_index()
    drivers_summary.columns = ['BUSINESS CITY', 'Number of Drivers', 'Number of Orders']
    
    # Display the summary table for number of drivers and orders in each business city
    #st.markdown("##### Summary table for Number of Drivers and Orders in Each Business City:")
    #st.table(drivers_summary)
    
    # Add a filter button for each business city
    for index, row in drivers_summary.iterrows():
        city_name = row['BUSINESS CITY']
        filter_button = st.button(f"Show Drivers for {city_name}")
        if filter_button:
            # Filter the DataFrame to get the driver names and number of orders for the selected city
            city_data = filtered_df[filtered_df['BUSINESS CITY'] == city_name]
            city_drivers = city_data.groupby('DRIVER NAME').size().reset_index(name='Number of Orders')
            st.write(f"Drivers operating in {city_name}:")
            st.write(city_drivers)

    # 2. Top 10 Riders
    st.header("Top 10 Riders")
    top_10_riders = df.groupby('DRIVER NAME')['ID'].count().nlargest(10).reset_index()
    top_10_riders.columns = ['Driver Name', 'Number of Orders']
    st.table(top_10_riders)

 

    # 3. Driver Performance
    df = calculate_distances(df)
    st.header("Driver Performance")
    driver_performance_pivot = pd.pivot_table(df,
    index='DRIVER NAME',
    values=['STATE', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
            'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
    aggfunc={'STATE': 'count',
             'Accepted by Business': 'mean',
             'Assigned Time': 'mean',
             'Accepted by Driver': 'mean',
             'Driver to Business': 'mean',
             'Driver in Business': 'mean',
             'Pickup to Customer': 'mean',
             'Average Delivery Time': 'mean'},
    margins=True
    ).round(1)
    
    column_order = ['STATE', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
        'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time']

    # Reorder the columns in the DataFrame
    driver_performance_pivot = driver_performance_pivot[column_order]
    
    # Display the driver performance pivot table
    st.write("Driver Performance Pivot Table:")
    st.write(driver_performance_pivot)
    
    
    # Function to handle file download
    def download_excel(dataframe):
        # Write the Excel file to a buffer
        excel_buffer = BytesIO()
        dataframe.to_excel(excel_buffer, index=True)
        excel_buffer.seek(0)
        
        # Encode the Excel data as base64
        b64 = base64.b64encode(excel_buffer.read()).decode()
        
        # Create download link
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="driver_performance_metrics.xlsx">Download Excel File</a>'
        
        # Display download link
        st.markdown(href, unsafe_allow_html=True)
    
    # Display the download button
    if st.button("Download Driver Performance Metrics"):
        download_excel(driver_performance_pivot)                                           
        
        
    # Search for driver name
    search_driver_name = st.text_input("Search Driver Name:")
    
    # Initialize an empty DataFrame
    filtered_driver_performance = pd.DataFrame()
    
    # Filter the DataFrame based on the search query
    if search_driver_name:
        filtered_driver_performance = driver_performance_pivot[
            driver_performance_pivot.index.str.contains(search_driver_name, case=False, na=False)
        ]
    
    # Round the values in the DataFrame to 1 decimal place
    filtered_driver_performance = filtered_driver_performance.round(1)
    
    # Display the filtered results
    st.write("Driver Performance Summary:")
    st.table(filtered_driver_performance)
    
    
    df = calculate_distances(df)
    # Dropdown for selecting a driver
    unique_driver_names = df['DRIVER NAME'].dropna().unique()
    selected_driver_name = st.selectbox("Select Driver Name:", unique_driver_names)
                           

    if selected_driver_name:
        # Filter dataframe by selected driver
        selected_driver_df = df[df['DRIVER NAME'] == selected_driver_name]
        
        if not selected_driver_df.empty:
            st.write(f"Orders for {selected_driver_name}:")
            
            # Display the relevant columns, including the newly added 'Distance (km)' and 'Distance Category'
            st.write(selected_driver_df[['ID', 'BUSINESS NAME', 'DELIVERY DATE', 'DISTANCE (km)', 'Distance Category',
                                         'Accepted by Business', 'Assigned Time', 'Accepted by Driver', 
                                         'Driver to Business', 'Driver in Business', 'Pickup to Customer', 
                                         'Average Delivery Time']])
            
            
            
            
            # Create a pivot table by Distance Category
            pivot_df = selected_driver_df.pivot_table(
                index='Distance Category',
                values=['ID', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver', 
                        'Driver to Business', 'Driver in Business', 'Pickup to Customer', 
                        'Average Delivery Time'],
                aggfunc={'ID': 'count', 
                         'Accepted by Business': 'mean', 
                         'Assigned Time': 'mean', 
                         'Accepted by Driver': 'mean', 
                         'Driver to Business': 'mean', 
                         'Driver in Business': 'mean', 
                         'Pickup to Customer': 'mean', 
                         'Average Delivery Time': 'mean'},
                margins=True
            ).rename(columns={'ID': 'Number of Orders', 
                              'Average Delivery Time': 'Average Delivery Time (mins)'})
            
            # Reorder the columns
            column_order = ['Number of Orders', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver', 
                            'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time (mins)']
            
            # Apply the new column order to the pivot table
            pivot_df = pivot_df[column_order]
            
            # Display the pivot table with the desired column order
            st.write("Driver Performance by Distance Category:")
            st.write(pivot_df)
            
            
            # Pie chart for number of orders by Distance Category
            order_counts = pivot_df['Number of Orders'].drop('All')  # Remove the "All" row for total orders
            labels = order_counts.index
            sizes = order_counts.values
            
            # Create the pie chart
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(labels)))
            ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
            
            # Display the pie chart
            st.header("Orders by Distance Category (Pie Chart)")
            st.pyplot(fig)


            # Assuming the data for the selected driver has been filtered and stored in 'selected_driver_df'
            # Make sure the relevant columns are available
            heat_data_list = selected_driver_df[['CUSTOMER LATITUDE', 'CUSTOMER LONGITUDE']].dropna().values.tolist()
            
            # Step 3: Create a Base Map
            # Center the map around an appropriate location (e.g., driver's deliveries or a fixed location)
            # Here, we use a central location for the driver's deliveries; adjust as needed
            m = folium.Map(location=[-6.8018, 39.2801], zoom_start=14)
            
            # Step 4: Add HeatMap Layer
            # Ensure heatmap visibility with appropriate parameters
            HeatMap(heat_data_list, radius=15, blur=10, max_zoom=1).add_to(m)
            
            # Step 5: Display the map (if running in a Streamlit environment)
            # Save the map as an HTML file to be embedded or downloaded
            map_filename = "driver_heatmap.html"
            m.save(map_filename)
            
            # Display the map (in Streamlit)
            st.header("Customer Location Heatmap for the Selected Driver")
            st.components.v1.html(m._repr_html_(), height=600)
            
            # Optionally, provide a download link for the heatmap
            def download_map(filename):
                with open(filename, 'r') as file:
                    map_data = file.read()
                b64 = base64.b64encode(map_data.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="{filename}">Download the Heatmap</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            # Button to download the heatmap HTML
            if st.button(f"Download Heatmap for {selected_driver_name}"):
                download_map(map_filename)

            
            # Function to download Excel file
            def download_excel(dataframe, filename="selected_driver_performance.xlsx"):
                excel_buffer = BytesIO()
                dataframe.to_excel(excel_buffer, index=True)
                excel_buffer.seek(0)
                b64 = base64.b64encode(excel_buffer.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
                st.markdown(href, unsafe_allow_html=True)
    
            # Download button for the filtered data
            if st.button(f"Download Pivot Table for {selected_driver_name}"):
                download_excel(selected_driver_df)

    # 4. Driver Working Hours
    st.header("Driver Working Hours")
    df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'], format='%H:%M:%S')
    df['HOUR'] = df['DELIVERY TIME'].dt.hour
    hour_bins = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    hour_labels = [f'{hour:02d}' for hour in range(24)]
    df['HOUR_CATEGORY'] = pd.cut(df['HOUR'], bins=hour_bins, labels=hour_labels, right=False)



    pivot_df = df.pivot_table(values='ID',
                              index='DRIVER NAME',
                              columns='HOUR_CATEGORY',
                              aggfunc=pd.Series.nunique,
                              fill_value=0)

    # Creating the 'TotalOrders' column
    pivot_df['TotalOrders'] = pivot_df.sum(axis=1)

    # Sorting the DataFrame based on the 'TotalOrders' column in descending order
    sorted_pivot_df = pivot_df.sort_values(by='TotalOrders', ascending=True)

    st.write("driver working hours table:")
    st.write(sorted_pivot_df)

    # Add a button to download the pivot table as an Excel file
    if st.button("Download Drivers Pivot Table"):
        sorted_pivot_df.to_excel('drivers_pivot_table.xlsx', sheet_name='Sheet1', index=True)
    


    # Creating the initial pivot table for bussy hours
    pivot_df2 = df.pivot_table(values='ID',
                              index='DRIVER NAME',
                              columns='HOUR_CATEGORY',
                              aggfunc=pd.Series.nunique,
                              fill_value=0)

    # specified hours (18, 19, 20)
    filtered_pivot_df = pivot_df2[['17','18', '19', '20', '21']]

    # Creating the 'TotalOrders' column
    filtered_pivot_df['TotalOrders'] = filtered_pivot_df.sum(axis=1)

    # Sorting the DataFrame based on the 'TotalOrders' column in descending order
    sorted_pivot_df = filtered_pivot_df.sort_values(by='TotalOrders', ascending=True)

    st.write("bussy hours- (18, 19, 20, 21, 22) :")
    st.write(sorted_pivot_df)

    # Add a button to download the pivot table as an Excel file
    if st.button("Download Drivers-bussy time"):
        sorted_pivot_df.to_excel('drivers_pivot-busy time.xlsx', sheet_name='Sheet1', index=True)
        
        


                
def weekly_report():
    st.markdown("### Weekly Report for Drivers")

    # File uploader
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file type and read the data
            if upload.type == 'application/vnd.ms-excel':
                df = pd.read_excel(upload, engine='openpyxl')
            else:
                df = pd.read_csv(upload)

            # Ensure all required columns are present
            required_columns = [
                'DRIVER NAME', 'ID', 'STATE', 'DELIVERY TIME', 'BUSINESS NAME', 'BUSINESS CITY'
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"The following columns are missing from the dataset: {', '.join(missing_columns)}")
                return

            # Ensure 'DELIVERY TIME' is in datetime format
            df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'], errors='coerce')
            df['DELIVERY DATE'] = df['DELIVERY TIME'].dt.date

            # Filter relevant rows
            df = df[df['STATE'] == 'Delivery Completed By Driver'].copy()



            # Filter by Business City
            cities = df['BUSINESS CITY'].dropna().unique()
            selected_city = st.sidebar.selectbox("Select Business City:", ['All'] + list(cities))
            if selected_city != 'All':
                df = df[df['BUSINESS CITY'] == selected_city]

            # Filter by Driver Name
            drivers = df['DRIVER NAME'].dropna().unique()
            selected_driver = st.sidebar.selectbox("Select Driver Name:", ['All'] + list(drivers))
            if selected_driver != 'All':
                df = df[df['DRIVER NAME'] == selected_driver]

            # Calculate various time metrics
            time_calculations = [
                ('Accepted by Business', 'ACCEPTED BUSINESS HOUR', 'DELIVERY TIME', 0),
                ('Assigned Time', 'ASSIGNED HOUR', 'ACCEPTED BUSINESS HOUR', 3),
                ('Accepted by Driver', 'ACCEPTED DRIVER HOUR', 'ASSIGNED HOUR', 3),
                ('Driver to Business', 'IN BUSINESS HOUR', 'ACCEPTED DRIVER HOUR', 7),
                ('Driver in Business', 'PICKUP HOUR', 'IN BUSINESS HOUR', 15),
                ('Pickup to Customer', 'DELIVERY HOUR', 'PICKUP HOUR', 15),
                ('Average Delivery Time', 'DELIVERY HOUR', 'DELIVERY TIME', 40)
            ]
            for name, end, start, default in time_calculations:
                df[name] = (pd.to_datetime(df[end], errors='coerce') - pd.to_datetime(df[start], errors='coerce')).dt.total_seconds() / 60
                df[name] = df[name].mask(df[name] < 0, default)

            # Driver Performance Pivot Table
            st.header("Driver Performance")
            driver_performance_pivot = pd.pivot_table(
                df,
                index='DRIVER NAME',
                values=['STATE', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
                        'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
                aggfunc={
                    'STATE': 'count',
                    'Accepted by Business': 'mean',
                    'Assigned Time': 'mean',
                    'Accepted by Driver': 'mean',
                    'Driver to Business': 'mean',
                    'Driver in Business': 'mean',
                    'Pickup to Customer': 'mean',
                    'Average Delivery Time': 'mean'
                },
                margins=True
            ).round(1)

            # Add total row for sum of orders and averages for timing columns
            column_order = ['STATE', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
                            'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time']
            driver_performance_pivot = driver_performance_pivot[column_order]

            # Display the driver performance pivot table
            st.write("Driver Performance Pivot Table:")
            st.write(driver_performance_pivot)

            # Function to handle file download
            def download_excel(dataframe):
                excel_buffer = BytesIO()
                dataframe.to_excel(excel_buffer, index=True)
                excel_buffer.seek(0)
                b64 = base64.b64encode(excel_buffer.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="driver_performance_metrics.xlsx">Download Excel File</a>'
                st.markdown(href, unsafe_allow_html=True)

            if st.button("Download Driver Performance Metrics"):
                download_excel(driver_performance_pivot)


            df = calculate_distances(df)
            # Dropdown for selecting a driver
            unique_driver_names = df['DRIVER NAME'].dropna().unique()
            selected_driver_name = st.selectbox("Select Driver Name:", unique_driver_names)
                                   

            if selected_driver_name:
                # Filter dataframe by selected driver
                selected_driver_df = df[df['DRIVER NAME'] == selected_driver_name]
                
                if not selected_driver_df.empty:
                    st.write(f"Orders for {selected_driver_name}:")
                    
                    # Display the relevant columns, including the newly added 'Distance (km)' and 'Distance Category'
                    st.write(selected_driver_df[['ID', 'BUSINESS NAME', 'DELIVERY DATE', 'DISTANCE (km)', 'Distance Category',
                                                 'Accepted by Business', 'Assigned Time', 'Accepted by Driver', 
                                                 'Driver to Business', 'Driver in Business', 'Pickup to Customer', 
                                                 'Average Delivery Time']])
                    
                    
                    
                    
                    # Create a pivot table by Distance Category
                    pivot_df = selected_driver_df.pivot_table(
                        index='Distance Category',
                        values=['ID', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver', 
                                'Driver to Business', 'Driver in Business', 'Pickup to Customer', 
                                'Average Delivery Time'],
                        aggfunc={'ID': 'count', 
                                 'Accepted by Business': 'mean', 
                                 'Assigned Time': 'mean', 
                                 'Accepted by Driver': 'mean', 
                                 'Driver to Business': 'mean', 
                                 'Driver in Business': 'mean', 
                                 'Pickup to Customer': 'mean', 
                                 'Average Delivery Time': 'mean'},
                        margins=True
                    ).rename(columns={'ID': 'Number of Orders', 
                                      'Average Delivery Time': 'Average Delivery Time (mins)'})
                    
                    # Reorder the columns
                    column_order = ['Number of Orders', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver', 
                                    'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time (mins)']
                    
                    # Apply the new column order to the pivot table
                    pivot_df = pivot_df[column_order]
                    
                   # Round the numeric columns to 1 decimal place
                    pivot_df = pivot_df.round(1)
                    
                    # Display the pivot table with the desired column order
                    st.write("Driver Performance by Distance Category:")
                    st.write(pivot_df)
                    
                    
                    # Pie chart for number of orders by Distance Category
                    order_counts = pivot_df['Number of Orders'].drop('All')  # Remove the "All" row for total orders
                    labels = order_counts.index
                    sizes = order_counts.values
                    
                    # Create the pie chart
                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(labels)))
                    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
                    
                    # Display the pie chart
                    st.header("Orders by Distance Category (Pie Chart)")
                    st.pyplot(fig)


                    # Assuming the data for the selected driver has been filtered and stored in 'selected_driver_df'
                    # Make sure the relevant columns are available
                    heat_data_list = selected_driver_df[['CUSTOMER LATITUDE', 'CUSTOMER LONGITUDE']].dropna().values.tolist()
                    
                    # Step 3: Create a Base Map
                    # Center the map around an appropriate location (e.g., driver's deliveries or a fixed location)
                    # Here, we use a central location for the driver's deliveries; adjust as needed
                    m = folium.Map(location=[-6.8018, 39.2801], zoom_start=14)
                    
                    # Step 4: Add HeatMap Layer
                    # Ensure heatmap visibility with appropriate parameters
                    HeatMap(heat_data_list, radius=15, blur=10, max_zoom=1).add_to(m)
                    
                    # Step 5: Display the map (if running in a Streamlit environment)
                    # Save the map as an HTML file to be embedded or downloaded
                    map_filename = "driver_heatmap.html"
                    m.save(map_filename)
                    
                    # Display the map (in Streamlit)
                    st.header("Customer Location Heatmap for the Selected Driver")
                    st.components.v1.html(m._repr_html_(), height=600)
                    
                    # Optionally, provide a download link for the heatmap
                    def download_map(filename):
                        with open(filename, 'r') as file:
                            map_data = file.read()
                        b64 = base64.b64encode(map_data.encode()).decode()
                        href = f'<a href="data:text/html;base64,{b64}" download="{filename}">Download the Heatmap</a>'
                        st.markdown(href, unsafe_allow_html=True)
                    
                    # Button to download the heatmap HTML
                    if st.button(f"Download Heatmap for {selected_driver_name}"):
                        download_map(map_filename)

                    
                    # Function to download Excel file
                    def download_excel(dataframe, filename="selected_driver_performance.xlsx"):
                        excel_buffer = BytesIO()
                        dataframe.to_excel(excel_buffer, index=True)
                        excel_buffer.seek(0)
                        b64 = base64.b64encode(excel_buffer.read()).decode()
                        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
                        st.markdown(href, unsafe_allow_html=True)
            
                    # Download button for the filtered data
                    if st.button(f"Download Pivot Table for {selected_driver_name}"):
                        download_excel(selected_driver_df)
                        
            
            
            
                    # Group by delivery date and calculate working hours
                    working_hours_df = selected_driver_df.groupby('DELIVERY DATE').apply(
                        lambda x: (x['DELIVERY TIME'].max() - x['DELIVERY TIME'].min()).total_seconds() / 3600
                    ).reset_index(name='Hours Worked')
            
                    # Create a pivot table showing working hours per day
                    pivot_hours_df = working_hours_df.pivot_table(
                        index='DELIVERY DATE',
                        values='Hours Worked',
                        aggfunc='sum',
                        margins=True,
                        margins_name='Total'  # Adds a 'Total' row
                    )
            
                    # Display the pivot table
                    st.write(f"Actual Working Hours for {selected_driver_name}:")
                    st.write(pivot_hours_df)
            
                    # Download option for the pivot table
                    def download_hours_excel(dataframe, filename="driver_working_hours.xlsx"):
                        excel_buffer = BytesIO()
                        dataframe.to_excel(excel_buffer, index=True)
                        excel_buffer.seek(0)
                        b64 = base64.b64encode(excel_buffer.read()).decode()
                        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
                        st.markdown(href, unsafe_allow_html=True)
            
                    # Button to download the working hours data
                    if st.button(f"Download Working Hours for {selected_driver_name}"):
                        download_hours_excel(pivot_hours_df)
            
                    # Optional: Add the total hours worked to the overall summary
                    total_hours = pivot_hours_df.loc['Total', 'Hours Worked']
                    st.write(f"**Total Hours Worked by {selected_driver_name}: {total_hours:.2f} hours**")
                                    
                        
        
            # 4. Driver Working Hours
            st.header("Driver Working Hours")
            df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'], format='%H:%M:%S')
            df['HOUR'] = df['DELIVERY TIME'].dt.hour
            hour_bins = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            hour_labels = [f'{hour:02d}' for hour in range(24)]
            df['HOUR_CATEGORY'] = pd.cut(df['HOUR'], bins=hour_bins, labels=hour_labels, right=False)



            pivot_df = df.pivot_table(values='ID',
                                      index='DRIVER NAME',
                                      columns='HOUR_CATEGORY',
                                      aggfunc=pd.Series.nunique,
                                      fill_value=0)

            # Creating the 'TotalOrders' column
            pivot_df['TotalOrders'] = pivot_df.sum(axis=1)

            # Sorting the DataFrame based on the 'TotalOrders' column in descending order
            sorted_pivot_df = pivot_df.sort_values(by='TotalOrders', ascending=True)

            st.write("driver working hours table:")
            st.write(sorted_pivot_df)

            # Add a button to download the pivot table as an Excel file
            if st.button("Download Drivers Pivot Table"):
                sorted_pivot_df.to_excel('drivers_pivot_table.xlsx', sheet_name='Sheet1', index=True)
            

    
            # Creating the initial pivot table for bussy hours
            pivot_df2 = df.pivot_table(values='ID',
                                      index='DRIVER NAME',
                                      columns='HOUR_CATEGORY',
                                      aggfunc=pd.Series.nunique,
                                      fill_value=0)

            # specified hours (18, 19, 20)
            filtered_pivot_df = pivot_df2[['17','18', '19', '20', '21']]

            # Creating the 'TotalOrders' column
            filtered_pivot_df['TotalOrders'] = filtered_pivot_df.sum(axis=1)

            # Sorting the DataFrame based on the 'TotalOrders' column in descending order
            sorted_pivot_df = filtered_pivot_df.sort_values(by='TotalOrders', ascending=True)

            st.write("bussy hours- (18, 19, 20, 21, 22) :")
            st.write(sorted_pivot_df)

            # Add a button to download the pivot table as an Excel file
            if st.button("Download Drivers-bussy time"):
                sorted_pivot_df.to_excel('drivers_pivot-busy time.xlsx', sheet_name='Sheet1', index=True)
                
                

        except Exception as e:
            st.error(f"Error loading the file: {e}")



         
            

def rejected_orders():
    st.title("REJECTED ORDERS SUMMARY")  
    
    if st.session_state.df is None:
        st.warning("Please upload data first in Data Analysis tab.")
        return
    
    df = st.session_state.df.copy()  # consistently use df
    
                  
    # Rejected orders
    rejected_orders = df.loc[df['STATE'] == 'Rejected'][['ID', 'BUSINESS NAME','PRODUCTS', 'SUBTOTAL','MESSAGES']]
    st.write("Rejected Orders:")
    
    # Create a multiselect widget to filter columns
    show_data = st.multiselect('Filter:', df.columns, default=['ID', 'BUSINESS NAME','PRODUCTS', 'SUBTOTAL','MESSAGES'])
    
    # Display the DataFrame with selected columns for rejected orders
    st.dataframe(rejected_orders[show_data], use_container_width=True)
    
    # Function to download rejected orders summary
    def download_excel(dataframe):
        # Write the Excel file to a buffer
        excel_buffer = BytesIO()
        dataframe.to_excel(excel_buffer, index=False)  # Index is False to exclude index column
        excel_buffer.seek(0)
        
        # Encode the Excel data as base64
        b64 = base64.b64encode(excel_buffer.read()).decode()
        
        # Create download link
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="rejected_orders_summary.xlsx">Download Excel File</a>'
        
        # Display download link
        st.markdown(href, unsafe_allow_html=True)
    
    # Display the download button for rejected orders
    if st.button("Download Rejected Orders Summary"):
        download_excel(rejected_orders)  
        
    # Failed orders
    failed_orders = df.loc[df['STATE'] == 'Delivery Failed By Driver'][['ID', 'BUSINESS NAME','PRODUCTS', 'SUBTOTAL','MESSAGES']]
    st.write("Failed Orders:")  
    
    # Display the DataFrame with selected columns for failed orders
    st.dataframe(failed_orders[show_data], use_container_width=True)     
    
    # Function to download failed orders summary
    def download_excel_failed(dataframe):
        # Write the Excel file to a buffer
        excel_buffer = BytesIO()
        dataframe.to_excel(excel_buffer, index=False)  # Index is False to exclude index column
        excel_buffer.seek(0)
        
        # Encode the Excel data as base64
        b64 = base64.b64encode(excel_buffer.read()).decode()
        
        # Create download link
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="failed_orders_summary.xlsx">Download Excel File</a>'
        
        # Display download link
        st.markdown(href, unsafe_allow_html=True)
    
    # Display the download button for failed orders
    if st.button("Download Failed Orders Summary"):
        download_excel_failed(failed_orders)    
    
    # Add a text input for search query
    search_query = st.text_input("Search by Order ID or Business Name:")
    
    # Initialize an empty DataFrame for filtered results
    filtered_orders = pd.DataFrame()
    
    # Filter orders based on search query
    if search_query:
        filtered_orders = rejected_orders[
            (rejected_orders['ID'].astype(str).str.contains(search_query, case=False)) |
            (rejected_orders['BUSINESS NAME'].str.contains(search_query, case=False))
        ]
        if not filtered_orders.empty:
            st.write("Filtered Orders:")
            st.write(filtered_orders)
        else:
            st.write("No matching orders found.")
            


if __name__ == "__main__":
    main()

if st.checkbox("By"):
    st.success("lusekelo2035")

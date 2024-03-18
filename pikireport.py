# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 01:29:43 2024

@author: USER
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def set_style():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] > 
        
        .main {
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
            background-color: #f4f4f4;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
            overflow-y: auto;
        }
        .main:hover {
            transform: scale(1.02);
        }
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
    
    
    
def data_analysis():
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])
    
    if upload is not None:
        try:
            # Check the file type and read the data
            if upload.type == 'application/vnd.ms-excel':
                data = pd.read_excel(upload, engine='openpyxl')
            else:
                data = pd.read_csv(upload)
               
            # Convert DELIVERY TIME to datetime and extract hour
            data['DELIVERY TIME'] = pd.to_datetime(data['DELIVERY TIME'])
            data['HOURS'] = data['DELIVERY TIME'].dt.hour

            # Filter data based on selected hours
            hours_range = st.slider("Select Hours Range:", min_value=0, max_value=23, value=(0, 23))
            selected_hours = list(range(hours_range[0], hours_range[1] + 1))
            filtered_df = data[data['HOURS'].isin(selected_hours)]
            
            # Display filtered data
            #st.write("Filtered df:")
            #st.write(filtered_df)
    
            # Data analysis options
            analysis_options = [
                "Summary table for Order status",
                "Number of Restaurants in Each Business City",
                "Customer Ordering Platform",
                "Top Customers"
            ]
            
            # Radio button to select the option within data analysis
            selected_option = st.sidebar.radio("Data Analysis Options", analysis_options)
            
            # Based on the selected option, display the corresponding information
            if selected_option == "Summary table for Order status":
                # Create the summary table for STATE
                state_summary = filtered_df['STATE'].value_counts().reset_index()
                state_summary.columns = ['STATE', 'Count']
                total_orders = filtered_df.shape[0]
                total_row = pd.DataFrame({'STATE': ['TOTAL ORDERS'], 'Count': [total_orders]})
                state_summary = pd.concat([total_row, state_summary], ignore_index=True)
    
                st.markdown("##### Summary table for Order status:")
                st.table(state_summary)
                
                
                 # Group orders by business city
                orders_by_city = data.groupby('BUSINESS CITY')
                
                
                for city_name, city_orders in orders_by_city:
                    # Group orders by state
                    state_counts = city_orders['STATE'].value_counts()
                    total_orders = len(city_orders)
                    
                    # Display an expander
                    with st.expander(f"{city_name}"):
                        st.write(f"###### Orders for {city_name} = ({total_orders} orders)")
                                               
                        st.columns(5, gap='small')  
                        
                        # Iterate through each state within the current city
                        for state, count in state_counts.items():
                            st.info(f"###### {state}")
                            st.metric(label="Total Orders", value=f"{count}")
                
                
               # based on status
                state_counts = data['STATE'].value_counts()
                total_orders = len(data)
                
                # Display the summary table
                st.markdown("### Summary table for Order status:")
                st.columns(5, gap='small')  # Divide the layout into 5 columns
                
                # Iterate through each state
                for state, count in state_counts.items():
                    with st.expander(f"{state} ({count} orders)"):
                        st.info(f"##### {state}")
                        st.metric(label="Total Orders", value=f"{count}")
                        
                        # Group orders by business city
                        orders_by_city = data[data['STATE'] == state].groupby('BUSINESS CITY').size().reset_index(name='Number of Orders')
                        
                        # Display summary of orders by business city
                        st.markdown("#### Orders by Business City:")
                        st.table(orders_by_city)
                                                 
                        
                
                def download_excel(dataframe):
                    # Write the Excel file to a buffer
                    excel_buffer = BytesIO()
                    dataframe.to_excel(excel_buffer, index=False)  # Index is False to exclude index column
                    excel_buffer.seek(0)
                    
                    # Encode the Excel data as base64
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    
                    # Create download link
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="order_status_summary.xlsx">Download Excel File</a>'
                    
                    # Display download link
                    st.markdown(href, unsafe_allow_html=True)
                
                # Display the download button
                if st.button("Download Order Status Summary"):
                    download_excel(state_summary)     
                    
    
                # Create pivot table 1
                pivot_df = filtered_df.pivot_table(index='BUSINESS CITY', columns='STATE', values='ID', aggfunc='count', margins=True).round(0)
                pivot_df.fillna(0, inplace=True)
    
                st.write("Pivot Table 1: SUMMARY OF ALL ORDERS STATUS BASED ON ALL BUSINESS CITIES")
                st.write(pivot_df)
    
                # Create pivot table 2
                pivot_df2 = filtered_df.pivot_table(index='BUSINESS CITY', values='ID', aggfunc='count', margins=False)
                pivot_df2.fillna(0, inplace=True)
                
                # Display pivot table 2 as a bar plot
                plt.figure(figsize=(12, 6))
                plt.barh(pivot_df2.index, pivot_df2['ID'], color='skyblue')
                plt.title("Number of Orders by Business City")
                plt.xlabel("Number of Orders")
                plt.ylabel("Business City")
                plt.grid(axis="x", linestyle="--", alpha=0.7)
                plt.tight_layout()
                st.pyplot(plt)
    
            elif selected_option == "Number of Restaurants in Each Business City":
                # Number of restaurants in each business city
                restaurant_counts = filtered_df[['BUSINESS NAME', 'BUSINESS CITY']].drop_duplicates().groupby('BUSINESS CITY').size().reset_index(name='Number of Restaurants')
                st.write("Number of Restaurants in Each Business City:")
                st.write(restaurant_counts)
    
                # Display restaurant counts as a bar plot
                plt.figure(figsize=(10, 6))
                sns.barplot(x='Number of Restaurants', y='BUSINESS CITY', data=restaurant_counts, palette="Blues_d")
                plt.title("Number of Restaurants in Each Business City")
                plt.xlabel("Number of Restaurants")
                plt.ylabel("Business City")
                plt.tight_layout()
                st.pyplot(plt)
    
            elif selected_option == "Customer Ordering Platform":
                # Customer ordering platform distribution
                platform_counts = filtered_df['CREATE_FROM'].value_counts().reset_index()
                platform_counts.columns = ['Platform', 'Count']
    
                st.write("Customer Ordering Platform:")
                st.write(platform_counts)
    
                # Display platform distribution as a pie chart
                plt.figure(figsize=(8, 8))
                plt.pie(platform_counts['Count'], labels=platform_counts['Platform'], autopct='%1.1f%%', startangle=140)
                plt.title("Customer Ordering Platform Distribution")
                plt.tight_layout()
                st.pyplot(plt)
    
            elif selected_option == "Top Customers":
                # Top customers by count of orders
                top_customers = filtered_df.groupby(['CUSTOMER EMAIL', 'CUSTOMER NAME']).size().reset_index(name='Order Count').sort_values(by='Order Count', ascending=False).head(10)
    
                st.write("Top Customers by Count of Orders:")
                st.write(top_customers)
    
                # Display top customers as a bar plot
                plt.figure(figsize=(10, 6))
                sns.barplot(y='CUSTOMER NAME', x='Order Count', data=top_customers, palette="viridis")
                plt.title("Top Customers by Count of Orders")
                plt.xlabel("Order Count")
                plt.ylabel("Customer Name")
                plt.tight_layout()
                st.pyplot(plt)
    
        except Exception as e:
            st.write("An error occurred:", e)

        

def delivery_time():
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file type and read accordingly
            if upload.type == 'application/vnd.ms-excel':
                df = pd.read_excel(upload, engine='openpyxl')
            else:
                df = pd.read_csv(upload)

            # Stage 1: Filter data for completed deliveries
            df2 = df[df['STATE'] == 'Delivery Completed By Driver'].copy()
            
                        
            df2['DELIVERY TIME'] = pd.to_datetime(df2['DELIVERY TIME'])
            df2['ACCEPTED BUSINESS HOUR'] = pd.to_datetime(df2['ACCEPTED BUSINESS HOUR'])
            df2['ASSIGNED HOUR'] = pd.to_datetime(df2['ASSIGNED HOUR'])
            df2['ACCEPTED DRIVER HOUR'] = pd.to_datetime(df2['ACCEPTED DRIVER HOUR'])
            df2['IN BUSINESS HOUR'] = pd.to_datetime(df2['IN BUSINESS HOUR'])
            df2['PICKUP HOUR'] = pd.to_datetime(df2['PICKUP HOUR'])
            df2['DELIVERY HOUR'] = pd.to_datetime(df2['DELIVERY HOUR'])

# Calculate time differences in minutes using df2 and df['ASSIGNED HOURS']
            df2['Accepted by Business'] = (df2['ACCEPTED BUSINESS HOUR'] - df2['DELIVERY TIME']).dt.total_seconds() / 60
            df2['Assigned Time'] = (df2['ASSIGNED HOUR'] - df2['DELIVERY TIME']).dt.total_seconds() / 60
            df2['Accepted by Driver'] = (df2['ACCEPTED DRIVER HOUR'] - df2['ASSIGNED HOUR']).dt.total_seconds() / 60
            df2['Driver to Business'] = (df2['IN BUSINESS HOUR'] - df2['ACCEPTED DRIVER HOUR']).dt.total_seconds() / 60
            df2['Driver in Business'] = (df2['PICKUP HOUR'] - df2['IN BUSINESS HOUR']).dt.total_seconds() / 60
            df2['Pickup to Customer'] = (df2['DELIVERY HOUR'] - df2['PICKUP HOUR']).dt.total_seconds() / 60
            df2['Average Delivery Time'] = (df2['DELIVERY HOUR'] - df2['DELIVERY TIME']).dt.total_seconds() / 60

# Handle negative values as specifie

            # Handle negative values as specified using df2
            df2['Accepted by Business'] = df2['Accepted by Business'].mask(df2['Accepted by Business'] < 0, 2)
            df2['Accepted by Business'] = df2['Accepted by Business'].mask(df2['Accepted by Business'] > 60, 60)
            
            df2['Assigned Time'] = df2['Assigned Time'].mask(df2['Assigned Time'] < 0, 3 )
            df2['Assigned Time'] = df2['Assigned Time'].mask(df2['Assigned Time'] > 30, 30)
            
            df2['Accepted by Driver'] = df2['Accepted by Driver'].mask(df2['Accepted by Driver'] < 0, 10)
            df2['Accepted by Driver'] = df2['Accepted by Driver'].mask(df2['Accepted by Driver'] > 60, 60)
            
            df2['Driver to Business'] = df2['Driver to Business'].mask(df2['Driver to Business'] < 0, 3)
            df2['Driver to Business'] = df2['Driver to Business'].mask(df2['Driver to Business'] > 60, 60)
            
            df2['Driver in Business'] = df2['Driver in Business'].mask(df2['Driver in Business'] < 0, 15)
            df2['Driver in Business'] = df2['Driver in Business'].mask(df2['Driver in Business'] > 90, 90)
            
            df2['Pickup to Customer'] = df2['Pickup to Customer'].mask(df2['Pickup to Customer'] < 0, 15)
            df2['Pickup to Customer'] = df2['Pickup to Customer'].mask(df2['Pickup to Customer'] > 90, 90)
            
            df2['Average Delivery Time'] = df2['Average Delivery Time'].mask(df2['Average Delivery Time'] < 0, 40)
            df2['Average Delivery Time'] = df2['Average Delivery Time'].mask(df2['Average Delivery Time'] > 120, 120)


            # Define the options for delivery time analysis
            delivery_time_options = [
                "Delivery Time Metrics",
          
                "Delivery Time by Drivers"
            ]
        
            # Radio button to select the option within delivery time analysis
            selected_option = st.sidebar.radio("Delivery Time Analysis Options", delivery_time_options)
        
            # Based on the selected option, display the corresponding information
            if selected_option == "Delivery Time Metrics":


                df2['DELIVERY TIME'] = pd.to_datetime(df2['DELIVERY TIME'])
                df2['HOURS'] = df2['DELIVERY TIME'].dt.hour
                                               
                                             
                pivot_table_df2 = df2.pivot_table(
                    index='BUSINESS CITY',
                    values=['STATE', 'DRIVER ID', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
                            'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
                    aggfunc={'STATE': 'count',
                             'DRIVER ID': 'nunique',
                             'Accepted by Business': 'mean',
                             'Assigned Time': 'mean',
                             'Accepted by Driver': 'mean',
                             'Driver to Business': 'mean',
                             'Driver in Business': 'mean',
                             'Pickup to Customer': 'mean',
                             'Average Delivery Time': 'mean'},
                    margins=True
                ).round(1)
                
                # Rename columns if necessary
                pivot_table_df2.rename(columns={'STATE': 'Total Orders', 'DRIVER ID': 'Total Drivers'}, inplace=True)
                
                # Reorder the columns if necessary
                column_order = ['Total Orders', 'Total Drivers', 'Accepted by Business', 'Assigned Time',
                                'Accepted by Driver', 'Driver to Business', 'Driver in Business', 'Pickup to Customer',
                                'Average Delivery Time']
                
                pivot_table_df2 = pivot_table_df2[column_order]
                
                st.write("Table of Delivery Time Metrics:")
                st.write(pivot_table_df2)
                
                # Function to handle file download
                def download_excel(dataframe):
                    # Write the Excel file to a buffer
                    excel_buffer = BytesIO()
                    dataframe.to_excel(excel_buffer, index=True)
                    excel_buffer.seek(0)
                    
                    # Encode the Excel data as base64
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    
                    # Create download link
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="delivery_time_metrics.xlsx">Download Excel File</a>'
                    
                    # Display download link
                    st.markdown(href, unsafe_allow_html=True)
                
                # Display the download button
                if st.button("Download Delivery Time Metrics"):
                    download_excel(pivot_table_df2)
                    
                    

                    
                #pivot Hours
                pivot_table_hours = df2.pivot_table(
                    index='HOURS',  # Set the index to the 'HOURS' column
                    values=['STATE', 'DRIVER ID', 'Accepted by Business', 'Assigned Time', 'Accepted by Driver',
                            'Driver to Business', 'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
                    aggfunc={'STATE': 'count',
                             'DRIVER ID': 'nunique',
                             'Accepted by Business': 'mean',
                             'Assigned Time': 'mean',
                             'Accepted by Driver': 'mean',
                             'Driver to Business': 'mean',
                             'Driver in Business': 'mean',
                             'Pickup to Customer': 'mean',
                             'Average Delivery Time': 'mean'},
                    margins=True
                ).round(1)
                
                # Rename columns 
                pivot_table_hours.rename(columns={'STATE': 'Total Orders', 'DRIVER ID': 'Total Drivers'}, inplace=True)
                
                # Reorder the columns 
                column_order = ['Total Orders', 'Total Drivers', 'Accepted by Business', 'Assigned Time',
                                'Accepted by Driver', 'Driver to Business', 'Driver in Business', 'Pickup to Customer',
                                'Average Delivery Time']
                
                pivot_table_hours = pivot_table_hours[column_order]
                
                st.write("Pivot Table of Delivery Time Metrics by Hours:")
                st.write(pivot_table_hours)
                                                     
            
            
                explode = (0.1, 0, 0, 0, 0, 0)
                bins = [0, 40, 45, 60, 90, 119, float('inf')]
                labels = ['Excellent', 'ideal', 'average', 'Delayed', 'Bad', 'Worse']
                colors = sns.color_palette("deep", len(labels))
                
                # Add a new column with the delivery time categories
                df2['Delivery Time Category'] = pd.cut(df2['Average Delivery Time'], bins=bins, labels=labels)
                
                # Count the number of orders in each category
                category_counts = df2['Delivery Time Category'].value_counts()
                
                # Create a pie chart
                #st.pyplot(plt.figure(figsize=(8, 8)))
                plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
                        startangle=140, explode=explode, colors=colors)
                plt.title('Distribution of Delivery Time Categories')
                plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
                
                legend_labels = labels
                
                # Manually set the legend labels and their positions
                plt.legend(legend_labels, title='Categories in minutes', loc='upper right', bbox_to_anchor=(1.5, 1))
                plt.tight_layout()
                # Show the pie chart
                st.pyplot(plt)
            
            
               # TABLE FOR DELIVERY CATEGORIES
                results = pd.DataFrame({
                    'Category': labels,
                    'Range of Classification': [f'{start} - {end}' for start, end in zip(bins[:-1], bins[1:])],
                })
            
                # Add a column for the number of orders in each category
                results['Number of Orders'] = [category_counts[label] for label in labels]
            
                # Calculate the percentage of the number of orders
                total_orders = results['Number of Orders'].sum()
                results['Percentage %'] = ((results['Number of Orders'] / total_orders) * 100).round(1)
            
                # Display the table of results
                st.write("Table of Delivery Time Categories:")
                st.write(results)
                
                # Function to handle file download
                def download_excel(dataframe):
                    # Write the Excel file to a buffer
                    excel_buffer = BytesIO()
                    dataframe.to_excel(excel_buffer, index=True)
                    excel_buffer.seek(0)
                    
                    # Encode the Excel data as base64
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    
                    # Create download link
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="(Table of Delivery Time Categories.xlsx">Download Excel File</a>'
                    
                    # Display download link
                    st.markdown(href, unsafe_allow_html=True)
                
                # Display the download button
                if st.button("Download Delivery Time Categories "):
                    download_excel(results)                
            

                
            elif selected_option == "Delivery Time by Drivers":
                
                                
                driver_performance_pivot = pd.pivot_table(df2,
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
                
                if st.button("Download Driver Performance Metrics", key='download_driver_performance_button'):
                 driver_performance_pivot.to_excel('driver_performance_metrics.xlsx', sheet_name='Driver_Performance', index=True)
              
                 
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
                
                unique_driver_names = df2['DRIVER NAME'].unique()
                
                # Create a dropdown select box for choosing the driver name
                selected_driver_name = st.selectbox("Select Driver Name:", unique_driver_names)
                
                # Filter the DataFrame based on the selected driver name
                filtered_orders = df2[df2['DRIVER NAME'] == selected_driver_name]
                
                # Display the list of orders for the selected driver
                if not filtered_orders.empty:
                    st.write("Orders for Selected Driver:")
                    st.write(filtered_orders[['ID', 'BUSINESS NAME', 'Accepted by Business', 'Assigned Time', 
                                              'Accepted by Driver', 'Driver to Business', 'Driver in Business', 
                                              'Pickup to Customer', 'Average Delivery Time']])
                
                    # Display total number of orders
                    st.write(f"Total Orders: {len(filtered_orders)}")
                else:
                    st.write("No orders found for the selected driver.")
                
                          
                # Display delivery time by drivers
                st.write("Delivery Time by Drivers:")
                # Add your code here to display delivery time by drivers
                

                            
        except Exception as e:
            st.write("Error loading the file. Please make sure it's a valid CSV or Excel file.")
            st.write(e)
            
            
def drivers_analysis():
    # Function to display drivers analysis content
    st.write("Drivers Analysis Content")
    
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file type and read accordingly
            if upload.type == 'application/vnd.ms-excel':
                df = pd.read_excel(upload, engine='openpyxl')
            else:
                df = pd.read_csv(upload)
                
                df2 = df[df['STATE'] == 'Delivery Completed By Driver'].copy()
                
                df2['DELIVERY TIME'] = pd.to_datetime(df2['DELIVERY TIME'])
                df2['ACCEPTED BUSINESS HOUR'] = pd.to_datetime(df2['ACCEPTED BUSINESS HOUR'])
                df2['ASSIGNED HOUR'] = pd.to_datetime(df2['ASSIGNED HOUR'])
                df2['ACCEPTED DRIVER HOUR'] = pd.to_datetime(df2['ACCEPTED DRIVER HOUR'])
                df2['IN BUSINESS HOUR'] = pd.to_datetime(df2['IN BUSINESS HOUR'])
                df2['PICKUP HOUR'] = pd.to_datetime(df2['PICKUP HOUR'])
                df2['DELIVERY HOUR'] = pd.to_datetime(df2['DELIVERY HOUR'])

    # Calculate time differences in minutes using df2 and df['ASSIGNED HOURS']
                df2['Accepted by Business'] = (df2['ACCEPTED BUSINESS HOUR'] - df2['DELIVERY TIME']).dt.total_seconds() / 60
                df2['Assigned Time'] = (df2['ASSIGNED HOUR'] - df2['DELIVERY TIME']).dt.total_seconds() / 60
                df2['Accepted by Driver'] = (df2['ACCEPTED DRIVER HOUR'] - df2['ASSIGNED HOUR']).dt.total_seconds() / 60
                df2['Driver to Business'] = (df2['IN BUSINESS HOUR'] - df2['ACCEPTED DRIVER HOUR']).dt.total_seconds() / 60
                df2['Driver in Business'] = (df2['PICKUP HOUR'] - df2['IN BUSINESS HOUR']).dt.total_seconds() / 60
                df2['Pickup to Customer'] = (df2['DELIVERY HOUR'] - df2['PICKUP HOUR']).dt.total_seconds() / 60
                df2['Average Delivery Time'] = (df2['DELIVERY HOUR'] - df2['DELIVERY TIME']).dt.total_seconds() / 60

    # Handle negative values as specifie

                # Handle negative values as specified using df2
                df2['Accepted by Business'] = df2['Accepted by Business'].mask(df2['Accepted by Business'] < 0, 2)
                df2['Accepted by Business'] = df2['Accepted by Business'].mask(df2['Accepted by Business'] > 60, 60)
                
                df2['Assigned Time'] = df2['Assigned Time'].mask(df2['Assigned Time'] < 0, 3 )
                df2['Assigned Time'] = df2['Assigned Time'].mask(df2['Assigned Time'] > 30, 30)
                
                df2['Accepted by Driver'] = df2['Accepted by Driver'].mask(df2['Accepted by Driver'] < 0, 10)
                df2['Accepted by Driver'] = df2['Accepted by Driver'].mask(df2['Accepted by Driver'] > 60, 60)
                
                df2['Driver to Business'] = df2['Driver to Business'].mask(df2['Driver to Business'] < 0, 3)
                df2['Driver to Business'] = df2['Driver to Business'].mask(df2['Driver to Business'] > 60, 60)
                
                df2['Driver in Business'] = df2['Driver in Business'].mask(df2['Driver in Business'] < 0, 15)
                df2['Driver in Business'] = df2['Driver in Business'].mask(df2['Driver in Business'] > 90, 90)
                
                df2['Pickup to Customer'] = df2['Pickup to Customer'].mask(df2['Pickup to Customer'] < 0, 15)
                df2['Pickup to Customer'] = df2['Pickup to Customer'].mask(df2['Pickup to Customer'] > 90, 90)
                
                df2['Average Delivery Time'] = df2['Average Delivery Time'].mask(df2['Average Delivery Time'] < 0, 40)
                df2['Average Delivery Time'] = df2['Average Delivery Time'].mask(df2['Average Delivery Time'] > 120, 120)
    
    
    
    # Define the options for drivers analysis
            drivers_analysis_options = [
                "Number of Drivers in Each Business City",
                "Driver Performance",
                "Driver Working Hours",
                "Top 10 Riders"
            ]
        
            # Radio button to select the option within drivers analysis
            selected_option = st.sidebar.radio("Drivers Analysis Options", drivers_analysis_options)
            
            # Based on the selected option, display the corresponding information
            if selected_option == "Number of Drivers in Each Business City":
                # Total number of drivers for the entire dataset
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
                st.markdown("##### Summary table for Number of Drivers and Orders in Each Business City:")
                st.table(drivers_summary)
                
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

                
            elif selected_option == "Driver Performance":
                
                driver_performance_pivot = pd.pivot_table(df2,
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
                
                unique_driver_names = df2['DRIVER NAME'].unique()
                
                
                
                # Create a dropdown select box for choosing the driver name
                selected_driver_name = st.selectbox("Select Driver Name:", unique_driver_names)
                
                # Filter the DataFrame based on the selected driver name
                filtered_orders = df2[df2['DRIVER NAME'] == selected_driver_name]
                
                # Display the list of orders for the selected driver
                if not filtered_orders.empty:
                    st.write("Orders for Selected Driver:")
                    st.write(filtered_orders[['ID', 'BUSINESS NAME', 'Accepted by Business', 'Assigned Time', 
                                              'Accepted by Driver', 'Driver to Business', 'Driver in Business', 
                                              'Pickup to Customer', 'Average Delivery Time']])
                
                    # Display total number of orders
                    st.write(f"Total Orders: {len(filtered_orders)}")
                else:
                    st.write("No orders found for the selected driver.")
                # Display the driver performance pivot table
              
                
            elif selected_option == "Driver Working Hours":
                
                # Creating the initial pivot table
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
                    
            
               
                
            elif selected_option == "Top 10 Riders":
                
                #NUMBER OF ORDERS
                pivot_df6 = df.pivot_table(index='DRIVER NAME', values='ID',
                                   aggfunc='count', margins=False).round(1).sort_values(by='ID', ascending=False).head(10)
            
                # Fill any missing values with 0 in the pivot table
                pivot_df6.fillna(0, inplace=True)
                st.write("Top 10 Riders Pivot Table:")
                st.write(pivot_df6)
                
                
                # Creating a barplot for the top 10 riders
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(y=pivot_df6.index, x='ID', data=pivot_df6, dodge=False, ax=ax)
                sns.set(style="whitegrid")
                plt.xticks(rotation=90)
                plt.title('RIDER PERFORMANCE')
                plt.tight_layout()
                st.pyplot(fig)
                
                # calculate the average "Accepted by Driver" time and count of orders
                driver_stats = df2.groupby('DRIVER NAME').agg(
                    AvgAcceptedTime=('Accepted by Driver', 'mean'),
                    TotalOrdersCompleted=('ID', 'count')
                )
                
                # Sort the drivers by average accepted time in ascending order and take the top 10
                top_15_drivers = driver_stats.nsmallest(15, 'AvgAcceptedTime').round(2)
                
                # Display driver names, average accepted time, and total orders completed
                st.write("Driver perfomance based on average order accepted time:")
                top_15_drivers[['AvgAcceptedTime', 'TotalOrdersCompleted']]    
            
            
        except Exception as e:
            st.write("Error loading the file. Please make sure it's a valid CSV or Excel file.")
            st.write(e)
            
            

def rejected_orders():
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file 
            if upload.type == 'application/vnd.ms-excel':
                df = pd.read_excel(upload, engine='openpyxl')
            else:
                df = pd.read_csv(upload)
                
            st.write("Data loaded successfully")
              
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
                    
        except Exception as e:
            st.write("Error loading the file. Please make sure it's a valid CSV or Excel file.")
            st.write(e)

if __name__ == "__main__":
    main()

if st.checkbox("By"):
    st.success("lusekelo2035")

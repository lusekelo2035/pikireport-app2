# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 01:29:43 2024

@author: USER
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    st.title("PIKI DELIVERY COMPANY")
    st.subheader("DaILY operation  report Analysis")

    # Navigation sidebar
    nav_page = st.sidebar.radio("Navigation", ["Data Analysis", "Delivery Time","drivers analysis"])

    if nav_page == "Data Analysis":
        data_analysis()
    elif nav_page == "Delivery Time":
        delivery_time()
    elif nav_page == "drivers analysis":
        drivers_analysis()
    


def data_analysis():
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file type and read accordingly
            if upload.type == 'application/vnd.ms-excel':
                data = pd.read_excel(upload, engine='openpyxl')
            else:
                data = pd.read_csv(upload)
                
                # Now you can use the 'data' DataFrame for further analysis
                st.write("Data loaded successfully")
                
            data['STATE'] = data['STATE'].replace({'Delivery Failed By Driver': 'FAILED ORDERS', 'Completed': 'PICKUP ORDERS'})
            data['STATE'] = data['STATE'].str.upper()

            # Create the summary table for STATE
            state_summary = data['STATE'].value_counts().reset_index()
            state_summary.columns = ['STATE', 'Count']
            total_orders = data.shape[0]
            total_row = pd.DataFrame({'STATE': ['TOTAL ORDERS'], 'Count': [total_orders]})
            state_summary = pd.concat([total_row, state_summary], ignore_index=True)

            st.write("Summary Table for Order STATUS:")
            st.write(state_summary.to_string(index=False, header=False, col_space=0))

                      
                     
            # Create pivot table 1
            pivot_df = data.pivot_table(index='BUSINESS CITY', columns='STATE', values='ID', aggfunc='count', margins=True).round(0)
            pivot_df.fillna(0, inplace=True)

            st.write("Pivot Table 1: SUMMARY OF ALL ORDERS STATUS BASED ON ALL BUSINESS CITIES")
            st.write(pivot_df)

            # Create pivot table 2
            pivot_df2 = data.pivot_table(index='BUSINESS CITY', values='ID', aggfunc='count', margins=False)
            pivot_df2.fillna(0, inplace=True)
            
                     
            # Create pie plot
            explode = (0.1, 0, 0, 0, 0, 0.1, 0.1, 0, 0.1, 0, 0, 0.3)
            plt.figure(figsize=(8, 8))
            plt.pie(pivot_df2['ID'], labels=pivot_df2.index, autopct='%1.1f%%', startangle=140, explode=explode)
            plt.title('Distribution of Orders by Business Cities')

            st.pyplot(plt)
            
            
            # number of restaurants
            unique_restaurants = data[['BUSINESS NAME', 'BUSINESS CITY']].drop_duplicates()
            city_restaurant_counts = unique_restaurants.groupby('BUSINESS CITY').size().reset_index(name='Number of Restaurants')
                             
            st.write("Number of Restaurants in Each Business City:")
            st.write(city_restaurant_counts)
            
            plt.figure(figsize=(12, 6))
            plt.barh(city_restaurant_counts['BUSINESS CITY'], city_restaurant_counts['Number of Restaurants'], color='skyblue')
            plt.title("Number of Restaurants in Each Business City")
            plt.xlabel("Number of Restaurants")
            plt.ylabel("Business City")
            plt.grid(axis="x", linestyle="--", alpha=0.7)
            
            for index, row in city_restaurant_counts.iterrows():
                plt.annotate(f'{int(row["Number of Restaurants"])}',
                             xy=(row["Number of Restaurants"], row["BUSINESS CITY"]),
                             xytext=(3, 0),
                             textcoords="offset points",
                             ha='left', va='center')
            
            plt.tight_layout()
            st.pyplot(plt)
            
            # Created from
            pivot_df1 = data.pivot_table(index='CREATE_FROM', values='ID', aggfunc='count', margins=True)
            pivot_df1.fillna(0, inplace=True)
            

            # Pie plot for 'orderingapp' and 'WEBSITE'
            orderingapp = data.loc[data['CREATE_FROM'] == 'orderingapp'].count()[0]
            WEBSITE = data.loc[data['CREATE_FROM'] == 'WEBSITE'].count()[0]
            
            plt.figure(figsize=(8, 5))
            plt.style.use('ggplot')
            
            labels = ['orderingapp', 'WEBSITE']
            colors = ['#abcdef', 'b']
            
            plt.pie([orderingapp, WEBSITE], labels=labels, colors=colors, autopct='%.2f %%')
            plt.title('Customer Ordering Platform')
            st.pyplot(plt)
            
            # Create bussiness data
            pivot_df5 = data.pivot_table(index='BUSINESS NAME', values='ID', aggfunc='count', margins=False).round(1).sort_values(by='ID', ascending=False).head(10)
            pivot_df5.fillna(0, inplace=True)

            st.write("Pivot Table :RESTAURANT WITH HIGH NUMBER OF ORDERS")
            st.write(pivot_df5)

           # Create bar plot using Seaborn
            plt.figure(figsize=(10, 6))
            sns.barplot(y=pivot_df5.index, x='ID', data=pivot_df5, dodge=False)
            sns.set(style="whitegrid")
            plt.xticks(rotation=90)
            plt.title('RESTAURANT WITH HIGH NUMBER OF ORDERS')
            plt.tight_layout()

            st.pyplot(plt)

           # Create pivot table 8
            pivot_df8 = data.pivot_table(index=['CUSTOMER EMAIL','CUSTOMER NAME'], values='ID', aggfunc='count', margins=False).round(1).sort_values(by='ID', ascending=False).head(10)
          
            pivot_df8.fillna(0, inplace=True)

            st.write("Pivot Table :CUSTOMER WITH HIGH NUMBER OF ORDERS")
            st.write(pivot_df8)

            # Create bar plot using Seaborn
            y_index = pivot_df8.index.get_level_values('CUSTOMER NAME')

            plt.figure(figsize=(10, 6))
            sns.barplot(y=y_index, x='ID', data=pivot_df8.reset_index(), dodge=False)
            sns.set(style="whitegrid")
            plt.xticks(rotation=90)
            plt.xlabel('Count of ID')
            plt.title('Top Customers by Count of ID')
            plt.tight_layout()

            st.pyplot(plt)
            
               
           
          
                      
            
            
            
          
            # Add your data analysis code here

        except Exception as e:
            st.write("Error loading the file. Please make sure it's a valid CSV or Excel file.")
            st.write(e)


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

            # Stage 4: Create the pivot table
            pivot_table_df2 = df2.pivot_table(
                index='BUSINESS CITY',
                values=['Accepted by Business', 'Assigned Time', 'Accepted by Driver', 'Driver to Business',
                        'Driver in Business', 'Pickup to Customer', 'Average Delivery Time'],
                aggfunc='mean',
                margins=True
            ).round(1)

            pivot_table_df2 = pivot_table_df2[['Accepted by Business', 'Assigned Time', 'Accepted by Driver', 'Driver to Business',
                                               'Driver in Business', 'Pickup to Customer', 'Average Delivery Time']]

            st.write("Table of Delivery Time Metrics:")
            st.write(pivot_table_df2)

            # Add a button to download the delivery time pivot table as an Excel file
            if st.button("Download Delivery Time Metrics"):
                pivot_table_df2.to_excel('delivery_time_metrics.xlsx', sheet_name='Sheet1', index=True)
                
                df2['DELIVERY TIME'] = pd.to_datetime(df2['DELIVERY TIME'])
            df2['HOURS'] = df2['DELIVERY TIME'].dt.hour

            # Define conditions for morning and evening shifts
            morning_shift_condition = (df2['HOURS'] >= 7) & (df2['HOURS'] <= 16)
            evening_shift_condition = (df2['HOURS'].isin([17, 18, 19, 20, 21, 22, 23, 24, 1, 2]))

            # Create DataFrames for morning and evening shifts
            morning_shift_df = df2[morning_shift_condition].copy()
            evening_shift_df = df2[evening_shift_condition].copy()

            # Stage 7: Pivot Tables for Morning and Evening Shifts
            appearance_names = {
                'STATE': 'Total Number of Orders',
                'DRIVER ID': 'Total Number of Drivers',
            }

            # Pivot table for morning shift
            morning_shift_pivot = morning_shift_df.pivot_table(
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

            # Rename columns for morning shift
            morning_shift_pivot.rename(columns=appearance_names, inplace=True)

            # Reorder the columns for morning shift
            column_order_morning = ['Total Number of Orders', 'Total Number of Drivers', 'Accepted by Business', 'Assigned Time',
                                     'Accepted by Driver', 'Driver to Business', 'Driver in Business', 'Pickup to Customer',
                                     'Average Delivery Time']
            morning_shift_pivot = morning_shift_pivot[column_order_morning]

            # Pivot table for evening shift
            evening_shift_pivot = evening_shift_df.pivot_table(
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

            # Rename columns for evening shift
            evening_shift_pivot.rename(columns=appearance_names, inplace=True)

            # Reorder the columns for evening shift
            column_order_evening = ['Total Number of Orders', 'Total Number of Drivers', 'Accepted by Business', 'Assigned Time',
                                     'Accepted by Driver', 'Driver to Business', 'Driver in Business', 'Pickup to Customer',
                                     'Average Delivery Time']
            evening_shift_pivot = evening_shift_pivot[column_order_evening]

            # Display the pivot tables for morning and evening shifts
            # Display the pivot tables for morning and evening shifts
            st.write("Morning Shift Pivot Table:")
            st.write(morning_shift_pivot)
            
            # Add a button to download the morning shift pivot table as an Excel file
            if st.button("Download Morning Shift Metrics", key='morning_shift_download_button'):
                morning_shift_pivot.to_excel('morning_shift_metrics.xlsx', sheet_name='Morning_Shift', index=True)
            
            st.write("\nEvening Shift Pivot Table:")
            st.write(evening_shift_pivot)
            
            # Add a button to download the evening shift pivot table as an Excel file
            if st.button("Download Evening Shift Metrics", key='evening_shift_download_button'):
                evening_shift_pivot.to_excel('evening_shift_metrics.xlsx', sheet_name='Evening_Shift', index=True)
               
                        # Stage 8: Distribution of Delivery Time Categories
            explode = (0.1, 0, 0, 0, 0, 0)
            bins = [0, 40, 45, 60, 90, 119, float('inf')]
            labels = ['Excellent', 'Average', 'Ideal', 'Delayed', 'Bad', 'Worse']
            colors = sns.color_palette("deep", len(labels))
            
            # Add a new column with the delivery time categories
            df2['Delivery Time Category'] = pd.cut(df2['Average Delivery Time'], bins=bins, labels=labels)
            
            # Count the number of orders in each category
            category_counts = df2['Delivery Time Category'].value_counts()
            
            # Create a pie chart
            st.pyplot(plt.figure(figsize=(8, 8)))
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

            # Add a button to download the results table as an Excel file
            if st.button("Download Delivery Time Categories"):
                results.to_excel('delivery_time_categories.xlsx', sheet_name='Sheet1', index=False)
               
            

        except Exception as e:
            st.write("Error loading the file. Please make sure it's a valid CSV or Excel file.")
            st.write(e)
            
            
def drivers_analysis():
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file type and read accordingly
            if upload.type == 'application/vnd.ms-excel':
                df = pd.read_excel(upload, engine='openpyxl')
            else:
                df = pd.read_csv(upload)

            # Total number of drivers for the entire dataset
            total_drivers_all = df['DRIVER ID'].nunique()
            st.write("TOTAL NUMBER OF DRIVERS (All Shifts): ", total_drivers_all)

            # Extract the hour part of the timestamp
            df['DELIVERY TIME'] = pd.to_datetime(df['DELIVERY TIME'])
            df['HOURS'] = df['DELIVERY TIME'].dt.hour

            # Define conditions for morning and evening shifts
            morning_shift_condition = (df['HOURS'] >= 7) & (df['HOURS'] <= 17)
            evening_shift_condition = (df['HOURS'].isin([18, 19, 20, 21, 22, 23, 24, 1, 2]))

            # Create DataFrames for morning and evening shifts
            morning_shift_df = df[morning_shift_condition].copy()
            evening_shift_df = df[evening_shift_condition].copy()

            # Total number of drivers for morning shift
            total_drivers_morning = morning_shift_df['DRIVER ID'].nunique()
            st.write("\nTOTAL NUMBER OF DRIVERS (Morning Shift): ", total_drivers_morning)

            # Total number of drivers for evening shift
            total_drivers_evening = evening_shift_df['DRIVER ID'].nunique()
            st.write("TOTAL NUMBER OF DRIVERS (Evening Shift): ", total_drivers_evening)

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

            st.write("Sorted Pivot Table:")
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
            filtered_pivot_df = pivot_df2[['18', '19', '20', '21', '22']]

            # Creating the 'TotalOrders' column
            filtered_pivot_df['TotalOrders'] = filtered_pivot_df.sum(axis=1)

            # Sorting the DataFrame based on the 'TotalOrders' column in descending order
            sorted_pivot_df = filtered_pivot_df.sort_values(by='TotalOrders', ascending=True)

            st.write("Sorted Pivot Table:")
            st.write(sorted_pivot_df)

            # Add a button to download the pivot table as an Excel file
            if st.button("Download Drivers-bussy time"):
                sorted_pivot_df.to_excel('drivers_pivot-busy time.xlsx', sheet_name='Sheet1', index=True)
                
            
           
                        
            
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
            
            rejected_orders = df.loc[df['STATE'] == 'Rejected'][['ID', 'BUSINESS NAME', 'MESSAGES']]
            st.write("Rejected Orders:")
            st.write(rejected_orders)

           # Add a button to download rejected orders to Excel
            if st.button("Download Rejected Orders"):
               rejected_orders.to_excel('rejected_orders.xlsx', sheet_name='Sheet1', index=False)

            

        
       
            # Group the data by driver and calculate the average "Accepted by Driver" time and count of orders
             
            
            
        except Exception as e:
            st.write("Error loading the file. Please make sure it's a valid CSV or Excel file.")
            st.write(e)

                  
           
              

if __name__ == "__main__":
    main()

if st.checkbox("By"):
    st.success("lusekelo")
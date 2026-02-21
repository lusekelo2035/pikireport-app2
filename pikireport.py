import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from sklearn.cluster import KMeans
import random


# Main Streamlit app code
def main():
    st.title("Restaurant and Customer Location Visualization")

    # File upload section
    upload = st.file_uploader("Upload Your Dataset (In CSV or Excel Format)", type=["csv", "xlsx"])

    if upload is not None:
        try:
            # Check the file type and read the data
            if upload.type == 'application/vnd.ms-excel':
                data = pd.read_excel(upload, engine='openpyxl')
            else:
                data = pd.read_csv(upload)

            # Interface layout
            st.sidebar.title("Navigation")
            page = st.sidebar.radio("Go to", ("Restaurant Locations", "Customer Locations"))

            if page == "Restaurant Locations":
                st.header("Restaurant Locations Map")

                # Create a Folium map centered around Dar es Salaam
                m = folium.Map(location=[-6.7924, 39.2083], zoom_start=11)
                
                # Define a dictionary to assign colors to each business city
                city_colors = {
                    "City Centre": "blue",
                    "Mikocheni": "green",
                    "Upanga": "red",
                    "masaki": "pink"
                    # Add more cities and corresponding colors as needed
                }

                # Add markers for each restaurant location
                for index, row in data.iterrows():
                    if not pd.isnull(row['BUSINESS LATITUDE']) and not pd.isnull(row['BUSINESS LONGITUDE']):
                        city = row['BUSINESS CITY']
                        color = city_colors.get(city, "black")  # Default to black if city not found in dictionary
                        folium.Marker([row['BUSINESS LATITUDE'], row['BUSINESS LONGITUDE']],
                                      popup=row['BUSINESS NAME'] + f" (ID: {row['ID']})",  # Include ID in popup
                                      icon=folium.Icon(color=color)).add_to(m)
    
                # Display the map using folium_static
                folium_static(m)
            
                # Show restaurant details
                st.subheader("Select a Restaurant to View Details:")
                selected_restaurant = st.selectbox("Restaurant", data['BUSINESS NAME'].unique())
                restaurant_data = data[data['BUSINESS NAME'] == selected_restaurant]
                st.write(f"Name: {selected_restaurant}")
                st.write(f"Number of Orders: {len(restaurant_data)}")

                # Dropdown to search for a restaurant and preview customer distribution
                st.subheader("Preview Customer Distribution at a Restaurant:")
                selected_restaurant_dropdown = st.selectbox("Select Restaurant", data['BUSINESS NAME'].unique())
                customer_data = data[data['BUSINESS NAME'] == selected_restaurant_dropdown]
            
                # Create a Folium map centered around the selected restaurant
                m_customer = folium.Map(location=[customer_data['BUSINESS LATITUDE'].iloc[0], customer_data['BUSINESS LONGITUDE'].iloc[0]], zoom_start=13)
            
                # Add markers for each customer location at the selected restaurant
                for index, row in customer_data.iterrows():
                    if not pd.isnull(row['CUSTOMER LATITUDE']) and not pd.isnull(row['CUSTOMER LONGITUDE']):
                        folium.Marker([row['CUSTOMER LATITUDE'], row['CUSTOMER LONGITUDE']],
                                      popup=row['CUSTOMER NAME']).add_to(m_customer)
            
                # Display the map using folium_static
                folium_static(m_customer)

            elif page == "Customer Locations":

                # Interface layout
                st.header("Customer Locations Map")
    
                # Create a Folium map centered around Dar es Salaam
                m = folium.Map(location=[-6.7924, 39.2083], zoom_start=11)
    
                # Add markers for each customer location
                for index, row in data.iterrows():
                    if not pd.isnull(row['CUSTOMER LATITUDE']) and not pd.isnull(row['CUSTOMER LONGITUDE']):
                        folium.Marker([row['CUSTOMER LATITUDE'], row['CUSTOMER LONGITUDE']],
                                      popup=row['CUSTOMER NAME']).add_to(m)
    
                # Display the map using folium_static
                folium_static(m)
    
                # Multiselect widget to filter clusters
                st.sidebar.header("Filter Clusters")
                clusters = st.sidebar.multiselect("Select Clusters", list(range(30)), list(range(30)))
    
                if clusters:
                    # Extract customer location coordinates
                    customer_locations = data[['CUSTOMER LATITUDE', 'CUSTOMER LONGITUDE']].dropna()
    
                    # Perform K-means clustering
                    kmeans = KMeans(n_clusters=30, random_state=42)
                    kmeans.fit(customer_locations)
                    data['Cluster'] = kmeans.predict(customer_locations)
    
                    # Create a Folium map centered around Dar es Salaam
                    m_cluster = folium.Map(location=[-6.7924, 39.2083], zoom_start=11)
    
                    # Define colors for clusters
                    cluster_colors = {i: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for i in range(30)}
    
                    # Add markers for each customer location with cluster coloring
                    for index, row in data.iterrows():
                        if not pd.isnull(row['CUSTOMER LATITUDE']) and not pd.isnull(row['CUSTOMER LONGITUDE']) and row['Cluster'] in clusters:
                            cluster_color = cluster_colors[row['Cluster']]
                            folium.Marker([row['CUSTOMER LATITUDE'], row['CUSTOMER LONGITUDE']],
                                          popup=row['CUSTOMER NAME'],
                                          icon=folium.Icon(color=cluster_color)).add_to(m_cluster)
    
                    # Display the map using folium_static
                    folium_static(m_cluster)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    
    #api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZGVsaXZlcnlhcGkucGlraS5jby50eiIsImF1ZCI6Imh0dHBzOlwvXC9kZWxpdmVyeWFwaS5waWtpLmNvLnR6IiwiaWF0IjoxNzA4NjA3ODgwLCJuYmYiOjE3MDg2MDc4ODAsImp0aSI6MjQ3ODR9.unjoo_0qMqUDJWKdrh819pRQsJYls05fyUIlx-v6u0c"

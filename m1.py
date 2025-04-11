import streamlit as st
import main

# Set the page title
st.header("Efficient Traffic Management System")
st.title("Login Page")

# Define hardcoded credentials (for demo purposes)
USERNAME = "admin"
PASSWORD = "1234"

# Create input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Add a "Login" button
if st.button("Login"):
    if username == USERNAME and password == PASSWORD:
        st.success("Login successful!")
        # Add the logic for redirection or showing the main app here
        st.write("Welcome to the Traffic Management System!")
        main.main("HW.jpg")
        main.main("image1.jpg")
        main.main("ROAD-ARTICLE2.jpg")
        main.main("image1.jpg")
    else:
        st.error("Invalid username or password. Please try again.")

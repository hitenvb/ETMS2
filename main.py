import vd
import vehicle_count_reader as reader
import streamlit as st
#Integrate CCTV capture by importing module over here


def adjust_green_signal_time(vehicle_count):
    base_green_time = 3  # Base green time in seconds
    vehicle_multiplier = 2  # Green time increases by 2 seconds per vehicle
    
    green_time = base_green_time + (vehicle_count * vehicle_multiplier)
    if(green_time>45):      #Handling the upper limit for green signal time
        return 45
    return green_time

def main(image_path):
    try:
        vd.logic(image_path)
        vehicle_count = reader.read_latest_vehicle_count("vehicle_log.csv")
        if vehicle_count < 0:
            print("Invalid vehicle count in the file. Please ensure the count is a non-negative integer.")
            return
        
        green_time = adjust_green_signal_time(vehicle_count)
        st.write("Adjusted Green Signal Time:", green_time, "seconds")
    except (ValueError, FileNotFoundError):
        print("Error reading vehicle count from file.")

# if __name__ == "__main__":
#     main()

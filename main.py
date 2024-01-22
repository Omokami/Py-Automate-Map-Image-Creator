import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
from glob import glob
import shutil

# Load environment variables
load_dotenv()
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')

# Initialize tkinter window
root = tk.Tk()
root.title("Map Screenshot Generator")

# Set the window size
root.geometry("300x300")

# Global variables
CSV_FILES = []

# Function to browse and select a specific CSV file
def browse_csv():
    global CSV_FILES
    selected_file = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if selected_file:
        CSV_FILES = [selected_file]

# Function to get user input for MAP_WIDTH, MAP_HEIGHT, and zoom
def get_user_input():
    global MAP_WIDTH, MAP_HEIGHT, ZOOM, TIME_DELAY, CSV_FILES
    width_input = width_entry.get()
    height_input = height_entry.get()
    zoom_input = zoom_entry.get()
    delay_input = delay_entry.get()
    
    if not width_input or not height_input or not zoom_input or not delay_input:
        messagebox.showwarning("Input Required", "Please enter values for Map Width, Map Height, Zoom Level, and Time Delay.")
        return

    try:
        MAP_WIDTH = int(width_input)
        MAP_HEIGHT = int(height_input)
        ZOOM = int(zoom_input)
        TIME_DELAY = float(delay_input)
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid input. Please enter valid integers for width, height, zoom and a number for delay.")
        return

    if not CSV_FILES:
        CSV_FILES = glob('csv/*.csv')
        if not CSV_FILES:
            messagebox.showinfo("No CSV Files", "No CSV files found in 'csv' folder. Exiting.")
            root.quit()

def move_csv_files():
    csv_files_to_move = glob('csv/*.csv')
    for csv_file in csv_files_to_move:
        os.makedirs('csv_done', exist_ok=True)
        destination_path = os.path.join('csv_done', os.path.basename(csv_file))
        shutil.move(csv_file, destination_path)

def start_processing():
    get_user_input()
    if CSV_FILES:
        root.quit()
        process_addresses()
        move_csv_files()
        messagebox.showinfo("CSV Files Moved", "All CSV files have been moved to 'csv_done' folder.")

# Create tkinter labels, entry fields, and buttons for user input
width_label = tk.Label(root, text="Map Width:", font=("Arial", 14))
width_label.pack()
width_entry = tk.Entry(root, font=("Arial", 14))
width_entry.pack()

height_label = tk.Label(root, text="Map Height:", font=("Arial", 14))
height_label.pack()
height_entry = tk.Entry(root, font=("Arial", 14))
height_entry.pack()

zoom_label = tk.Label(root, text="Zoom Level:", font=("Arial", 14))
zoom_label.pack()
zoom_entry = tk.Entry(root, font=("Arial", 14))
zoom_entry.pack()

delay_label = tk.Label(root, text="Time Delay (sec):", font=("Arial", 14))
delay_label.pack()
delay_entry = tk.Entry(root, font=("Arial", 14))
delay_entry.pack()

browse_button = tk.Button(root, text="Browse CSV", font=("Arial", 14), command=browse_csv)
browse_button.pack()

run_button = tk.Button(root, text="Run", font=("Arial", 14), command=start_processing)
run_button.pack()

root.mainloop()

MAPBOX_STYLE_ID = "mapbox://styles/saschanohles/clrixnqws00nb01qq10h5c9mr"
image_names = []

def geocode_address(address):
    endpoint = "https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    params = {"access_token": MAPBOX_ACCESS_TOKEN, "limit": 1}
    response = requests.get(endpoint.format(address=address), params=params)
    data = response.json()

    if response.status_code == 200 and data.get("features"):
        location = data["features"][0]["geometry"]["coordinates"]
        return location
    else:
        print(f"Geocoding failed for address: {address}")
        return None

def create_map_html(location):
    with open("map.html", "w") as f:
        f.write(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Display a map on a webpage</title>
                <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
                <link href="https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.css" rel="stylesheet">
                <script src="https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.js"></script>
                <style>
                    body {{ margin: 0; padding: 0; }}
                    #map {{ position: absolute; top: 0; bottom: 0; width: {MAP_WIDTH}px; height: {MAP_HEIGHT}px; }}
                </style>
            </head>
            <body>
                <div id="map"></div>
                <script>
                    mapboxgl.accessToken = '{MAPBOX_ACCESS_TOKEN}';
                    const map = new mapboxgl.Map({{
                        style: '{MAPBOX_STYLE_ID}',
                        container: 'map',
                        center: {location},
                        zoom: {ZOOM}
                    }});
                </script>
            </body>
            </html>
        """)

def capture_map_screenshot(address, screenshot_filename):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={MAP_WIDTH},{MAP_HEIGHT}")
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)

    location = geocode_address(address)
    if location:
        create_map_html(location)
        driver.get("file://" + os.path.join(os.getcwd(), "map.html"))
        time.sleep(TIME_DELAY)
        os.makedirs('map images', exist_ok=True)
        driver.save_screenshot(os.path.join('map images', screenshot_filename))
        driver.quit()
        os.remove("map.html")

def process_addresses():
    addresses = []
    for csv_file in CSV_FILES:
        with open(csv_file, mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            for row in reader:
                image_names.append(row[0].split(";")[0])
                address = f"{row[0].split(';')[1]}, {row[1]}"
                addresses.append(address)

    for i, address in enumerate(addresses):
        screenshot_filename = f"{image_names[i]}.png"
        capture_map_screenshot(address, screenshot_filename)

def process_csv_folder():
    global CSV_FILES
    CSV_FILES = glob('csv/*.csv')
    if not CSV_FILES:
        print("No new CSV files found. Checking again after 1 second.")
        return False
    else:
        process_addresses()
        move_csv_files()
        print("Processed all CSV files. Checking for new files after 1 second.")
        return True

if __name__ == "__main__":
    start_processing()
    while True:
        if not process_csv_folder():
            time.sleep(1)

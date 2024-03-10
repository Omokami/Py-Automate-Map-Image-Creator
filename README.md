# Automate Map Image Creation from CSV Data

## Overview

The Map Screenshot Generator is a Python-based application designed to automate the process of creating map images based on addresses listed in CSV files. Utilizing the Mapbox API for geocoding and map rendering, this tool is ideal for users who need to generate visual representations of multiple locations efficiently. The application features a simple GUI for user input and processes CSV files to create map images, which are saved automatically.

## Video Preview

[![Video Preview](https://github.com/DevRex-0201/Project-Images/blob/main/video%20preview/Py-Automate-Map-Image-Creator.png)](https://drive.google.com/file/d/1xIcAe6KGHZ6pfhMZrk-b1DOV0ybj0V4X/view?usp=drive_link)

Click on the image above to watch a video demonstration of Automate Map Image Creation from CSV Data.

## Features

- **Automated Map Image Creation**: Converts address data from CSV files into map images.
- **User-Friendly Interface**: Simple GUI for easy operation and configuration.
- **Customizable Map Dimensions**: Allows setting map width, height, and zoom level.
- **Batch Processing**: Supports processing of multiple addresses from CSV files.
- **Mapbox API Integration**: Uses Mapbox for accurate and detailed map rendering.
- **Automatic File Management**: Moves processed CSV files to a designated folder.

## Requirements

- Python 3.x
- Mapbox Access Token: Obtain from [Mapbox](https://www.mapbox.com/)
- Required Python Libraries: `os`, `time`, `requests`, `selenium`, `csv`, `tkinter`, `dotenv`, `shutil`
- Selenium WebDriver: Chrome WebDriver compatible with the installed Chrome version
- Internet Connection

## Installation

1. **Clone/Download the Repository**: Get the project files onto your local machine.
2. **Install Dependencies**:
   - Install Python 3.x from the official [Python website](https://www.python.org/downloads/).
   - Install required Python libraries by running `pip install -r requirements.txt` in the project directory.
   - Download the Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in the project folder or system path.
3. **Set Up Mapbox Access Token**:
   - Create a `.env` file in the project root.
   - Add `MAPBOX_ACCESS_TOKEN=your_access_token_here` in the `.env` file.

## Usage

1. **Start the Application**: Run the script `python map_screenshot_generator.py`.
2. **Configure Settings**:
   - Set map dimensions and zoom level in the GUI.
   - Optionally, browse and select a specific CSV file or use the default folder `csv`.
3. **Run the Process**: Click the `Run` button to start processing addresses from the CSV file(s).
4. **Access Output**:
   - Map images will be saved in the `map images` folder.
   - Processed CSV files are moved to the `csv_done` folder.

## CSV File Format

- Ensure the CSV files are in the format `Name;Address, City` (semicolon-separated values).
- Place CSV files in the `csv` folder or select them through the GUI.

## Known Limitations

- Internet speed and stability might affect the performance and accuracy of the map rendering.
- The free tier of Mapbox API has usage limits; consider upgrading for heavy usage.

## Contributing

Contributions to improve the Map Screenshot Generator are welcome. Please adhere to the following guidelines:

- Fork the repository and create a new branch for your feature or fix.
- Write clear and concise commit messages.
- Ensure compatibility with the existing codebase.
- Create a pull request with a detailed description of changes.

# Boston Data Streamlit App

This repository contains a Streamlit app for visualizing Boston crime data. The app includes various visualizations such as heatmaps and bar charts to analyze crime reports, shootings, and gun recovery data.

## Getting Started

Follow these instructions to set up a Python environment, install the necessary packages, and run the Streamlit app on your local machine.

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

### Setting Up the Environment

#### macOS

1. **Open Terminal**.

2. **Navigate to the project directory**:
   ```sh
   cd path/to/your/project
   ```

3. **Create a virtual environment**:
   ```sh
   python3 -m venv venv
   ```

4. **Activate the virtual environment**:
   ```sh
   source venv/bin/activate
   ```

#### Windows

1. **Open Command Prompt**.

2. **Navigate to the project directory**:
   ```sh
   cd path\to\your\project
   ```

3. **Create a virtual environment**:
   ```sh
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   ```sh
   .\venv\Scripts\activate
   ```

### Installing Necessary Packages

With the virtual environment activated, install the required packages using `pip`:

```sh
pip install -r requirements.txt
```


### Running the Streamlit App

With the virtual environment activated and the necessary packages installed, you can run the Streamlit app using the following command:

```sh
streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser.

### Deactivating the Virtual Environment

Once you are done working with the app, you can deactivate the virtual environment:

#### macOS and Windows

```sh
deactivate
```

## Additional Information
- If you encounter any issues, please refer to the [Streamlit documentation](https://docs.streamlit.io/)

**Data Sources**
- [Crime Incident Reports](https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system/resource/b973d8cb-eeb2-4e7e-99da-c92938efc9c0)
- [Gun Recovery](https://data.boston.gov/dataset/boston-police-department-firearm-recovery-counts)
- [Shootings](https://data.boston.gov/dataset/shootings)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This README.md file provides step-by-step instructions for setting up a Python environment, installing necessary packages, and running the Streamlit app on both macOS and Windows. It also includes additional information and a license section.
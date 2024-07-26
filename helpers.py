import pandas as pd
import geopandas as gpd
import os
import shutil


table_to_keywords = { # find_destination_table() should work EVEN if number of tables changes, or if new key words are added
    "VPHF_Reports": ["VPHF"], # VPHF_#9.txt
    "VSECOM_Reports": ["VSECOM"],  # VSECOM_#9.txt
    "Soil_Tests": ["SoilTest"], # CURCSoilTestResults2018-2024.csv
    "Weather_Reports": ["Hourly Data for Freeville"], # B1_Hourly Data for Freeville, NY - [id=fre newa, lat=42.4975, lon=-76.2998].csv
    "Crop_Management": ["CropManagement"], # A1_CropManagementFotF_2023.xlsx
    "Yield_Reports": ["clean_yield"], # CURC_silage_clean_yield_2017-2023.csv
    "Hexagon_Grids": ["FieldsHexgrids"], # CURCFieldsHexgrids.geojson
    "Field_Grids": ["boundary"] # CURC22_boundary.shp
}

def find_destination_table(filename): # File Type -> Database Table
    for table in table_to_keywords.keys(): # Table_Name
        for keyword in table_to_keywords[table]:
            if keyword in filename:
                return table
    raise Exception("No Database Destination.")

def read_file(filepath, file_type, destination_table):
    df = None # Placeholder

    if file_type == "txt":
        df = pd.read_table(filepath)
    elif file_type == "csv":
        if destination_table == "Yield_Reports":
            df = pd.read_csv(filepath, dtype={"Field": "string"})
    elif file_type == "xlsx":
        df = pd.read_excel(filepath)
        df = df.replace({pd.NaT: None})
    else: # Ex. file_type == "geojson", "shp", "pdf"
        try:
            df = pd.read_table(filepath)
        except Exception as e:
            print("REREADING...")
            try:
                df = gpd.read_file(filepath, dtype = {"hexagon": "int"})
            except Exception as e:
                raise e
    
    assert df is not None, "Failed File -> DataFrame Conversion"
    print(f"Sending To: {destination_table} TABLE...")
    return df

def read_and_address_file(filepath):
    file_name = filepath.split('/')[-1] # Ex. VPHF_#1.txt
    file_type = file_name.split('.')[-1] # Ex. txt
    destination_table = find_destination_table(file_name)
    print(f"File Name: {file_name}")
    print(f"File Type: {file_type}")
    print(f"Addressed To: {destination_table} TABLE")

    return read_file(filepath, file_type, destination_table), destination_table



def list_of_files_in_folder(folder_path):
    return [f"{folder_path}{file}" for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

def move_file(filepath, destination_folder_path):
    file_name = filepath.split('/')[-1]
    destination_folder_name = destination_folder_path.split('/')[-2]

    if os.path.isdir(destination_folder_path):
        shutil.move(filepath, destination_folder_path)
        print(f"{file_name} moved to /{destination_folder_name}")
    else:
        print(f"No Such Directory: '/{destination_folder_name}'")  

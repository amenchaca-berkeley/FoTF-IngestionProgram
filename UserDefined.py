'''
Change Parameters for Program as Needed.
'''



# Define Used Directories & Subdirectories
data_collection_folder = "/Users/alanmenchaca/Downloads/DataDrop/"
data_ingested_folder = f"{data_collection_folder}Ingested/"
data_unusable_folder = f"{data_collection_folder}Unusable/"

# Ignore these files
_ignore_ = [".DS_Store"] ### MacOS creates hidden metadata file for folders sometimes ###

# Database Table : keywords in corresponding data files
# find_destination_table() should work EVEN if number of tables changes, or if new key words are added
table_to_keywords = {
    "VPHF_Reports": ["VPHF"], # VPHF_#9.txt
    "VSECOM_Reports": ["VSECOM"],  # VSECOM_#9.txt
    "Soil_Tests": ["SoilTest"], # CURCSoilTestResults2018-2024.csv
    "Weather_Reports": ["Hourly Data for Freeville"], # B1_Hourly Data for Freeville, NY - [id=fre newa, lat=42.4975, lon=-76.2998].csv
    "Crop_Management": ["CropManagement"], # A1_CropManagementFotF_2023.xlsx
    "Yield_Reports": ["clean_yield"], # CURC_silage_clean_yield_2017-2023.csv
    "Hexagon_Grids": ["FieldsHexgrids"], # CURCFieldsHexgrids.geojson
    "Field_Grids": ["boundary"] # CURC22_boundary.shp
}





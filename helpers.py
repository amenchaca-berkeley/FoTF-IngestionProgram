import userDefined as ud
import pandas as pd
import os
import shutil

def find_destination_table(filename): # File Type -> Database Table
    for table in ud.table_to_keywords.keys(): # Table_Name
        for keyword in ud.table_to_keywords[table]:
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
        else:
            df = pd.read_csv(filepath, index_col=None)
    elif file_type == "xlsx":
        df = pd.read_excel(filepath)
        df = df.replace({pd.NaT: None})
    else: # Last resort
        df = pd.read_table(filepath)
    
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
        if os.path.isdir(f"{destination_folder_path}{file_name}"): 
            print("FILE ALREADY EXISTS IN DESTINATION DIRECTORY!")
            return
        shutil.move(filepath, destination_folder_path)
        print(f"{file_name} moved to /{destination_folder_name}")
    else:
        print(f"No Such Directory: '/{destination_folder_name}'")  
    




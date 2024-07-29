# Error: Missing optional dependency 'openpyxl'.  Use pip or conda to install openpyxl.
import userDefined as ud
import pandas as pd
import psycopg2 as pg4
import helpers

def main():
    # Get list of files in data collection folder (supposed to be new files)
    new_file_names = helpers.list_of_files_in_folder(ud.data_collection_folder)
    to_ingest_files = [file for file in new_file_names if file.split('/')[-1] not in ud._ignore_]

    # Ends program if no new files need to be added
    if not to_ingest_files: 
        print("No New Files")
        exit()

    # Database connection established
    conn = pg4.connect(
        dbname="postgres",
        user="postgres",
        password="0000",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    print("....................")
    print("Connection Opened!")
    print("----------------------------------------")


    for filepath in to_ingest_files:
        print("--------------------")
        try:
            # Read file as Dataframe & find its destination
            data_file_df, destination_table = helpers.read_and_address_file(filepath)

            # Get the column values from the DataFrame
            columns = data_file_df.columns.tolist()
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))

            # Iterate over DataFrame rows and insert into the table
            for index, row in data_file_df.iterrows():
                cursor.execute(f'''
                    INSERT INTO {destination_table}
                    VALUES ({placeholders});
                ''', tuple(row))

            # Commit changes to database
            conn.commit()
            print(f"Ingested: {filepath.split('/')[-1]}")
            helpers.move_file(filepath, ud.data_ingested_folder)


        except Exception as e:
            print(f"Error: {e}")
            helpers.move_file(filepath, ud.data_unusable_folder)
        print("--------------------")


    # Close connection
    cursor.close()
    conn.close()
    print("----------------------------------------")
    print("Connection Closed!")
    print("....................")



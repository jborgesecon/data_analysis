from dotenv import load_dotenv
import kagglehub
import sqlite3
import shutil
import os
import glob


load_dotenv()

# OBJECTS
path = os.path.expanduser(os.getenv('database_path'))

all_datasets = {
    'income_inequality': "soumyodippal000/global-income-inequality-analysis1820-2022",
    'inflation': "razvanmihaihanghicel/inflation-rates-by-country-and-region-19742019",
    'food_prices': "alhamomarhotaki/global-food-prices-database-wfp"
}

# # LOCAL FILES

# grab the file name to add to a DataFrame
def get_file(db, schema, table):
    file = glob.glob(f"{path}\\{db}\\{schema}\\{table}")
    return file[0]

# downloads datasets from kaggle
def kaggle_download(dataset_name, db, schema):
    """Optional Docstring"""

    destination = f"{path}\\{db}\\{schema}"
    try:
        downloaded_path = kagglehub.dataset_download(dataset_name)
        # destination = os.path.expanduser(destination_folder)
        files = glob.glob(f"{downloaded_path}\\*")

        for file in files:
            if os.path.isdir(file):
                print('Subfolders, go check')
                return None
            elif os.path.isfile(file):
                shutil.move(file, destination)
                print(f"Moved {file} to: {destination}")
            else:
                print(f"{file} is neither a file nor a directory")
                return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None


# # SQLITE

# crete connection
# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('economics.db')

# file read helper
def read_sql_file(filepath):
    with open(filepath, 'r') as file:

    # query = (f"queries\\{filename}.sql")
        return file.read()

# cursor
def run_query(filename):
    c = conn.cursor()
    c.execute(read_sql_file(f"queries\\{filename}.sql"))
    response = c.fetchall()
    conn.commit()
    conn.close()
    return response
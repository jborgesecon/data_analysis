from dotenv import load_dotenv
import sqlalchemy as sa
import kagglehub
import requests
import sqlite3
import shutil
import os
import glob


load_dotenv()

# OBJECTS
path = 'other_datasets'

all_datasets = {
    'kaggle_economics': {
        'income_inequality': "soumyodippal000/global-income-inequality-analysis1820-2022",
        'inflation': "razvanmihaihanghicel/inflation-rates-by-country-and-region-19742019",
        'food_prices': "alhamomarhotaki/global-food-prices-database-wfp"
    },
    'ptransp': {
        'viagens': "https://portaldatransparencia.gov.br/download-de-dados/viagens/{year}",
        'receitas': "https://portaldatransparencia.gov.br/download-de-dados/receitas/{year}",
        'orcamento': "https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa/{year}",
        'despesas': "https://portaldatransparencia.gov.br/download-de-dados/despesas-execucao/{year}",
        'licitacoes': "https://portaldatransparencia.gov.br/download-de-dados/licitacoes/{year}"     # 201301
    }
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

# downloads datasets from Portal da Transparencia
def ptransp_download(db, base_url, dataset_name, year):
    destination = f"{path}\\{db}"
    url = base_url.replace("{year}", str(year))

    try:
        response = requests.get(url)
        response.raise_for_status()
        zip_file_path = os.path.join(destination, f"{dataset_name}_{year}.zip")

        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(response.content)

        print(f"successfully downloaded: {zip_file_path}")

    except Exception as e:
        print(f'error in {url}: {e}')

    return

# # SQLITE

# crete connection
# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('economics.db')      # deprecated, use sqlite_conn instead

# file read helper
def read_sql_file(filepath, pd_dataframe=True):
    if pd_dataframe:
        path1 = f"queries\\{filepath}.sql"
        with open(path1, 'r') as file:
            return file.read()
    else:
        with open(filepath, 'r') as file:
            return file.read()

# cursor (deprecated, using sqlalchemy instead)
def run_query(filename):
    c = conn.cursor()
    c.execute(read_sql_file(f"queries\\{filename}.sql", False))
    response = c.fetchall()
    conn.commit()
    conn.close()
    return response


# engines

uname = os.getenv('uname')
passwd = os.getenv('passwd')
host = os.getenv('host')
port = os.getenv('port')
dbname = os.getenv('dbname')
cockroach_con_str = f"cockroachdb://{uname}:{passwd}@{host}:{port}/{dbname}"

cockroach_conn = sa.create_engine(cockroach_con_str)
sqlite_conn = sa.create_engine("sqlite:///economics.db")
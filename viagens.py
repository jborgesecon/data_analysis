import navigation as nav
import pandas as pd
import glob
import zipfile
from unidecode import unidecode


# define path and collect files
path = "other_datasets\\ptransp_viagens\\*"
files = glob.glob(path)
df = pd.DataFrame()

# for file in files:
#     print(file)

# print('\n')
# print(len(files))

# open file and add it to a pandas dataframe
for file in files:
    with zipfile.ZipFile(file, 'r') as zip_ref:
        datasets = zip_ref.namelist()
        with zip_ref.open(datasets[-1]) as my_file:
            df1 = pd.read_csv(my_file, encoding='latin1', sep=';', dtype='object')
            df = pd.concat([df, df1], ignore_index=True)
            print(f'{file}: ok!')
            # print(df.info())

# rename columns
col_remap = [
    'id_viagem',                # int
    'num_proposta',             # int
    'situacao',                 # obj
    'viagem_urgente',           # bool
    'justificativa_urgencia',   # obj
    'cod_orgao_superior',       # int
    'nome_orgao_superior',      # obj
    'cod_orgao_solicitante',    # int
    'nome_orgao_solicitante',   # obj
    'cpf_viajante',             # obj
    'nome_viajante',            # obj
    'cargo',                    # obj
    'funcao',                   # obj
    'descricao_funcao',         # obj
    'dt_inicio',                # datetime
    'dt_fim',                   # datetime
    'destinos',                 # obj
    'motivo',                   # obj
    'valor_diarias',            # float
    'valor_passagens',          # float
    'valor_devolucao',          # float
    'valor_outros_gastos'       # float
]

df.columns = col_remap


# # DATA TREATMENT

# normalize objects: all uppercase, no special characters
treated_colums1 = [
    'situacao',                 # obj
    'justificativa_urgencia',   # obj
    'nome_orgao_superior',      # obj
    'nome_orgao_solicitante',   # obj
    'cpf_viajante',             # obj
    'nome_viajante',            # obj
    'cargo',                    # obj
    'funcao',                   # obj
    'descricao_funcao',         # obj
    'destinos',                 # obj
    'motivo'                    # obj
]

def obj_normalizer(row):
    if pd.isna(row):
        return row
    try:
        normalized = unidecode(row).upper()
        return normalized
    except Exception as e:
        print(f'Error occured: {e}')
        return row

df[treated_colums1] = df[treated_colums1].map(obj_normalizer)
# print(df['destinos'].unique())
# print(df['nome_orgao_superior'].unique())

# transforming from obj to datetime
treated_colums2 = [
    'dt_inicio',                # datetime
    'dt_fim',                   # datetime
]

def date_treatment(row):
    try:
        return pd.to_datetime(row, dayfirst=True)
    except ValueError as e:
        print(f'Error on {row}: {e}')
        return row
df[treated_colums2] = df[treated_colums2].map(date_treatment)
# print(df[treated_colums2].head())

# transforming from obj to float
treated_colums3 = [
    'valor_diarias',            # float
    'valor_passagens',          # float
    'valor_devolucao',          # float
    'valor_outros_gastos'       # float
]

for col in treated_colums3:
    df[col] = df[col].str.replace(',', '.').astype(float)
print(df['valor_passagens'].sum())

treated_colums4 = [
    'id_viagem',
    'num_proposta',
    'cod_orgao_superior',
    'cod_orgao_solicitante'
]

for col in treated_colums4:
    df[col] = df[col].astype(int)

df['viagem_urgente'] = df['viagem_urgente'].map({'SIM': 1, 'NÃO': 0})
df['viagem_urgente'] = df['viagem_urgente'].astype(bool)


print(df.info())

df.to_sql('ptransp.viagens', nav.sqlite_conn, if_exists='replace')
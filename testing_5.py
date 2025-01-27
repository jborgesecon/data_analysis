import pandas as pd
import glob
import zipfile


path = "other_datasets\\ptransp_viagens\\*"
files = glob.glob(path)
df = pd.DataFrame()

# for file in files:
#     print(file)

# print('\n')
# print(len(files))

# open file and add it to a pandas dataframe
# for file in files:
with zipfile.ZipFile(files[-1], 'r') as zip_ref:
    datasets = zip_ref.namelist()
    with zip_ref.open(datasets[-1]) as my_file:
        df1 = pd.read_csv(my_file, encoding='latin1', sep=';', dtype='object')
        df = pd.concat([df, df1], ignore_index=True)
        print(f'{files[-1]}: ok!')
        print(df.info())
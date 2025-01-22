import pandas as pd
from navigation import get_file, kaggle_download


# testing navigation

# main = pd.read_csv(get_file('kaggle','economics', 'gini-coefficient.csv'))
main = pd.read_csv(get_file('kaggle','economics', 'inflation.csv'))
print(main.head())
print(main.info())
print('ok\n')

kaggle_download(dataset_name="alhamomarhotaki/global-food-prices-database-wfp", db='kaggle', schema='economics')

import navigation as nav
import pandas as pd


main = pd.read_csv(nav.get_file('kaggle','economics', 'inflation.csv'))
# main.to_sql('inflation', nav.conn, schema='main', if_exists='replace', index=False)

df = pd.read_sql(nav.read_sql_file('person', True), nav.conn)
print(df.head())
print(df.info())

# a = pd.DataFrame(nav.run_query('inflation_1'))
# print(a)

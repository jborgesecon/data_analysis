import navigation as nav
import pandas as pd



df = pd.read_sql(nav.read_sql_file('person'), nav.sqlite_conn)
print(df.info())
politico = 'jair'
result = df[df['NM_CANDIDATO'].str.contains(politico, case=False, na=False)]
# result = df[df['NM_CANDIDATO'].unique()]
print(result)
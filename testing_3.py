import navigation as nav
import pandas as pd


df1 = pd.read_sql(nav.read_sql_file('quanitativo1', True), nav.cockroach_conn)
df2 = pd.read_sql(nav.read_sql_file('quanitativo2', True), nav.cockroach_conn)
df3 = pd.read_sql(nav.read_sql_file('quanitativo3', True), nav.cockroach_conn)


df3['novo_ccusto'] = df3['novo_ccusto'].str.replace('.', '', regex=False).astype('Int64')

df1['matricula'] = df1['matricula'].astype(int)
df2['matricula'] = df2['matricula'].astype(int)

tables = {
    'jg': df1,
    'tadeu': df2,
    'depara': df3
}

gestao = tables['jg']['tipo_gestao'].unique().tolist()
months = tables['jg']['month'].unique().tolist()

data = []
for i in gestao:
    for ii in months:
        jg1 = df1[(df1['month'] == ii) & (df1['tipo_gestao'] == i)]
        td1 = df2[(df2['month'] == ii) & (df2['tipo_gestao'] == i)]
        matriculas = sorted(set(jg1['matricula'].tolist() + td1['matricula'].tolist()))

        for iii in matriculas:
            if iii in jg1['matricula'].values:
                cc = jg1[jg1['matricula'] == iii]['MASCARA'].values
                dt_init = jg1[jg1['matricula'] == iii]['dt_inicio_contrato'].values
                dt_fim = jg1[jg1['matricula'] == iii]['dt_fim_contrato'].values
                dt_desl = jg1[jg1['matricula'] == iii]['dt_desl_termino'].values
                status = None
            else:
                cc = td1[td1['matricula'] == iii]['cc_index'].values
                dt_init = td1[td1['matricula'] == iii]['dt_inicio_contrato'].values
                dt_fim = td1[td1['matricula'] == iii]['dt_fim_contrato'].values
                dt_desl = td1[td1['matricula'] == iii]['dt_desl_termino'].values
                status = td1[td1['matricula'] == iii]['matricula_status'].values

            row = {
                'month': ii,
                'gestao': i,
                'matricula': iii,
                'in_jg': iii in jg1['matricula'].values,
                'count_jg': jg1[jg1['matricula'] == iii]['matricula'].count(),
                'in_td': iii in td1['matricula'].values,
                'count_td': td1[td1['matricula'] == iii]['matricula'].count(),
                'in_both': iii in jg1['matricula'].values and iii in td1['matricula'].values,
                'status': status,
                'ccusto': cc[0],
                'dt_init': dt_init[0],
                'dt_fim': dt_fim[0],
                'dt_desl': dt_desl[0]
            }

            data.append(row)



final_df = pd.DataFrame(data)
print(final_df.info())
final_df.to_sql('quantitativo', nav.conn, schema='main', if_exists='replace', index=False)




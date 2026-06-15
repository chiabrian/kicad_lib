import pandas as pd
import sqlite3
import os

curr_path = os.path.dirname(os.path.abspath(__file__))

Tables = {}
Tables['Capacitors'] = ['Comment','Voltage','Tolerance','Dielectric','ESR','Package']
Tables['Connectors'] = ['Comment','Current','Voltage','Other']
Tables['Integrated Circuits'] = ['Comment','Voltage','Current','Other']
Tables['Resistors'] = ['Comment','Power','Tolerance','Package']
Tables['Mechanical'] = ['Comment','Voltage','Current','Other']
Tables['Diodes'] = ['Comment','VF','Current','VR','trr','Other']
Tables['Inductors'] = ['Comment','Current','Tolerance','DCR','Other']

print(f'{curr_path}/TypeList.csv')
type_df = pd.read_csv(f'{curr_path}/TypeList.csv',dtype=str)

# Regenerate Description based on parameters
# Check Category and Type
# Fill in empty cells with '-'
for t in Tables:
    print(f'Processing {t}')
    parts = pd.read_csv(f'{curr_path}/{t}.csv',dtype=str)
    parts = parts.fillna('-')
    for row in parts.iterrows():
        # Check Single Match of Category and type
        filtered_df = type_df[type_df['Cat'].str.fullmatch(row[1]['Cat']) & type_df['Type'].str.fullmatch(row[1]['Type'])]
        if len(filtered_df) != 1:
            print(f'Table {t} Row {row[0]} {filtered_df} {parts.loc[row[0]]}')
        desc = f'{filtered_df['Cat_Ab'].iloc[0]} {filtered_df['Type_Ab'].iloc[0]}'
        for param in Tables[t]:
            if row[1][param] != '-':
                desc = desc + ' ' + row[1][param]
        parts.loc[row[0],'Description'] = desc
    parts.to_csv(t+'.csv',index=False)

    sql_lib = sqlite3.connect('local_lib.sqlite')
for t in Tables:
    df = pd.read_csv(f'{curr_path}/{t}.csv',dtype=str)
    df.to_sql(t, sql_lib, if_exists='replace', index=False)
    print(f'Saving SQlite Table {t}')
sql_lib.close()

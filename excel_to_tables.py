import pandas as pd

excel_file = pd.ExcelFile('QDFH.xlsx')

sheet_names = excel_file.sheet_names
data_sheets = sheet_names[1:-4]


# single consonant treatments
single_treatment_tables = []

for sheet_name in data_sheets[0:33]: #[0:33]

        df = excel_file.parse(sheet_name) 
        print(f"Sheet: {sheet_name}")

        # get basic info
        number = df.iloc[1,1]
        treatment = df.iloc[2,1]
        environment = df.iloc[3, 1]
        
        table = df.iloc[5:17, :]
        
        # pivot table so rows = cols
        melted = table.melt(id_vars = 'A - Consonantism', var_name = 'Variable', value_name = 'Value')
        pivot = melted.pivot(index = 'Variable', columns = 'A - Consonantism', values = 'Value')
        pivot.set_index('Languages', inplace = True)
        pivot.reset_index(inplace = True)

        
        # deal with a/b/c versions
        pivot['version'] = pivot.groupby('Languages').cumcount().add(1)

        
        pivot.insert(0, 'treatment', treatment)
        pivot.insert(1, 'environment', environment)

        # clean language names and empty rows
        pivot['Languages'] = pivot['Languages'].str.replace('\n', ' ', regex = False)
        pivot = pivot.dropna(subset = ['Languages'])

        single_treatment_tables.append(pivot)


all_df = pd.concat(single_treatment_tables, axis = 0)

all_df.to_csv('single_consonants_data.csv')



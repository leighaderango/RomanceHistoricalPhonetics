import pandas as pd
from itertools import product
import re

consonants_long = pd.read_csv('all_consonants_data.csv')


consonants_grouped = consonants_long.groupby(['treatment', 'environment', 'Languages', 'version'])


display_tables = []

for setting, df in consonants_grouped:
    print(setting)

    df.sort_values('position', inplace=True) 
    positions_list = []

    sonority_avg = 0
    place_avg = 0

    for _,row in df.iterrows(): # for each position in the setting

        if pd.notna(row['Sonority value']):
            sonority_avg += row['Sonority value']
        if pd.notna(row['Place value']):
            place_avg += row['Place value']

        orig_ipa = row['IPA']

        # if ipa is not null and has a tilde, then split
        if isinstance(orig_ipa, str) and ('~' in orig_ipa):
            split = orig_ipa.split('~')

            positions_list.append(split)

        # if orig_ipa is not null but does not have a tilde, use ipa as position
        elif isinstance(orig_ipa, str):
            positions_list.append([orig_ipa])

    
    
    combos = product(*positions_list)

    # Join characters, skipping '∅'
    display = [''.join(c for c in combo if c != '∅') for combo in combos]

    temp_display = '|'.join(display[:2])

    if len(temp_display) != 1:
        sonority_avg = sonority_avg/len(df)
        place_avg = place_avg/len(df)
    
    display_table = pd.DataFrame({'treatment': [setting[0]],
                                    'environment': [setting[1]],
                                    'language': [setting[2]],
                                    'version': [setting[3]],
                                    'display': [temp_display],
                                    'sonority_avg': [sonority_avg],
                                    'place_avg': [place_avg]})


    display_tables.append(display_table)


all_displays = pd.concat(display_tables, axis = 0)

all_displays.to_csv('display_data.csv')



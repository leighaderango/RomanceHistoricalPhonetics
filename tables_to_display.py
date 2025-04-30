import pandas as pd
from itertools import product
import numpy as np

consonants_long = pd.read_csv('all_consonants_data.csv')


consonants_grouped = consonants_long.groupby(['number', 'treatment', 'environment', 'Languages', 'version'])
#consonants_grouped = consonants_long.sample(1000, random_state = 42).groupby(['treatment', 'environment', 'Languages', 'version'])

""" groups = [('7.0', 'C-', '#_E', 'ABR', np.float64(1.0)),
('7.0', 'C-', '#_E', 'AMR ESP', np.float64(1.0)),
('7.0', 'C-', '#_E', 'AND ESP', np.float64(1.0)),
('7.0', 'C-', '#_E', 'ARG', np.float64(1.0)),
('7.0', 'C-', '#_E', 'ARO', np.float64(1.0)),
('7.0', 'C-', '#_E', 'ARP', np.float64(1.0)),
('7.0', 'C-', '#_E', 'ASL', np.float64(1.0)),
('7.0', 'C-', '#_E', 'BAL', np.float64(1.0)),
('7.0', 'C-', '#_E', 'BR POR', np.float64(1.0)),
('7.0', 'C-', '#_E', 'CAM', np.float64(1.0)),
('7.0', 'C-', '#_E', 'CAS ESP', np.float64(1.0)),
('7.0', 'C-', '#_E', 'CAT', np.float64(1.0)),
('7.0', 'C-', '#_E', 'COR', np.float64(1.0)),
('7.0', 'C-', '#_E', 'CPN SRD', np.float64(1.0)),
('7.0', 'C-', '#_E', 'EU FRA', np.float64(1.0)),
('7.0', 'C-', '#_E', 'EU POR', np.float64(1.0)),
('7.0', 'C-', '#_E', 'FUR', np.float64(1.0)),
('7.0', 'C-', '#_E', 'GAL', np.float64(1.0)),
('7.0', 'C-', '#_E', 'GAS OCC', np.float64(1.0)),
('7.0', 'C-', '#_E', 'ITA', np.float64(1.0)),
('7.0', 'C-', '#_E', 'LAT', np.float64(1.0)),
('7.0', 'C-', '#_E', 'LIG', np.float64(1.0)),
('7.0', 'C-', '#_E', 'LMO', np.float64(1.0)),
('7.0', 'C-', '#_E', 'LOG SRD', np.float64(1.0)),
('7.0', 'C-', '#_E', 'OCC', np.float64(1.0)),
('7.0', 'C-', '#_E', 'PGL', np.float64(1.0)),
('7.0', 'C-', '#_E', 'QBC FRA', np.float64(1.0)),
('7.0', 'C-', '#_E', 'RMH', np.float64(1.0)),
('7.0', 'C-', '#_E', 'ROM', np.float64(1.0)),
('7.0', 'C-', '#_E', 'SCN', np.float64(1.0)),
('7.0', 'C-', '#_E', 'VAL', np.float64(1.0)),
('7.0', 'C-', '#_E', 'VEN', np.float64(1.0)),
('7.0', 'C-', '#_E', 'WAL', np.float64(1.0)),
('38', 'CL-', '#_', 'ABR', np.float64(1.0)),
('38', 'CL-', '#_', 'AMR ESP', np.float64(1.0)),
('38', 'CL-', '#_', 'AND ESP', np.float64(1.0)),
('38', 'CL-', '#_', 'ARG', np.float64(1.0)),
('38', 'CL-', '#_', 'ARO', np.float64(1.0)),
('38', 'CL-', '#_', 'ARP', np.float64(1.0)),
('38', 'CL-', '#_', 'ASL', np.float64(1.0)),
('38', 'CL-', '#_', 'BAL', np.float64(1.0)),
('38', 'CL-', '#_', 'BR POR', np.float64(1.0)),
('38', 'CL-', '#_', 'CAM', np.float64(1.0)),
('38', 'CL-', '#_', 'CAS ESP', np.float64(1.0)),
('38', 'CL-', '#_', 'CAT', np.float64(1.0)),
('38', 'CL-', '#_', 'COR', np.float64(1.0)),
('38', 'CL-', '#_', 'CPN SRD', np.float64(1.0)),
('38', 'CL-', '#_', 'EU FRA', np.float64(1.0)),
('38', 'CL-', '#_', 'EU FRA', np.float64(2.0)),
('38', 'CL-', '#_', 'EU POR', np.float64(1.0)),
('38', 'CL-', '#_', 'FUR', np.float64(1.0)),
('38', 'CL-', '#_', 'GAL', np.float64(1.0)),
('38', 'CL-', '#_', 'GAS OCC', np.float64(1.0)),
('38', 'CL-', '#_', 'ITA', np.float64(1.0)),
('38', 'CL-', '#_', 'LAT', np.float64(1.0)),
('38', 'CL-', '#_', 'LAT', np.float64(2.0)),
('38', 'CL-', '#_', 'LIG', np.float64(1.0)),
('38', 'CL-', '#_', 'LMO', np.float64(1.0)),
('38', 'CL-', '#_', 'LOG SRD', np.float64(1.0)),
('38', 'CL-', '#_', 'OCC', np.float64(1.0)),
('38', 'CL-', '#_', 'PGL', np.float64(1.0)),
('38', 'CL-', '#_', 'QBC FRA', np.float64(1.0)),
('38', 'CL-', '#_', 'RMH', np.float64(1.0)),
('38', 'CL-', '#_', 'ROM', np.float64(1.0)),
('38', 'CL-', '#_', 'SCN', np.float64(1.0)),
('38', 'CL-', '#_', 'VAL', np.float64(1.0)),
('38', 'CL-', '#_', 'VEN', np.float64(1.0)),
('38', 'CL-', '#_', 'WAL', np.float64(1.0))]

sub_table = [consonants_grouped.get_group(group) for group in groups]
sub_table = pd.concat(sub_table).groupby(['number', 'treatment', 'environment', 'Languages', 'version'])
 """

display_tables = []

for setting, df in consonants_grouped: # for each col in each sheet
    print(setting) # print col id

    df.sort_values('position', inplace=True) 
    positions_list = []

    sonority_avg = 0
    place_avg = 0
    voice_avg = 0

    for _,row in df.iterrows(): # for each segment in the column

        if pd.notna(row['Sonority value']):
            sonority_avg += row['Sonority value']
        if pd.notna(row['Place value']):
            place_avg += row['Place value']
        if pd.notna(row['voice']):
            voice_avg += row['voice']

        
        orig_ipa = row['IPA']


        # if ipa of segment is not null and has only a tilde, then split
        if isinstance(orig_ipa, str) and ('~' in orig_ipa) and ('(' not in orig_ipa):
            split = orig_ipa.split('~')

            positions_list.append(split) # append list of possible outcomes to positions_list

        # else if orig_ipa has a set of parenthesis

        elif isinstance(orig_ipa, str) and ('(' in orig_ipa):
            split = orig_ipa.split('(')
            positions_list.append(split)

        # finally if orig_ipa is not null but does not have a tilde or parenthesis, use ipa as position
        elif isinstance(orig_ipa, str):
            positions_list.append([orig_ipa]) # else append only possible outcome to positions_list
         
         # each element of positions_list represents possible outcomes at that index of the segments
            
    
    # create all versions of possible display strings
        # where phi is empty
        
        # ex. QU- #_a' RMH should show k|kw
        # CL- #_ ARP is an example of two tildes, should show tl|kj

    # create list to store all possible display strings
    combos = []

    # if only one segment
    if len(positions_list) == 1:
        # if one possibility:
        if len(positions_list[0]) == 1:
            # add only possibility to combos
            combos.append(positions_list[0][0])
        else:
            if any([')' in position for position in positions_list[0]]):
                range_string = '('.join(positions_list[0])
                combos.append(str(range_string))
            else: 
                range_string = '~'.join(positions_list[0])
                combos.append(str(range_string))

    # if two segments:
    elif len(positions_list) == 2:
        # if both segments have two parts, zip indicies
        if len(positions_list[0]) == 2 & len(positions_list[1]) == 2:
            zipped = zip(positions_list[0], positions_list[1])
            combos = [''.join(pair) for pair in zipped]
             
        elif (len(positions_list[0]) == 2 or len(positions_list[1]) == 2): 
            combos = [''.join(pair) for pair in product(*positions_list)]
        else:
            combos = [''.join(item for sublist in positions_list for item in sublist)]


    if any([')' in combo for combo in combos]):
        display = '('.join(combos)
    else:
        display = '~'.join(combos)


    if len(display) > 1:
        if display[-2:] != '~∅':
            display = display.replace('∅', '')


    if len(display) == 0:
        continue


    if len(positions_list) > 1:
        sonority_avg = sonority_avg/len(df)
        place_avg = place_avg/len(df)
        voice_avg = voice_avg/len(df)


    
    display_table = pd.DataFrame({'number': float(setting[0].strip('abcdefghijklmnopqrstuvwxyz')),
                                  'treatment': [setting[1]],
                                    'environment': [setting[2]],
                                    'language': [setting[3]],
                                    'version': [setting[4]],
                                    'display': [display.replace(' ', '')],
                                    'sonority_avg': [sonority_avg],
                                    'place_avg': [place_avg],
                                    'voice_avg': [voice_avg]})


    display_tables.append(display_table) 



all_displays = pd.concat(display_tables, axis = 0).sort_values(by = 'number')


all_displays.to_csv('display_data.csv')





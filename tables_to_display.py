import pandas as pd
from itertools import product
import numpy as np

consonants_long = pd.read_csv('all_consonants_data.csv')


consonants_grouped = consonants_long.groupby(['number', 'treatment', 'environment', 'Languages', 'version'])
#consonants_grouped = consonants_long.sample(1000, random_state = 42).groupby(['treatment', 'environment', 'Languages', 'version'])

""" groups = [('79', '-DJ-', 'V_V', 'AMR ESP', 'a'),
('79', '-DJ-', 'V_V', 'AMR ESP', 'b'),
('79', '-DJ-', 'V_V', 'AND ESP', 'a'),
('79', '-DJ-', 'V_V', 'AND ESP', 'b'),
('79', '-DJ-', 'V_V', 'ARG', 'a'),
('79', '-DJ-', 'V_V', 'ARG', 'b'),
('79', '-DJ-', 'V_V', 'ARO', 'a'),
('79', '-DJ-', 'V_V', 'ARP', 'a'),
('79', '-DJ-', 'V_V', 'ASL', 'a'),
('79', '-DJ-', 'V_V', 'ASL', 'b'),
('79', '-DJ-', 'V_V', 'BAL', 'a'),
('79', '-DJ-', 'V_V', 'BR POR', 'a'),
('79', '-DJ-', 'V_V', 'BR POR', 'b'),
('79', '-DJ-', 'V_V', 'CAS ESP', 'a'),
('79', '-DJ-', 'V_V', 'CAS ESP', 'b'),
('79', '-DJ-', 'V_V', 'CAT', 'a'),
('79', '-DJ-', 'V_V', 'EU FRA', 'a'),
('79', '-DJ-', 'V_V', 'EU POR', 'a'),
('79', '-DJ-', 'V_V', 'EU POR', 'b'),
('79', '-DJ-', 'V_V', 'GAL', 'a'),
('79', '-DJ-', 'V_V', 'GAL', 'b'),
('79', '-DJ-', 'V_V', 'GAS OCC', 'a'),
('79', '-DJ-', 'V_V', 'GAS OCC', 'b'),
('79', '-DJ-', 'V_V', 'ITA', 'a'),
('79', '-DJ-', 'V_V', 'ITA', 'b'),
('79', '-DJ-', 'V_V', 'LAT', 'a'),
('79', '-DJ-', 'V_V', 'OCC', 'a'),
('79', '-DJ-', 'V_V', 'OCC', 'b'),
('79', '-DJ-', 'V_V', 'QBC FRA', 'a'),
('79', '-DJ-', 'V_V', 'ROM', 'a'),
('79', '-DJ-', 'V_V', 'SCN', 'a'),
('79', '-DJ-', 'V_V', 'VAL', 'a'),
('79', '-DJ-', 'V_V', 'WAL', 'a')]

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
    print(positions_list)

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
        if '∅∅' in display:
            display = display.replace('∅∅', '∅')

        if display[-2:] != '~∅' and len(display) > 1:
            display = display.replace('∅', '')
        
        if (display[0] == '∅') & (display[:1] != '∅~'):
            display = display[1:]


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





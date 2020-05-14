import pandas as pd

file = pd.read_csv("client_info_latest.csv")
columns_name = list(file.columns)
kept_columns = [
    'Customer ID', 
    'Customer name', 
    'Customer type', 
    'Company number', 
    'Company name', 
    'Continent', 
    'Country', 
    'State', 
    'Telephone', 
    'Email', 
    'Postcode', 
    'Address'
    ]

missed_info = dict()
for i in kept_columns:
    missed_info.update({i:file[file[i].isnull()]})
merge_final = pd.DataFrame()
for key in missed_info:
    merge_final = pd.concat([merge_final,missed_info[key]])    
merge_final = merge_final[~merge_final.index.duplicated(keep = 'first')]

#to csv
merge_final.to_csv('./info_missed_final.csv', encoding="utf_8_sig")
import pandas as pd

file = pd.read_csv("client_info_2.csv")
columns_name = list(file.columns)
kept_columns = [
    'State', 
    'Telephone', 
    'Postcode', 
    ]
missed_info = dict()
for i in kept_columns:
    missed_info.update({i:file[file[i].isnull()]})
merge_final = pd.DataFrame()
for key in missed_info:
    merge_final = pd.concat([merge_final,missed_info[key]])    
merge_final = merge_final[~merge_final.index.duplicated(keep = 'first')]
#to csv
merge_final.to_csv('./info_missed_final_2nd.csv', encoding="utf_8_sig")


file_2 = pd.read_csv("client_info_2.csv", encoding="utf_8_sig")
search_school_id = file_2[~file_2.loc[:,"School"].isnull()].loc[:, "School"]

file_3 = pd.read_csv("school_info.csv", encoding="utf_8_sig")
school_id = file_3.loc[:,"School"]

State_index = file_2[file_2["State"].isnull()].index
phone_index = file_2[file_2["Telephone"].isnull()].index
Postcode_index = file_2[file_2["Postcode"].isnull()].index

def replce_info(pd_index, pd_file, column_name):
    global search_school_id
    global file_2
    for i in pd_index:
        print(i)  
        try:
            replace = pd_file[pd_file['School'] == search_school_id[i]][column_name].dropna().reset_index(drop = True)
        except KeyError:
            next
        if replace.empty:
            pass
        else:
            file_2.loc[i,column_name] = replace[0]



replce_info(State_index, file_3, "State")
replce_info(phone_index, file_3, "Telephone")
replce_info(Postcode_index, file_3, "Postcode")

file_2.to_csv("./merged_final2.csv", encoding="utf_8_sig")

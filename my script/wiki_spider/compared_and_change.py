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



file_2 = pd.read_csv("info_missed_final_2nd.csv")
search_school_id = file_2[~file_2.loc[: ,"school_ID"].isnull()].loc[: ,"school_ID"]

file_3 = pd.read_csv("merged_final.csv", index_col=0)
school_id = file_3[~file_3.loc[:,"Company number"].duplicated(keep='first')]

for i in search_school_id.index:
    State = file_3[file_3['Company number'] == search_school_id[i]]["State"].dropna().reset_index(drop = True)
    phone = file_3[file_3['Company number'] == search_school_id[i]]["Telephone"].dropna().reset_index(drop = True)
    Postcode = file_3[file_3['Company number'] == search_school_id[i]]["Postcode"].dropna().reset_index(drop = True)
    if State.empty:
        pass
    else:
        file_2["State"][i] = State[0]
    if phone.empty:
        pass
    else:
        file_2["Telephone"][i] = phone[0]
    if Postcode.empty:
        pass
    else:
        file_2["Postcode"][i] = Postcode[0]
        
file_2.to_csv("./merged_final2.csv", encoding="utf_8_sig")
import pandas as pd

class index(object):
    '''
    the index file need to be CSV format for both
    '''
    def __init__(self, index_file_name):
        self.filename = index_file_name
    def read_csv(self):
        self.index_list = list()
        self.pd_index = pd.read_excel(self.filename, sheet_name='10X_index')
        self.client_indexname = pd.read_excel(self.filename, sheet_name='client')
        self.transfer_name = self.client_indexname.loc[self.client_indexname.index.repeat(4)].reset_index(drop=True)
        try:
            for row in self.client_indexname.iloc[:, 0]:
                self.index_list.extend(list(self.pd_index[self.pd_index.values == row].values[0][1:5]))
            self.transfer_name['index'] = self.index_list
        except IndexError as e:
            raise NameError ("please check the index name in client index")

    def save_file(self):
        self.transfer_name.to_csv("./10X_transferred.csv", encoding="utf_8_sig", index = False)


if __name__ == "__main__":
    # main_script
    warning_1 = input("Please input your client index in 10X_index.xlsx file, sheet name is client, input Enter to continue!")
    file = "C:\\Users\\Jerry\\Documents\\GitHub\\Note-Python\\my script\\index\\10X_index.xlsx"
    run_1 = index(file)
    try:
        run_1.read_csv()
        run_1.save_file()
    except NameError:
        raise NameError

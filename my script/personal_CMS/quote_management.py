# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 22:05:40 2018

@author: yiwen, Jerry

happy every day!!
"""
import platform
import tkinter.filedialog
import tkinter as tk
from Quotesection import start_folder
from process_SIF import SIF
from section import *


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(column=0, row=0)
        self.bgColor = '#EEEEEE'
        self.config(bg=self.bgColor, borderwidth=20)
        self.create_widgets()
        self.quoteinfotext.focus()
        # bind shift-enter key to generate quotation
        master.bind_all('<Shift-Return>', lambda e: self.contract_check())

    def paste_quote_text(self, event):
        """
        Binded function to paste clipboard content into Text, after striping
        This is helpful to solve performance issues when a lot of \t are copied from excel
        """
        clipboard = self.clipboard_get()
        self.quoteinfotext.insert('end', clipboard.strip())
        return "break"

    def focus_next(self, event):
        """binded function that switch the focus to the next widget"""
        event.widget.tk_focusNext().focus()
        # return 'break' is a trick to stop the original functionality of the event
        return "break"

    def create_widgets(self):
        # get the username and password
        tk.Label(self, text="CMS Username:").grid(column=2, row=0)
        self.user = tk.Text(self, width=20, height=1)
        self.user.grid(column=3, row=0)
        self.user.bind("<Tab>", self.focus_next)
        tk.Label(self, text="CMS Password: ").grid(column=2, row=1)
        self.user_password = tk.Text(self, width=20, height=1)
        self.user_password.grid(column=3, row=1)
        self.user_password.bind("<Tab>", self.focus_next)
        
        self.QuoteGenerator = tk.Label(self, text=
        'Quote Generator',
                                bg=self.bgColor, height=1, font=('Helvetica', 11, 'bold'))
        self.QuoteGenerator.grid(column=0, row=1, columnspan=1)

        self.quoteinfotext = tk.Text(self, height=5)
        if platform.system() == 'Darwin':
            self.quoteinfotext.bind('<Command-v>', self.paste_quote_text)
        self.quoteinfotext.bind('<Control-v>', self.paste_quote_text)
        self.quoteinfotext.bind("<Tab>", self.focus_next)
        self.quoteinfotext.grid(column=0, row=2, columnspan=4)
        
        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=2, row=11, columnspan=4)
        self.run = tk.Button(self, text = 'set folder', command=self.set_folder, highlightbackground=self.bgColor)
        self.run.grid(column=2, row=12, columnspan=1)
        self.clear = tk.Button(
            self, text='Clear All', command=self.clearall, highlightbackground=self.bgColor)
        self.clear.grid(column=0, row=12, columnspan=1)
        
        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=0, row=13, columnspan=4)

        self.OtherTools = tk.Label(self, text=
        'Contract/SIF Upload',
                                bg=self.bgColor, font=('Helvetica', 11, 'bold'))
        self.OtherTools.grid(column=0, row=15, columnspan=1)

        # get the path of file and submit the SIF
        self.quote_label = tk.Label(self, text="Quote Number").grid(column=0, row=16, columnspan=1)
        self.quotenumber = tk.Text(self, width=20, height=1)
        self.quotenumber.grid(column=1, row=16, columnspan=1)
        self.quotenumber.bind("<Tab>", self.focus_next)
        self.Contract_check_button = tk.Button(self, text="check Contract#", command=self.contract_check).grid(column=2,row=16)
        self.Contractmessage = tk.StringVar()
        tk.Entry(self, textvariable=self.Contractmessage).grid(column=3, row=16)
        
        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=0, row=17, columnspan=4)
        
        self.path_button = tk.Button(self, text="openfile", command=self.selectPath).grid(column=0, row=18)
        self.SIF_upload_button = tk.Button(self, text="upload SIF", command=self.SIF_upload).grid(column=2, row=18)
        self.file_path = tk.StringVar()
        tk.Label(self, textvariable = self.file_path).grid(column=1, row=18)
        tk.Label(self, text='success | fail: ').grid(column=3, row=17)
        self.SIFmessage = tk.StringVar()
        tk.Label(self, textvariable=self.SIFmessage).grid(column=3, row=20)
        
        self.errorLabel = tk.Label(self, bg=self.bgColor, fg='red')
        self.errorLabel.grid(column=0, row=21, columnspan=4)
        
    def set_folder(self):
        quote_info = self.quoteinfotext.get('1.0', 'end').strip()
        try:
            start_folder(quote_info)
            self.errorLabel.config(text='Success!')
        except Exception as e:
            self.errorLabel.config(text=str(e))

    def selectPath(self):
        '''
        this module can read the file path
        the return path will be bond to self.path
        '''
        '''choose file and return the path'''
        self.path = tkinter.filedialog.askopenfilename()
        self.file_path_message = re.search(r'(/\w+((-|_)\w+)*\.xlsx)$', self.path).group(0)
        self.file_path.set(self.file_path_message)
        # self.path.set(path_)
        print(self.path)

    def SIF_upload(self):
        quotename = self.quotenumber.get('1.0', 'end').strip()
        user = self.user.get('1.0', 'end').strip()
        pd = self.user_password.get('1.0', 'end').strip()
        sifupload = SIF()
        try:
            if self.path and quotename:
                try:
                    sifupload.login_user(user, pd)
                    sifupload.SIF_info_submit(quotename)
                    file_name = 'uploadSIF.xlsx'
                    sifupload.file_submit(file_name, self.path)
                    sifupload.sample_check()
                    self.SIFmessage.set(sifupload.message)
                except (KeyError, IndexError) as e:
                    self.SIFmessage.set(str(e) + ", batchID created without product info updated")
            else:
                raise AttributeError
        except AttributeError:
            err = str('please select SIF path and input quote#')
            self.SIFmessage.set(err)

    def contract_check(self):
        quote_name = self.quotenumber.get('1.0', 'end').strip()
        user = self.user.get('1.0', 'end').strip()
        pd = self.user_password.get('1.0', 'end').strip()
        try:
            contract_search = SIF()
            if user and quote_name:
                contract_search.login_user(user,pd)
            else:
                raise KeyError(f'no username or quote# detected')
            contract_search.contract_search(quote_name)
            self.Contractmessage.set(contract_search.contractno)
        except (KeyError, TypeError) as e:
            self.errorLabel.config(text=str(e))

    def clearall(self):
        self.quoteinfotext.delete('1.0', 'end')
        self.errorLabel.config(text='')
        self.SIFmessage.set('')
        self.file_path.set('')
        self.Contractmessage.set('')
        self.quotenumber.delete('1.0', 'end')

def main():
    root = tk.Tk()
    root.title('TSgo')
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()

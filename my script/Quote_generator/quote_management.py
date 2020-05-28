# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 22:05:40 2018

@author: yiwen, Jerry

happy every day!!
"""
import platform
import tkinter.filedialog
import tkinter as tk
from Quotesection import start, start_folder
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
        master.bind_all('<Shift-Return>', lambda e: self.get_quotation())

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

    def autoselect(self):
        if self.rRNAremoval_check.get() == True:
            self.library_type.set(True)
        else:
            self.library_type.get()

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

        self.label1 = tk.Label(
            self, text='Special price required? Input first and second price below.', bg=self.bgColor, height=2)
        self.label1.grid(column=0, row=3, columnspan=4)
        self.pricelabel1 = tk.Label(
            self, text='First product price:', bg=self.bgColor)
        self.pricelabel1.grid(column=0, row=4)
        self.pricetext1 = tk.Text(self, width=20, height=1)
        self.pricetext1.bind("<Tab>", self.focus_next)
        self.pricetext1.grid(column=1, row=4)
        self.pricelabel2 = tk.Label(
            self, text='Second product price:', bg=self.bgColor)
        self.pricelabel2.grid(column=2, row=4)
        self.pricetext2 = tk.Text(self, width=20, height=1)
        self.pricetext2.bind("<Tab>", self.focus_next)
        self.pricetext2.grid(column=3, row=4)

        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=0, row=5, columnspan=4)

        self.label2 = tk.Label(
            self, text='Different sample number for BI analysis? If so, input the analysis sample number:',
            bg=self.bgColor)
        self.label2.grid(column=0, row=6, columnspan=3)
        self.BInumbertext = tk.Text(self, width=20, height=1)
        self.BInumbertext.bind("<Tab>", self.focus_next)
        self.BInumbertext.grid(column=3, row=6, columnspan=1)

        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=0, row=7, columnspan=4)

        self.label3 = tk.Label(
            self, text='Input the species latin name if species is different than "human", "mouse", "rat":',
            bg=self.bgColor)
        self.label3.grid(column=0, row=8, columnspan=3)
        self.speciestext = tk.Text(self, width=20, height=1)
        self.speciestext.bind("<Tab>", self.focus_next)
        self.speciestext.grid(column=3, row=8, columnspan=1)

        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=0, row=9, columnspan=4)

        self.library_type = tk.BooleanVar()
        self.library_type.set(False)
        self.strandedbutton = tk.Checkbutton(self, text='check if need stranded EukmRNA library',
                                             variable=self.library_type,
                                             onvalue=True, offvalue=False, bg=self.bgColor, command=self.autoselect)
        self.strandedbutton.grid(column=0, row=10, columnspan=2)

        self.rRNAremoval_check = tk.BooleanVar()
        self.rRNAremoval_check.set(False)
        self.rRNAremovalbutton = tk.Checkbutton(self, text='check if need rRNA removal/FFPE RNAseq',
                                                variable=self.rRNAremoval_check,
                                                onvalue=True, offvalue=False, bg=self.bgColor, command=self.autoselect)
        self.rRNAremovalbutton.grid(column=2, row=10, columnspan=2)
        
        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=2, row=11, columnspan=4)

        self.run = tk.Button(self, text='Generate New Quote',
                             command=self.get_quotation, highlightbackground=self.bgColor)
        self.run.grid(column=3, row=12, columnspan=1)
        self.run = tk.Button(self, text='submit CMS lead',
                             command=self.submit_lead, highlightbackground=self.bgColor)
        self.run.grid(column=1, row=12, columnspan=2)
        self.run = tk.Button(self, text = 'set folder', command=self.set_folder, highlightbackground=self.bgColor)
        self.run.grid(column=2, row=12, columnspan=1)
        self.clear = tk.Button(
            self, text='Clear All', command=self.clearall, highlightbackground=self.bgColor)
        self.clear.grid(column=0, row=12, columnspan=1)
        
        #add a space line
        tk.Label(self, bg=self.bgColor).grid(column=0, row=13, columnspan=4)
        tk.Label(self, bg=self.bgColor).grid(column=0, row=14, columnspan=4)

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

        '''self.blanktemplates = tk.Label(self, text=
        'Click the below buttons \n\n to acquire blank templates:',
                                       bg=self.bgColor)
        self.blanktemplates.grid(column=5, row=0, columnspan=1)
        self.eukmrnatemplate = tk.Button(self, text='Euk mRNAseq',
                                         command=self.get_quotation, highlightbackground=self.bgColor)
        self.eukmrnatemplate.grid(column=5, row=1, columnspan=1)'''
        
    def get_quotation(self):
        quote_info = self.quoteinfotext.get('1.0', 'end').strip()
        price1 = self.pricetext1.get('1.0', 'end').strip()
        price2 = self.pricetext2.get('1.0', 'end').strip()
        BInumber = self.BInumbertext.get('1.0', 'end').strip()
        species = self.speciestext.get('1.0', 'end').strip()
        rRNAremoval_check = self.rRNAremoval_check.get()
        library_type = self.library_type.get()
        try:
            start(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check)
            self.errorLabel.config(text='Success!')
        except Exception as e:
            self.errorLabel.config(text=str(e))
            raise

    def set_folder(self):
        quote_info = self.quoteinfotext.get('1.0', 'end').strip()
        price1 = self.pricetext1.get('1.0', 'end').strip()
        price2 = self.pricetext2.get('1.0', 'end').strip()
        BInumber = self.BInumbertext.get('1.0', 'end').strip()
        species = self.speciestext.get('1.0', 'end').strip()
        rRNAremoval_check = self.rRNAremoval_check.get()
        library_type = self.library_type.get()
        try:
            start_folder(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check)
            self.errorLabel.config(text='Success!')
        except Exception as e:
            self.errorLabel.config(text=str(e))

    def submit_lead(self):
        quote_info = self.quoteinfotext.get('1.0', 'end').strip()
        price1 = self.pricetext1.get('1.0', 'end').strip()
        price2 = self.pricetext2.get('1.0', 'end').strip()
        BInumber = self.BInumbertext.get('1.0', 'end').strip()
        species = self.speciestext.get('1.0', 'end').strip()
        rRNAremoval_check = self.rRNAremoval_check.get()
        library_type = self.library_type.get()
        password = self.user_password.get('1.0', 'end').strip()
        from login import lead_submit, run_it
        try:
            run_it(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check, password)
            self.errorLabel.config(text='Success!')
        except Exception as e:
            self.errorLabel.config(text=str(e))
            raise

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
        self.pricetext1.delete('1.0', 'end')
        self.pricetext2.delete('1.0', 'end')
        self.BInumbertext.delete('1.0', 'end')
        self.speciestext.delete('1.0', 'end')
        self.errorLabel.config(text='')
        self.SIFmessage.set('')
        self.file_path.set('')
        self.Contractmessage.set('')
        self.quotenumber.delete('1.0', 'end')
        self.library_type.set(False)
        self.rRNAremoval_check.set(False)

def main():
    root = tk.Tk()
    root.title('TSgo')
    root.iconbitmap('./icon/biology.ico')
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
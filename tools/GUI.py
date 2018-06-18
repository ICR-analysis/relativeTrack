# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

@author: Adam Tyson
"""
import tkinter as tk
import tkinter.filedialog
import os

def chooseDir():
    print('Getting image directory')
    # choose a directory and move into it
    root = tk.Tk()
    root.withdraw()
    imDir = tk.filedialog.askdirectory(title='Select image directory')
    os.chdir(imDir)


def get_opt_radio():
    class OptGUI:
        def __init__(self, a):
            # self.master = tk.Tk()
            self.save_csv_opt = tk.IntVar()
            self.save_csv_opt.set(0)

            self.plot_opt = tk.IntVar()
            self.plot_opt.set(0)

            self.track_opt = tk.IntVar()
            self.track_opt.set(0)

            self.static_opt = tk.IntVar()
            self.static_opt.set(0)

            self.test_opt = tk.IntVar()
            self.test_opt.set(0)

            self.savecsv = False
            self.plot = False
            self.cellTrack = False
            self.staticAnalysis = False
            self.test = False

            tk.Label(text="Save results as .csv?", height=2).grid(
                row=0, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.save_csv_opt, value=1).grid(
                row=1, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.save_csv_opt,
                           value=0).grid(row=3, sticky=tk.W, column=0)

            tk.Label(text="Plot intermediate results?",  height=2).grid(
                row=5, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.plot_opt, value = 1).grid(
                row=6, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.plot_opt,
                           value=0).grid(row=7, sticky=tk.W, column=0)

            tk.Label(text="Perform tracking analysis?",  height=2).grid(
                row=8, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.track_opt, value = 1).grid(
                row=9, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.track_opt,
                           value=0).grid(row=10, sticky=tk.W, column=0)

            tk.Label(text="Perform static, frame-by-frame analysis"
                          " (no tracking)?",  height=2).grid(
                row=11, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.static_opt, value = 1).grid(
                row=12, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.static_opt,
                           value=0).grid(row=13, sticky=tk.W, column=0)

            tk.Label(text="Testing?",  height=2).grid(
                row=14, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.test_opt, value = 1).grid(
                row=15, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.test_opt,
                           value=0).grid(row=16, sticky=tk.W, column=0)


            tk.Button(a, text="Proceed",
                      command=self.quit_loop).grid(row=17, column=2)
            # a.bind('<Return>', (lambda e, b=name_button: b.invoke()))
            # name_button.bind('<Return>', self.quit_loop)
            root.mainloop()

        def quit_loop(self):

            if self.save_csv_opt.get() == 1:
                self.savecsv = True

            if self.plot_opt.get() == 1:
                self.plot = True

            if self.track_opt.get() == 1:
                self.cellTrack = True

            if self.static_opt.get() == 1:
                self.staticAnalysis = True

            if self.test_opt.get() == 1:
                self.test = True

            del self.save_csv_opt
            del self.plot_opt
            del self.static_opt
            del self.track_opt
            del self.test_opt

            root.destroy()

    root = tk.Tk()
    # root.withdraw()
    root.title('Options')
    opt = OptGUI(root)
    return opt


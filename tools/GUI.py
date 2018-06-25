# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

"""
import tkinter as tk
import tkinter.filedialog
import os
from datetime import datetime


def choose_dir():
    print('Getting image directory')
    # choose a directory and move into it
    root = tk.Tk()
    root.withdraw()
    direc = tk.filedialog.askdirectory(title='Select image directory')
    os.chdir(direc)
    return direc


def get_opt_radio():
    class OptGUI:
        def __init__(self, a):
            print('Getting options')

            self.save_csv_opt = tk.IntVar()
            self.save_csv_opt.set(0)

            self.plot_opt = tk.IntVar()
            self.plot_opt.set(1)

            self.cut_far_opt = tk.IntVar()
            self.cut_far_opt.set(1)

            self.test_opt = tk.IntVar()
            self.test_opt.set(0)

            self.savecsv = False
            self.plot_inter_static = False
            self.plot_inter_temporal = False
            self.plot_final_summary = False
            self.cutFarCells = False
            self.test = False

            tk.Label(text="Save results as .csv?", height=2).grid(
                row=0, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.save_csv_opt, value=1).grid(
                row=1, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.save_csv_opt,
                           value=0).grid(row=3, sticky=tk.W, column=0)

            tk.Label(text="Plotting?",  height=2).grid(
                row=5, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Intermediate - static",
                           variable=self.plot_opt, value=1).grid(
                row=6, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Intermediate - temporal",
                           variable=self.plot_opt, value=2).grid(
                row=7, sticky=tk.W, column=0)
            tk.Radiobutton(text="Final - summary", variable=self.plot_opt,
                           value=3).grid(row=8, sticky=tk.W, column=0)
            tk.Radiobutton(text="None", variable=self.plot_opt,
                           value=0).grid(row=9, sticky=tk.W, column=0)

            tk.Label(text="Remove distant cells?",  height=2).grid(
                row=10, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.cut_far_opt, value = 1).grid(
                row=11, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.cut_far_opt,
                           value=0).grid(row=12, sticky=tk.W, column=0)

            tk.Label(text="Testing?",  height=2).grid(
                row=13, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="Yes",
                           variable=self.test_opt, value = 1).grid(
                row=14, sticky=tk.W, columnspan=3)
            tk.Radiobutton(text="No", variable=self.test_opt,
                           value=0).grid(row=15, sticky=tk.W, column=0)

            tk.Button(a, text="Proceed",
                      command=self.quit_loop).grid(row=16, column=2)
            # a.bind('<Return>', (lambda e, b=name_button: b.invoke()))
            # name_button.bind('<Return>', self.quit_loop)
            root.mainloop()

        def quit_loop(self):

            if self.save_csv_opt.get() == 1:
                self.savecsv = True

            if self.plot_opt.get() == 1:
                self.plot_inter_static = True
            elif self.plot_opt.get() == 2:
                self.plot_inter_temporal = True
            elif self.plot_opt.get() == 3:
                self.plot_final_summary = True

            if self.cut_far_opt.get() == 1:
                self.cutFarCells = True

            if self.test_opt.get() == 1:
                self.test = True

            del self.save_csv_opt
            del self.plot_opt
            del self.cut_far_opt
            del self.test_opt

            root.destroy()

    root = tk.Tk()
    # root.withdraw()
    root.title('Options')
    root.geometry('250x500')

    opt = OptGUI(root)
    return opt


def get_var():
    class VarGUI:  # vars in class refer to all instances of class

        def __init__(self, a):  # self refers to specific instance of class
            self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.frame_plot = 0
            self.frames_keep = 0  # set to 0 to run all

            # approx radius (must be odd)
            label_text1 = tk.StringVar()
            label_text1.set("Estimated cell diameter (pixels)")
            label1 = tk.Label(textvariable=label_text1, height=4)
            label1.grid(row=0)

            self.radius = tk.StringVar()
            text1 = tk.Entry(textvariable=self.radius)
            text1.insert(tk.END, 25)  # default
            text1.grid(row=0, column=1)
#
            # minimum total fluorescence of a single object
            label_text2 = tk.StringVar()
            label_text2.set("Minimum cell fluorescence mass")
            label2 = tk.Label(textvariable=label_text2, height=4)
            label2.grid(row=1)

            self.minFluroMass = tk.StringVar()
            text2 = tk.Entry(textvariable=self.minFluroMass)
            text2.insert(tk.END, 1300)  # default
            text2.grid(row=1, column=1)
#
            # maximum total fluorescence of a single object
            label_text3 = tk.StringVar()
            label_text3.set("Maximum cell fluorescence mass")
            label3 = tk.Label(textvariable=label_text3, height=4)
            label3.grid(row=2)

            self.maxFluroMass = tk.StringVar()
            text3 = tk.Entry(textvariable=self.maxFluroMass)
            text3.insert(tk.END, 50000)  # default
            text3.grid(row=2, column=1)
#

            label_text4 = tk.StringVar()
            label_text4.set("Large object threshold adjustment")
            label4 = tk.Label(textvariable=label_text4, height=4)
            label4.grid(row=3)

            self.obj_thresh_adj = tk.StringVar()
            text4 = tk.Entry(textvariable=self.obj_thresh_adj)
            text4.insert(tk.END, 0.8)  # default
            text4.grid(row=3, column=1)
#

            label_text5 = tk.StringVar()
            label_text5.set("Large object thresholding smoothing")
            label5 = tk.Label(textvariable=label_text5, height=4)
            label5.grid(row=4)

            self.obj_thresh_smooth = tk.StringVar()
            text5 = tk.Entry(textvariable=self.obj_thresh_smooth)
            text5.insert(tk.END, 50)  # default
            text5.grid(row=4, column=1)
#

            #  Radius to analyse for static analysis
            label_text6 = tk.StringVar()
            label_text6.set("Analysis radius (pixels from object centre)")
            label6 = tk.Label(textvariable=label_text6, height=4)
            label6.grid(row=5)

            self.staticSearchRad = tk.StringVar()
            text6 = tk.Entry(textvariable=self.staticSearchRad)
            text6.insert(tk.END, 500)  # default
            text6.grid(row=5, column=1)
            #

            # Proceed button
            name_button = tk.Button(text="Proceed", command=self.fetch_vars)
            name_button.grid(row=6, column=1)
            # bind return to button
            root.bind('<Return>', (lambda e, b=name_button: b.invoke()))

        def fetch_vars(self):
            self.radius = int(round(float(self.radius.get())))
            self.minFluroMass = int(round(float(self.minFluroMass.get())))
            self.maxFluroMass = int(round(float(self.maxFluroMass.get())))
            self.obj_thresh_adj = float(self.obj_thresh_adj .get())
            self.obj_thresh_smooth = int(round(float(self.obj_thresh_smooth.get())))

            self.staticSearchRad = int(round(float(self.staticSearchRad.get())))

            # force search radius to be odd (for trackpy)
            if self.radius % 2 == 0:
                self.radius = self.radius + 1

            root.destroy()

    root = tk.Tk()
    # root.withdraw()
    root.title('Choose parameters (set to 0 to disable)')
    root.geometry('400x500')

    var = VarGUI(root)
    root.mainloop()

    var.separation = var.radius
    return var


def run():
    opt = get_opt_radio()
    var = get_var()
    direc = choose_dir()
    return opt, var, direc

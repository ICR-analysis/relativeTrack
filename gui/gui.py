# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-07-10

"""
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
import numpy as np
import gui.options_variables as options_var


def gui_run():
    options = get_opt()
    variables = get_var()
    variables['plot_style'] = 'seaborn-muted'

    direc = choose_dir()
    return options, variables, direc


def choose_dir():
    print('Getting image directory')
    # choose a directory and move into it
    root = tk.Tk()
    root.withdraw()
    direc = tk.filedialog.askdirectory(title='Select image directory')
    os.chdir(direc)
    return direc


def get_opt():
    class OptGUI:
        def __init__(self, root):

            self.opt_names,\
                self.opt_prompts,\
                self.opt_defaults =\
                options_var.opt_initialise()

            self.opts_get = []
            self.opts = []
            self.option_dict = []
            self.gui_fill()
            self.return_dict()

        def gui_fill(self):
            row = 0
            count = 0
            for opt_prompt in self.opt_prompts:
                opt_tmp = tk.BooleanVar()
                opt_tmp.set(self.opt_defaults[count])
                self.opts_get.append(opt_tmp)
                tk.Label(root, text=opt_prompt, height=2).grid(
                    row=row, sticky=tk.W, columnspan=2)
                tk.Radiobutton(root, text="Yes",
                               variable=opt_tmp, value=True).grid(
                    row=row+1, sticky=tk.W, column=0)
                tk.Radiobutton(root, text="No", variable=opt_tmp,
                               value=False).grid(
                    row=row+1, sticky=tk.W, column=1)

                row = row+2
                count = count + 1

            tk.Button(root, text="Proceed",
                      command=self.quit_loop).grid(row=row, column=2)

            # <Return> to progress
            root.bind('<Return>', lambda event: self.quit_loop())
            # to bring to front
            root.attributes("-topmost", True)
            root.focus_force()
            root.mainloop()

        def quit_loop(self):
            for var in self.opts_get:
                self.opts.append(var.get())

            root.destroy()

        def return_dict(self):
            self.option_dict = dict(zip(self.opt_names, self.opts))

    root = tk.Tk()
    root.title('Options')
    opt = OptGUI(root)
    return opt.option_dict


def get_var():
    class OptGUI:
        def __init__(self, root):
            self.var_names,\
                self.var_prompts,\
                self.var_defaults = options_var.var_initialise()

            self.var_get = []
            self.var = []
            self.var_float = []
            self.variable_dict = []
            self.gui_fill()
            self.return_dict()

        def gui_fill(self):
            row = 0
            count = 0
            for var_prompt in self.var_prompts:
                var_tmp = tk.StringVar()
                self.var_get.append(var_tmp)

                label_text = tk.StringVar()
                label_text.set(var_prompt)
                label = tk.Label(root, textvariable=label_text, height=4)
                label.grid(row=row)

                text = tk.Entry(root, textvariable=var_tmp)
                text.insert(tk.END, self.var_defaults[count])  # default
                text.grid(row=row, column=1)

                row = row+1
                count = count + 1

            tk.Button(root, text="Proceed",
                      command=self.quit_loop).grid(row=row, column=2)

            # <Return> to progress
            root.bind('<Return>', lambda event: self.quit_loop())

            # to bring to front
            root.attributes("-topmost", True)
            root.focus_force()
            root.mainloop()

        def quit_loop(self):
            for variable in self.var_get:
                self.var.append(variable.get())
            root.destroy()

        def return_dict(self):
            self.var_float = list(np.float_(self.var))
            self.variable_dict = dict(zip(self.var_names, self.var_float))

    while True:
        try:
            root = tk.Tk()
            root.title('Variables')
            var = OptGUI(root)
        except ValueError:
            error = tk.Tk()
            error.withdraw()
            messagebox.showinfo(
                'Input error', 'Please try again, enter numerical values')
            error.destroy()
            continue
        break

    variable_dict = var.variable_dict
    variable_dict = options_var.var_force(variable_dict)

    return variable_dict

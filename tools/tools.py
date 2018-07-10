# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-06-21

"""
import pandas as pd
from datetime import datetime


def save_1d_csv(movies, heading, *args):
    # saves properties of movies to a csv, with movies.heading as heading
    # *args must match the attribute of the class
    print('Saving results to .csv')

    for arg in args:
        df = pd.DataFrame()
        for i in range(0, len(movies)):
            df_new = pd.DataFrame(
                {getattr(movies[i], heading): getattr(movies[i], arg)})
            df = pd.concat([df, df_new], axis=1)  # concat because diff lengths
        df.to_csv(arg+'.csv', encoding='utf-8', index=False)
        del df


def options_variables_write(options, variables, direc):
    with open(direc + '\\analysis_options.txt', 'w') as file:
        file.write('directory: ' + direc + '\n')
        file.write('Analysis carried out: ' +
                   datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '\n')

        file.write('\n\n**************  OPTIONS **************\n\n')

        for key, value in options.items():
            file.write('%s: %s\n' % (key, value))

        file.write('\n\n**************  VARIABLES **************\n\n')

        for key, value in variables.items():
            file.write('%s: %s\n' % (key, value))

        file.close()
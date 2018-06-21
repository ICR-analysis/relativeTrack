# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-06-21

"""
import pandas as pd


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

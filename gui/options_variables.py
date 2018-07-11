"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-07-10

"""


def opt_initialise():
    opt_names = [
        'savecsv',
        'save_vars',
        'plot_inter_temporal',
        'plot_inter_static',
        'plot_final_summary',
        'cutFarCells',
        'bleach_correction',
        'mult_obj_support',
        'test',
    ]

    opt_prompts = [
        'Save results as .csv?',
        'Save analysis options as .txt?',
        'Plot intermediate results (dynamic)?',
        'Plot intermediate results (static)?',
        'Plot final results?',
        'Remove distant cells?',
        'Correct for bleaching?',
        'Multiple object support?',
        'Testing?',
    ]

    opt_defaults = [
        False,
        False,
        False,
        False,
        False,
        True,
        True,
        False,
        False,
    ]

    return opt_names, opt_prompts, opt_defaults


def var_initialise():
    var_names =[
        'diameter',
        'minFluroMass',
        'maxFluroMass',
        'obj_thresh_adj',
        'obj_thresh_smooth',
        'staticSearchRad',
        'noise_smooth',
        'crop_ratio_mult_obj',
    ]

    var_prompts = [
        'Estimated cell diameter (pixels)',
        'Minimum cell fluorescence mass',
        'Maximum cell fluorescence mass',
        'Large object threshold adjustment',
        'Large object thresholding smoothing',
        'Analysis radius (pixels from object centre)',
        'Noise removal (cell image smoothing width)',
        'Fraction of centre for multiple object support (0 to disable)',
                    ]

    var_defaults = [
        31,
        5000,
        100000,
        0.9,
        40,
        500,
        15,
        0.6,
    ]

    return var_names, var_prompts, var_defaults


def var_force(variable_dict):
    if 'diameter' in variable_dict.keys():
        if variable_dict['diameter'] % 2 == 0:
            variable_dict['diameter'] = variable_dict['diameter'] +1

    return variable_dict

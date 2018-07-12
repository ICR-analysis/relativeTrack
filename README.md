## relativeTrack
Work in progress.
##### Adam Tyson | 2018-07-11 | adam.tyson@icr.ac.uk

#### Measures (bulk, i.e. not individual) cell motion with respect to a central, large object. Despite the name, it no longer tracks anything, but trackpy does a great job at this, if needed.

##### Probably requires Python > 3.5
	numpy
	scipy
	pandas
	scikit-image
	matplotlib
	tk
	seaborn
	pims
	numba (optional)
	trackpy (v0.33)
	
	
## Instructions (install):
1. Download [anaconda](https://www.anaconda.com/download/) or [miniconda](https://conda.io/miniconda.html)
2. Set up a conda environment (e.g. by opening "Anaconda Prompt") and run:
	`conda create --name relativeTrack numpy scipy pandas scikit-image matplotlib tk seaborn pims numba trackpy-0.3.3` then 
	`source activate coloc3DT`
3. Clone or download repository (e.g. **Clone or download -> Download ZIP**, then unzip **relativeTrack-master.zip**)
4. Navigate to `/relativeTrack` in terminal, or in IDE (e.g. PyCharm, Spyder)
5. Run main program `python relativeTrack.py`
	
## Instructions (use):

1. Export 2D maximum projection timelapses as multipage tiff (default if <4GB in Slidebook), one image per channel. All images can be saved into the same directory.
    * The central object image must end  **C0.tif** and cell image must end **C1.tif** (can obviously be changed)
	
2. Confirm or change options (the defaults can be changed in `relativeTrack.gui.options_variables`:
	* **Save results as .csv?** - save all generated parameters to a csv file. One column per timelapse, one file per parameter
	* **Save analysis options as .txt?** - saves all chosen options and parameters to a .txt file to be reused
	* **Plot intermediate results (dynamic)?** - plot scroll plots to assess object segmentation and cell detection
	* **Plot intermediate results (static)?** - static figures to show segmentation and intermediate results
	* **Plot final results?** - plot final results (all image's results overlaid)
	* **Remove distant cells?** - only analyse cells in a circle centred on the object
	* **Correct for bleaching?** - correct for the effect of bleaching for object detection
	* **Multiple object support?** - options to select a single object if more than one exist in the image
	* **Testing?** - only analyses the first 5 frames from the timelapse
	
3. Confirm or change variables (the defaults can be changed in `relativeTrack.gui.options_variables`:
	* **Estimated cell diameter (pixels)** - rough estimate of the cell diameter
	* **Minimum cell fluorescence mass** - cut off, "cells" with lower than this are not included in the analysis.
	* **Maximum cell fluorescence mass** - cut off, "cells" with higher than this are not included in the analysis.
	* **Large object threshold adjustment** - arbitrary threshold multiplier. Increase to be more stringent (and vice versa)
	* **Large object thresholding smoothing** - smoothing magnitude forobject segmentation. To reduce heterogeneity in the object, and allow it to be segmented as a whole.
	* **Analysis radius (pixels from object centre)** - parameter for the **Remove distant cells?** option. 
	* **Noise removal (cell image smoothing width)** - useful to remove very small, but bright objects (e.g. camera noise)
	* **Fraction of centre for multiple object support (0 to disable)** If selecting one object from many, use this to "focus" the search into the centre of the field of view.
                  
	
The script will then run through all images corresponding to a string (e.g. '*C0.tif'), and will find the corresponding C1 images for all timelapses. This data will be loaded, the cells will be detected (subject to the parameters above), and the object will be detected. Various descriptors of object size, and cell position will be calculated and saved, along with the analysis parameters. The static and final plots will be shown, followed by the dynamic plots. These will be shown one at a time, close one to see the next. Details about the analysis will be printed. 
 

## Outputs:
* **analysis_options.txt** - all options and variables defined above
* **area_object.csv** - total area of object over time
* **num_cells_total.csv** - total number of cells included in analysis over time
* **num_cells_in_obj.csv** - total number of cells in object over time

### TODO:
* Save distances from all cells to object
* Save generated plots and segmented images
* Add 3D support
* Allow various thresholding options (e.g. re-use absolute values from previous analysis)
* Interactive segmentation (see effect of parameters in real time)
* Option to re-use analysis parameters (read **analysis_options.txt**)
* Add option in GUI to define filenames (e.g. T0_C0 vs Time_0_Channel_0)
* Parallel option
* Move all options to GUI

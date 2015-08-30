# pyIBGraph
(Pronounced pie-B-graph.)

A program to draw IB Physics (2016 syllabus) style graphs, powered by Python 3, LaTeX, matplotlib and NumPy.

Min/max lines are drawn by finding the centre of the data and progressively increasing/decreasing the slope of the line through this point until it encompasses all desired points (by default, the caps of the error bars).

If the min/max lines appear to miss the caps slightly, increase `MINMAX_TRIES` in the script.

## Dependencies
Arch Linux package dependencies:
- python-matplotlib
  - pulls in python and python-numpy
- texlive-latexextra (various packages required)
  - pulls in texlive-core (lualatex, TeX Gyre fonts and various core packages required)

## Configuration and Usage
pyIBGraph reads data from a four-column comma-separated .csv file, with each data point being one row of the data file. The columns are the *x*-coordinate, the uncertainty in the *x*-coordinate, the *y*-coordinate, and the uncertainty in the *y*-coordinate.

Settings for the program are located at the top of the script:
- **`DATA_FILE`**: the name of the .csv file to read data from (e.g. `"data.csv"`)
- **`OUTPUT_NAME`**: the name of the .pdf file to output the graph to (e.g. `"graph.pdf"`)
- **`X_Q`**, **`Y_Q`**: the symbol or name for the *x*/*y* variable, as a LaTeX math-mode expression (e.g. `"P^{-1}"`)
- **`X_U`**, **`Y_U`**: the unit for the *x*/*y* variable, as a LaTeX math-mode expression (e.g. `"kPa^{-1}"`)
  - Use `""` if dimensionless.
- **`EQ_POS`**: the position for the R-squared value and equations of the lines of best fit (e.g. `"upper left"`)
- **`LEG_POS`**: the position for the legend (e.g. `"lower right"`)
- **`SWING_MODE`**: the mode for calculating the minimum and maximum lines through the data
  - `"cap"`: swing the lines to encompass the caps of all error bars
  - `"corner"`: swing the lines to encompass all corners formed by the error bars
  - `"bar"`: swing the lines to encompass all individual error bars, excluding caps
  - `"ends"`: draw a line from the top-left/bottom-right corner formed by the error bars of the leftmost data point, to the bottom-right/top-left corner formed by the error bars of the rightmost data point (pre-2016 style)
- **`SWING_CENTRE`**: the mode for calculating the middle of the data through which to swing the minimum and maximum lines
  - Use `""` if using `SWING_MODE = "ends"`.
  - `"middle"`: use the point on the line of best fit at the middle of the *x* data ((*x*<sub>max</sub> + *x*<sub>min</sub>) / 2)
  - `"mean"`: use the point on the line of best fit at the mean of the *x* data
  - `"median"`: use the point on the line of best fit at the median of the *x* data
- **`ERRORBAR_CAP_SIZE`**: the size of the error bar caps, in points (e.g. `3`)
- **`MINMAX_TRIES`**: number of tries to attempt to swing the error bars (e.g. `3`)
  - Use `1` if using `SWING_MODE = "ends"`.

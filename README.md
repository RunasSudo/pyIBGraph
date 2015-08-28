# pyIBGraph
(Pronounced pie-B-graph.)

A program to draw IB Physics (2016 syllabus) style graphs, powered by Python 3, matplotlib and NumPy.

Min/max lines are drawn by finding the centre of the data (max-min / 2) and progressively increasing/decreasing the slope of the line through this point until it encompasses the caps of all error bars.

If the min/max lines appear to miss the caps slightly, increase MINMAX_TRIES in the script.

## Dependencies
Arch Linux package dependencies:
- python-matplotlib
- texlive-core
- texlive-latexextra

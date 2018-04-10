# plotui
## Running the program
Run the program with the file "PlotUI/plotui/main.py" OR from the shell by typing "bash" when your current directory is "./PlotUI/bin".
## Using the program
### Graph Options
#### Label Options
- **[Add title]**: Adds a title to the graph from the adjacent entry box.
- **[Add x-axis label]**: Adds a label to the x-axis from the adjacent entry box.
- **[Add y-axis label]**: Adds a label to the y-axis from the adjacent entry box.
#### Scaling Options
- **[Scale]**: Scales the axis according to limits defined in the above entry boxes.
- **[Autoscale]**: Calculates the axis limits from the maximum/minimum values of all plotted functions, and scales the axis according to these values.
#### Tick Options
- TODO
### Export Options
- **[Export type]**: Use the radio buttons to select your desired export type.
  - **PNG image**: Exports the graph as a png image.
  - **LaTeX dat file**: Exports the graph as a dat file for use with the LaTeX package pgfplots.
    - **[Export mode]**: Currently the export function prints all plot data to a file, separating sets with a new line. See TODO.md for future implementations.
- **[File name]**: The output file name. A relevant extension will be appended.
- **[Export]**: Exports the graph as the selected format.
### Plot Options
- **[Add plot]**: Adds a line to the graph. The function of the line is selected from the adjacent drop down box.
#### Plots
- **[Legend]**: This checkbox chooses whether to display a legend for the given line or not. The legend value is defined by the adjacent entry box.
- **[Redraw plot]**: Redraws the line from the user inputted values.
- **[X variable]**: Defines which x variable to plot from a given plot function.
- **[Y variable]**: Defines which y variable to plot from a given plot function.
- **[Range]** : Defines the range over which to plot a given variable.
### Plot Types
The following plot types can be plotted.
- **Straight Line**
  - Plots a straight line to the graph over the specified ranges.
- **Model 1**
  - Implemented most of the dependant/independant variables, still some TODO.

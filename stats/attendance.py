import pandas as pd
import matplotlib.pyplot as plt

from data import games #import games from data.py
# Select Attendance
# The games DataFrame contains the attendance for each game. An attendance row looks like this:
# type multi2    multi3 ... year
# info attendance  45342 ... 1946
# We need to select all of these rows, so below the import statements select these rows using loc[] with the conditions:
# games['type'] == 'info'
# games['multi2'] == 'attendance'
# Select only the year, and multi3 columns.
# loc[] returns the new selection as a DataFrame. Call this new DataFrame attendance.
attendance = games.loc[(games['type'] == 'info') & (games['multi2'] == 'attendance'), ['year', 'multi3']]
# Column Labels
# The attendance DataFrame only has two columns now. Change the labels of these columns to year and attendance with the columns property.
attendance.columns = ['year', 'attendance']
# Convert to Numeric
# Select all rows and just the attendance column of the attendance DataFrame with the loc[] function.
# Hint: dataframe.loc[:, 'column']
# Assign to this selection the result of calling pd.to_numeric().
# As an argument to the pd.to_numeric() function call, pass in the same loc[] selection as above.
# Hint: selection = pd.to_numeric(selection)
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[:, 'attendance'])
# Plot DataFrame
# Call plot() on the attendance DataFrame with the keyword arguments x='year', y='attendance', figsize=(15, 7) and kind='bar'.
# To show the plot you will need to call plt.show(). Hint: plt is an alias for matplotlib.pyplot which was imported earlier.
attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')
# Axis Labels
# To add a bit of polish to the plot, change the x-axis and y-axis labels.
# Above plt.show(), use the plt.xlabel() function to add an x-axis label of Year.
# Change the y-axis label to Attendance using plt.ylabel().
plt.xlabel('Year')
plt.ylabel('Attendance')
# Mean Line
# Add code below the axis labels to draw a dashed green line perpendicular to the x-axis at the mean.
# Hint: Use the plt.axhline() function, the dataframe['column'].mean() function, and the keyword arguments of plt.axhline(): label, linestyle, and color.
plt.axhline(y=attendance['attendance'].mean(), label='Mean', linestyle='--', color='green')
#show attendance
plt.show()

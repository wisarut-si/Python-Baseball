import pandas as pd
import matplotlib.pyplot as plt
from data import games
# Select All Plays
# Open the file called pitching.py, this module's file, in the stats folder. At the top, you will find that pandas and matplotlib have already been imported.
# Import the games DataFrame from data. With access to the games DataFrame we can condense the data to just rows of type play.
# As a shortcut, use games[] to access the DataFrame.In the square brackets, use a conditional to test if the type column's value equals 'play'.
# Store this new DataFrame in a variable called plays.
plays = games[games['type'] == 'play']
# Select All Strike Outs
# Now that we have a DataFrame that includes only plays, let's pare it down even further.
# Select all rows of the plays DataFrame that contain the letter K in the event column.
# To do this use shortcut selection dataframe[] and the str.contains() function. Hint: dataframe[dataframe['column'].str.contains()]
# Call this new DataFrame strike_outs.
strike_outs = plays[plays['event'].str.contains('K')]
# Group by Year and Game
# To plot the strike outs of every game the data needs to be grouped.
# Group the strike_outs DataFrame by year and then game_id. Hint: dataframe.groupby([column1, column2])
# Immediately after the groupby() function, chain a call to the size() function.
# Reassign the result to strike_outs.
strike_outs = strike_outs.groupby(['year', 'game_id']).size()
# Reset Index
# strike_outs is now a groupby object that is grouped by year and game_id. It also contains a new column that contains the number of strike outs in the game.
# To convert this groupby object to a DataFrame and to name the column that was created, use the reset_index() function with a keyword argument of name='strike_outs'.
# Reassign this set of operations to strike_outs.
strike_outs = strike_outs.reset_index(name='strike_outs')
# Apply an Operation to Multiple Columns
# A frequently needed operation when working with DataFrames is to apply a function to multiple columns.
# Select all rows (:), the year, and strike_outs columns of the strike_outs DataFrame with the loc[] function.
# Right after the loc[] function, chain a call to apply() and pass in the function to apply pd.to_numeric. Hint: loc[].apply(function to apply).
# This converts the two selected columns values to numeric. Because apply() returns a new DataFrame, assign the chain dataframe.loc[].apply() to the same variable strike_outs.
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)
# Change Plot Formatting
# To plot the strikes_outs DataFrame, call plot().
# In the call to plot, specify the x-axis as the year, and the y-axis as strike_outs, and use a scatter plot. This is all done with keyword arguments.
# Adjust the legend to say Strike Outs instead of strikes_outs by chaining a call to the legend() function on plot().
# Don't forget to show the plot.
strike_outs.plot( y='strike_outs', x='year', kind='scatter').legend(['Strike Outs'])
plt.show()

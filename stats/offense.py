import pandas as pd
import matplotlib.pyplot as plt
from data import games
# Select All Plays
# In the file called offense.py in the stats folder you will find similar imports as the last module.
# Import the games DataFrame from data.
# Now that we have access to the games DataFrame.
# Select all rows that have a type of play. Use the shortcut method. Hint: square brackets, simple boolean comparison.
# Assign this new DataFrame to a variable called plays.
# To make it easier to access certain columns, label them with the columns property: 'type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', and 'year'.
plays = games[games['type'] == 'play']
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']
# Select Only Hits
# The plays DataFrame now contains all plays from every All-star game.
# The question we want to answer in this plot is: "What is the distribution of hits across innings?"
# For this we need just the hits, singles, doubles, triples, and home runs.
# Use loc[], str.contains() and the regex '^(?:S(?!B)|D|T|HR)' to select the rows where the event column's value starts with S (not SB), D, T, and HR in the plays DataFrame.
# Only return the inning and event columns. Assign the resulting DataFrame to hits.
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning', 'event']]
# Convert Column Type
# Convert the inning column of the hits DataFrame from strings to numbers using the pd.to_numeric() function. Hint: select the column with loc[]
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])
# Replace Dictionary
# The event column of the hits DataFrame now contains event information of various configurations. It contains where the ball was hit and other information that isn't needed. We will replace this with the type of hit for grouping later on.
# Create a dictionary called replacements that contains the following key value pairs
#   r'^S(.*)': 'single'
#   r'^D(.*)': 'double'
#   r'^T(.*)': 'triple'
#   r'^HR(.*)': 'hr'
replacements = {
    r'^S(.*)': 'single',
    r'^D(.*)': 'double',
    r'^T(.*)': 'triple',
    r'^HR(.*)': 'hr'
}
# Replace Function
# Call the replace() function on the hits['event'] column and pass in the replacements dictionary as the first parameter and regex=True as a keyword argument.
# Assign the result which is a DataFrame to hit_type.
hit_type = hits['event'].replace(replacements, regex=True)
# Add A New Column
# We have previously created new columns using groupby and concatenated DataFrames together. This time we will add a new column with assign().
# Below the replace() function, call assign() on the hits DataFrame, and pass in the keyword argument with the new column name and the new column hit_type=hit_type.
# Reassign the new resulting DataFrame to hits.
hits = hits.assign(hit_type=hit_type)
# Group By Inning and Hit Type
# In one line of code, group the hits DataFrame by inning and hit_type, call size() to count the number of hits per inning, and then reset the index of the resulting DataFrame.
# When reseting the index name the newly created column count.
# Since the final function call reset_index() returns a DataFrame make sure you reassign the resulting DataFrame to the variable hits.
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count')
# Convert Hit Type to Categorical
# Since there are only four types of hits let's save some memory by making hits['hit_type'] a categorical column with pd.Categorical().
# Pass a second parameter as a list 'single', 'double', 'triple', and 'hr'. This specifies the order.
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr'])
# Sort Values
# Sort the values in the hits DataFrame by inning and hit_type using the sort_values() function. Remember to reassign this operation to hits.
hits = hits.sort_values(['inning', 'hit_type'])
# Reshape With Pivot
# We need to reshape the hits DataFrame for plotting.
# Call the pivot() function on the hits DataFrame.
# Pass the pivot() function three keyword arguments index='inning', columns='hit_type', and values='count'
# Reassign the result of pivot() to hits.
hits = hits.pivot(index='inning', columns='hit_type', values='count')
# Stacked Bar Plot
# The most appropriate plot for our data is a stacked bar chart. To create this type of plot call plot.bar() with stacked set to True on the hits DataFrame.
# As always, show the plot.
hits.plot.bar(stacked=True)

plt.show()

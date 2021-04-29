import pandas as pd
import matplotlib.pyplot as plt
# Import Existing DataFrames
# In this module we will answer the question: 'What is the DER by league since 1978?'
# Note: 'DER' stands for 'Defensive Efficiency Ratio', and is used as a metric to gauge team defense.
# Open defense.py and keep it open for the duration of the module. Pandas and Matplotlib have been imported.
# For this module there are three DataFrames that have been prepared: games, info and events. Import them from frames.
from frames import games, info, events
# Query Function
# After the import statements, use the query() function to select all rows of the games DataFrame that have a type of play but do not have NP as an event.
# Save the resulting DataFrame as plays.
plays = games.query("type == 'play' & event != 'NP'")
# Column Labels
# Adjust the column labels of the plays DataFrame so they match these values: 'type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year'.
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']
# Shift DataFrame
# There are some spots in the event data where there are consecutive rows that represent the same at bat.
# To calculate plate appearances, which is a factor of DER, these need to be removed.
# To remove these consecutive rows it is best to use the shift() function. The shift() function moves the index a specified amount up or down.
# To select all rows that do not match a consecutive row in the player column use the row condition plays['player'].shift() != plays['player'] in a loc[] function.
# Also, refine the columns to 'year', 'game_id', 'inning', 'team', and 'player'. The resulting DataFrame should be called pa.
pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team', 'player']]
# Group Plate Appearances
# We need to then calculate the plate appearances for each team for each game.
# Below the pa DataFrame use a groupby() function to group the pa DataFrame by 'year', 'game_id', and 'team'.
# As usual on groupby() chain a call to size() to count the plate appearances. After size() chain a call to reset_index(), passing in the right keyword argument to name the newly created column, PA.
# Reassign everything back to pa.
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA')
# Set the Index
# In order to calculate the DER of a team, we need to reshape the data by the type of event that happened at each plate appearance. The event types need to be the columns of our DataFrame. The unstack() function is perfect for this.
# Before we unstack(), the index needs to be adjusted.
# Set the index of the events DataFrame to four columns, 'year', 'game_id', 'team', and 'event_type' with the set_index() function.
# Make sure you reassign the resulting DataFrame to events.
events = events.set_index(['year', 'game_id', 'team', 'event_type'])
# Unstack the DataFrame
# Call unstack() on the events DataFrame. Also, chain two more calls to fillna(0) and reset_index().
# reset_index() returns a DataFrame, so reassign it to events.
events = events.unstack().fillna(0).reset_index()
# Manage Column Labels
# After we unstack() our events DataFrame it will have multiple levels of column labels. Use droplevel() to remove one level.
# droplevel() needs to be called on events.columns and then re-assigned to events.columns.
# Next, change the events DataFrame column labels to the following: 'year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', and 'SO'.
# Lastly, remove the label of the index using rename_axis(). Pass in a label of None and make sure it is on the columns axis.
# This operation returns a new DataFrame so save it to events.
events.columns = events.columns.droplevel()
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']
events = events.rename_axis(None, axis='columns')
# Merge - Plate Appearances
# We now have two DataFrames that have similar columns. The pa DataFrame has year, game_id, team and PA.
# The events DataFrame has year, game_id, and team as well as a column for every event_type. For convenience lets merge them together with pd.merge().
# As the first two arguments pd.merge() requires the two DataFrames to merge, in our case events and pa.
# There are several other keyword arguments that can be used with pd.merge().
# In our case, we will use how set to outer, and both left_on and right_on set to a list of columns to merge on, 'year', 'game_id', and 'team'.
# Like many Pandas functions, pd.merge() returns a DataFrame. Save this one as events_plus_pa.
events_plus_pa = pd.merge(events, pa, how='outer', left_on=['year', 'game_id', 'team'], right_on=['year', 'game_id', 'team'])
# Merge - Team
# events_plus_pa contains almost all of the information we need to calculate the DER of each All-star team.
# The final piece needed is which league was the home team and which was the visiting team.
# The info DataFrame that was imported from frames has already been prepared with the necessary columns and configuration.
# We can do a straight across merge between events_plus_pa and info to add the correct team.
# Call pd.merge() only passing in the two DataFrames to merge. Save the result as defense.
defense = pd.merge(events_plus_pa, info)
# Calculate DER
# Below the pd.merge() call, calculate the DER of each team.
# Add a new column to the defense DataFrame with defense.loc[:, 'DER']
# Set this equal to the calculation: 1 - ((H + ROE) / (PA - BB - SO - HBP - HR)), pulling each of these as a column from the defense DataFrame.
# Convert the year column of the defense DataFrame to numeric values with loc[] and pd.to_numeric().
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) / (defense['PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))
defense.loc[:, 'year'] = pd.to_numeric(defense['year'])
# Reshape With Pivot
# We are only going to plot the DER of the All-star teams in the last 40 years.
# Select these rows of our defense DataFrame with loc[] and a condition of defense['year'] >=  1978. Keep in mind we only need the 'year', 'defense', and 'DER' columns. Assign the resulting DataFrame to der.
# Call pivoton der to adjust the data for plotting. Use the keyword arguments 'index', 'columns' and 'values' in pivot with the correct column labels.
# Reassign the pivot() call to der.
der = defense.loc[defense['year'] >=  1978, ['year', 'defense', 'DER']]
der = der.pivot(index='year', columns='defense', values='DER')
# Plot Formatting - xticks
# For the DER plot, we will use the default line plot type.
# Call plot on der with a few keyword arguments: x_compat set to True, xticks set to a range(1978, 2018, 4), and rotate the labels by 45 degrees with rot=45.
# Show the der plot with plt.show().
der.plot(x_compat=True, xticks=range(1978, 2018, 4), rot=45)

plt.show()

import os
# the OS module in Python provides functions for interacting with the operating system. OS comes under Python’s standard utility modules.
# This module provides a portable way of using operating system-dependent functionality.
# The *os* and *os.path* modules include many functions to interact with the file system
import glob
# module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell,
# although results are returned in arbitrary order. No tilde expansion is done, but *, ?,
# and character ranges expressed with [] will be correctly matched.
# This is done by using the os.scandir() and fnmatch.fnmatch() functions in concert,
# and not by actually invoking a subshell. Note that unlike fnmatch.fnmatch(), glob treats filenames beginning with a dot (.) as special cases.
# (For tilde and shell variable expansion, use os.path.expanduser() and os.path.expandvars().)
import pandas as pd #data frame
# Select all files from games folder by using glob ,'folder','everyfiles*.files_type'
game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))
# Use sort function to sort 'game_files'
game_files.sort()
# The game_files list now contains a sorted list of file names i.e. ['1933AS.EVE', '1934AS.EVE', ..., '2017AS.EVE', '2018AS.EVE']
# To read each of these files into Pandas, create a for in loop that loops through game_files. Call the current file game_fi
# In the body of the for in loop, set a variable called game_frame equal to pd.read_csv(). Pass in the current file game_file as the first argument.
# Now that the current game_file is being passed to pd.read_csv(), add a names keyword argument to the pd.read_csv()call,
# set it equal to a list with the values: 'type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', and 'event'.
game_frames = []
for game_file in game_files:
    game_frame = pd.read_csv(game_file, names=['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)
# Above the for in loop, create an empty list called game_frames.
# In the body of the for in loop below the pd.read_csv() call, append the current game_frame to the game_frames list.
# Concatenate DataFrames
# Below the for in loop create a variable called games and assign it a call to the pd.concat() function. Pass in the list of DataFrames game_frames.
games = pd.concat(game_frames)
# Clean Values
# We now have a large DataFrame called games that contains all of the data from all of the event files. Let's clean up some of the data so that it will not hinder our analysis.
# Use the loc[] function to select rows that have a value of ?? in the multi5 column in the games DataFrame. Replace ?? with an empty string.
# Hint: dataframe.loc[row condition, [columns]] = new value
games.loc[games['multi5'] == '??', ['multi5']] = ''
# Each row of data should be associated with the proper game id. This can be accomplished with the extract() function.
# Below the existing code:
# Select just the multi2 column of the games DataFrame using games['multi2'].
# Call the extract() function of the str namespace on this column. Hint: dataframe['column'].str.extract()
# Pass the regular expression, r'(.LS(\d{4})\d{5})' to the extract() function.
# The extract() function returns a DataFrame, so assign this resulting DataFrame to the variable identifiers.
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
# Forward Fill Identifiers
# The identifiers DataFrame now has two columns. For rows that match the regex, the row has the correct extracted values
# We need these values to be filled in for all rows on the identifiers DataFrame.
# To do this, call the fillna() function on the identifiers DataFrame. Provide a keyword argument to fillna() of method='ffill'.
# Assign the resulting DataFrame back to identifiers.
identifiers = identifiers.fillna(method='ffill')
# Rename Columns
# Let's change the column labels of the identifiers DataFrame.
# Below the fillna() function call, set the columns property of the identifiers DataFrame to a list with the values 'game_id', and 'year'.
identifiers.columns = ['game_id', 'year']
# Concatenate Identifier Columns
# Use pd.concat() to append the columns of the identifiers DataFrame to the games DataFrame.
# Assign the games variable the result of a call to pd.concat()
# Pass three arguments to pd.concat().
# The first argument is the list of the DataFrames to concatenate: [games, identifiers].
# The second and third arguments are the keyword arguments, axis=1, and sort=False.
games = pd.concat([games, identifiers], sort=False, axis=1)
# Fill NaN Values
# Fill in all NaN values in the games DataFrame with ' ' using the fillna() function.
# Don't forget to reassign the resulting DataFrame to games.
games = games.fillna(' ')
# Categorical Event Type
# To slightly reduce the memory used by the games DataFrame we can provide Pandas with a clue to what data is contained in certain columns.
# The type column of our games DataFrame only contains one of six values - info, start, play, com, sub, and data. Pandas can optimize this column with Categorical().
# Select all rows and just the type column with the loc[] function. Hint: use the : wildcard .
# Assign this the result of pd.Categorical(), passing in a call to games.loc[] with the same row and column selection.
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])
# Print DataFrame
# To ensure that the games DataFrame contains the correct data, print the first five rows to the terminal.
print(games.head())

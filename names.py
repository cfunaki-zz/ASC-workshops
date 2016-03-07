# F9 key runs the currently selected portion of code

import pandas as pd
import numpy as np

# Set the file path for your data files
directory = 'C:/Users/Chris/Documents/ASC/Workshops/Birth names'

# Load text file into DataFrame
headers = ['name', 'sex', 'births']
names = pd.read_csv('%s/yob2010.txt' % directory, names=headers)

# Access a column using [] notation
names['name']
# Can similarly be done using dot notation
names.sex

# Access row (known as index) using [] notation
names[0:1]
names[:10]
boy_names = names[names.sex == 'M']
girl_names = names[names.sex == 'F']

# Use both methods to grab individual item
# Column then row indexer
names.sex[10]

# Summary statistics using .describe()
names.describe()

# Total births by gender
names.groupby('sex').births.sum()

names.pivot_table('births', columns='sex', aggfunc=sum)

# Let's compile all of the years of data together
# To do so we need to pull each file consecutively
years = range(1880, 2011, 10)
pieces = []

# Add data for each year to pieces
for year in years:
    path = '%s/yob%d.txt' % (directory, year)
    frame = pd.read_csv(path, names=headers)
    frame['year'] = year
    pieces.append(frame)
# Concatenate all pieces into a single DataFrame
names = pd.concat(pieces, ignore_index=True)

# Check beginning and end of dataframe
names.head()
names.tail()

# Aggregate total births for each year and gender grouping
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
total_births.tail()

# Line plot of births for males and females across the years
total_births.plot(title='Total births by sex and year')

# Proportion of births with given name for each gender and each year
# Function for adding a proportion variable
def add_prop(group):
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group
names = names.groupby(['year', 'sex']).apply(add_prop)

# Check that the proportions add up to 1 for each group
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

# Function to get top 1000 most popular names from each year/sex grouping
def get_top1000(group):
	return group.sort_index(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)

# Separate boys and girls into different DataFrames
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

# Sum total births for each name and year grouping
# This data contains years as the x variable, as time series data
total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)

# Subset the total births for specific names and make a plot for each name
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12,10), grid=False, title="Number of births per year")

# Look at proportion of names
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

# Only boys names in year 2010
df = boys[boys.year == 2010]

# Get cumulative sum of proportion
prop_cumsum = df.sort_index(by='prop', ascending=False).prop.cumsum()
# First top 10 names make up 9% of total names
prop_cumsum[:10]

# How many names does it take to get to 50% of all boys names?
int(prop_cumsum.searchsorted(0.5)) + 1
# 117 names

# Now let's check out 1900
df = boys[boys.year == 1900]
in1900 = df.sort_index(by='prop', ascending=False).prop.cumsum()
int(in1900.searchsorted(0.5)) + 1
# Only takes 25 names to get to 50%

# We can make a general function for this
def get_quantile_count(group, q=0.5):
	group = group.sort_index(by='prop', ascending=False)
	return int(group.prop.cumsum().searchsorted(q)) + 1

# Now we have a DataFrame for diversity of names for each year
diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

diversity.head()

# Graph it
diversity.plot(title='Number of popular names in top 50%')


# Get last letter from name column
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

# Table with each letter, and count for each year and sex grouping
table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)

# Let's look at 3 representative years across the data
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
subtable.head()

# Find the proportion of each last letter used within each year/sex grouping
subtable.sum()
letter_prop = subtable / subtable.sum().astype(float)

# Graph of last letters changing across the years
letter_prop['M'].plot(kind='bar', title='Male')
letter_prop['F'].plot(kind='bar', rot=0, title='Female')

# Get table for all years
letter_prop = table / table.sum().astype(float)

# Now subset by letters, rather than years, and transpose
# This gives us time series data, where years are the x axis
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
dny_ts.head()
dny_ts.plot()


# Check for all variations of the name Lesley by checking which names start with 'lesl'
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
lesley_like

# Filter only names that are in the lesley_like array
filtered = top1000[top1000.name.isin(lesley_like)]
# How often does each name occur?
filtered.groupby('name').births.sum()

# Get table of proportion of male and female Lesley names by year
table = filtered.pivot_table('births', index='year', columns='sex', aggfunc=sum)
table = table.div(table.sum(1), axis=0)
# Graph as a time series plot
table.plot()
# Lesley used to be a predominantly male name
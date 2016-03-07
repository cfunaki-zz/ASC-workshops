x = 5
type(x)

five = '5'
type(five)

11 / x # Integer division drops decimal

x = float(5)

11 / x

five = str(five)
type(five)

# Concatenate strings using the plus sign
hello = 'He' + 'llo'
print hello

# You can concatenate using string variables too!
phrase = five + ' hours'
print phrase


# List of numbers
y = [1, 2, 3, 4]
type(y)

# Indexing lists
y[0] # first index
y[1] # second index
y[2] # third index

y[:] # all indices
y[1:] # all indices second onward
y[:2] # all indices up to 2
y[1:3]
y[-1]

y[0] + y[2]

# Create a 3x3 matrix of numbers
A = [[1,2,3], [11,12,13], [21,22,23]]

import pandas as pd
# Put the matrix into a DataFrame
df = pd.DataFrame(data=A, columns=['A', 'B', 'C'])

# Create a 3x3 matrix of numbers
B = [[1,2,3], [11,12,13], [21,22]]

df_B = pd.DataFrame(data=B, columns=['A', 'B', 'C'])

# Indexing from a DataFrame

df['A'] # Get an individual column

df.ix[1] # Get an indidual row

df[1:2] # Another way to retrieve a row

df[1:] # 2nd row onwards

df[0:2] # Index 0 through 1

# Get single data unit
df.ix[1]['A']

df['A'][1]
df['A'][1:]

# Summary statistics
df.describe()

cars = pd.read_csv('mtcars.csv')

cars.describe()

cars['mpg']

cars['mpg'] > 15

high_mpg = cars[cars['mpg'] > 15]

# Two ways to get summary statistics
high_mpg.describe()

high_mpg['mpg'].count()
high_mpg['mpg'].mean()
high_mpg['mpg'].std()
high_mpg['mpg'].min()
high_mpg['mpg'].max()
high_mpg['mpg'].sum()
#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


ls


# In[3]:


import pandas as pd


# In[4]:


import openpyxl


# In[28]:


import numpy as np


# In[96]:


import datetime


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[11]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx",nrows=30000)


# In[8]:


df.head()


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[12]:


df.shape


# In[10]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[ ]:


# All the current active pet licensing data (name, breed, owner address) for New York City as of April 28, 2016


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[ ]:


# What is the most popular breed in your NYC zip code?
# Where is the highest concentration of dogs in NYC?
# What is NYC's favorite dog colors?
# How many dogs in NYC are trained?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[22]:


df['Primary Breed'].value_counts().head(10)


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[26]:


df.dropna(subset=['Primary Breed']).shape


# In[35]:


df['Primary Breed'] = df['Primary Breed'].replace('Unknown', np.nan)


# In[36]:


df


# In[37]:


df.dropna(subset=['Primary Breed'])


# In[38]:


df.dropna(subset=['Primary Breed']).shape


# In[40]:


df['Primary Breed'].value_counts().head(10)


# ## What are the most popular dog names?

# In[51]:


df['Animal Name'].value_counts().head(10)


# In[55]:


df['Animal Name'].replace({
    'UNKNOWN': np.nan,
    'Unknown': np.nan
}).value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[56]:


# No dogs have my name
df[df['Animal Name'] == "Nathalie"]


# In[61]:


# 202 dogs are named Max
df[df['Animal Name'] == "Max"].shape


# In[62]:


# 11 dogs are named Maxwell
df[df['Animal Name'] == "Maxwell"].shape


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[68]:


df.shape


# In[64]:


df['Guard or Trained'].value_counts()


# In[67]:


df['Guard or Trained'].value_counts() / 3000 * 100


# ## What are the actual numbers?

# In[71]:


df['Guard or Trained'].value_counts(dropna=False)


# In[75]:


df['Guard or Trained'].value_counts(dropna=False) / 3000 * 10


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[77]:


# see above


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[82]:


df['Guard or Trained'] = df['Guard or Trained'].replace(np.nan,'No')


# In[83]:


df['Guard or Trained'].value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[95]:


# Including the NaNs to make sure all Yes's are accounted for
df[df['Guard or Trained'] == "Yes"]['Primary Breed'].value_counts(dropna=False)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[97]:


df['Animal Birth']


# In[98]:


df['Year'] = df['Animal Birth'].apply(lambda birth: birth.year)


# In[99]:


df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[104]:


df['Age'] = (2021 - df['Year']) * 7


# In[108]:


df['Age'].mean()


# # Joining data together

# In[ ]:





# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[111]:


df_zips = pd.read_csv("zipcodes-neighborhoods.csv")
df_zips


# In[110]:


df.head(2)


# In[114]:


df = df.merge(df_zips, left_on='Owner Zip Code', right_on='zip')


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[134]:


df['Animal Name'].replace('Unknown',np.nan)


# In[139]:


df['Animal Name'] = df['Animal Name'].replace('Unknown',np.nan)


# In[142]:


df['Animal Name'] = df['Animal Name'].replace('UNKNOWN',np.nan)


# In[146]:


df['Animal Name'] = df['Animal Name'].replace('unknown',np.nan)


# In[167]:


df['Animal Name'] = df['Animal Name'].replace('NO NAME',np.nan)


# In[149]:


df['Animal Name'] = df['Animal Name'].replace('Dog Name Not Provided',np.nan)


# In[147]:


df[df.borough == "Bronx"]['Animal Name'].value_counts(dropna=True).head(10)


# In[150]:


df[df.borough == "Brooklyn"]['Animal Name'].value_counts(dropna=True).head(10)


# In[165]:


# Checking neighborhoods within Manhattan
df_zips[df_zips['borough'] == "Manhattan"]


# In[168]:


df[df.neighborhood == "Upper East Side"]['Animal Name'].value_counts(dropna=True).head(10)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[191]:


df.head(2)


# In[213]:


df.groupby(by='neighborhood')['Primary Breed'].value_counts()


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[228]:


# Males are most likely to be spayed
df.groupby(by='Spayed or Neut')['Animal Gender'].value_counts(dropna=False)


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[306]:


color_pattern = 'black|white|grey'
df[
    df['Animal Dominant Color'].str.contains(color_pattern,regex=True,case=False) & \
    df['Animal Secondary Color'].str.contains(color_pattern,regex=True,case=False) & \
    df['Animal Third Color'].str.contains(color_pattern,regex=True,case=False)
]


# In[307]:


len(df[
    df['Animal Dominant Color'].str.contains(color_pattern,regex=True,case=False) & \
    df['Animal Secondary Color'].str.contains(color_pattern,regex=True,case=False) & \
    df['Animal Third Color'].str.contains(color_pattern,regex=True,case=False)
])


# ## How many dogs are in each borough? Plot it in a graph.

# In[240]:


df['borough'].value_counts()


# In[247]:


df['borough'].value_counts().sort_values(ascending=True).plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[249]:


df_pop = pd.read_csv("boro_population.csv")


# In[348]:


df_pop


# In[349]:


df


# In[253]:


df = df.merge(df_pop,left_on='borough',right_on='borough')


# In[293]:


dcp = pd.DataFrame(df.borough.value_counts())


# In[350]:


dcp


# In[296]:


df['borough'].value_counts()


# In[363]:


dcp = dcp.rename(columns={'borough': 'num_dogs'})


# In[374]:


dcp = dcp.merge(df_pop, left_index=True, right_on='borough')


# In[381]:


dcp


# In[380]:


# Manhattan has the highest number dogs per capita
dcp.num_dogs / dcp.population * 100


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[329]:


pd.set_option("display.max_columns", None)


# In[343]:


groups = df.groupby(by='borough')['Primary Breed']


# In[342]:


df.groupby(by='borough')['Primary Breed'].value_counts(ascending=False)


# In[347]:


for borough, breed in groups:
    print(borough)
    print(breed.value_counts().head())


# ## What percentage of dogs are not guard dogs?

# In[183]:


df['Guard or Trained'].value_counts() / 30000 * 100


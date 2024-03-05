# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 19:07:11 2024

@author: howoo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------
# Data wrangling
# ---------------------------------

# Define data path
path_data = 'C:/Users/howoo/OneDrive/Documents/Personal/Education/Masters/Exeter/04 MTHM604/02 Projects/03 Sustainable Food/01 Data/Doctoral_study_data_for_Devon_schools/Survey_data'

# Import data
school_1a = pd.read_excel(path_data + '/School_1a_2021.xlsx', skiprows=[1])
school_1b = pd.read_excel(path_data + '/School_1b_2021.xlsx', skiprows=[1])
school_2 = pd.read_excel(path_data + '/School_2_2021.xlsx', skiprows=[1])
school_3 = pd.read_excel(path_data + '/School_3_2021.xlsx', skiprows=[1])

# Add columns to 1b to make consistent with 1a and 2
school_1b['Q5_2_TEXT'], school_1b['Q6_2_TEXT'] = np.nan, np.nan

# Add school names
school_1a['School'] = '1a'
school_1b['School'] = '1b'
school_2['School'] = '2'

# Append 1a, 1b and 2
df_schools = school_1a.append(school_1b).append(school_2)

# Cleanse Q36: support for meat-free days
set(df_schools['Q36']) # Check unique values
df_schools['Q36'].replace(['It depends, please specify:'], ['Depends'], inplace=True)
set(df_schools['Q36']) # Check unique values

# Cleanse Q37: frequency of meat-free days
set(df_schools['Q37']) # Check unique values
df_schools['Q37'] = df_schools['Q37'].map(
    {'More than three days/ week ': '>3',
    'One day/ week ': 1,
    'Other. Please add/ elaborate on your answer further.': 'Other',
    'Three days/ week ': 3,
    'Two days/ week ': 2,
    'nan': np.nan})
set(df_schools['Q37']) # Check unique values

# Cleanse Q4: ethnicity
set(df_schools['Q4']) # Check unique values
df_schools['Q4'] = df_schools['Q4'].map(
    {'Asian /Asian British- Indian, Pakistani, Bangladeshi, other': 'Asian',
     'Black/Black British – Caribbean, African, other': 'Black',
     'Chinese / Chinese British': 'Chinese',
     'Middle Eastern/ Middle Eastern British – Arab, Turkish, other': 'Middle Eastern',
     'Mixed race- White and Black/ Black British': 'Mixed - White and Black',
     'Mixed race- other': 'Mixed - Other',
     'Other ethnic group': 'Other',
     'Prefer not to say': 'Not provided',
     'White – British, Irish, other': 'White',
     'nan': np.nan})
set(df_schools['Q4']) # Check unique values


# ---------------------------------
# Exploratory analysis
# ---------------------------------

# Plot proportion of responses to meat-free days by school

# Calculate proportion of each response and unstack
props_school = df_schools.groupby('School')['Q36'].value_counts(normalize=True).unstack()
props_school = props_school[['Yes', 'No', 'Depends']] # Reorder columns

# Plot bar graph
ax = props_school.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion')
ax.set_title('Q36: Do meat-free days* sound like a good idea to you?')
ax.legend(title = None, bbox_to_anchor=(1, 1))

plt.show()



# Plot proportion of responses to meat-free days by ethnicity

# Calculate counts of each response and unstack (to check sample size)
counts_ethnicity = df_schools.groupby('Q4')['Q36'].value_counts(normalize=False).unstack()
counts_ethnicity = counts_ethnicity[['Yes', 'No', 'Depends']] # Reorder columns

# Calculate proportion of each response and unstack
props_ethnicity = df_schools.groupby('Q4')['Q36'].value_counts(normalize=True).unstack()
props_ethnicity = props_ethnicity[['Yes', 'No', 'Depends']] # Reorder columns

# Plot bar graph
ax = props_ethnicity.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion')
ax.set_title('Q36: Do meat-free days* sound like a good idea to you?')
ax.legend(title = None, bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)

plt.show()





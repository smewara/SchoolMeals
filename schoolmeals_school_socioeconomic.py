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
df_schools['Q36_Cleansed'] = df_schools['Q36'].map(
    {'It depends, please specify:': 'Depends',
     'No': 'No',
     'Yes': 'Yes',
     'nan': np.nan})
set(df_schools['Q36_Cleansed']) # Check unique values

# Cleanse Q37: frequency of meat-free days
set(df_schools['Q37']) # Check unique values
df_schools['Q37_Cleansed'] = df_schools['Q37'].map(
    {'More than three days/ week ': '>3',
    'One day/ week ': 1,
    'Other. Please add/ elaborate on your answer further.': 'Other',
    'Three days/ week ': 3,
    'Two days/ week ': 2,
    'nan': np.nan})
set(df_schools['Q37_Cleansed']) # Check unique values

# Cleanse Q4: ethnicity
set(df_schools['Q4']) # Check unique values
df_schools['Ethnicity'] = df_schools['Q4'].map(
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
set(df_schools['Ethnicity']) # Check unique values

# Cleanse Q3: stakeholder
set(df_schools['Q3']) # Check unique values
set(df_schools['Q3_4_TEXT']) # Check unique values
# Step 1: Cleanse Q3
df_schools['Stakeholder'] = df_schools['Q3'].map(
    {'A caterer at a primary school': 'Staff - Other',
     'A parent/ carer of primary school children': 'Parent/Carer',
     'Other': 'Other',
     'Senior leadership management team member at a primary school': 'Staff - Other',
     'Teacher/ teaching assistant at a primary school': 'Staff - Teaching',
     'nan': np.nan})
# Step 2: Replace 'Other' with 'Yes', 'No' or nan depending on free text
df_schools['Stakeholder'] = np.where(
    df_schools['Stakeholder'] == 'Other',
    df_schools['Q3_4_TEXT'].map(
        {'A parent of one primary aged child. ': 'Parent/Carer',
         'Administrator of school lunches': 'Staff - Other',
         'Producer/farmer': np.nan,
         'nan': np.nan}),
    df_schools['Stakeholder'])
# Check unique values
set(df_schools['Stakeholder']) # Check unique values


# Cleanse Q17: payment for school meals (parents/carers only)
set(df_schools['Q17']) # Check unique values
set(df_schools['Q17_4_TEXT']) # Check unique values when Q17 is 'Other'
# Step 1: Cleanse Q17
df_schools['FSM_Eligibility'] = df_schools['Q17'].map(
    {'No, my child(ren) is/are eligible for free school meals': 'Yes',
     'No, my child(ren) is/are in KS1 ( reception, year 1 or year 2)': np.nan, # Can't tell whether child would be eligible for FSM
     'Other, please specify below:': 'Other',
     'Yes': 'No',
     'nan': np.nan})
# Step 2: Replace 'Other' with 'Yes', 'No' or nan depending on free text
df_schools['FSM_Eligibility'] = np.where(
    df_schools['FSM_Eligibility'] == 'Other',
    df_schools['Q17_4_TEXT'].map(
        {"Doesn't have school meals": np.nan,
         'For the first child': 'No',
         'I pay for one child, but not the other who is in KS1': 'No',
         'If they had school meals I would have to pay. ': 'No',
         'No school meals': np.nan,
         'No they never eat them': np.nan,
         'No, we don’t pay for school meals and not eligible for free school meals': 'No',
         'None in reception': np.nan,
         'One is free due to foundation year, the other is year 3 and we pay': 'No',
         'Pay for first child, don’t pay for 2nd as yr 1': 'No',
         'Take own packed lunch': np.nan,
         'We supply her with a packed lunch': np.nan,
         'Would have to for the older in KS2 but not the younger ones ': 'No',
         'nan': np.nan}),
    df_schools['FSM_Eligibility'])
# Check unique values
set(df_schools['FSM_Eligibility']) 


# ---------------------------------
# Exploratory analysis
# ---------------------------------

# Plot proportion of responses to meat-free days by school

# Calculate counts of each response and unstack (to check sample size)
counts_school = df_schools.groupby('School')['Q36_Cleansed'].value_counts(normalize=False).unstack()
counts_school = counts_school[['Yes', 'No', 'Depends']] # Reorder columns

# Calculate proportion of each response and unstack
props_school = df_schools.groupby('School')['Q36_Cleansed'].value_counts(normalize=True).unstack()
props_school = props_school[['Yes', 'No', 'Depends']] # Reorder columns

# Plot bar graph
ax = props_school.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion')
ax.set_title('Q36: Do meat-free days* sound like a good idea to you? \n Comparison by school')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()



# Plot proportion of responses to meat-free days by ethnicity

# Calculate counts of each response and unstack (to check sample size)
counts_ethnicity = df_schools.groupby('Ethnicity')['Q36_Cleansed'].value_counts(normalize=False).unstack()
counts_ethnicity = counts_ethnicity[['Yes', 'No', 'Depends']] # Reorder columns

# Calculate proportion of each response and unstack
props_ethnicity = df_schools.groupby('Ethnicity')['Q36_Cleansed'].value_counts(normalize=True).unstack()
props_ethnicity = props_ethnicity[['Yes', 'No', 'Depends']] # Reorder columns

# Plot bar graph
ax = props_ethnicity.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Ethnicity')
ax.set_ylabel('Proportion')
ax.set_title('Q36: Do meat-free days* sound like a good idea to you? \n Comparison by ethnicity')
ax.legend(title = None, loc='upper center')
plt.xticks(rotation=45)

plt.show()




# Plot proportion of responses to meat-free days by stakeholder

# Create categorical column
df_schools['Stakeholder'] = pd.Categorical(df_schools['Stakeholder'],
                                           categories=['Parent/Carer', 'Staff - Teaching', 'Staff - Other'],
                                           ordered=True)

# Calculate counts of each response and unstack (to check sample size)
counts_stakeholder = df_schools.groupby('Stakeholder')['Q36_Cleansed'].value_counts(normalize=False).unstack()
counts_stakeholder = counts_stakeholder[['Yes', 'No', 'Depends']] # Reorder columns

# Calculate proportion of each response and unstack
props_stakeholder = df_schools.groupby('Stakeholder')['Q36_Cleansed'].value_counts(normalize=True).unstack()
props_stakeholder = props_stakeholder[['Yes', 'No', 'Depends']] # Reorder columns

# Plot bar graph
ax = props_stakeholder.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Stakeholder')
ax.set_ylabel('Proportion')
ax.set_title('Q36: Do meat-free days* sound like a good idea to you? \n Comparison by stakeholder')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()




# Plot proportion of responses to meat-free days by FSM eligibility

# Calculate counts of each response and unstack (to check sample size)
counts_fsm = df_schools.groupby('FSM_Eligibility')['Q36_Cleansed'].value_counts(normalize=False).unstack()
counts_fsm = counts_fsm[['Yes', 'No', 'Depends']] # Reorder columns

# Calculate proportion of each response and unstack
props_fsm = df_schools.groupby('FSM_Eligibility')['Q36_Cleansed'].value_counts(normalize=True).unstack()
props_fsm = props_fsm[['Yes', 'No', 'Depends']] # Reorder columns

# Plot bar graph
ax = props_fsm.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Eligible for free school meals')
ax.set_ylabel('Proportion')
ax.set_title('Q36: Do meat-free days* sound like a good idea to you? \n Comparison by eligibility for free school meals')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()



# Contingency table between ethnicity and FSM eligibility
ethnicity_fsm = pd.crosstab(index=df_schools['Ethnicity'].fillna('NA'),
                            columns=df_schools['FSM_Eligibility'].fillna('NA'),
                            margins=True)
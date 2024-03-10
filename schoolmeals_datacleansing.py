import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------
# Data wrangling
# ------------------------------------------------------------------

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
school_1a['School'] = "1a: St Leonard's"
school_1b['School'] = "1b: Trinity"
school_2['School'] = "2: Doddiscombsleigh"

# Append 1a, 1b and 2
df_schools = pd.concat([school_1a, school_1b, school_2], ignore_index = True)

# Cleanse Q36: support for meat-free days
# Check unique values
set(df_schools['Q36'])
# Cleanse Q36
df_schools['Q36_Cleansed'] = df_schools['Q36'].map(
    {'It depends, please specify:': 'Depends',
     'No': 'No',
     'Yes': 'Yes',
     'nan': None})
# Categorical column
df_schools['Q36_Cleansed'] = pd.Categorical(df_schools['Q36_Cleansed'],
                                            categories=['Yes', 'No', 'Depends'],
                                            ordered=True)
# Check unique values
set(df_schools['Q36_Cleansed'])


# Cleanse Q37: frequency of meat-free days
# Check unique values
set(df_schools['Q37']) 
set(df_schools['Q37_5_TEXT'])
# Step 1: Cleanse Q37, conservative approach taken (e.g. 2-3 would become 2)
df_schools['Q37_Numeric'] = df_schools['Q37'].map(
    {'More than three days/ week ': 4,
    'One day/ week ': 1,
    'Other. Please add/ elaborate on your answer further.': 'Other',
    'Three days/ week ': 3,
    'Two days/ week ': 2,
    'nan': np.nan})
# Step 2: Replace 'Other' with number or nan depending on free text, this could be used for regression
df_schools['Q37_Numeric'] = np.where(
    df_schools['Q37_Numeric'] == 'Other', df_schools['Q37_5_TEXT'].map(
        {'1 or 1 + fish': 1,
         '2 or 3 days a week sounds good to me': 2,
         'Again, it depends on how much children enjoy it. ': np.nan,
         'As I said previously every day for both ': 5,
         'At least one day a week, but it would probably need a period of more gradual change for young children to make big changes': 1,
         'Daily meat is not necessary in a balanced diet.': np.nan,
         'Depends on what is and becomes socially acceptable over time, and how many school meals a child has in a week. Approximately 1-2 per week based on a child having a school meal 5 times per week seems about right at the moment.': 1,
         'Don’t feel this is a priority': np.nan,
         'I feel it would be better to have a meat and a meat free option': np.nan,
         'I think it should be reversed to be only one meat day per week': 1,
         'I think there should always be a meat/fish option': np.nan,
         'I’d be happy to go meat free so long as it is high quality and varied food options.': 5,
         'Make meals that are tasty and no one will care if there is meat in it. ': np.nan,
         'Meat once a week at school would be reasonable ': 1,
         'My 5 year old is a vegetarian (her own choice) and would like a meat free option every day!': np.nan,
         'One to begin with': 1,
         'Prefer to be guided by what the evidence suggests for sustainable and environmentally friendly and what parents and children feel is acceptable. Personally I aim for 3 days but for some that will be too much and for others too little.': np.nan,
         'every day there should be a meat free option, I worry having more than one entirely meat free day might put more people off': 1,
         'nan': np.nan}),
    df_schools['Q37_Numeric'])
# Step 3: Add categorical columnn grouping 4 and 5 days into '4+', this could be used for plots
df_schools['Q37_Bins'] = np.where(df_schools['Q37_Numeric'] > 3, '4+', df_schools['Q37_Numeric'])
df_schools['Q37_Bins'] = pd.Categorical(df_schools['Q37_Bins'],
                                        categories=[1, 2, 3, '4+'],
                                        ordered=True)
# Check unique values
set(df_schools['Q37_Numeric'])
set(df_schools['Q37_Bins'])



# Cleanse Q4: ethnicity
set(df_schools['Q4']) # Check unique values
# Step 1: Add new column abbreviating Q4
df_schools['Ethnicity'] = df_schools['Q4'].map(
    {'Asian /Asian British- Indian, Pakistani, Bangladeshi, other': 'Asian',
     'Black/Black British – Caribbean, African, other': 'Black',
     'Chinese / Chinese British': 'Chinese',
     'Middle Eastern/ Middle Eastern British – Arab, Turkish, other': 'Middle Eastern',
     'Mixed race- White and Black/ Black British': 'Mixed - White and Black',
     'Mixed race- other': 'Mixed - Other',
     'Other ethnic group': 'Other',
     'Prefer not to say': np.nan,
     'White – British, Irish, other': 'White',
     'nan': np.nan})
# Step 2: Add new column mapping ethnic minority groups to 'Ethnic Minority' as there is little data in these groups
df_schools['Ethnicity_2'] = df_schools['Q4'].map(
    {'Asian /Asian British- Indian, Pakistani, Bangladeshi, other': 'Ethnic Minority',
     'Black/Black British – Caribbean, African, other': 'Ethnic Minority',
     'Chinese / Chinese British': 'Ethnic Minority',
     'Middle Eastern/ Middle Eastern British – Arab, Turkish, other': 'Ethnic Minority',
     'Mixed race- White and Black/ Black British': 'Ethnic Minority',
     'Mixed race- other': 'Ethnic Minority',
     'Other ethnic group': 'Ethnic Minority',
     'Prefer not to say': np.nan,
     'White – British, Irish, other': 'White',
     'nan': np.nan})
df_schools['Ethnicity_2'] = pd.Categorical(df_schools['Ethnicity_2'],
                                        categories=['White', 'Ethnic Minority'],
                                        ordered=True)
# Check unique values
set(df_schools['Ethnicity'])
set(df_schools['Ethnicity_2'])


# Cleanse Q3: stakeholder
# Check unique values
set(df_schools['Q3']) 
set(df_schools['Q3_4_TEXT'])
# Step 1: Add new column containing cleansed stakeholder
df_schools['Stakeholder'] = df_schools['Q3'].map(
    {'A caterer at a primary school': 'Staff - Other',
     'A parent/ carer of primary school children': 'Parent/Carer',
     'Other': 'Other',
     'Senior leadership management team member at a primary school': 'Staff - Other',
     'Teacher/ teaching assistant at a primary school': 'Staff - Teaching',
     'nan': np.nan})
# Step 2: Replace 'Other' with stakeholder or nan depending on free text
df_schools['Stakeholder'] = np.where(
    df_schools['Stakeholder'] == 'Other',
    df_schools['Q3_4_TEXT'].map(
        {'A parent of one primary aged child. ': 'Parent/Carer',
         'Administrator of school lunches': 'Staff - Other',
         'Producer/farmer': np.nan,
         'nan': np.nan}),
    df_schools['Stakeholder'])
# Create categorical column
df_schools['Stakeholder'] = pd.Categorical(df_schools['Stakeholder'],
                                           categories=['Parent/Carer', 'Staff - Teaching', 'Staff - Other'],
                                           ordered=True)
# Check unique values
set(df_schools['Stakeholder']) # Check unique values


# Cleanse Q17: whether parents pay for school meals
# Check unique values
set(df_schools['Q17']) 
set(df_schools['Q17_4_TEXT']) # Free text when Q17 is 'Other'
# Step 1: Cleanse Q17
df_schools['FSM_Eligibility'] = df_schools['Q17'].map(
    {'No, my child(ren) is/are eligible for free school meals': 'Eligible',
     'No, my child(ren) is/are in KS1 ( reception, year 1 or year 2)': np.nan, # Can't tell whether child would be eligible for FSM
     'Other, please specify below:': 'Other',
     'Yes': 'Not Eligible',
     'nan': np.nan})
# Step 2: Replace 'Other' with 'Yes', 'No' or nan depending on free text
df_schools['FSM_Eligibility'] = np.where(
    df_schools['FSM_Eligibility'] == 'Other',
    df_schools['Q17_4_TEXT'].map(
        {"Doesn't have school meals": np.nan,
         'For the first child': 'Not Eligible',
         'I pay for one child, but not the other who is in KS1': 'Not Eligible',
         'If they had school meals I would have to pay. ': 'Not Eligible',
         'No school meals': np.nan,
         'No they never eat them': np.nan,
         'No, we don’t pay for school meals and not eligible for free school meals': 'Not Eligible',
         'None in reception': np.nan,
         'One is free due to foundation year, the other is year 3 and we pay': 'Not Eligible',
         'Pay for first child, don’t pay for 2nd as yr 1': 'Not Eligible',
         'Take own packed lunch': np.nan,
         'We supply her with a packed lunch': np.nan,
         'Would have to for the older in KS2 but not the younger ones ': 'Not Eligible',
         'nan': np.nan}),
    df_schools['FSM_Eligibility'])
# Check unique values
set(df_schools['FSM_Eligibility']) 


# Cleanse Q35: how much respondent would be prepared to pay for sustainable school meals
# Check unique values
set(df_schools['Q35'])
set(df_schools['Q35_8_TEXT']) # Free text when Q35 is 'Other'
# Step 1: Cleanse Q35
df_schools['Q35_Cleansed'] = df_schools['Q35'].map(
    {'Other, please specify below:': 'Other',
     '£2.50': 2.5,
     '£2.75': 2.75,
     '£3.00': 3,
     'nan': np.nan})
# Step 2: Replace 'Other' with number or nan depending on free text
df_schools['Q35_Cleansed'] = np.where(
    df_schools['Q35_Cleansed'] == 'Other',
    df_schools['Q35_8_TEXT'].map(
        {' Would pay more dependent on what is on offer. ': np.nan,
         '2.00': 2,
         '3.50': 3.5,
         'As much as is necessary.': np.nan,
         'As teacher just having a meal once in a while yes , but as a parent paying everyday would try to Combine school lunch and packed lunch ': np.nan,
         'But I understand affordability across families will be variable.': np.nan,
         'Depends on quality': np.nan,
         "I can't answer this, as whilst greater cost is fine for me, it might exclude other people. I think it is important that meals are affordable ": np.nan,
         'I would be prepared to pay up to £2.50 but I feel if they changed options such as more meat free days and less sugary puddings per week, they could potentially save money to spent it elsewhere. ': 3,
         'More than £3 if it ticked the boxes from my previous answer': 3,
         'Or up to £5.00': 5,
         'Possibly even more depending on the quality of what was offered. ': np.nan,
         'Provided the portion size is adequate for the different age groups.': np.nan,
         'is this FSM top up? ~£1': 3.35,
         '£2.75 but I would want larger portions really. My daughter eats loads at home and is often hungry at school!': 2.75,
         '£3.50': 3.5,
         '£4': 4,
         '£4.00': 4,
         "£5 if it's worth it": 5,
         'nan': np.nan}),
    df_schools['Q35_Cleansed'])
# Step 3: Calculate premium over current cost of school meals
df_schools['Q35_CurrentCost'] = np.where(
    df_schools['School'] == "1a: St Leonard's", 2.35, np.where(
        df_schools['School'] == "1b: Trinity", 2.2, np.where(
            df_schools['School'] == "2: Doddiscombsleigh", 2.35, np.nan)))
df_schools['Q35_Premium'] = df_schools['Q35_Cleansed'] - df_schools['Q35_CurrentCost']
# Convert to numeric
df_schools['Q35_Premium'] = pd.to_numeric(df_schools['Q35_Premium'], errors='coerce').fillna(np.nan)


# Summarise dataframe
df_schools.info()
df_schools.describe(include = 'all')

# Export csv
df_schools.to_csv('df_schools.csv')


# ------------------------------------------------------------------
# Plots for Q36: Do meat-free days sound like a good idea to you?
# ------------------------------------------------------------------

# Plot support for meat-free days by school

# Calculate counts of each response and unstack (to check sample size)
counts_school = df_schools.groupby('School')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_school = df_schools.groupby('School')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_school.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion of respondents from each school')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by school')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()


# Plot support for meat-free days by school, parents/carers only

# Calculate counts of each response and unstack (to check sample size)
counts_school_pc = df_schools[df_schools['Stakeholder'] == 'Parent/Carer']\
    .groupby('School')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_school_pc = df_schools[df_schools['Stakeholder'] == 'Parent/Carer']\
    .groupby('School')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_school_pc.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion of respondents from each school')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by school, parents/carers only')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()


# Plot support for meat-free days by school, staff only

# Calculate counts of each response and unstack (to check sample size)
counts_school_staff = df_schools[df_schools['Stakeholder'] != 'Parent/Carer']\
    .groupby('School')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_school_staff = df_schools[df_schools['Stakeholder'] != 'Parent/Carer']\
    .groupby('School')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_school_staff.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion of respondents from each school')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by school, staff only')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()




# Plot support for meat-free days by stakeholder

# Calculate counts of each response and unstack (to check sample size)
counts_stakeholder = df_schools.groupby('Stakeholder')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_stakeholder = df_schools.groupby('Stakeholder')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_stakeholder.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Stakeholder')
ax.set_ylabel('Proportion of respondents from each stakeholder group')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by stakeholder')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()




# Plot support meat-free days by ethnicity

# Calculate counts of each response and unstack (to check sample size)
counts_ethnicity = df_schools.groupby('Ethnicity')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_ethnicity = df_schools.groupby('Ethnicity')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_ethnicity.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Ethnicity')
ax.set_ylabel('Proportion of respondents from each ethnic group')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by ethnicity')
ax.legend(title = None, loc='upper center')
plt.xticks(rotation=45)

plt.show()



# Plot support for meat-free days by ethnicity (white and minority)

# Calculate counts of each response and unstack (to check sample size)
counts_ethnicity2 = df_schools.groupby('Ethnicity_2')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_ethnicity2 = df_schools.groupby('Ethnicity_2')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_ethnicity2.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Ethnicity')
ax.set_ylabel('Proportion of respondents from each ethnic group')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by ethnicity')
ax.legend(title = None, loc='upper center')
plt.xticks(rotation=0)

plt.show()




# Plot support for meat-free days by FSM eligibility

# Calculate counts of each response and unstack (to check sample size)
counts_fsm = df_schools.groupby('FSM_Eligibility')['Q36_Cleansed'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_fsm = df_schools.groupby('FSM_Eligibility')['Q36_Cleansed'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_fsm.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('Eligible for free school meals')
ax.set_ylabel('Proportion of respondents from each eligibility group')
ax.set_title('Q36: Do meat-free days sound like a good idea to you? \n Comparison by eligibility for free school meals')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()



# Contingency table between ethnicity and FSM eligibility
ethnicity_fsm = pd.crosstab(index=df_schools['Ethnicity'].fillna('NA'),
                            columns=df_schools['FSM_Eligibility'].fillna('NA'),
                            margins=True)



# Plot additional amount willing to pay vs support for meat-free days

ax = sns.catplot(x='Q36_Cleansed', y='Q35_Premium', data=df_schools,
              col='School', jitter=0.2, alpha=0.8, palette='viridis',
              legend=False)
ax.set_axis_labels('Q36: Do meat-free days sound like a good idea to you?',
                   'Additional amount per meal willing to pay (£)')
sns.despine()



# ------------------------------------------------------------------
# Plots for Q37: How many meat-free days would sound reasonable to you?
# ------------------------------------------------------------------

# Plot proportion of responses to meat-free days by school

# Calculate counts of each response and unstack (to check sample size)
counts_school_days = df_schools.groupby('School')['Q37_Bins'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_school_days = df_schools.groupby('School')['Q37_Bins'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_school_days.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion of respondents from each school')
ax.set_title('Q37: How many meat-free days would sound reasonable to you? \n Comparison by school')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()


# Plot proportion of responses to # meat-free days by school, parents/carers only

# Calculate counts of each response and unstack (to check sample size)
counts_school_days = df_schools[df_schools['Stakeholder'] == 'Parent/Carer']\
    .groupby('School')['Q37_Bins'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_school_days = df_schools[df_schools['Stakeholder'] == 'Parent/Carer']\
    .groupby('School')['Q37_Bins'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_school_days.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion of respondents from each school')
ax.set_title('Q37: How many meat-free days would sound reasonable to you? \n Comparison by school, parents/carers only')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()


# Plot proportion of responses to # meat-free days by school, staff only

# Calculate counts of each response and unstack (to check sample size)
counts_school_days = df_schools[df_schools['Stakeholder'] != 'Parent/Carer']\
    .groupby('School')['Q37_Bins'].value_counts(normalize=False).unstack()

# Calculate proportion of each response and unstack
props_school_days = df_schools[df_schools['Stakeholder'] != 'Parent/Carer']\
    .groupby('School')['Q37_Bins'].value_counts(normalize=True).unstack()

# Plot bar graph
ax = props_school_days.plot(kind='bar', stacked=False, colormap='viridis')

# Customize the plot
ax.set_xlabel('School')
ax.set_ylabel('Proportion of respondents from each school')
ax.set_title('Q37: How many meat-free days would sound reasonable to you? \n Comparison by school, staff only')
ax.legend(title = None)
plt.xticks(rotation=0)

plt.show()
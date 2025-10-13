# %%
#Imports
%pip install ipython
import pandas as pd
import numpy as np
import random 
from IPython.display import display

#Limits
NumStudents = 150
MaxMark = 130
MaxTimeMin = 180

#categories
AGE_GROUPS = ['18-25', '25-35', '35-45', 'over 45']
STUDY_HOURS = ['1-2', '2-3', '4-5']

#Generating random data

#Student Number
student_numbers = np.arange(1, NumStudents + 1)

#Student Age Group (Within catogories)
age_groups = random.choices(AGE_GROUPS, k=NumStudents)

#Average Hours Spent (Within catogories)
study_hours = random.choices(STUDY_HOURS, k=NumStudents)

#call twice to make sure Exam 1 and Exam 2 have independent results
def generate_exam_data(NumStudents, MaxMark, max_time):
    """Generates raw marks and time taken for a single exam."""
    
    raw_marks = np.random.randint(0, MaxMark + 1, size=NumStudents)
    
    #Time Taken (from 0 to maxtime)
    time_taken = np.random.randint(20, max_time + 1, size=NumStudents) # Started at 20 min to be a bit more realistic
    
    return raw_marks, time_taken

#Generate data for Exam 1
exam1_marks, exam1_time = generate_exam_data(NumStudents, MaxMark, MaxTimeMin)

#Generate data for Exam 2
exam2_marks, exam2_time = generate_exam_data(NumStudents, MaxMark, MaxTimeMin)

# %%
#Create DataFrame for Exam 1
data_exam1 = {
    'studentNumber': student_numbers,
    'studentAgeGroup': age_groups,
    'avgHoursSpentStudyingOnCampus': study_hours,
    'studentMark_Raw': exam1_marks,
    'timeTakenOnExamination_minutes': exam1_time
}

df_exam1 = pd.DataFrame(data_exam1)
df_exam1 = df_exam1.set_index('studentNumber') #Tells pandas to use student number as the index

#Create DataFrame for Exam 2
data_exam2 = {
    'studentNumber': student_numbers,
    'studentAgeGroup': age_groups,
    'avgHoursSpentStudyingOnCampus': study_hours,
    'studentMark_Raw': exam2_marks,
    'timeTakenOnExamination_minutes': exam2_time
}

df_exam2 = pd.DataFrame(data_exam2)
df_exam2 = df_exam2.set_index('studentNumber') #Tells pandas to use student number as the index

#Calculate Percentage for both 
#Adding column 'studentMark_Percentage'
df_exam1['studentMark_Percentage'] = (df_exam1['studentMark_Raw'] / MaxMark) * 100
df_exam2['studentMark_Percentage'] = (df_exam2['studentMark_Raw'] / MaxMark) * 100

#Rounding
df_exam1['studentMark_Percentage'] = df_exam1['studentMark_Percentage'].round(2)
df_exam2['studentMark_Percentage'] = df_exam2['studentMark_Percentage'].round(2)

# %%
#Adding zero values to remove later

# Function to inject 0's into the raw marks and fix the percentage column too
def force_some_zeros(df, column_name, percent_to_zero=0.05):
    
    # Figure out how many to change (5% of students)
    num_to_zero = int(len(df) * percent_to_zero)
    
    # Grab random student indexes to mess with
    student_indexes = np.random.choice(df.index, size=num_to_zero, replace=False)
    
    # Set the raw mark to 0 for those students
    df.loc[student_indexes, column_name] = 0

    # Gotta update the percentage column to 0.00 as well
    # Using the new, clean column name!
    df.loc[student_indexes, 'studentMark_Percentage'] = 0.00
    
    print(f"I forced {num_to_zero} raw marks to 0 in {df.name} for the cleaning demo.")

# Set names for the print messages
df_exam1.name = "df_exam1"
df_exam2.name = "df_exam2"

# Introduce zero values in the raw mark columns using the function
# Using the new, clean column name: 'studentMark_Raw'
force_some_zeros(df_exam1, 'studentMark_Raw')
force_some_zeros(df_exam2, 'studentMark_Raw')

# %%
# Display
print("First 5 rows of Exam 1")
display(df_exam1.head(5))
print("\n")

# %%
print("First 5 rows of Exam 2")
display(df_exam2.head(5))
print("\n")

# %%
#Export DataFrames to CSV
# Using index=True here to include the studentNumber column, as it's the index now
df_exam1.to_csv('examination_data_exam1.csv') 
df_exam2.to_csv('examination_data_exam2.csv')

print("Successfully saved two CSV files:")
print("examination_data_exam1.csv")
print("examination_data_exam2.csv")

# %%
#Clean data
# FIX: Applying the cleaning to df_exam1 using the correct, clean column name
initial_rows_exam1 = len(df_exam1)

# Filter the DataFrame to keep only the rows where the raw mark is NOT equal to 0
df_exam1_cleaned = df_exam1[df_exam1['studentMark_Raw'] != 0].copy()

print(f"--- Data Cleaning on df_exam1 ---")
print(f"Initial rows: {initial_rows_exam1}")
print(f"Rows with a 0 raw mark removed: {initial_rows_exam1 - len(df_exam1_cleaned)}")
print(f"Rows remaining: {len(df_exam1_cleaned)}")
print(f"----------------------------------\n")

# Clean data for Exam 2
# FIX: Applying the cleaning to df_exam2 using the correct, clean column name
initial_rows_exam2 = len(df_exam2)

# Filter the DataFrame to keep only the rows where the raw mark is NOT equal to 0
df_exam2_cleaned = df_exam2[df_exam2['studentMark_Raw'] != 0].copy()

print(f"--- Data Cleaning on df_exam2 ---")
print(f"Initial rows: {initial_rows_exam2}")
print(f"Rows with a 0 raw mark removed: {initial_rows_exam2 - len(df_exam2_cleaned)}")
print(f"Rows remaining: {len(df_exam2_cleaned)}")
print(f"----------------------------------")
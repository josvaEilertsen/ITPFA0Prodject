# %%
#Imports
#%pip install ipython
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

#Generating random sample data

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

# Set names for the print messages
df_exam1.name = "df_exam1"
df_exam2.name = "df_exam2"

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
# Question 2: Create frequency tables

print("--- Frequency Table for Student Age Groups (Exam 1) ---")
age_freq_exam1 = df_exam1['studentAgeGroup'].value_counts()
display(age_freq_exam1)
print("\n")

print("--- Frequency Table for Avg Study Hours (Exam 1) ---")
hours_freq_exam1 = df_exam1['avgHoursSpentStudyingOnCampus'].value_counts()
display(hours_freq_exam1)
print("\n")

#grade boundaries and labels for the marks.
mark_ranges = [0, 49.99, 59.99, 69.99, 79.99, 100]
mark_labels = [
    'Fail (0-49)', 
    'D (50-59)', 
    'C (60-69)', 
    'B (70-79)', 
    'A (80-100)'
]

#new temporary column containing the mark categories for each
df_exam1['markCategory'] = pd.cut(df_exam1['studentMark_Percentage'], bins=mark_ranges, labels=mark_labels, include_lowest=True)

print("--- Frequency Table for Student Marks (Exam 1) ---")
mark_freq_exam1 = df_exam1['markCategory'].value_counts().sort_index() #order and count grade
display(mark_freq_exam1)
print("\n")

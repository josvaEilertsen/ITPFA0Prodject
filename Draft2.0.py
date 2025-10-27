# %%
#Imports
#%pip install ipython
import pandas as pd
import numpy as np
import random 
import matplotlib.pyplot as plt
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

# %%
#Question 2 - graphs 
#Bar Chart: Ages and Number of Students
#count
age_counts = df_exam1['studentAgeGroup'].value_counts()

#Define catogories
age_order = ['18-25', '25-35', '35-45', 'over 45']
age_counts = age_counts.reindex(age_order)

#Creating the chart
plt.figure(figsize=(10, 6))
plt.bar(age_counts.index, age_counts.values, color='skyblue')

#Adding title and label
plt.title('Number of Students in Each Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Students')

#Grid linees
plt.grid(axis='y', linestyle='--', alpha=0.7)

#Save chart
plt.savefig('age_distribution_bar_chart.png')

#Clear plt
plt.clf()

#%%
#Line graph
#group the DataFrame by avgHoursSpentStudyingOnCampus
#calculate average studentMark_Percentage 
correlation_data = df_exam1.groupby('avgHoursSpentStudyingOnCampus')['studentMark_Percentage'].mean()

#Sort data
correlation_data = correlation_data.sort_index()

#Creating the chart
plt.figure(figsize=(10, 6))
#The line style
plt.plot(correlation_data.index, correlation_data.values, marker='o', linestyle='-', color='green')

#Adding title and label
plt.title('Correlation Between Study Hours and Exam Marks')
plt.xlabel('Average Hours Spent Studying on Campus')
plt.ylabel('Average Student Mark (%)')
plt.grid(True)
plt.savefig('marks_vs_study_hours_line_graph.png')
plt.clf()

# %%
#Scatter Chart
plt.figure(figsize=(10, 6))
plt.scatter(df_exam1['timeTakenOnExamination_minutes'], df_exam1['studentMark_Percentage'], alpha=0.5, color='purple')

plt.title('Student Mark vs. Time Taken on Examination')
plt.xlabel('Time Taken on Examination (minutes)')
plt.ylabel('Student Mark (%)')
plt.grid(True)
plt.savefig('mark_vs_time_taken_scatter.png')
plt.clf()

#%%
#Scatter chart
plt.figure(figsize=(10, 6))

plt.scatter(df_exam1['studentAgeGroup'], df_exam1['avgHoursSpentStudyingOnCampus'], alpha=0.5, color='orange')

plt.title('Time Spent on Campus vs. Student Age Group')
plt.xlabel('Student Age Group')
plt.ylabel('Average Hours Spent Studying on Campus')
plt.grid(True)
plt.savefig('campus_time_vs_age_scatter.png')
plt.clf()
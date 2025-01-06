import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ================================
# STEP 1: CREATE DATASETS
# ================================

# Employee Information
employee_data = {
    "Employee ID": [101, 102, 103, 104],
    "Name": ["Alice Smith", "Bob Johnson", "Clara Davis", "David Lee"],
    "Department": ["Sales", "IT", "HR", "Sales"],
    "Job Role": ["Sales Executive", "Software Engineer", "HR Manager", "Account Manager"],
    "Hire Date": ["2018-03-15", "2019-07-10", "2020-01-25", "2021-11-08"],
    "Age": [29, 35, 42, 30],
    "Gender": ["F", "M", "F", "M"]
}
df_employee = pd.DataFrame(employee_data)

# Training Records
training_data = {
    "Employee ID": [101, 102, 103, 104],
    "Training Name": ["Sales Skills", "Advanced Coding", "HR Policy Updates", "Negotiation Techniques"],
    "Completion Date": ["2023-02-15", "2023-03-10", "2023-01-20", "2023-05-22"],
    "Hours Spent": [8, 15, 10, 12],
    "Certification Status": ["Certified", "Certified", "Not Certified", "Certified"]
}
df_training = pd.DataFrame(training_data)

# Performance Metrics
performance_data = {
    "Employee ID": [101, 102, 103, 104],
    "Month": ["2023-06", "2023-06", "2023-06", "2023-06"],
    "Performance Rating": [4.5, 4.8, 4.0, 4.2],
    "Projects Completed": [5, 7, 3, 4],
    "Leave Days Taken": [2, 0, 1, 4]
}
df_performance = pd.DataFrame(performance_data)

# ================================
# STEP 2: CLEANING DATA
# ================================

# Clean Employee Information
df_employee['Hire Date'] = pd.to_datetime(df_employee['Hire Date'])  # Standardize date format

# Clean Training Data
df_training['Completion Date'] = pd.to_datetime(df_training['Completion Date'])  # Standardize date format
df_training['Certification Status'] = df_training['Certification Status'].map({"Certified": 1, "Not Certified": 0})  # Binary encoding

# Merge Datasets
df_combined = pd.merge(df_employee, df_training, on="Employee ID")
df_combined = pd.merge(df_combined, df_performance, on="Employee ID")

# Check for missing values
print("Missing values:\n", df_combined.isnull().sum())

# Replace missing numerical values with mean (if any)
for col in df_combined.select_dtypes(include=np.number).columns:
    df_combined[col].fillna(df_combined[col].mean(), inplace=True)

# ================================
# STEP 3: DATA ANALYSIS
# ================================

# Calculate department-wise average performance rating
dept_performance = df_combined.groupby('Department')['Performance Rating'].mean()
print("\nAverage Performance Rating by Department:\n", dept_performance)

# Correlation Analysis
correlation_matrix = df_combined[['Hours Spent', 'Performance Rating', 'Leave Days Taken']].corr()
print("\nCorrelation Matrix:\n", correlation_matrix)

# ================================
# STEP 4: VISUALIZATION
# ================================

# Heatmap of Correlations
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix Heatmap")
plt.show()

# Bar Chart: Average Performance Rating by Department
dept_performance.plot(kind='bar', color='skyblue', figsize=(8, 5))
plt.title("Average Performance Rating by Department")
plt.ylabel("Performance Rating")
plt.xlabel("Department")
plt.xticks(rotation=45)
plt.show()

# Scatter Plot: Hours Spent vs Performance Rating
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_combined, x='Hours Spent', y='Performance Rating', hue='Department', palette='viridis', s=100)
plt.title("Hours Spent on Training vs Performance Rating")
plt.show()

# ================================
# STEP 5: AUTOMATION (Optional)
# ================================

# Save cleaned and analyzed data
df_combined.to_csv("Cleaned_Workforce_Data.csv", index=False)
print("\nCleaned data saved to 'Cleaned_Workforce_Data.csv'")
import pandas as pd
import numpy as np
from datetime import datetime

# Load datasets
employee_file = "Employee_Information.csv"
training_file = "Training_Records.csv"
performance_file = "Performance_Metrics.csv"

try:
    # Read CSV files
    employee_data = pd.read_csv(employee_file)
    training_data = pd.read_csv(training_file)
    performance_data = pd.read_csv(performance_file)
    print("Datasets successfully loaded.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Step 1: Merge datasets
try:
    merged_data = pd.merge(employee_data, training_data, on="Employee ID", how="left")
    merged_data = pd.merge(merged_data, performance_data, on="Employee ID", how="left")
    print("Datasets successfully merged.")
except KeyError as e:
    print(f"Error: {e}")
    exit()

# Step 2: Data cleaning
# Fill missing values with defaults or calculated values
merged_data.fillna({
    "Department": "Unknown",
    "Performance Rating": merged_data["Performance Rating"].mean(),
    "Leave Days Taken": 0,
    "Completion Date": datetime.now()  # Example: Fill missing completion dates with today's date
}, inplace=True)

# Standardize column names (lowercase and underscores instead of spaces)
merged_data.columns = [col.strip().replace(" ", "_").lower() for col in merged_data.columns]

# Convert date columns to datetime format
date_columns = ["hire_date", "completion_date"]
for col in date_columns:
    if col in merged_data.columns:
        merged_data[col] = pd.to_datetime(merged_data[col], errors="coerce")

# Add a calculated column for analysis
if "completion_date" in merged_data.columns:
    merged_data["training_completion_year"] = merged_data["completion_date"].dt.year

# Step 3: Save cleaned data
cleaned_file_path = "Cleaned_Workforce_Data.csv"
merged_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data has been saved as '{cleaned_file_path}'.")

# Optional: Provide a direct download link in environments like Jupyter Notebook
try:
    from IPython.display import FileLink
    display(FileLink(cleaned_file_path))
except ImportError:
    print("FileLink functionality is only available in Jupyter Notebook.")

# Step 4: Summary statistics for quick verification
print("\nSummary of Cleaned Data:")
print(merged_data.describe(include="all"))
print("\nPreview of Cleaned Data:")
print(merged_data.head())

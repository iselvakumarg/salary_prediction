#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:11:17 2024

@author: selva
"""


import pandas as pd

# Constants
CURRENT_YEAR = 2024

# Read the data
df = pd.read_csv("glassdoor_jobs.csv")

#### Clean Salary Estimate column ####

# encoded the textual salary reference into new columns
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if "per hour" in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if "employer provided salary:" in x.lower() else 0)

df = df[df["Salary Estimate"] != "-1"] 

# remove text from the salary range
salary = df["Salary Estimate"].apply(lambda x: x.split('(')[0])

# remove dollar sign and k at the end of the numerical
minus_kd = salary.apply(lambda x: x.replace("$","").replace("K",""))

# remove the textual salary mode from salary
salary_estimate = minus_kd.apply(lambda x: x.lower().replace("per hour", "").replace("employer provided salary:", ""))

# obtain min. salary from the estimate
df['min_salary'] = salary_estimate.apply(lambda x: int(x.split('-')[0]))

# obtain max. salary from the estimate
df['max_salary'] = salary_estimate.apply(lambda x: int(x.split('-')[1]))

# create avg. salary from the created min and max salary columns 
df['avg_salary'] = (df['min_salary']+df['max_salary'])/2


#### Clean Company Name column ####

# x['Company Name'][:-3] because the rating is like 3.4 which is not a decimal so considered as 3 space string so that's y -3
df['company_name_text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)

#### Creating StateField From location ####

df['job_state'] = df['Location'].apply(lambda x: x.split(",")[1])

# Creating a Column to check the headquarters and worklocation is same or not
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

#### Age of the Company ####
df['age'] = df.Founded.apply(lambda x: x if x < 1 else CURRENT_YEAR - x)


#### Mapping Keywords on Job Description ####

df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

df['r_studio'] = df['Job Description'].apply(lambda x: 1 if 'r-studio' in x.lower() or 'r studio' in x.lower() else 0)

df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

#### Drop Unnamed data ####

df.columns

final_df = df.drop("Unnamed: 0", axis=1)

#### Create Excel file ####

final_df.to_csv("salary_data_cleaned.csv", index=False)

#### Checking the Final data ####

final_csv = pd.read_csv("salary_data_cleaned.csv")


import pandas as pd

file_path = r"C:\Users\siddh\Assignment_Timecard.xlsx" 

df = pd.read_excel(file_path)  ## Reading file using pandas

df = df.drop('Unnamed: 9', axis=1)
df = df.drop('Unnamed: 10', axis=1) ## Dropping empty and unnecessary columns

def getNameFromID(Position_ID):  ## Function to get the Employee name from Position ID
    return df.loc[df['Position ID'] == Position_ID, 'Employee Name'].iloc[0]

def dropDuplicates(ls):  ## Function to drop duplicates while preserving order
    seen = set()
    unique = []
    for i in ls:
        if i in seen:
            continue
        unique.append(i)
        seen.add(i)
    return unique

Position_IDs = list(set(df['Position ID']))

## TASK 1 - Who has worked for 7 consecutive days.

def getMaxConsecutiveDays(Position_ID): 
    ls = df[df['Position ID'] == Position_ID]
    lst = list(pd.to_datetime(ls['Time'], format="%Y %m %d").dt.date)  ## Convert to date-time using to_datetime
    lst = dropDuplicates(lst) ## Dropping shifts on the same dates
    mx = 0
    cnt = 0
    for i in range(len(lst) - 1):
        if (lst[i + 1] - lst[i]).days == 1:
            cnt += 1
        else:
            cnt = 0
        mx = max(mx, cnt)
    return mx

Employee_Dict = dict()
Threshold_Days = 7
for Position_ID in Position_IDs:
    MaxConsecutiveDays = getMaxConsecutiveDays(Position_ID)
    if MaxConsecutiveDays >= Threshold_Days:
        Employee_Name = getNameFromID(Position_ID)
        Employee_Dict[Position_ID] = Employee_Name
EmployeesWithConsecutiveDays = pd.DataFrame({'ID': Employee_Dict.keys(), 'Name': Employee_Dict.values()})
print(f"Employees with {Threshold_Days} consecutive days are ")
print(EmployeesWithConsecutiveDays)
print()


## TASK 2 who have less than 10 hours of time between shifts but greater than 1 hour

def hasShiftWithinRange(Position_ID, range_start, range_end):
    ls = df[df['Position ID'] == Position_ID]
    lst = list(pd.to_datetime(ls['Time'], format="%Y %m %d"))
    lsto = list(pd.to_datetime(ls['Time Out'], format="%Y %m %d")) 
    ## Assumption - Time between shifts is time out of current shift minus time in of next shift
    for i in range(len(lst) - 1):
        time_diff = ((lst[i + 1] - lsto[i]).total_seconds()) / 3600
        if range_start < time_diff < range_end:
            return True
    return False

Employee_Dict = {}
range_start = 1
range_end = 10
for Position_ID in Position_IDs:
    if hasShiftWithinRange(Position_ID, 1, 10):
        Employee_Name = getNameFromID(Position_ID)
        Employee_Dict[Position_ID] = Employee_Name

EmployeesWithShiftRange = pd.DataFrame({'ID': Employee_Dict.keys(), 'Name': Employee_Dict.values()})
print(f"Employees having shift range between {range_start} and {range_end} hours are" )
print(EmployeesWithShiftRange)
print()

## Task 3  - c) Who has worked for more than 14 hours in a single shift

def getMaxShiftTime(Position_ID):
    ls = df[df['Position ID'] == Position_ID]
    ls = ls.fillna('-')
    lst = list((ls['Timecard Hours (as Time)']))
    return max(lst)

Employee_Dict = {}
Threshold_Time = 14
for Position_ID in Position_IDs:
    hours = getMaxShiftTime(Position_ID)
    if hours == '-':
        continue
    else:
        hours = int(hours.split(':')[0])
    if hours > 14:
        Employee_Name = getNameFromID(Position_ID)
        Employee_Dict[Position_ID] = Employee_Name

EmployeesWithMaxTime = pd.DataFrame({'ID': Employee_Dict.keys(), 'Name': Employee_Dict.values()})
print(f"Employees with Shift Time Above {Threshold_Time} hours are")
print(EmployeesWithMaxTime)
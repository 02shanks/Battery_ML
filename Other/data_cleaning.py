#Libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import os
import more_itertools as mit
from bisect import bisect_right
import datetime

#Functions
def skip_to(file, line,**kwargs):
    '''
    Reads a csv file from a specified line given a string present in that line

    Parameters :
    file (string): .csv file complete path
    line (string): Header element Eg: 'Time Stamp'
    **kwargs: arguments present in pandas.read_csv method

    Returns:
    Pandas dataframe

    '''
    if os.stat(file).st_size == 0:
        raise ValueError("File is empty")
    with open(file) as f:
        pos = 0
        cur_line = f.readline()
        while line not in cur_line:
            pos = f.tell()
            cur_line = f.readline()
        f.seek(pos)
        return pd.read_csv(f, **kwargs)


def time_conv(x):
    '''
    Returns the time in seconds

    Parameters :
    x: Timestamp in HH:MM:SS

    Returns:
    X value in seconds

    '''
    # x=x.strftime("%H:%M:%S")
    h,m,s = map(int,x.split(':'))
    return ((h*60+m)*60+s)

#Main function
def user_data_filter(csv_filepath,output_path,max_minutes=60,header_start_colname='Time'):
    '''
    Returns the clean dataframe after filtering the data uploaded by the user 

    Parameters :
    csv_filepath (string): .csv file complete path 
    output_path (string): Path to save output file 
    max_minutes (int): Maximum number of minutes of data required Eg: 20 
    header_start_colname (string): Unique value - Header identificator Eg: 'Time Stamp','Time'

    Returns:
    Cleaned dataframe and saves the cleaned dataframe in the output path provided

    '''
    #Deletes unwanted rows from top
    data1=skip_to(csv_filepath,header_start_colname)

    #Discards unnamed columns
    data1=data1.drop(data1.columns[data1.columns.str.contains('Unnamed')==True].to_list(),axis=1)
    # print(data1.isnull().sum().values)

    #Drops the first row after header - usually the row containing units
    #data1=data1.drop([0])

    #Drops null values from the data
    data1=data1.dropna()

    #Time stamp conversion to Hours minutes and seconds
    data1['Time']=pd.to_datetime(data1['Time']).dt.time
    data1['Time']=data1['Time'].astype(str)

    #Drops duplicate rows with respect to time column
    data1=data1.drop_duplicates(subset='Time')

    #Converts time to seconds
    data1['Time_mod']=data1['Time'].apply(time_conv)

    #Identifies all temperature columns
    col_list=data1.columns[data1.columns.str.lower().str.contains('temperature')==True].to_list()

    #Identifies current columns
    curr_col=data1.columns[data1.columns.str.lower().str.contains('current')==True].to_list()
    for val in curr_col:
        col_list.append(val)
    # print(col_list)

    #Identifies voltage columns
    vol_col=data1.columns[data1.columns.str.lower().str.contains('voltage')==True].to_list()
    for val in vol_col:
        col_list.append(val)
    # print(col_list)

    #Datatype conversion to numeric - float
    data1[col_list] = data1[col_list].apply(pd.to_numeric)
    col_list.append('Time')
    col_list.append('Time_mod')
    # print(col_list)
    data2=data1[col_list]

    #Identifies all values between 0 and 0.05 in the current column - resting period
    data3=data2.loc[(data2['Current']<=0.05) & (data2['Current']>=0.0)]
    data3=data3.reset_index()
    grp_inds1=[list(group) for group in mit.consecutive_groups(data3['index'])]
    # plt.plot(data2['Time'],data2['Current'])
    # plt.show()

    #Detects the starting of the pulse after resting period
    pulse_st_ind=0
    for i in grp_inds1:
        if len(i)>1:
            diff=data2['Time_mod'].loc[i[-1]] - data2['Time_mod'].loc[i[0]]
            if diff>300:
                req_ind = i[-1]
                pulse_st_ind=req_ind

    #Discard the values before pulse start
    data4=data2.loc[pulse_st_ind:].reset_index()
    data4['Time_mod1']=data4['Time_mod']-data4['Time_mod'].loc[0]

    #Subset the data upto max_minutes specified by user 
    if data4['Time_mod1'].iloc[-1]<=max_minutes*60:
        data_fin=data4.drop(['index','Time_mod','Time','Time_mod1'],axis=1)
        data_fin['Time']=data4['Time_mod1']
        data_fin.to_csv(output_path,index=False)
    else:
        idx = bisect_right(data4['Time_mod1'].values, max_minutes*60)
        data_fin=data4.loc[0:idx-1]
        data_fin=data_fin.drop(['index','Time_mod','Time','Time_mod1'],axis=1)
        data_fin['Time']=data4['Time_mod1']
        data_fin.to_csv(output_path,index=False)

    return data_fin



# user_data_filter(r".\test.csv", r".\test_1.csv")
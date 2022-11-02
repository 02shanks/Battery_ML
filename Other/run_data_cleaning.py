from cgitb import text
from fileinput import filename
import data_cleaning
import csv
import os
import pandas as pd
import xlrd

# data_file = {'charge_discharge_file_1' : r"C:\Work\Project\TPE_data\tpe_data\Cell1_1C_modified_train.xlsx"}
# file_location = data_file['charge_discharge_file_1']
# read_file = pd.read_excel (file_location, converters={'names':str,'ages':str})
# read_file = read_file.astype(str)
# read_file.to_csv (r".\output.csv",  date_format='%Y-%m-%d %H:%M:%S', index = None, header=True)
# data_cleaning.user_data_filter(r".\output.csv", r"cleaned_data.csv")
  
# printing the human readable type of the file

# data_file = {'charge_discharge_file_1' : r"/home/oorja/project/TPE_data/Cell1_1C_modified_train.csv"}
data_file = {'charge_discharge_file_1' : r"C:\Work\Project\TPE_data\tpe_data\my_training.txt"}
data_file = {'charge_discharge_file_1' : r"C:\Work\Project\TPE_data\tpe_data\Cell1_1C_modified_train.xlsx"}


file_location = data_file['charge_discharge_file_1']

extension = os.path.splitext(file_location)[1]
print(extension)
  
if extension == ".text":
    reader = csv.reader(open(file_location, "r"), delimiter='\t')
    writer = csv.writer(open(r".\output.csv", 'w'), delimiter=',')
    writer.writerows(reader)
    data_cleaning.user_data_filter(r".\output.csv", r"cleaned_data.csv")
elif (extension == ".csv"):
    data_cleaning.user_data_filter(file_location, r"cleaned_data.csv")
elif extension == ".xlsx":
    read_file = pd.read_excel (file_location)
    time_col_name=read_file.columns[np.where(read_file.columns.str.lower().str.contains('time')==True)[0].tolist()[0]]
    read_file[time_col_name] = pd.to_datetime(read_file[time_col_name], unit ='D').astype('datetime64[s]').dt.time
    read_file.to_csv (r".\output.csv", date_format='%H:%M:%S', index = None, header=True)
    data_cleaning.user_data_filter(r".\output.csv", r"cleaned_data.csv")
elif extension == ".xls":
    read_file = pd.read_excel (file_location)
    time_col_name=read_file.columns[np.where(read_file.columns.str.lower().str.contains('time')==True)[0].tolist()[0]]
    read_file[time_col_name] = pd.to_datetime(read_file[time_col_name], unit ='D').astype('datetime64[s]').dt.time
    read_file.to_csv (r".\output.csv", date_format='%H:%M:%S', index = None, header=True)
    data_cleaning.user_data_filter(r".\output.csv", r"cleaned_data.csv")








# data_cleaning.user_data_filter(file_location, r"/home/oorja/project/TPE_data/cleaned_data.csv")




# while uploading to production server, change file path
# input file location - r"/home/oorja/project/thermal_property_estimation/database/Cell1_1C_modified_train.csv"
# output file location - r"/home/oorja/project/thermal_property_estimation/database/cleaned_data.csv"


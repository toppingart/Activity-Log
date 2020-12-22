import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint # pretty print (in its own rows)

def delete_rows(sheets, row_start, row_end, month_list):
    for month in month_list:
        sheets.delete_rows(row_start,row_end)

def delete_cols(sheets, col_num, month_list):
    for num in range(2,len(month_list)):
        sheets.delete_columns(month_list[num])


scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
months = ["September", "October", "November", "December", "January", "February", "March", "April", "May", "June"]

# setting up credentials and connecting to sheet
creds = ServiceAccountCredentials.from_json_keyfile_name("sheets.json", scope) # name of our json file
client = gspread.authorize(creds)

for month in months:
    sheets = client.open("Elena Xu - VOLUNTEER LOG 2017-2018").worksheet(month) 
    sheets.update_cell(1,6,"hours")


"""
for month in months:
    sheets = client.open("Elena Xu - VOLUNTEER LOG 2017-2018").worksheet(month) 
    sheets.delete_rows(1,6)"""


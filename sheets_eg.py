import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint # pretty print (in its own rows)

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# setting up credentials and connecting to sheet
creds = ServiceAccountCredentials.from_json_keyfile_name("sheets.json", scope) # name of our json file
client = gspread.authorize(creds)

# name of sheet
sheet = client.open("Volunteer Hours + Activities Log").sheet1 # getting the first sheet

# ----------------------------------------
# data = sheet.get_all_records()
# len(data) --> number of rows with data (does not include the headers at the beginning/top)
# print(data)

# get a certain row
# row = sheet.row_values(3) # get row 3
# pprint(row)

# get col
#col = sheet.col_values(3)
#pprint(col)

# get a certain cell
#cell = sheet.cell(1,3).value
#pprint(cell)

# insert row 
# note: does not override, pushes down instead
#insert_row = ["test","1"]
#sheet.insert_row(insert_row,31)

# delete row
# sheet.delete_row(4) # which row number you want to delete

# update cell
# sheet.update_cell(2,2,"CHANGED") # coordinates (vertical,horizontal)

# get number of rows (includes the blank ones)
# num_rows = sheet.row_count


# Sources:
# https://www.youtube.com/watch?v=cnPlKLEGR7E
# ---------------------------------------

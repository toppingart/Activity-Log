
import global_vars
from imports import *

"""
Used to change the date (as a string) to a datetime object.

Input: 
- the results (dictionaries in a list)
"""
def to_datetime(results):
    for result in results:
        date = result['date']
        if isinstance(date,str) and len(date.strip()) == 8: #12/02/20
            datetime_obj = datetime.strptime(date, "%m/%d/%y")
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'date': datetime_obj}})

        elif isinstance(date,str) and len(date.strip()) == 19: # 12/01/20 - 12/02/20
            start_date = result['date'][:8]
            end_date = result['date'][11:]
            start_datetime = datetime.strptime(start_date, "%m/%d/%y")
            end_datetime = datetime.strptime(end_date, "%m/%d/%y")
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'startdate': start_datetime}})
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'enddate': end_datetime}})

"""
Checks if the date entered by the user is a valid date (valid day, month, and year).

Input: the date (as a string)
"""
def check_date(date):
    if len(date.strip()) == 8:
        check_date = datetime.strptime(date, "%m/%d/%y") 
    else:
        raise ValueError # not valid (eg. 01/32/19)





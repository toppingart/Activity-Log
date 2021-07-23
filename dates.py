
"""
Used to change the date (as a string) to a datetime object.

Input: 
- vol
- the results (dictionaries in a list)
Output: None
"""
def to_datetime(results):

    for result in results:
        date = result['date']
        if isinstance(date,str) and len(date.strip()) == 8:
            #12/02/20
            datetime_obj = datetime.strptime(date, "%m/%d/%y")
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'date': datetime_obj}})

        elif isinstance(date,str) and len(date.strip()) == 19:
            # 12/01/20 - 12/02/20
            start_date = result['date'][:8]
            end_date = result['date'][11:]
            start_datetime = datetime.strptime(start_date, "%m/%d/%y")
            end_datetime = datetime.strptime(end_date, "%m/%d/%y")
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'startdate': start_datetime}})
            global_vars.vol.update_one({'_id': result['_id']}, {'$set': {'enddate': end_datetime}})





"""
Checks if the date entered by the user is a valid date (valid day, month, and year).

Input: the date (as a string)
Output: None
"""
def check_date(date):
    if len(date.strip()) == 8:
        check_date = datetime.strptime(date, "%m/%d/%y") 
    else:
        raise ValueError



def filter_by_date(results, *widgets):
    if var1.get() == 1:
        results.sort('date', pymongo.DESCENDING)
        return results

"""
Takes the user to the appropiate method depending on if they want to edit one date or two dates (start and end date)

Input:
- vol
- result (all the details)
- *widgets

Output: None
Calls: one_day_option() or multiple_days_option()
"""
def make_date_changes(result, *widgets):
    count = global_vars.vol.count_documents({"startdate": {"$exists": True}, '_id': result['_id']})
    if count == 0: # one date
        one_day_option(result, True, *widgets)
    else:
        multiple_days_option(result, True, *widgets)


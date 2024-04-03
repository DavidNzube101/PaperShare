import datetime as dt
from datetime import datetime, timedelta

def split_date(date):
    month_dict = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    try:
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:10])

        if month in month_dict:
            spelt_month = month_dict[month]
        else:
            spelt_month = ''

        date_dict = {
            "Year": year,
            "Month": month,
            "MonthW": spelt_month,
            "Day": day
        }
        return date_dict
    except ValueError:
        raise ValueError("Invalid date format")

def format_ordinal(number):
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return str(number) + suffix

def clean_date(date, style=""):
    try:
        date_info = split_date(date)
        day, month, month_word, year = date_info["Day"], date_info["Month"], date_info["MonthW"], date_info["Year"]

        if style == "MDY":
            day_str = format_ordinal(day)
            return f"{month_word} {day_str}, {year}"
        else:
            day_str = format_ordinal(day)
            return f"{day_str} of {month_word}, {year}"
    except:
        return date

def compare(t, target, operator="<"):
    t_formatted = datetime.combine(datetime.today(), datetime.strptime(t, "%H:%M").time())#strftime("%H:%M")

    deadline = datetime.combine(datetime.today(), datetime.strptime(target, "%H:%M").time())

    if operator == "<":
        if t_formatted < deadline:
            return False
        else:
            return True

    elif operator == ">":
        if t_formatted > deadline:
            return True
        else:
            return False

    elif operator == ">=":
        if t_formatted <= deadline:
            return True
        else:
            return False

    elif operator == "<=":
        if t_formatted >= deadline:
            return False
        else:
            return True

    else:
        return ""
            
def compare_cc(target, operator="<"):
    # t = "00:00"
    """
    target: 

    """

    current_time = datetime.now().time()#strftime("%H:%M")

    deadline = datetime.combine(datetime.today(), datetime.strptime(target, "%H:%M").time())

    if operator == "<":
        if current_time < deadline.time():
            return False
        else:
            return True

    elif operator == ">":
        if current_time > deadline.time():
            return True
        else:
            return False

    elif operator == ">=":
        if current_time <= deadline.time():
            return True
        else:
            return False

    elif operator == "<=":
        if current_time >= deadline.time():
            return False
        else:
            return True

    else:
        if current_time < deadline.time():
            return False
        else:
            return True
    
    

# # Example usage:
# date_string = "2023-11-07"
# formatted_date = clean_date(date_string, style="MDY")
# print(formatted_date)


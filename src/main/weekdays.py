import datetime


def make_week_days():
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_day = datetime.datetime.today().weekday()
    week_days[current_day] = "Today"
    if current_day > 0:
        week_days[current_day - 1] = "Yesterday"
    if current_day < 6:
        week_days[current_day + 1] = "Tomorrow"
    print(week_days)

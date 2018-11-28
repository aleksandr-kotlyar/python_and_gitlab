import datetime


def make_week_days():
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(0, len(week_days)):
        if datetime.datetime.today().weekday() == i:
            week_days[i] = "Today"
            if i > 0:
                week_days[i - 1] = "Yesterday"
            if i < 6:
                week_days[i + 1] = "Tomorrow"
    print(week_days)

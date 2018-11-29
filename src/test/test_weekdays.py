from src.main.weekdays import make_week_days


def test_current_week():
    days = make_week_days()
    print(days)

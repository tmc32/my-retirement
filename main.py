import datetime
import calendar
import os
import time

import holidays


REFRESH_INTERVAL_SECONDS = 1


def clear_screen():
    os.system("cls")


def get_last_working_day():
    # Get today's date
    today = datetime.date.today()

    # Find the last calendar day of the current month
    _, last_day_num = calendar.monthrange(today.year, today.month)
    last_date = datetime.date(today.year, today.month, last_day_num)

    # Load UK Bank Holidays (England/Wales)
    uk_holidays = holidays.UnitedKingdom(subdiv="ENG", years=[today.year])

    # Roll back if it's a weekend (5=Sat, 6=Sun) or a Bank Holiday
    while last_date.weekday() >= 5 or last_date in uk_holidays:
        last_date -= datetime.timedelta(days=1)

    # Return as a full datetime object (set to 5:00 PM / 0:00 for "end of day")
    return datetime.datetime.combine(last_date, datetime.time(0, 0, 0))


def get_28th_or_last_working_day():
    now = datetime.datetime.now()
    today = now.date()

    def target_for(year, month):
        uk_holidays = holidays.UnitedKingdom(subdiv="ENG", years=[year])
        target_date = datetime.date(year, month, 28)
        # Roll back if it's a weekend (5=Sat, 6=Sun) or a Bank Holiday
        while target_date.weekday() >= 5 or target_date in uk_holidays:
            target_date -= datetime.timedelta(days=1)
        return datetime.datetime.combine(target_date, datetime.time(0, 0, 0))

    target = target_for(today.year, today.month)

    # Once this month's target (the 28th, or the working day before it) has
    # been reached, count down to next month's instead
    if now >= target:
        year, month = (today.year + 1, 1) if today.month == 12 else (today.year, today.month + 1)
        target = target_for(year, month)

    return target


def run_countdown():
    now = datetime.datetime.now()
    # target = get_last_working_day()
    target = get_28th_or_last_working_day()

    # Calculate the gap
    diff = target - now

    # If the last working day has already passed today
    if diff.total_seconds() < 0:
        print("The last working day of this month has already passed!")
        return

    # Total Unit Calculations
    total_seconds = diff.total_seconds()
    total_minutes = total_seconds / 60
    total_hours = total_seconds / 3600
    total_days = total_seconds / 86400
    total_weeks = total_days / 7

    print(f"TARGET: Last Working Day of {target.strftime('%B %Y')}")
    print(f"Date:   {target.strftime('%A, %d %B %Y at %I:%M %p')}")
    print("-" * 50)
    print(f"Weeks:   {total_weeks:.2f}")
    print(f"Days:    {total_days:.2f}")
    print(f"Hours:   {total_hours:,.1f}")
    print(f"Minutes: {total_minutes:,.0f}")
    print(f"Seconds: {total_seconds:,.0f}")
    print("-" * 50)

    # Detailed breakdown
    days_part = diff.days
    hours_part, rem = divmod(diff.seconds, 3600)
    minutes_part, seconds_part = divmod(rem, 60)
    print(f"Time remaining: {days_part}d {hours_part}h {minutes_part}m {seconds_part}s")
    print("")


def calculate_retirement_no_dependencies():
    now = datetime.datetime.now()
    target = datetime.datetime(2039, 12, 7)

    mtarget = datetime.datetime(2032, 10, 1)

    diff = target - now

    mdiff = mtarget - now

    # Standard calculations
    days = diff.days
    seconds = diff.total_seconds()

    mdays = mdiff.days
    msecs = mdiff.total_seconds()

    # Derived calculations
    years = days / 365.25
    weeks = days / 7
    hours = seconds / 3600
    minutes = seconds / 60

    myears = mdays / 365.25
    mweeks = mdays / 7
    mhours = msecs / 3600
    mminutes = msecs / 60

    # Roughly calculating months (using average month length)
    months = days / 30.44

    mmonths = mdays / 30.44

    print(f"Retirement Countdown (Standard Lib Version):")
    print(f"{'-' * 40}")
    print(f"Years:   {years:.2f}")
    print(f"Months:  {months:.1f}")
    print(f"Weeks:   {weeks:.1f}")
    print(f"Days:    {days:,}")
    print(f"Hours:   {hours:,.0f}")
    print(f"Minutes: {minutes:,.0f}")
    print(f"Seconds: {seconds:,.0f}")
    print("")

    print(f"Mortgage Countdown (Standard Lib Version):")
    print(f"{'-' * 40}")
    print(f"Years:   {myears:.2f}")
    print(f"Months:  {mmonths:.1f}")
    print(f"Weeks:   {mweeks:.1f}")
    print(f"Days:    {mdays:,}")
    print(f"Hours:   {mhours:,.0f}")
    print(f"Minutes: {mminutes:,.0f}")
    print(f"Seconds: {msecs:,.0f}")
    print("")


def run_loop():
    import msvcrt

    print("Press 'q' to quit.")
    while True:
        clear_screen()
        calculate_retirement_no_dependencies()
        run_countdown()
        print("Press 'q' to quit. Refreshing every second...")

        elapsed = 0.0
        while elapsed < REFRESH_INTERVAL_SECONDS:
            if msvcrt.kbhit() and msvcrt.getwch().lower() == "q":
                return
            time.sleep(0.1)
            elapsed += 0.1


if __name__ == "__main__":
    try:
        run_loop()

    except ImportError:
        print("Error: Please run 'pip install holidays' first.")

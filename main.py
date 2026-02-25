import datetime


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

    print(f"Morgate Countdown (Standard Lib Version):")
    print(f"{'-' * 40}")
    print(f"Years:   {myears:.2f}")
    print(f"Months:  {mmonths:.1f}")
    print(f"Weeks:   {mweeks:.1f}")
    print(f"Days:    {mdays:,}")
    print(f"Hours:   {mhours:,.0f}")
    print(f"Minutes: {mminutes:,.0f}")
    print(f"Seconds: {msecs:,.0f}")


calculate_retirement_no_dependencies()

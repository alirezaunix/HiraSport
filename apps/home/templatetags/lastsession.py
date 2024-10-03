import jdatetime
from datetime import timedelta


def lastsession(payment_date, num_sessions):
    # Convert payment_date string to jdatetime object
    payment_date = jdatetime.datetime.strptime(payment_date, "%Y-%m-%d").date()

    # Define the class days (0 = Saturday, 2 = Monday, 4 = Wednesday)
    class_days = [0, 2, 4]

    # Find the next class day on or after the payment date
    start_date = payment_date
    while start_date.weekday() not in class_days:
        start_date += timedelta(days=1)

    last_session_date = start_date
    sessions_left = num_sessions-1

    while sessions_left > 0:
        if last_session_date.weekday() in class_days:
            sessions_left -= 1
        last_session_date += timedelta(days=1)

    # Find the next session date after the last paid session
    next_session_date = last_session_date
    while next_session_date.weekday() not in class_days:
        next_session_date += timedelta(days=1)

    return next_session_date

if __name__ == "__main__":
    # Example usage
    # Example payment date (2023-09-06 in Gregorian, which is a Wednesday)
    payment_date = "1403-09-03"
    num_sessions = 4  # Number of sessions paid for

    next_session = lastsession(payment_date, num_sessions)
    print(f"Payment date: {payment_date}")
    print(
        f"Next session date after last paid session: {next_session.strftime('%Y-%m-%d')}")

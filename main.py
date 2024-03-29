import datetime

from config import Config
from database import Database
from riverlevel import river_level
from mail import warning_mail


def main():
    # Initial database with config values
    db = Database(Config)

    # Find when the last measurement in database was taken
    latest_query = "SELECT MAX(DateTime) from height"
    try:
        latest = db.run_query(latest_query)[0][0] - \
                 datetime.timedelta(minutes=5)

        # Checks to see if path was previously flooded
        date_str = latest.strftime(r'%Y-%m-%d %H:%M:%S')
        path_query = f"SELECT path_closed FROM height WHERE DateTime > '{date_str}'"  # noqa: E501
        path_close = db.run_query(path_query)
        prev_flood = (1,) in path_close

        # Add 10 minutes to avoid getting repeat queries
        latest += datetime.timedelta(minutes=10)

    except TypeError:
        # Database is currently empty - let's go back as far as possible
        latest = datetime.datetime.now() - datetime.timedelta(weeks=52)
        prev_flood = False

    # Get new River level measurements (and reverse order so latest is first)
    measures = river_level(since=latest)[::-1]

    # Path is inpassable if river level > 3.6 m
    path_flood = 3.6
    send_flood_mail = False
    send_drop_mail = False

    for h, dt, inFlood in measures:
        if h >= path_flood:
            path_closed = 1
            flood_level = h
            # Dont want to send multiple emails if we have a large
            send_flood_mail = True
        else:
            path_closed = 0
            # Check to see if path was previously flooded
            if prev_flood:
                send_drop_mail = True
                flood_level = h

        sql_data_query = "INSERT INTO height (DateTime, level, in_Flood, path_closed) VALUES('{0}', '{1}', '{2}', '{3}')"  # noqa: E501

        db.run_query(sql_data_query.format(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                           h, inFlood, path_closed))

    # Now we have dealt with backlog, and send emails if needed
    if send_flood_mail:
        # River is in flood, but only send mail if it has only just flooded
        if not prev_flood:
            warning_mail(flood_level, flood=True)
    elif send_drop_mail:
        # Send email out to say that the path is no longer flooded
        warning_mail(flood_level, flood=False)


if __name__ == '__main__':
    main()

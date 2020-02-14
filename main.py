from config import Config
from database import Database
from riverlevel import river_level
import datetime
import os

def warning_mail(h, flood):
    '''
    Sends warning email to me when the path is flooded using mail
    server on Pi
    Inputs:
        h           -   River levvel
        flood       -   Boolean to say if path is flooded
    '''
    # Get email to send alert to (in enviroment variables
    to_addr = os.environ.get('EMAIL_TO')

    if flood:
        # Construct command-line message
        cmd = 'echo "The path is currently flooded and the river level is at {0:.2f} m" | mail -s "Flood Alert" {1}'.format(h ,to_addr)
    else:
        cmd = 'echo "The path should have cleared - The river level is at {0:.2f} m" | mail -s "Flood Alert" {1}'.format(h ,to_addr)

    # Send it off to OS
    os.popen(cmd)

# Initial database with config values
db = Database(Config)

# Find when the last measurement in database was taken
latest_query = "SELECT MAX(DateTime) from height"
latest = db.run_query(latest_query)[0][0] + datetime.timedelta(minutes=5)

# Check last 8 measurements to see if path was previously flooded
path_query = "SELECT path_closed FROM height ORDER BY id DESC LIMIT 8"
path_close = db.run_query(path_query)
prev_flood = (1,) in path_close
print(path_close)


# Get new River level measurements (and reverse order so latest is first)
Measures = river_level(since=latest)[::-1]

# Path is inpassable if river level > 3.6 m
path_flood = 3.6
send_flood_mail = False
send_drop_mail = False

for h, dt, inFlood in Measures:
    if h >= path_flood:
        path_closed = 1
        flood_level = h
        # Dont want to send multiple emails if we have a large
        send_flood_mail = True
    else:
        path_closed = 0
        # Check to see if path was previously flooded
        if path_close[0][0]:
            send_drop_mail = True
            flood_level = h

    sql_data_query = "INSERT INTO height (DateTime, level, in_Flood, path_closed) VALUES('{0}', '{1}', '{2}', '{3}')"

    db.run_query(sql_data_query.format(dt.strftime('%Y-%m-%d %H:%M:%S'), h, inFlood, path_closed))

if send_flood_mail:
    # River is in flood, but only send mail if it has only just flooded
    if not prev_flood:
        warning_mail(flood_level, flood=True)
elif send_drop_mail:
    # Send email out to say that the path is nolonger flooded
    warning_mail(flood_level, flood=False)

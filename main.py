from config import Config
from database import Database
from riverlevel import river_level
import datetime
import os

def warning_mail():
    '''
    Sends warning email to me when the path is flooded using mail
    server on Pi
    '''
    # Get email to send alert to (in enviroment variables
    to_addr = os.environ.get('EMAIL_TO')
    
    # Construct command-line message
    cmd = 'echo "The path is currently flooded" | mail -s "Flood Alert" {0}'.format(to_addr)
    
    # Send it off to OS
    os.popen(cmd)
   

# Initial database with config values
db = Database(Config)

# Find when the last measurement in database was taken
latest_query = "SELECT MAX(DateTime) from height"
latest = db.run_query(latest_query)[0][0] + datetime.timedelta(minutes=5)

# Get new River level measurements (and reverse order so latest is first)
Measures = river_level(since=latest)[::-1]

# Path is inpassable if river level > 3.6 m
path_flood = 3.6
send_mail = False

for h, dt, inFlood in Measures:
    if h >= path_flood:
        path_closed = 1
        # Dont want to send multiple emails if we have a large 
        send_mail = True
    else:
        path_closed = 0

    sql_data_query = "INSERT INTO height (DateTime, level, in_Flood, path_closed) VALUES('{0}', '{1}', '{2}', '{3}')"
    
    db.run_query(sql_data_query.format(dt.strftime('%Y-%m-%d %H:%M:%S'), h, inFlood, path_closed))

if send_mail:
    warning_mail()

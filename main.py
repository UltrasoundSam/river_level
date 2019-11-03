from config import Config
from database import Database
from riverlevel import river_level
import datetime

# Initial database with config values
db = Database(Config)

# Find when the last measurement in database was taken
latest_query = "SELECT MAX(DateTime) from height"
latest = db.run_query(latest_query)[0][0] + datetime.timedelta(minutes=5)

# Get new River level measurements (and reverse order so latest is first)
Measures = river_level(since=latest)[::-1]

for h, dt, inFlood in Measures:
    sql_data_query = "INSERT INTO height (DateTime, level, in_Flood) VALUES('{0}', '{1}', '{2}')".format(dt.strftime('%Y-%m-%d %H:%M:%S'), h, inFlood)
    db.run_query(sql_data_query)


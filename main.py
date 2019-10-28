from config import Config
from database import Database
from riverlevel import river_level

# Initial database with config values
db = Database(Config)

# Get new River level measurement
dt, h = river_level()

sql_data_query = "INSERT INTO height (DateTime, level) VALUES('{0}', '{1}')".format(dt.strftime('%Y-%m-%d %H:%M:%S'), h)
db.run_query(sql_data_query)

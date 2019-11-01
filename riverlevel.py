import requests
from datetime import datetime

def river_level(station_id='L2406'):
    '''
    Function that calls the Environment Agency's API to get instanteous
    measurement of river levels at its numerous recording stations.
    Input:
        station_id  - Unique Station ID (defaults to Viking Recorder)
    Output:
        (dt, level) - Tuple (date of measurement, river level)
    '''
    # Format URL and get data
    requrl = 'https://environment.data.gov.uk/flood-monitoring/id/stations/{0}'.format(station_id)
    payload = requests.get(requrl).json()

    # Collect data
    data = payload['items']['measures'][1]['latestReading']
    Curlevel = data['value']
    FloodLevel = payload['items']['stageScale']['typicalRangeHigh']

    if Curlevel >= FloodLevel:
        inFlood = 1
    else:
        inFlood = 0

    # Read timestamp
    datestr = "%Y-%m-%dT%H:%M:%S%z"
    dt = datetime.strptime(data['dateTime'], datestr)
    return (dt, Curlevel, inFlood)

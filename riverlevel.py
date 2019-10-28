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
    requrl = 'https://environment.data.gov.uk/flood-monitoring/id/stations/{0}/measures'.format(station_id)
    payload = requests.get(requrl).json()
    
    # Collect data
    data = payload['items'][0]['latestReading']
    level = data['value']
    
    # Read timestamp
    datestr = "%Y-%m-%dT%H:%M:%S%z"
    dt = datetime.strptime(data['dateTime'], datestr)
    return (dt, level)

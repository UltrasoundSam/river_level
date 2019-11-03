import requests
from datetime import datetime

def river_level(since, station_id='L2406'):
    '''
    Function that calls the Environment Agency's API to get instanteous
    measurement of river levels at its numerous recording stations.
    Input:
        since       - Datetime object to record all measurements since
        station_id  - Unique Station ID (defaults to Viking Recorder)
    Output:
        (dt, level, inflood) - List of Tuples (date of measurement, river level)
    '''
    # Datetime format
    datestr = "%Y-%m-%dT%H:%M:%S%z"

    # Find out Flood level
    maxurl = 'https://environment.data.gov.uk/flood-monitoring/id/stations/{0}'.format(station_id)
    flood = requests.get(maxurl).json()
    FloodLevel = flood['items']['stageScale']['typicalRangeHigh']

    # Format URL and get data
    requrl = 'https://environment.data.gov.uk/flood-monitoring/id/stations/{0}/readings?_sorted&since={1}Z'.format(station_id, since.strftime(datestr))
    payload = requests.get(requrl).json()

    Measures = []
    for item in payload['items']:
        # Get current river level and time of measurement
        Curlevel = item['value']
        dt = datetime.strptime(item['dateTime'], datestr)

        # Check to see if river is currently in flood
        if Curlevel >= FloodLevel:
            inFlood = 1
        else:
            inFlood = 0

        Measures.append((Curlevel, dt, inFlood))

    return Measures

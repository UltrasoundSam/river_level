import requests
from datetime import datetime
from urllib.parse import urljoin


def river_level(since: datetime,
                station_id: str = 'L2406') -> list[float, float, float]:
    '''
    Function that calls the Environment Agency's API to get instanteous
    measurement of river levels at its numerous recording stations.
    Input:
        since       - Datetime object to record all measurements since
        station_id  - Unique Station ID (defaults to Viking Recorder)
    Output:
        (dt, level, inflood) - List of Tuples (date of measurement,
                                               river level)
    '''
    # Datetime format
    datestr = "%Y-%m-%dT%H:%M:%S%z"

    # Define base url
    base_url = 'https://environment.data.gov.uk/flood-monitoring/id/stations/'

    # Find out Flood level
    maxurl = urljoin(base_url, station_id)
    flood = requests.get(maxurl).json()
    FloodLevel = flood['items']['stageScale']['typicalRangeHigh']

    # Format URL and get data
    since_str = since.strftime(datestr)
    req_str = f'{station_id}/readings?_sorted&_limit=5000&since={since_str}Z'
    requrl = urljoin(base_url, req_str)
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

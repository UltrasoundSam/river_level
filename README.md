# river_level
Monitors the river level on my way to the station and will notify me if flooded

This project is to help me avoiding walking along a riverside path on my way to work, only to discovered that the pathway is flooded and impassable. Whilst flood alerts are issued for the area of interest, I have found that the path is often easily passable even if a flood alert has been issued, and consequently doesn't help me decide whether to walk along the river or not. 

Here, I am capturing the data from the Environment Agency's Near Real-time River level monitoring API (https://environment.data.gov.uk/flood-monitoring/doc/reference) and placing it into a database. I'm also checking to see whether it is in flood, and whether the river level is above the level at which the path usually floods. 

As well as being able to save the data in a database for further use (the real-time API data only last for ~28 days, before being archived), it will also mean I can be notified when the path is likely impassable.

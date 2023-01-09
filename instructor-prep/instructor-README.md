# Instructor preparation and customization

I hope other instructors of introductory computer science courses 
will find this student project useful as a real-world, non-trivial 
example of recursion that is within the grasp of a beginning 
programmer.  We use it toward the end of the first academic term in 
our majors sequence. 

A project is more relatable, I believe, if it uses local and 
relevant data.  The data we use in Eugene is from a bicycle ride 
that starts and ends in Eugene.  If you are a runner in Salem, 
perhaps you could substitute data captured from one of your runs. If 
you are a hiker in Ashland, perhaps you have data from a hike.

## Python libraries: Instructor's virtual environment

This project is designed so that your students do not need to use 
Python cartographic modules like `gpxpy` and `utm`, but you do. You 
will need to create a virtual environment for the preparation.  In 
the `instructor-prep` directory, execute

```commandline
python3 -m venv env
.   /env/bin/activate
pip3 install -r requirements.txt
```

This should install the modules you need locally.  To leave the 
virtual environment, use `deactivate`.  To enter it again, use 
`env/bin/activate`.   

## Translate activity data from latlon GPX to UTM CSV.  

Whatever your outside activity, if you use a GPS device or record 
your activity with GPS tracking on your phone, you can probably 
obtain this data in GPX format.  For example, you can obtain GPX 
downloads from Strava.   

A GPX file contains longitude and latitude 
for points along the path of the activity, in XML format. Distance 
calculations with latitude and longitude are complex because they 
are distances on a sphere.  Therefor the first thing we need to do 
is to convert them to plane coordinates in meters, the UTM 
coordinate system.  This will entail some distortion, because the 
earth is round, and there is no distortion-free method to map 
spherical coordinates to plane coordinates.  The distortion is 
acceptably small for areas less than about 100 miles by 100 miles, 
which is sufficient for most non-motorized outdoor activities.  
Program `gpx_dump.py` takes a GPX file and produces a CSV file 
containing UTM "easting" and "westing" coordinates.  Take note of 
the UTM "zone" it uses, because that will be important in 
registering a path to a map imagine. 

## Register a map image

We need a simple mapping from UTM coordinates to pixel coordinates 
in the image of a map.  Perhaps if you are an expert in using GIS 
tools, you can obtain such a map image from your favorite GIS tools. 
(And perhaps then you can also document how you did it, so others 
can follow your example.)  I am not expert in GIS tools, so I worked 
out the following procedure for obtaining a registered map image. 

### Capture map region as PNG

I like to start with SVG map images from Wikimedia Commons, to avoid 
copyright issues.  You can scale and crop the SVG map to get a good 
high resolution PNG of the region you need. 
You could also capture a screenshot of the area 
of interest from a web map product like Google Maps, but be careful 
of restrictions on reproduction and distribution.  OpenStreetMaps is 
a good source of open source map data and images, and the Leaflet 
javascript framework is fantastic for making customized maps.  For 
the UO version of this project, I took a screen-shot of a region in 
OpenStreetMaps. 

Save a PNG of the image you wish to use as a basemap.  Remember that 
larger regions will suffer more distortion from the mismatch between 
plane coordinates (UTM) and the map projection. 

### Get coordinates of two widely spaced features

We will need 


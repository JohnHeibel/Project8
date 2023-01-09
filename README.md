# Project 8: Path Simplifier
CS1 student project:  Douglas-Peucker polyline
simplifier for a GPS trace.

![Smith River loop, reduced from 14392 points to 353 points](
docs/img/SmithLoop-550x350.png
)

### Objective

More exercise with recursion, in a practical application. 

## Overview

Ramer-Douglas-Peucker (also known as
Douglas-Peucker and as Duda-Hart split-and-merge)
is an important geometry algorithm for reducing the number of points 
in a path to produce a good approximation. For example,
the route shown in the illustration above started as 14,392 readings 
from a GPS device.  The program developed in this project reduced 
it to 
the 353 points that are plotted on the basemap.  
Ramer-Douglas-Peucker is widely used in cartography and robotics, 
and has other applications. 


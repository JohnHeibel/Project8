"""Configuration file for path simplification"""

# Basemap with dimensions
BASEMAP_IMAGE = "basemaps/Oregon-Siuslaw-Smith.png"
BASEMAP_WIDTH_PX = 987
BASEMAP_HEIGHT_PX = 565

# CSV file of raw path UTM coordinates
UTM_CSV = "data/Smith_River_300k_pre-ride_2022.csv"

TOLERANCE_METERS = 100

# We need UTM and Pixel coordinates of two
# landmarks, widely spaced (e.g., near northeast and southwest corners,
# or near northwest and southeast).  These will be used to
# "register" the image for conversion of UTM coordinates to
# pixel coordinates.
#
# Landmark 1, UTM  (Bridge at entry to Reedsport)
P1_UTM_E = 411248
P1_UTM_N = 4840075
# Landmark 2, UTM  (I 105 meets Hwy 126)
P2_UTM_E = 505519
P2_UTM_N = 4876926
# Landmark 1, Pixels   (Bridge at entry to Reedsport)
P1_PX_X = 69
P1_PX_Y = 460
# Landmark 2, Pixels  (I105 meets Hwy 126)
P2_PX_X = 922
P2_PX_Y = 118

# Derived easting, northing for pixel 0,0 and width,height
# Slope m of y = mx + b with y being UTM coordinates, x being pixel coordinates
_m_easting =  (P2_UTM_E - P1_UTM_E)/(P2_PX_X - P1_PX_X)
_m_northing = (P2_UTM_N - P1_UTM_N)/(P2_PX_Y - P1_PX_Y)

# Evaluate at screen coordinates (0, 0); y - mx = b
ORIGIN_EASTING = P2_UTM_E - _m_easting * P2_PX_X
ORIGIN_NORTHING = P2_UTM_N - _m_northing * P2_PX_Y

# Evaluate at extent of screen y = mx + b
EXTENT_EASTING = _m_easting * BASEMAP_WIDTH_PX + ORIGIN_EASTING
EXTENT_NORTHING = _m_northing * BASEMAP_HEIGHT_PX + ORIGIN_NORTHING




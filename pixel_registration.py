"""Simple utility for getting pixel coordinates from image,
use together with gpx_dump.landmark_convert to get configuration
numbers to register UTM coordinates to pixel coordinates in basemap.
"""
import graphics.graphics as graphics
import config

win_width = config.BASEMAP_WIDTH_PX
win_height = config.BASEMAP_HEIGHT_PX
window = graphics.GraphWin("Base map registration", win_width, win_height)
basemap = graphics.Image(graphics.Point(win_width // 2, win_height // 2),
                         config.BASEMAP_IMAGE)
basemap.draw(window)

while True:
    pt = window.getMouse()
    print(pt)



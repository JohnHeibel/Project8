"""Plot of UTM coordinates on registered basemap"""

import graphics.utm_plot
import config

from typing import Optional

canvas: Optional[graphics.utm_plot.Map] = None
cursor: Optional[tuple[float, float]] = None

def init():
    """Create the display"""
    global canvas
    canvas = graphics.utm_plot.Map(config.BASEMAP_IMAGE,
                (config.BASEMAP_WIDTH_PX, config.BASEMAP_HEIGHT_PX),
                (config.ORIGIN_EASTING, config.ORIGIN_NORTHING),
                (config.EXTENT_EASTING, config.EXTENT_NORTHING))
    cursor = None

def move_to(point: tuple[float, float]):
    """Set location from which next plot_to will start"""
    global cursor
    cursor = point

def plot_to(point: tuple[float, float]):
    global cursor
    if canvas:
        if cursor:
            canvas.plot_segment(cursor, point)
        cursor = point

def scratch(from_point: tuple[float, float], to_point: tuple[float, float]):
    """Writes a light scratch line that can be erased later"""
    if canvas:
        canvas.plot_segment(from_point, to_point, color=graphics.utm_plot.LIGHT, trial=True)

def clean_scratches():
    """Erase scratchmarks from plot"""
    if canvas:
        canvas.erase_trial_strokes()

def wait_to_close():
    """Prompt user for permission to shut down"""
    global canvas
    global cursor
    if canvas:
        input("Press enter to quit")
        canvas.close()
        canvas = None
        cursor = None


"""Plot UTM points on a basemap image.
M Young, 2022-09-17
"""

import graphics.graphics as graphics

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

PT_MARK_SIZE = 3  # pixels

# Contrasty colors for at least 10 groups
COLOR_WHEEL = [
    graphics.color_rgb(255,0,0),
    graphics.color_rgb(0,255,255),
    graphics.color_rgb(127,0,255),
    graphics.color_rgb(127,255,0),
    graphics.color_rgb(255,0,255),
    graphics.color_rgb(255,127,0),
    graphics.color_rgb(0,0,255),
    graphics.color_rgb(0,127,255),
    graphics.color_rgb(50,50,0),
    graphics.color_rgb(255,0,127)
]

# Colors for path simplification project
# Initially we'll use light grey for trial lines, dark red for the final path
LIGHT = graphics.color_rgb(247,146,230)  # Hot violet
DARK = graphics.color_rgb(150,0,0)

next_color = 0
def choose_color() -> object:
    """Returns next color in color wheel,
    cycling around if necessary.
    """
    global next_color
    choice = COLOR_WHEEL[next_color]
    next_color += 1
    if next_color >= len(COLOR_WHEEL):
        next_color = 0
    return choice

class Map:
    """A plot in UTM coordinates with a georeferenced image"""
    def __init__(self, basemap_path: str,
                 window: tuple[int, int],
                 utm_origin: tuple[int, int],
                 utm_ne_extent: tuple[int, int]):
        win_width, win_height = window
        self.win_width, self.win_height = window
        self.utm_origin_easting, self.utm_origin_northing = utm_origin
        self.utm_extent_easting, self.utm_extent_northing = utm_ne_extent
        self.utm_width = self.utm_extent_easting - self.utm_origin_easting
        self.utm_height = self.utm_extent_northing - self.utm_origin_northing
        self.window = graphics.GraphWin(basemap_path, win_width, win_height)
        self.basemap = graphics.Image(graphics.Point(win_width//2, win_height//2), basemap_path)
        self.basemap.draw(self.window)
        # Conversion factor from meters (UTM) to pixels
        self.pixels_per_meter_easting = self.win_width / self.utm_width
        self.pixels_per_meter_northing = self.win_height / self.utm_height
        # Should be very close but not identical
        log.debug(f"Pixels per meter {self.pixels_per_meter_easting}, {self.pixels_per_meter_northing}")
        # We will keep a list of "trial strokes" that can be erased when the full plot is done
        self.trial_strokes: list[graphics.Line] = []


    def pixel_coordinates(self, easting, northing) -> tuple[int, int]:
        """Convert easting, northing to x,y in canvas space"""
        pixel_x = int(self.pixels_per_meter_easting * (easting - self.utm_origin_easting))
        pixel_y = int(self.pixels_per_meter_northing * (northing - self.utm_origin_northing))
        return (pixel_x, pixel_y)

    def plot_point(self, easting, northing, size_px: int=PT_MARK_SIZE, color: str = "red") -> graphics.Circle:
        pixel_x, pixel_y = self.pixel_coordinates(easting, northing)
        symbol = graphics.Circle(graphics.Point(pixel_x, pixel_y), size_px)
        symbol.setFill(color)
        symbol.draw(self.window)
        return symbol

    def move_point(self, symbol: graphics.Circle, new_pos: tuple[int, int]):
        """Move point to new easting, northing"""
        easting, northing = new_pos
        pixel_x, pixel_y = self.pixel_coordinates(easting, northing)
        old_center = symbol.getCenter()
        old_x, old_y = old_center.x, old_center.y
        symbol.move(pixel_x - old_x, pixel_y - old_y)

    def plot_segment(self,
                      utm_start: tuple[int, int], utm_end: tuple[int, int],
                      color=DARK, trial=False):
        """Plot segment from utm_start to utm_end.
        If trial, segment may be erased by erase_trial_marks.
        """
        easting_start, northing_start = utm_start
        x_start, y_start = self.pixel_coordinates(easting_start, northing_start)
        easting_end, northing_end = utm_end
        x_end, y_end = self.pixel_coordinates(easting_end, northing_end)
        symbol = graphics.Line(graphics.Point(x_start, y_start),
                               graphics.Point(x_end, y_end))
        if trial:
            self.trial_strokes.append(symbol)
        symbol.setWidth(2)
        symbol.setOutline(color)
        symbol.draw(self.window)

    def erase_trial_strokes(self):
        """Erases ALL of them"""
        for mark in self.trial_strokes:
            mark.undraw()
        self.trial_strokes = []


    def connect_all(self,
             symbol: graphics.Circle,
             group: list[tuple[float, float]]):
        color = choose_color()
        symbol.setFill(color)
        center = symbol.getCenter()
        for easting, northing in group:
            x, y = self.pixel_coordinates(easting, northing)
            ray = graphics.Line(center, graphics.Point(x, y))
            ray.setOutline(color)
            ray.draw(self.window)

    def close(self):
        self.window.close()
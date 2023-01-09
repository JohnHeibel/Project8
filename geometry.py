"""A couple useful operations in plane geometry:
  - Find the normal intercept of a point and a line
  - Find the distance of a point from a line
    (which we'll call deviation, i.e., how far the point is from a line
    that would ideally go through it).

First version of these functions was written for a web app that displayed progress of
cyclists with satellite trackers on brevets (long distance cycling events).
Reworked slightly 2022 for student projects at U Oregon.
"""

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def deviation_sq(p1: tuple[float, float], p2: tuple[float, float], p: tuple[float, float]) -> float:
    """Square of shortest distance from point p to a line through p1,p2.
    Faster than distance.  Note we want do do these calculations in floating point,
    rather than integers, so that we can properly compare fractional distances.
    """
    intercept = normal_intercept(p1, p2, p)
    # Standard distance formula, sqrt((x2-x1)^2 +(y2-y1)^2)
    in_x, in_y = intercept
    p_x, p_y = p
    dx = in_x - p_x
    dy = in_y - p_y
    return dx*dx + dy*dy


def normal_intercept(p1: tuple[float, float],
                     p2: tuple[float, float],
                     p: tuple[float, float]) -> tuple[float, float]:
    """
    The point at which a line through p1 and p2
    intersects a normal dropped from p.  See normals.md
    for an illustration.
    """
    log.debug("Normal intercept {}-{} from {}"
                  .format(p1, p2, p))

    p1_x, p1_y = p1
    p2_x, p2_y = p2
    p_x, p_y = p
    # Special cases: slope or normal slope is undefined
    # for vertical or horizontal lines, but the intersections
    # are trivial for those cases

    if p2_x == p1_x:
        log.debug("Intercept at {}".format((p1_x,p_y)))
        return (p1_x, p_y)
    elif p2_y == p1_y:
        log.debug("Intercept at {}".format((p_x, p1_y)))
        return (p_x, p1_y)

    # The slope of the segment, and of a normal ray
    seg_slope = (p2_y - p1_y)/(p2_x - p1_x)
    normal_slope = 0 - (1.0 / seg_slope)

    # For y=mx+b form, we need to solve for b (y intercept)
    seg_b = p1_y - seg_slope * p1_x
    normal_b = p_y - normal_slope * p_x

    # Combining and subtracting the two line equations to solve for
    x_intersect = (seg_b - normal_b) / (normal_slope - seg_slope)
    y_intersect = seg_slope * x_intersect + seg_b
    # Colinear points are ok!

    log.debug("Intercept at {}".format(x_intersect, y_intersect))
    return (x_intersect, y_intersect)

def test():
    """Simple test cases for geometry calculations.
    See docs/img/Deviation.png
    """
    # Just the right triangle, line p1,p2 along hypotenuse
    p1 = (2.0,2.0)
    p2 = (4.0,4.0)
    p = (2.0,4.0)
    dev = deviation_sq(p1, p2, p)
    assert abs(dev - 2.0) < 0.01
    # A line along the path should have deviation 0
    assert abs(deviation_sq(p1, p2, p1)) < 0.01
    assert abs(deviation_sq(p1, p2, p2)) < 0.01
    assert abs(deviation_sq(p1, p2, (3,3))) < 0.01
    # Same if we offset by 1000,5000
    p1 = (1002.0,5002.0)
    p2 = (1004.0,5004.0)
    p = (1002.0,5004.0)
    dev = deviation_sq(p1, p2, p)
    assert abs(dev - 2.0) < 0.01
    assert abs(deviation_sq(p1, p2, p1)) < 0.01
    assert abs(deviation_sq(p1, p2, p2)) < 0.01
    assert abs(deviation_sq(p1, p2, (1003.0,5003.0))) < 0.01


if __name__ == "__main__":
    test()
    print("Tested")


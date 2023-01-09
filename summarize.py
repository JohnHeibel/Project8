"""Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: John Heibel
Credits: HOWTO doc
"""

import csv
import doctest

import geometry
import map_view
import config
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def read_points(path: str) -> list[tuple[float, float]]:
    out_list = []
    with open(path, newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        for row in reader:
            pair = (int(row["Easting"]), int(row["Northing"]))
            out_list.append(pair)
    return out_list

def summarize(points: list[tuple[float, float]],
              tolerance: int = config.TOLERANCE_METERS,
              ) -> list[tuple[float, float]]:
    """
     >>> path = [(0,0), (1,1), (2,2), (2,3), (2,4), (3,4), (4,4)]
     >>> expect = [(0,0), (2,2), (2,4), (4,4)]
     >>> simple = summarize(path, tolerance=0.5)
     >>> simple == expect
     True
    """
    
    summary: list[tuple[float, float]] = [points[0]]
    epsilon = float(tolerance * tolerance)

    def simplify(start: int, end: int):
        """Add necessary points in (start, end] to summary."""
        
        log.debug(f"Simplifying from {start}: {points[start]} to {end}: {points[end]}, {points[start+1:end]}")
        log.debug(f"Summary so far: {summary}")
        map_view.scratch(points[start], points[end])
        if(end-start > 2):
            map_view.scratch(points[start], points[end])
        max_val = 0
        p = 0
        for i in range(start,end):
            cur = geometry.deviation_sq(points[start], points[end], points[i])
            if(cur > epsilon and cur > max_val):
                max_val = cur
                p = i
        if(max_val <= epsilon):
            log.debug(f"Reached base case. Summary is {summary}")
            map_view.plot_to(points[end])
            summary.append(points[end])
            
        else:
            simplify(start, p)
            simplify(p, end)
              
        return

    simplify(0, len(points)-1)
    map_view.clean_scratches()

    return summary


def main():
    points = read_points(config.UTM_CSV)
    map_view.init()
    path = summarize(points)
    print(f"Amount of points before summarizing is {len(points)}, Amount of points after summarizing is {len(path)}")
    map_view.wait_to_close()
    

if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()

# -*- coding: utf-8 -*-

import numpy as np
import gdspy

import argparse


def main(size, numOfTurn, width, space, layerNum):
    
    # The GDSII file is called a library, which contains multiple cells.
    lib = gdspy.GdsLibrary()
    gdspy.current_library=gdspy.GdsLibrary()

    # Geometry must be placed in cells.
    coil = lib.new_cell('COIL')
    
    start = (-0.5*width*(numOfTurn-1) - 0.5*space*numOfTurn, 0.5*width)
    bottomLeft = (-0.5*size + 0.5*width, 0.5*width)
    topLeft = (-0.5*size + 0.5*width, size - 0.5*width)
    topRight = (0.5*size - 0.5*width, size - 0.5*width)
    bottomRight = (0.5*size - 0.5*width, 0.5*width)
    end = (0.5*width*(numOfTurn-1) + 0.5*space*numOfTurn, 0.5*width)
    
    path = gdspy.FlexPath(
        [start,
        bottomLeft,
        topLeft,
        topRight,
        bottomRight,
        end],
        width, gdsii_path=True, layer=(int)(layerNum))
    coil.add(path)

    coilPaths = [gdspy.FlexPath(
            [(start[0], start[1] + (i+1)*(width+space)),
            (bottomLeft[0] + (i+1)*(width+space), bottomLeft[1] + (i+1)*(width+space)),
            (topLeft[0] + (i+1)*(width+space), topLeft[1] - (i+1)*(width+space)),
            (topRight[0] - (i+1)*(width+space), topRight[1] - (i+1)*(width+space)),
            (bottomRight[0] - (i+1)*(width+space), bottomRight[1] + (i+1)*(width+space)),
            (end[0], end[1] + (i+1)*(width+space))],
            width, gdsii_path=True, layer=(int)(layerNum)) for i in range(numOfTurn-1)]

    for coilPath in coilPaths:
        coil.add(coilPath)

    imPaths = [gdspy.FlexPath(
            [(end[0], end[1] + i*(width+space)),
            (start[0] + (0.5+i)*width + (1+i)*space, start[1] + i*(width+space)),
            (start[0] + (0.5+i)*width + (1+i)*space, start[1] + (i+1)*(width+space)),
            (start[0], start[1] + (i+1)*(width+space))],
            width, gdsii_path=True, layer=(int)(layerNum)) for i in range(numOfTurn-1)]

    for imPath in imPaths:
        coil.add(imPath)

    # Add the top-cell to a layout and save
    top = lib.new_cell("TOP")
    top.add(gdspy.CellReference(coil, origin=(0, 0)))
    lib.write_gds("coil.gds")
    coil.write_svg('coil.svg')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', default=100.0, type=float, help='size of a coil[um]')
    parser.add_argument('--n', default=2, type=int, help='number of turns')
    parser.add_argument('--w', default=1.0, type=float, help='line width[um]')
    parser.add_argument('--s', default=1.0, type=float, help='line space[um]')
    parser.add_argument('layerNum', type=int, help='layer number of the output GDSII file')
    args = parser.parse_args()
    
    main(args.size, args.n, args.w, args.s, args.layerNum)

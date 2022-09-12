#! /usr/bin/python3

__all__ = []

# __version__1.0

import plots
import random
import mapUtils
import traceback
import numpy as np
import house_exterior
import interfaceUtils
from fence import Fence
from store import Store
from sector import Sector
from park import ParkBuilder
from Pathfinding import Pathfinder
from worldLoader import WorldSlice
from userUtils import UserUtilities
from build_house import HouseBuilder

# Do we send blocks in batches to speed up the generation process?
USE_BATCHING = True

# x position, z position, x size, z size1
area = (1663, 2684, 250, 250)  # default build area

# see if a build area has been specified
# you can set a build area in minecraft using the /setbuildarea command
buildArea = interfaceUtils.requestBuildArea()
if buildArea != -1:
    x1 = buildArea["xFrom"]
    z1 = buildArea["zFrom"]
    x2 = buildArea["xTo"]
    z2 = buildArea["zTo"]
    # print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)

'''
    @rectangleOverlap: that function check if any two structure are overlapping inside the build area
    @param:
        r1: area of first rectangle
        r2: area of second rectangle
    @return:
        boolean
'''


def rectanglesOverlap(r1, r2):
    """Check that r1 and r2 do not overlap."""
    if (r1[0] >= r2[0] + r2[2]) or (r1[0] + r1[2] <= r2[0]) or (r1[1] + r1[3] <= r2[1]) or (r1[1] >= r2[1] + r2[3]):
        return False
    else:
        return True


if __name__ == '__main__':
    print(f"Build area is at position {area[0]}, {area[1]} with size {area[2]}, {area[3]}")

    # load the world data
    # this uses the /chunks endpoint in the background
    worldSlice = WorldSlice(area)

    # Initiating all the classes that will be used for build settelment.
    pathfinder = Pathfinder(area)
    park_builder = ParkBuilder(area)
    userUtils = UserUtilities(area)
    house_builder = HouseBuilder(area)
    fence_builder = Fence(area)
    store_builder = Store(area)
    sector = Sector(area)

    # calculate a heightmap suitable for building:
    heightmapGround = mapUtils.calcGoodHeightmap(worldSlice)
    heightmapTree = worldSlice.heightmaps["MOTION_BLOCKING"]
    heightmapWater = worldSlice.heightmaps["OCEAN_FLOOR"]

    # getting the water location in the build area
    water_location = heightmapTree - heightmapWater

    # build fence around the build area
    fence_builder.build(area, heightmapGround)
    sectors = sector.calculate_sectors(heightmapGround, water_location)
    # creating build area map array to keep track of all our build
    build_area_map = np.zeros((area[2], area[3]), dtype=np.int64)

    values, counts = np.unique(sectors, return_counts=True)

    index = np.argpartition(-counts, kth=len(values) - 1)

    # creating separate district in build area
    sector_values = values[index]
    districts = []
    for i in range(len(sector_values)):
        loc = np.where(sectors == sector_values[i])
        minx = np.min(loc[0])
        minz = np.min(loc[1])
        maxx = np.max(loc[0])
        maxz = np.max(loc[1])
        district = (area[0] + minx, area[1] + minz, maxx - minx, maxz - minz)
        districts.append(district)

    # we create the intersection of path
    # using the center of the largest sector
    max = -1
    d_choice = -1
    count = 0
    for i in districts:
        s_count = np.where(sectors == count)
        c_length = int(len(s_count[0]))
        if c_length > max:
            max = c_length
            d_choice = count
        count += 1
    first_intersection = False
    int_idx = 0
    while not first_intersection:
        d = districts[d_choice]
        try:
            d_center = (((d[0] + (d[0] + d[2])) // 2), ((d[1] + (d[1] + d[3])) // 2))
            build_area_map[d_center[0] - area[0], d_center[1] - area[1]] = 20
        except:
            int_idx += 1
            continue
        first_intersection = True

    # initial count of store and park in the build area
    storeCount = random.randrange(5, 8)
    parkCount = random.randrange(4, 6)
    store = 0
    park = 0

    for i in range(len(districts)):
        sector_number = sector_values[i]
        # district -1 is the location of water, we don't want to build any structure on water.
        if sector_number == -1:
            continue
        iterationCount = 0
        district_area = districts[i]
        if district_area[2] < 40 or district_area[3] < 40:
            continue
        # how many house we want in each district
        houseCount = (district_area[2] // 20) + (district_area[3] // 20)
        structures = []  # this lis contains all the house , stores , small and medium structures.
        house = 0
        epoch_count = 0
        # If we need to search for new structure to build
        new_build = True
        # how many attempts was for build location search
        attempt = 0
        # we will loop through the district until build enough houses or reach 70000 iteration
        while house < houseCount and iterationCount < 70000:
            # we try to look for proper build location 250 times for a specific
            # build structure, if we fail , we try to build another structure.
            if attempt == 250:
                attempt = 0
                new_build = True
            if new_build:
                isStore = False
                building_park = False
                our_rand = random.uniform(0, 1)
                # checking the probability of building a store or gazebo
                if store <= storeCount and our_rand < .2:
                    isStore = True
                    chance = random.uniform(0, 1)
                    if chance < .6:
                        size = "large"
                        current_build = "Large Store"
                    elif chance < .75:
                        size = "small"
                        current_build = "Small Gazebo"
                    else:
                        size = "medium"
                        current_build = "Medium Gazebo"
                    plot = plots.store_plot(size)

                # Checking the probability of building a park
                elif 0.2 <= our_rand < .35 and park < parkCount:  # build park before build anything else
                    plot = np.zeros((random.randint(10, 20), random.randint(10, 20)), dtype=np.int64)
                    plot[1:plot.shape[0] - 1, 1:plot.shape[1] - 1] = 50

                    plot[plot.shape[0] // 2, 0] = 5
                    plot[plot.shape[0] // 2, -1] = 5
                    building_park = True
                    current_build = "A park"

                # if none of the above happening, we will build a house
                else:
                    storey = 1  # initial storey

                    # we check the probability of being a multistorey house.
                    if np.random.uniform(0, 1) < .6:
                        storey = random.randint(2, 3)

                    # we create the plot for the house
                    plot = np.zeros((random.randint(12, 15), random.randint(16, 20)), dtype=np.int64)
                    plot, floor_plot, roof_plot = plots.house_plot(plot, storey)
                    current_build = "A House"

                # once we have created plot for a build we will try to find a locaition
                # to build the structure for 250 times.
                new_build = False

            houseSizeX = plot.shape[0]
            houseSizeZ = plot.shape[1]

            # in this section we check if the plot is perfect fit for a specific area
            if district_area[0] + 1 >= district_area[0] + district_area[2] - houseSizeX - 1:
                iterationCount += 1
                attempt += 1
                continue

            if district_area[1] + 1 >= district_area[1] + district_area[3] - houseSizeZ - 1:
                iterationCount += 1
                attempt += 1
                continue
            houseX = random.randrange(
                district_area[0] + 1, district_area[0] + district_area[2] - houseSizeX - 1)
            houseZ = random.randrange(
                district_area[1] + 1, district_area[1] + district_area[3] - houseSizeZ - 1)
            houseRect = (houseX, houseZ, houseSizeX, houseSizeZ)
            houseRect_pad = (houseX - 3, houseZ - 3, houseSizeX + 6, houseSizeZ + 6)

            overlapsExisting = False

            try:
                build_slice = build_area_map[houseX - 2 - area[0]: houseX + plot.shape[0] + 2 - area[0],
                              houseZ - 2 - area[1]: houseZ + plot.shape[1] + 2 - area[1]]
            except:

                iterationCount += 1
                attempt += 1
                continue

            can_fit = np.any(build_slice == 1)
            road_fit = np.any(build_slice == 3)

            overlapsExisting = False
            for structure in structures:
                if rectanglesOverlap(houseRect_pad, structure):
                    overlapsExisting = True
                    break

            if can_fit or road_fit:
                overlapsExisting = True
                iterationCount += 1
                attempt += 1
                continue

            # slicing the house location form the sector map, to check if every block of the house is inside same
            # sector.
            slice = sectors[houseX - area[0]:houseX - area[0] + plot.shape[0],
                    houseZ - area[1]:houseZ - area[1] + plot.shape[1]]

            non_sec_count = 0
            for sx in range(slice.shape[0]):
                for sz in range(slice.shape[1]):

                    if slice[sx, sz] != sector_number:
                        non_sec_count += 1

            canFit = True
            if non_sec_count >= 10:
                canFit = False

            if np.any(slice == -1):
                canFit = False

            attempt += 1
            iterationCount += 1

            # If everything is fine, we start building.
            if not overlapsExisting and canFit:
                print(
                    f"Building {current_build} at {houseRect[0]}, {houseRect[1]} with size {houseRect[2]},{houseRect[3]}")
                new_build = True
                attempt = 0

                intersections = np.where(build_area_map == 20)
                # find the average height of each corner height of the house
                houseY = sum((
                    userUtils.heightAt(houseX, houseZ, heightmapGround),
                    userUtils.heightAt(houseX + houseSizeX - 1, houseZ, heightmapGround),
                    userUtils.heightAt(houseX, houseZ + houseSizeZ - 1, heightmapGround),
                    userUtils.heightAt(houseX + houseSizeX - 1, houseZ + houseSizeZ - 1, heightmapGround)
                )) // 4

                if building_park:  # if a park is building
                    plot = park_builder.build_park(houseX, houseY, houseZ, houseSizeX, houseSizeZ, build_area_map,
                                                   heightmapGround, heightmapTree)
                    doors = np.where(plot == 5)
                    park += 1
                # if we are not going to build store, we are building house
                elif not isStore:
                    # give the house a random height
                    houseSizeY = random.randrange(3, 5)
                    # build the house!
                    plot, roof_plot, floor_plot = plots.plot_rolling(plot, roof_plot, floor_plot)
                    stair_plot = plots.stair_plot(roof_plot, plot, houseSizeY)
                    house_builder.buildHouse(houseX, houseY, houseZ, houseX + houseSizeX,
                                             houseY + houseSizeY, houseZ + houseSizeZ, plot, roof_plot, storey,
                                             heightmapGround,
                                             heightmapTree, stair_plot)
                    house_builder.buildHouseInterior(houseX, houseY, houseZ, houseX + houseSizeX,
                                                     houseY + houseSizeY, houseZ + houseSizeZ, plot, floor_plot,
                                                     heightmapGround,
                                                     stair_plot, storey)
                    plot = house_builder.buildHouseProperty(houseX, houseY, houseZ, houseX + houseSizeX,
                                                            houseY + houseSizeY, houseZ + houseSizeZ, plot,
                                                            heightmapGround,
                                                            intersections, pathfinder, area)
                    house += 1
                    doors = np.where(plot == 15)
                else:
                    store_builder.build(houseX, houseY, houseZ, houseX + houseSizeX, houseZ + houseSizeZ, plot, size,
                                        heightmapGround, heightmapTree)
                    doors = np.where(plot == 5)
                    store += 1
                structures.append(houseRect)

                # once the structure is build , we start building the path using A star heuristic
                for pr in range(plot.shape[0]):
                    for pc in range(plot.shape[1]):
                        plot[pr, pc] = 1 if plot[pr, pc] != 15 else 2
                build_area_map[houseX - area[0]:houseX - area[0] + plot.shape[0],
                houseZ - area[1]: houseZ - area[1] + plot.shape[1]] = plot

                # creating intersection of a road
                intersections = np.where(build_area_map == 20)
                try:
                    nx = doors[0][0] + houseX
                    nz = doors[1][0] + houseZ

                except:
                    print("Door not found")
                    continue
                bestChoice = -1
                dist = 10000000
                for i in range(len(intersections[0])):
                    dist_test = pathfinder.aStarHeuristic(nx - area[0], nz - area[1], intersections[0][i],
                                                          intersections[1][i])
                    if dist_test < dist:
                        dist = dist_test
                        bestChoice = i
                try:

                    print(
                        f"A-Star: {nx - area[0]}, {nz - area[1]}, {intersections[0][bestChoice]}, {intersections[1][bestChoice]} ")
                    path = pathfinder.aStarSearch(build_area_map, nx - area[0], nz - area[1],
                                                  intersections[0][bestChoice],
                                                  intersections[1][bestChoice], heightmapGround)
                    build_area_map = pathfinder.drawPath(build_area_map, nx, nz, path, heightmapGround, worldSlice,
                                                         area[0], area[1])
                    iterationCount = iterationCount + 1

                except Exception:
                    print(traceback.format_exc())

    if USE_BATCHING:
        # we need to send any blocks remaining in the buffer
        interfaceUtils.sendBlocks()

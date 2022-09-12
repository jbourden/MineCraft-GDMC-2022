import random
import numpy as np
import interfaceUtils
import house_exterior
from userUtils import UserUtilities


class ParkBuilder:

    def __init__(self, area):
        self.area = area
        self.utils = UserUtilities(area)

    '''
        @build_park: build a park on a specific location.
        @param:
            x1, y1, z1: the location fo the park
            p_width: park width
            p_length: park length
            heightmapGround: height map of build area of surface
            heightmapTree: height map of the trees in the build area
        @return:
             park plot: a 2 dimensional array
    '''

    def build_park(self, x1, y1, z1, p_width, p_length, master_map, heightmapGround, heightmapTree):

        self.utils.fill_plot(x1, x1 + p_width + 1, y1, z1, z1 + p_length + 1, heightmapGround, "minecraft:bricks")
        self.utils.clean_plot((x1 - 1, z1 - 1, x1 + p_width + 1, z1 + p_length + 1), y1, heightmapTree)
        p_length_n = p_length - 1 if p_length % 2 == 0 else p_length
        p_width_n = p_width - 1 if p_width % 2 == 0 else p_width
        park_plot = np.zeros((p_width_n, p_length_n), dtype='int64')
        park_structure = []

        self.make_courtyard(x1, y1, z1, p_width_n, p_length_n)

        park_plot[0, park_plot.shape[1] // 2 - 1] = 5
        park_plot[park_plot.shape[0] // 2 - 1, 0] = 5
        park_plot[park_plot.shape[0] - 1, park_plot.shape[1] // 2 - 1] = 5
        park_plot[park_plot.shape[0] // 2 - 1, park_plot.shape[1] - 1] = 5

        return park_plot

    def make_courtyard(self, x1, y1, z1, c_wid, c_len):

        colors = ["minecraft:bricks", "minecraft:quartz_block", 'minecraft:cobblestone', 'minecraft:black_concrete',
                  "minecraft:oak_wood"]
        wall_col = colors[random.randint(0, len(colors) - 1)]
        floor_col = colors[random.randint(0, len(colors) - 1)]
        x2 = x1 + c_wid if x1 + c_wid % 2 == 1 else x1 + c_wid + 1
        z2 = z1 + c_len if z1 + c_len % 2 == 1 else z1 + c_len + 1

        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if (x == x1 and z == ((z1 + z2) // 2)) or (x == x1 and z == 1 + ((z1 + z2) // 2)) or (
                        x == x1 and z == ((z1 + z2) // 2 - 1)):
                    continue
                elif (x == x2 and z == ((z1 + z2) // 2)) or (x == x2 and z == 1 + ((z1 + z2) // 2)) or (
                        x == x2 and z == ((z1 + z2) // 2 - 1)):
                    print("hit me")
                    continue
                elif (z == z2 and x == ((x1 + x2) // 2)) or (z == c_wid + z1 and x == ((x1 + x2) // 2) + 1) or (
                        z == c_wid + z1 and x == ((x1 + x2) // 2) - 1):
                    continue
                elif (z == z1 and x == ((2 * x1 + c_wid) // 2)) or (z == z1 and x == ((x1 + x2) // 2) + 1) or (
                        z == z1 and x == ((x1 + x2) // 2) - 1):
                    continue

                elif x == x1 or z == z1 or x == x2 or z == z2:
                    interfaceUtils.placeBlockBatched(x, y1, z, wall_col)
                    interfaceUtils.placeBlockBatched(x, y1 + 1, z, wall_col)

                else:
                    interfaceUtils.placeBlockBatched(x, y1 - 1, z, floor_col)

        for x in range(x1 + 2, x2 - 1):
            interfaceUtils.placeBlockBatched(x, y1, (z1 + z2) // 2, wall_col)

        for z in range(z1 + 2, z2 - 1):
            interfaceUtils.placeBlockBatched((x1 + x2) // 2, y1, z, wall_col)

        house_exterior.buildFlowerBed(x1 + 3, y1, z1 + 3, (x1 + x2) // 2 - 5 - x1, (z1 + z2) // 2 - 5 - z1, True)
        house_exterior.buildFlowerBed(x1 + 3, y1, (z1 + z2) // 2 + 2, (x1 + x2) // 2 - 5 - x1, (z1 + z2) // 2 - 5 - z1,
                                      True)
        house_exterior.buildFlowerBed((x1 + x2) // 2 + 2, y1, (z1 + z2) // 2 + 2, (x1 + x2) // 2 - 5 - x1,
                                      (z1 + z2) // 2 - 5 - z1, True)
        house_exterior.buildFlowerBed((x1 + x2) // 2 + 2, y1, z1 + 3, (x1 + x2) // 2 - 5 - x1, (z1 + z2) // 2 - 5 - z1,
                                      True)

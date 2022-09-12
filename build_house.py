import plots
import random
import numpy as np
import interfaceUtils
import house_exterior
from Pathfinding import Pathfinder
from userUtils import UserUtilities

"""
Class HouseBuilder:
    This class builds the houses in the settlement
    Builds house interior, such as basement, furniture, and all the house decoration 
    Builds house exterior, fence around the house, swimming pools or flower bed in side the house. 
"""


class HouseBuilder:
    def __init__(self, area):
        self.area = area
        self.utils = UserUtilities(area)

    '''
        @buildHouse: create house base, wall,door and roof . 
        @param:
            x1, y1, z1, x2, y2, z2 : the location and the height of the house in the build area
            plot, roof: plot map for house and the roof of the house
            storey: how many storey is the house
            stairs: stair plot of the house
            heightmapGround: height map for ground blocks
            heightmapTree: height map for trees or any kind of obstacle above the build location
        @return:
            none
    '''

    def buildHouse(self, x1, y1, z1, x2, y2, z2, plot, roof, storey, heightmapGround, heightmapTree, stairs):
        # flatten the ground

        self.utils.clean_plot((x1, z1, x2, z2), y1, heightmapTree)
        self.utils.fill_plot(x1, x2, y1, z1, z2, heightmapGround, "minecraft:stone_bricks")

        colors = ["minecraft:bricks",
                  "minecraft:polished_blackstone_bricks",
                  "minecraft:stripped_acacia_wood",
                  "minecraft:polished_andesite",
                  "minecraft:birch_wood"
                  ]

        doors = ['minecraft:birch_door', 'minecraft:jungle_door',
                 'minecraft:oak_door', 'minecraft:acacia_door', 'minecraft:warped_door',
                 'minecraft:dark_oak_door', 'minecraft:spruce_door']

        roof_colors = ['minecraft:brick_slab',
                       'minecraft:polished_blackstone_brick_slab',
                       'minecraft:acacia_slab',
                       'minecraft:polished_andesite_slab',
                       'minecraft:quartz_slab']

        ground_colors = ["minecraft:grass_block",
                         "minecraft:stripped_acacia_wood",
                         "minecraft:mossy_stone_bricks",
                         "minecraft:stone_bricks"]

        stair_color = ['minecraft:glowstone',
                       'minecraft:end_stone',
                       'minecraft:end_stone_bricks',
                       'minecraft:lodestone'
                       ]
        secondary_color_index = random.randint(0, len(colors) - 1)
        secondary_color = colors[secondary_color_index]
        main_color = colors[random.randint(0, len(colors) - 1)]
        ground_clr = ground_colors[random.randint(0, len(ground_colors) - 1)]
        roof_color = roof_colors[secondary_color_index]
        door = doors[random.randint(0, len(doors) - 1)]

        stair_block = stair_color[random.randint(0, len(stair_color) - 1)]
        striped = random.uniform(0, 1)

        floor_height = y2 - y1

        if storey > 1:
            y2 = y1 + (floor_height * storey) + storey
            open_balcony = False
            if random.randint(0, 10) > 5:
                open_balcony = True

        for x in range(plot.shape[0]):
            for z in range(plot.shape[1]):
                x_pos, z_pos = x1 + x, z1 + z

                interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, ground_clr)
                if plot[x, z] == 1:
                    for y in range(y1, y2):
                        if y % 2 == 0 and striped < 0.45:
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, secondary_color)
                        else:
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, main_color)

                    for y in range(y1, y2):
                        if y1 < y < y2 and y % 2 == 1:
                            window_chance = random.random()
                            if window_chance < 0.3:
                                interfaceUtils.placeBlockBatched(x_pos, y, z_pos, "glass")

                if plot[x, z] == 3:
                    for y in range(y1, y2):
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, secondary_color)

                if plot[x, z] == 4:
                    for y in range(y1 + 3, y2):
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, main_color)
                    interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, f"{door}[half=lower,facing=east,hinge=left]")
                    interfaceUtils.placeBlockBatched(x_pos, y1 + 1, z_pos,
                                                     f"{door}[half=upper,facing=east,hinge=left]")
                    interfaceUtils.placeBlockBatched(x_pos, y1 + 2, z_pos, secondary_color)

                if plot[x, z] == 8:
                    for y in range(y1, y2):
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, main_color)
                    for y in range(y1, y1 + 3):
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, secondary_color)
                if plot[x, z] == 11:
                    for y in range(y1, y2):
                        if y - y1 == 0:
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos,
                                                             f"{door}[half=lower,facing=east,hinge=left]")

                        elif y - y1 == 1:
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos,
                                                             f"{door}[half=upper,facing=east,hinge=left]")
                        else:
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, main_color)

                if storey > 1:
                    if roof[x, z] == 1 or roof[x, z] == 2 or roof[x, z] == 3 or roof[x, z] == 4:
                        s = 1
                        block_visit = False
                        index = 1

                        for y in range(y1, y2):

                            current_stair = stairs[index]
                            if s < storey:
                                if not block_visit:
                                    if current_stair[x, z] > 0:
                                        interfaceUtils.placeBlockBatched(x_pos, y + (current_stair[x, z]) - 1, z_pos,
                                                                         stair_block)
                                        block_visit = True

                            if y == y1 + ((s * floor_height) + s) - 1:
                                if s < storey:
                                    if current_stair[x, z] < 1:
                                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos,
                                                                         "minecraft:polished_blackstone_bricks")

                                    if current_stair[x, z] == -1:
                                        interfaceUtils.placeBlockBatched(x_pos, y + 1, z_pos, "minecraft:iron_bars")
                                else:
                                    interfaceUtils.placeBlockBatched(x_pos, y, z_pos,
                                                                     "minecraft:polished_blackstone_bricks")
                                if s < storey:
                                    if plot[x, z] == 11:
                                        interfaceUtils.placeBlockBatched(x_pos, y + 1, z_pos,
                                                                         f"{door}[half=lower,facing=east,hinge=left]")
                                        interfaceUtils.placeBlockBatched(x_pos, y + 2, z_pos,
                                                                         f"{door}[half=upper,facing=east,hinge=left]")

                                if roof[x, z] == 4:
                                    for h in range(y + 1, y + 1 + floor_height):
                                        if h != y2:
                                            interfaceUtils.placeBlockBatched(x_pos, h, z_pos, "air")
                                            if not open_balcony:
                                                interfaceUtils.placeBlockBatched(x_pos, h, z_pos, "glass")

                                    if open_balcony:
                                        interfaceUtils.placeBlockBatched(x_pos, y + 1, z_pos, "iron_bars")
                                s += 1
                                if index == 0:
                                    index = 1
                                else:
                                    index = 0

                    blocks = ["blackstone_wall", "glass"]
                    if plot[x, z] == 1 or plot[x, z] == 8 or plot[x, z] == 4:
                        for k in range(y2 + 1, y2 + 5):
                            interfaceUtils.placeBlockBatched(x_pos, k, z_pos, "air")
                        block = self.utils.blockColor(x, z, blocks)
                        interfaceUtils.placeBlockBatched(x_pos, y2, z_pos, block)
                        interfaceUtils.placeBlockBatched(x_pos, y2 + 1, z_pos, "iron_bars")
                    if plot[x, z] == 3:
                        interfaceUtils.placeBlockBatched(x_pos, y2, z_pos, "redstone_block")
                        interfaceUtils.placeBlockBatched(x_pos, y2 + 1, z_pos, "redstone_lamp")
        pitched_roof = False
        if storey > 1:
            probability = random.uniform(0, 1)
            if probability < .6:
                pitched_roof = True

        if storey == 1 or pitched_roof:
            # Getting the main roof location
            mr_loc = np.where(roof == 1)
            mr_x1 = np.min(mr_loc[0])
            mr_z1 = np.min(mr_loc[1])

            mr_x2 = np.max(mr_loc[0])
            mr_z2 = np.max(mr_loc[1])

            # Random pitch height.
            pitch = random.randint(3, 7)

            # Will keep drawing pitch height until it doesn't have the indicies anymore
            try:
                type = "bottom"
                for i in range(pitch + 1):
                    for x in range(mr_x1 + i - 1, mr_x2 + 2 - i):
                        for z in range(mr_z1 + i - 1, mr_z2 + 2 - i):
                            interfaceUtils.placeBlockBatched(x + x1, int(y2 + i / 2), z + z1,
                                                             f'{roof_color}[type={type}]')
                    if type == "top":
                        type = "bottom"
                    else:
                        type = "top"
            except:
                print("Pitch too high.")

            # Grabbing the location of the secondary roof
            mr_loc = np.where(roof == 2)
            mr_x1 = np.min(mr_loc[0])
            mr_z1 = np.min(mr_loc[1])

            mr_x2 = np.max(mr_loc[0])
            mr_z2 = np.max(mr_loc[1])

            for x in range(mr_x1 - 1, mr_x2 + 2):
                for z in range(mr_z1 - 1, mr_z2 + 2):
                    interfaceUtils.placeBlockBatched(x + x1, y2, z + z1, secondary_color)

    '''
        @buildHouseInterior: create house interior , basement and stairs to the basement. 
        @param:
            x1, y1, z1, x2, y2, z2 : the location and the height of the house in the build area
            house_plot, floor_plot: plot map for house and the floor of the house
            heightmapGround: height map for ground blocks
            heightmapTree: height map for trees or any kind of obstacle above the build location
        @return:
            none
    '''

    def buildHouseInterior(self, x1, y1, z1, x2, y2, z2, house_plot, floor_plot, heightmapGround, stair, storey):
        make_basement = False
        make_upper_floor = False

        ## Find the points of the main square
        wall_points = np.where(floor_plot == 1)
        hx1 = np.min(wall_points[0])
        hx2 = np.max(wall_points[0])
        hz1 = np.min(wall_points[1])
        hz2 = np.max(wall_points[1])

        floor_height = y2 - y1
        basement_plot = floor_plot[hx1: hx2 + 1, hz1: hz2 + 1]
        main_plot = floor_plot[hx1: hx2 + 1, hz1: hz2 + 1]
        basement = False
        basement_prob = random.uniform(0, 1)
        if basement_prob < .45:
            basement = True

        if basement:
            # Clear space for the basement
            for y in range(y1 - 1, y1 - floor_height - 1, - 1):
                for x in range(hx1 + 1 + x1, hx2 + x1):
                    for z in range(hz1 + 1 + z1, hz2 + z1):
                        if y == y1 - floor_height - 1:
                            interfaceUtils.placeBlockBatched(x, y - 1, z, "minecraft:granite")
                        else:
                            interfaceUtils.placeBlockBatched(x, y, z, "minecraft:air")
            basement_y = y1 - (y2 - y1) - 1
            for x in range(stair[0].shape[0]):
                for z in range(stair[0].shape[1]):
                    x_pos, z_pos = x1 + x, z1 + z
                    if stair[0][x, z] > 0:
                        interfaceUtils.placeBlockBatched(x_pos, basement_y + stair[0][x, z] - 1, z_pos, "bricks")

                    if house_plot[x, z] == 2 and stair[0][x, z] < 1:
                        interfaceUtils.placeBlockBatched(x_pos, y1 - 1, z_pos, "minecraft:polished_blackstone_bricks")
                        if stair[0][x, z] == -1:
                            interfaceUtils.placeBlockBatched(x_pos, y1, z_pos, 'minecraft:iron_bars')
                    if floor_plot[x, z] == 3 or floor_plot[x, z] == 1:
                        for y in range(basement_y, y1):
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, 'minecraft:orange_glazed_terracotta')
        beds = ['minecraft:gray_bed', 'minecraft:light_gray_bed', 'minecraft:cyan_bed', 'minecraft:blue_bed']
        furniture = ["bed", 'book_shelf', "couch", 'scaffolding', 'enchanting_table', "chest"]
        carpets = ['minecraft:white_carpet', 'minecraft:orange_carpet', 'minecraft:magenta_carpet', 'minecraft'
                                                                                                    ':light_blue_carpet',
                   'minecraft:yellow_carpet', 'minecraft:lime_carpet', 'minecraft:gray_carpet']
        furniture_plots_all = plots.furniture_plot(stair, storey, basement, floor_plot, house_plot)

        for f_plot in range(len(furniture_plots_all)):
            furniture_plots = furniture_plots_all[f_plot]
            if f_plot == 0:
                y = y1
            if f_plot == 1:
                y = y + floor_height + 1
            if f_plot == 2:
                y = y + floor_height + 1
            if basement and f_plot == len(furniture_plots_all) - 1:
                y = y1 - floor_height - 1

            carpet = carpets[random.randrange(0, len(carpets))]
            for x in range(furniture_plots.shape[0]):
                for z in range(furniture_plots.shape[1]):
                    x_pos, z_pos = x1 + x, z1 + z
                    location = furniture_plots[x, z]
                    furn = furniture[random.randrange(0, len(furniture))]
                    if location == 8:
                        interfaceUtils.placeBlockBatched(x_pos, y + floor_height - 1, z_pos, 'minecraft:beacon')
                    if location == 2 or location == 8 or location == -2:
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, carpet)
                    if location != 4 and location != 5 and location != 6 and location != 7:
                        continue
                    if location == 4:
                        dir = [-1, 0]
                        next_move = [0, 1]
                        direction = "west"
                        l_direction = "north"
                        r_direction = "south"
                    if location == 5:
                        dir = [0, -1]
                        next_move = [1, 0]
                        direction = "north"
                        l_direction = "west"
                        r_direction = "east"
                    if location == 6:
                        dir = [0, 1]
                        next_move = [1, 0]
                        direction = "south"
                        l_direction = "west"
                        r_direction = "east"

                    if location == 7:
                        dir = [1, 0]
                        next_move = [0, 1]
                        direction = "east"
                        l_direction = "north"
                        r_direction = "south"
                    if furn == "bed":
                        bed = beds[random.randrange(0, len(beds))]
                        if furniture_plots[x - dir[0], z - dir[1]] == 2:
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos, f"{bed}[facing={direction},part=head]")
                            interfaceUtils.placeBlockBatched(x_pos - dir[0], y, z_pos - dir[1],
                                                             f"{bed}[facing={direction},part=foot]")
                            furniture_plots[x - dir[0], z - dir[1]] = -1
                            if furniture_plots[x + next_move[0], z + next_move[1]] == location:
                                furniture_plots[x + next_move[0], z + next_move[1]] = -1
                                interfaceUtils.placeBlockBatched(x_pos + next_move[0], y, z_pos + next_move[1],
                                                                 "white_wool")
                                interfaceUtils.placeBlockBatched(x_pos + next_move[0], y + 1, z_pos + next_move[1],
                                                                 "soul_lantern")
                    if furn == "book_shelf":
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, 'minecraft:bookshelf')
                        interfaceUtils.placeBlockBatched(x_pos, y + 1, z_pos, 'minecraft:bookshelf')
                        if furniture_plots[x + next_move[0], z + next_move[1]] == location:
                            interfaceUtils.placeBlockBatched(x_pos + next_move[0], y, z_pos + next_move[1],
                                                             'minecraft:bookshelf')
                            interfaceUtils.placeBlockBatched(x_pos + next_move[0], y + 1, z_pos + next_move[1],
                                                             'minecraft:bookshelf')
                        furniture_plots[x + next_move[0], z + next_move[1]] = -1

                    if furn == "scaffolding":
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, 'minecraft:scaffolding')
                        interfaceUtils.placeBlockBatched(x_pos, y + 1, z_pos, 'minecraft:scaffolding')
                        if furniture_plots[x + next_move[0], z + next_move[1]] == location:
                            interfaceUtils.placeBlockBatched(x_pos + next_move[0], y, z_pos + next_move[1],
                                                             'minecraft:scaffolding')
                            interfaceUtils.placeBlockBatched(x_pos + next_move[0], y + 1, z_pos + next_move[1],
                                                             'minecraft:scaffolding')
                            furniture_plots[x + next_move[0], z + next_move[1]] = -1
                    if furn == "enchanting_table":
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, 'minecraft:enchanting_table')
                        furniture_plots[x + next_move[0], z + next_move[1]] = -1
                    if furn == "couch":
                        if furniture_plots[x - next_move[0], z - next_move[1]] == location and \
                                furniture_plots[x + next_move[0], z + next_move[1]] == location:
                            interfaceUtils.placeBlockBatched(x_pos - next_move[0], y, z_pos - next_move[1],
                                                             f'minecraft:birch_trapdoor[facing={l_direction}, half=bottom,'
                                                             f'open=true]')
                            interfaceUtils.placeBlockBatched(x_pos, y, z_pos,
                                                             f'minecraft:sandstone_stairs[facing={direction},half=bottom, '
                                                             f'shape=straight]')
                            interfaceUtils.placeBlockBatched(x_pos + next_move[0], y, z_pos + next_move[1],
                                                             f'minecraft:birch_trapdoor[facing={r_direction}, half=bottom,'
                                                             f'open=true]')
                            furniture_plots[x + next_move[0], z + next_move[1]] = -1
                    if furn == "chest":
                        interfaceUtils.placeBlockBatched(x_pos, y, z_pos, 'minecraft:ender_chest')

    '''
        @buildHouseProperty: create house property , such as wall around the house. 
        @param:
            x1, y1, z1, x2, y2, z2 : the location and the height of the house in the build area
            plot: plot map for house
            heightmapGround: height map for ground blocks
            intersections: the closest path loacation
            heightmapTree: height map for trees or any kind of obstacle above the build location
            pathfinder: the path finder for the house
        @return:
            none
    '''

    def buildHouseProperty(self, x1, y1, z1, x2, y2, z2, plot, heightmapGround, intersections, pathfinder, area):
        ground_colors = ["minecraft:black_concrete",
                         "minecraft:stripped_acadia_wood",
                         "minecraft:mossy_stone_bricks",
                         "minecraft:stone_bricks"]

        fence_color = ["minecraft:dark_oak_fence", 'minecraft:nether_brick_fence', 'minecraft:crimson_fence',
                       'minecraft:warped_fence']
        ground_clr = ground_colors[random.randint(0, len(ground_colors) - 1)]
        fence = fence_color[random.randrange(0, len(fence_color))]

        ## Draw the fence
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):

                if (x == x1 or x == x2) or (z == z1 or z == z2):

                    for h in range(12):
                        interfaceUtils.placeBlockBatched(x, y1 + h, z, "minecraft:air")

                    for h in range(2):
                        if h == 0:
                            interfaceUtils.placeBlockBatched(x, y1 + h, z, "minecraft:black_concrete")
                        else:
                            interfaceUtils.placeBlockBatched(x, y1 + h, z, fence)

        ## Draw the ground
        for x in range(x1 + 1, x2):
            for z in range(z1 + 1, z2):
                if plot[x - x1, z - z1] == 0:
                    interfaceUtils.placeBlockBatched(x, y1 - 1, z, ground_clr)

        center_point = ((x1 + x2) // 2, (z1 + z2) // 2)

        bestChoice = -1
        dist = 1000000

        for i in range(len(intersections[0])):
            try:
                dist_test = pathfinder.aStarHeuristic(center_point[0] - area[0], center_point[1] - area[1],
                                                      intersections[0][i], intersections[1][i])
                if dist_test < dist:
                    dist = dist_test
                    bestChoice = i
            except:
                print("something went wrong with finding the intersection?")
                continue

        e_points = []

        p1 = (x1, (int((z1 + z2) // 2)))
        p2 = (x2, (int((z1 + z2) // 2)))
        p3 = (int(((x1 + x2) / 2)), z1)
        p4 = (int(((x1 + x2) / 2)), z2)

        e_points.append(p1)
        e_points.append(p2)
        e_points.append(p3)
        e_points.append(p4)

        pt_choice = ()
        pt_min = 10000000

        for pt in e_points:
            dist_test = pathfinder.aStarHeuristic(pt[0] - area[0], pt[1] - area[1], intersections[0][bestChoice],
                                                  intersections[1][bestChoice])
            if dist_test < pt_min:
                pt_min = dist_test
                pt_choice = pt

        if pt_choice == p1:
            plot[0, int(plot.shape[1] // 2)] = 15
            for h in range(4):
                interfaceUtils.placeBlockBatched(x1, y1 + h, ((z1 + z2) // 2), "minecraft:air")
                interfaceUtils.placeBlockBatched(x1, y1 + h, ((z1 + z2) // 2) - 1, "minecraft:air")
                interfaceUtils.placeBlockBatched(x1, y1 + h, ((z1 + z2) // 2) + 1, "minecraft:air")

        elif pt_choice == p2:
            plot[plot.shape[0] - 1, int(plot.shape[1] // 2)] = 15
            for h in range(4):
                interfaceUtils.placeBlockBatched(x2, y1 + h, int((z1 + z2) // 2), "minecraft:air")
                interfaceUtils.placeBlockBatched(x2, y1 + h, int((z1 + z2) // 2) - 1, "minecraft:air")
                interfaceUtils.placeBlockBatched(x2, y1 + h, int((z1 + z2) // 2) + 1, "minecraft:air")

        elif pt_choice == p3:
            plot[int(plot.shape[0] // 2), 0] = 15
            for h in range(4):
                interfaceUtils.placeBlockBatched(int((x1 + x2) // 2), y1 + h, z1, "minecraft:air")
                interfaceUtils.placeBlockBatched(int((x1 + x2) // 2) + 1, y1 + h, z1, "minecraft:air")
                interfaceUtils.placeBlockBatched(int((x1 + x2) // 2) - 1, y1 + h, z1, "minecraft:air")

        else:
            plot[int(plot.shape[0] // 2), plot.shape[1] - 1] = 15
            for h in range(4):
                interfaceUtils.placeBlockBatched(int((x1 + x2) // 2), y1 + h, z2, "minecraft:air")
                interfaceUtils.placeBlockBatched(int((x1 + x2) // 2) + 1, y1 + h, z2, "minecraft:air")
                interfaceUtils.placeBlockBatched(int((x1 + x2) // 2) - 1, y1 + h, z2, "minecraft:air")

        empty_num = np.where(plot[1:plot.shape[0] - 2, 1: plot.shape[1] - 2] == 0)
        if len(empty_num[0]) / (plot.shape[0] * plot.shape[1]) < .60:
            ##build flowerbed
            fb_build = True
            fb_count = 1000
            fb_epoch = 0
            while fb_count <= 20000 and fb_build:

                r_w = random.randint(3, 9)
                r_h = random.randint(3, 9)

                r_x = random.randint(x1 + 1, x2 - 2)
                r_z = random.randint(z1 + 1, z2 - 2)

                if r_x - 3 - x1 < 2 or r_z - 3 - z1 < 2 or r_x + r_w + 2 - x1 > plot.shape[0] - 2 or r_z + r_h - z1 > \
                        plot.shape[1] - 2:
                    fb_count += 1
                    continue

                flower_slice = plot[r_x - x1 - 4: r_x + r_w + 1 - + 4, r_z - z1 - 4: r_z - z1 + r_h + 1 + 4]
                if np.all(flower_slice == 0):
                    house_exterior.buildFlowerBed(r_x, y1, r_z, r_w, r_h, False)
                    plot[r_x - x1 - 3: r_x + r_w + 1 - + 3, r_z - z1 - 3: r_z - z1 + r_h + 1 + 3] = 19
                    fb_build = False
                else:
                    fb_count += 1

        else:

            ##build flowerbed
            pool_build = True
            pool_count = 1000
            pool_epoch = 0

            while pool_count <= 20000 and pool_build:

                # if pool_count % 10 == 0:
                #     print(f'Pool Epoch: {pool_epoch}')
                #     pool_epoch += 1

                r_w = random.randint(8, 12)
                r_l = random.randint(8, 12)

                r_x = random.randint(x1 + 1, x2 - 2)
                r_z = random.randint(z1 + 1, z2 - 2)

                if r_x - 2 - x1 < 2 or r_z - 2 - z1 < 2 or r_x + r_w + 2 - x1 > plot.shape[0] - 2 or r_z + r_l - z1 > \
                        plot.shape[1] - 2:
                    pool_count += 1
                    continue

                pool_slice = plot[r_x - x1 - 2: r_x + r_w + 1 + 2, r_z - z1 - 2: r_z - z1 + r_l + 1 + 2]
                if np.all(pool_slice == 0):
                    house_exterior.buildSwimmingPool(r_x, y1, r_z, r_w, r_l)
                    plot[r_x - x1 - 1: r_x + r_w + 1 + 2, r_z - z1 - 1: r_z - z1 + r_l + 2] = 19
                    pool_build = False
                else:
                    pool_count += 1

        ### Draw the corner blocks with lamp
        interfaceUtils.placeBlockBatched(x1 + 1, y1, z1 + 1, "minecraft:black_concrete")
        interfaceUtils.placeBlockBatched(x1 + plot.shape[0] - 1, y1, z1 + 1, "minecraft:black_concrete")
        interfaceUtils.placeBlockBatched(x1 + 1, y1, z1 + plot.shape[1] - 1, "minecraft:black_concrete")
        interfaceUtils.placeBlockBatched(x1 + plot.shape[0] - 1, y1, z1 + plot.shape[1] - 1, "minecraft:black_concrete")
        interfaceUtils.placeBlockBatched(x1 + 1, y1 + 1, z1 + 1, "minecraft:lantern")
        interfaceUtils.placeBlockBatched(x1 + plot.shape[0] - 1, y1 + 1, z1 + 1, "minecraft:lantern")
        interfaceUtils.placeBlockBatched(x1 + 1, y1 + 1, z1 + plot.shape[1] - 1, "minecraft:lantern")
        interfaceUtils.placeBlockBatched(x1 + plot.shape[0] - 1, y1 + 1, z1 + plot.shape[1] - 1, "minecraft:lantern")

        return plot

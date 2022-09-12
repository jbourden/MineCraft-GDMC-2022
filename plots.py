import random
import numpy as np

__all__ = []
'''
    @store_plot: generate plot for structure other than houses, such as store, and 
    2 different out door structure.
    @param:
        size: size of the structure. 
    @return:
        return the 2d array
'''


def store_plot(size):
    # small structure
    if size == "small":
        store = np.array(
            [[1, 2, 2, 2, 2, 1],
             [2, 7, 7, 7, 7, 2],
             [2, 6, 6, 6, 6, 2],
             [2, 6, 6, 6, 6, 2],
             [1, 4, 1, 3, 3, 1]], dtype=np.int64)
    # medium structure
    if size == "medium":
        store = np.array(
            [
                [0, 7, 7, 7, 7, 7, 7, 7, 0],
                [7, 1, 2, 3, 9, 3, 2, 1, 7],
                [7, 2, 3, 4, 8, 4, 3, 2, 7],
                [7, 3, 10, 8, 6, 8, 11, 3, 7],
                [7, 2, 3, 4, 8, 4, 3, 2, 7],
                [7, 1, 2, 3, 12, 3, 2, 1, 7],
                [0, 7, 7, 7, 7, 7, 7, 7, 0]
            ], dtype=np.int64
        )
    # large store plot
    if size == "large":
        store_l = random.randrange(8, 12)
        store_w = random.randrange(10, 15)
        store = np.zeros((store_l, store_w), dtype=np.int64)

        store[:, 0] = 1
        store[0, :] = 1
        store[store_l - 1, 0:store_w] = 1  # solid walls
        store[2:store_l - 2, store_w - 1] = 4  # glass walls
        sideGlassWall = random.randrange(0, 11)
        if sideGlassWall > 7:
            store[0, 2:store_w - 2] = 4
            store[store_l - 1, 2:store_w - 2] = 4

        if sideGlassWall <= 6:
            side = random.randrange(0, 2)
            if side == 0:
                store[0, 2:store_w - 2] = 4
            else:
                store[store_l - 1, 2:store_w - 2] = 4

        store[0, 0] = 3  # top left corner
        store[0, store_w - 1] = 3
        store[store_l - 1, 0] = 3
        store[store_l - 1, store_w - 1] = 3  # corners
        store[1:store_l - 1, 1:store_w - 1] = 2  # floor
        store = np.where(store == 0, 6, store)

        rand = random.uniform(0, 1)
        if rand < .6:
            store[1:store_l - 1, 1] = 7
            store[2:store_l - 2, 5] = 7
            store[3:store_l - 3, 7] = 7
        else:
            store[1, 1:store_w - 2] = 8
            store[store_l - 2, 1:store_w - 2] = 8
            store[3, 2: 7] = 8
            store[5, 2: 7] = 8

    plot = np.pad(store, ((2, 2), (2, 2)))
    plot[plot.shape[0] // 2, -1] = 5

    return plot


'''
    @create_plot: generate plot for houses.
    @param:
        plot: a 2 dimensional numpy array with random size. 
        plot_location: the location of the house in build area.
    @return:
         2 dimensional array
'''


def house_plot(plot, storey):
    twoSquares = False

    m_sqr_l = random.randrange(8, plot.shape[1])
    m_sqr_w = random.randrange(8, plot.shape[0] - 3)

    # starting coords
    startX = (plot.shape[0] - m_sqr_w) // 2
    startZ = (plot.shape[1] - m_sqr_l) // 2

    roof_plot = np.copy(plot)
    roof_plot[startX:startX + m_sqr_w + 1, startZ:startZ + m_sqr_l + 1] = 1

    # The main shape in the plot map
    plot[startX:startX + m_sqr_w + 1, startZ:startZ + m_sqr_l + 1] = 1

    # The carpet in the plot map
    plot[startX + 1:startX + m_sqr_w, startZ + 1:startZ + m_sqr_l] = 2

    # Decorate the corners
    plot[startX, startZ] = 3  # top left corner
    plot[startX, startZ + m_sqr_l] = 3  # top right corner

    # Checking to see if we can fit another square in our plot
    # so, we can build multi-section houses
    if plot.shape[0] - m_sqr_w >= 4:
        twoSquares = True

    else:
        floor_plot = np.copy(plot)
        roof_plot = np.copy(plot)

    if twoSquares:

        # Shift the map up.
        plot = np.roll(plot, -startX, axis=0)
        roof_plot = np.roll(roof_plot, -startX, axis=0)

        floor_plot = np.copy(plot)
        startX = 0

        # Drawing the second square
        s_sqr_l = random.randint(4, 7)
        s_sqr_w = plot.shape[0] - startX - m_sqr_w - 1
        s_sqr_start = random.randrange(startZ, startZ + m_sqr_l - s_sqr_l + 1)
        plot[startX + m_sqr_w:m_sqr_w + s_sqr_w + 1, s_sqr_start:s_sqr_start + s_sqr_l + 1] = 1
        plot[startX + m_sqr_w + 1:m_sqr_w + s_sqr_w, s_sqr_start + 1:s_sqr_start + s_sqr_l] = 2

        for i in range(startX + m_sqr_w, m_sqr_w + s_sqr_w + 1):
            for j in range(s_sqr_start, s_sqr_start + s_sqr_l + 1):

                if roof_plot[i, j] != 1:
                    roof_plot[i, j] = 2

    # Decorate the bottom corners
    if not twoSquares:
        try:
            plot[startX + m_sqr_w, startZ] = 3  # bottom left
            plot[startX + m_sqr_w, startZ + m_sqr_l] = 3  # bottom right
        except:
            print("couldn't do it")
    else:
        if s_sqr_start != startZ:
            plot[startX + m_sqr_w, startZ] = 3  # bottom left
        plot[m_sqr_w + s_sqr_w, s_sqr_start] = 3  # bottom left
        if s_sqr_start + s_sqr_l != startZ + m_sqr_l:
            plot[startX + m_sqr_w, startZ + m_sqr_l] = 3  # bottom right
        plot[m_sqr_w + s_sqr_w, s_sqr_start + s_sqr_l] = 3  # bottom right

    # placing doors
    plot[startX + (m_sqr_w // 2), startZ] = 4
    plot[startX + (m_sqr_w // 2) - 1, startZ] = 8
    plot[startX + (m_sqr_w // 2) + 1, startZ] = 8

    if twoSquares:
        # we place the location of the door
        plot[startX + m_sqr_w + s_sqr_w, s_sqr_start + (s_sqr_l // 2)] = 4
        plot[startX + m_sqr_w + s_sqr_w, (s_sqr_start + (s_sqr_l // 2)) + 1] = 8
        plot[startX + m_sqr_w + s_sqr_w, (s_sqr_start + (s_sqr_l // 2)) - 1] = 8
        plot[startX + m_sqr_w, s_sqr_start + (s_sqr_l // 2)] = 11
    else:
        plot[startX + m_sqr_w, startZ + (m_sqr_l // 2)] = 4
        plot[startX + m_sqr_w, (startZ + (m_sqr_l // 2)) + 1] = 8
        plot[startX + m_sqr_w, (startZ + (m_sqr_l // 2)) - 1] = 8

    if twoSquares and storey > 1:
        balcony = np.random.uniform(0, 1)
        if balcony <= .6:
            # if we have balcony we mark it in our roof plot
            s_sqr = np.where(roof_plot == 2)
            min_x = np.min(s_sqr[0])
            max_x = np.max(s_sqr[0])
            min_z = np.min(s_sqr[1])
            max_z = np.max(s_sqr[1])
            roof_plot[min_x:max_x + 1, min_z] = 4
            roof_plot[max_x, min_z:max_z + 1] = 4
            roof_plot[min_x:max_x + 1, max_z] = 4

    # we do random flipping in the plot to change the direction of house
    flip_rand = np.random.uniform(0, 1)
    side_padding = random.randint(4, 7)
    top_bottom_padding = random.randint(4, 8)

    if .33 < flip_rand < .66:
        plot = np.flipud(plot)
        floor_plot = np.flipud(floor_plot)
        roof_plot = np.flipud(roof_plot)
    if flip_rand >= .66:
        plot = np.fliplr(plot)
        floor_plot = np.fliplr(floor_plot)
        roof_plot = np.fliplr(roof_plot)

    # we add padding so our house will have space around ot walk around.
    plot = np.pad(plot, ((side_padding, top_bottom_padding), (top_bottom_padding, side_padding)))
    floor_plot = np.pad(floor_plot,
                        ((side_padding, top_bottom_padding), (top_bottom_padding, side_padding)))
    roof_plot = np.pad(roof_plot, ((side_padding, top_bottom_padding), (top_bottom_padding, side_padding)))

    return plot, floor_plot, roof_plot


'''
    @stair_plot: generate  stair plot for multi storey houses or house with basement.
    @param:
        roof: The roof plot of the house, 
        plot: the main floor plot of the house. 
        floor_height: the height of each floor 
        
    @return:
        array of stairs locaiton plot
'''


def stair_plot(roof, plot, floor_height):
    west_east = [[0, 1], [0, -1]]
    north_south = [[1, 0], [-1, 0]]
    stair_location = []
    all_stairs = []

    # looking for the walls of the house
    walls = np.where(roof == 1)
    west_wall = plot[np.min(walls[0]), np.min(walls[1]):np.max(walls[1]) + 1]
    east_wall = plot[np.max(walls[0]), np.min(walls[1]):np.max(walls[1]) + 1]
    north_wall = plot[np.min(walls[0]):np.max(walls[0]) + 1, np.min(walls[1])]
    south_wall = plot[np.min(walls[0]):np.max(walls[0]) + 1, np.max(walls[1])]

    # Take the wall that does not have any doors.
    if np.all(west_wall != 4) and np.all(west_wall != 11):
        stair_dir = west_east[random.randrange(0, len(west_east))]
        stair_location.append(("west", stair_dir))

    if np.all(east_wall != 4) and np.all(east_wall != 11):
        stair_dir = west_east[random.randrange(0, len(west_east))]
        stair_location.append(("east", stair_dir))

    if np.all(north_wall != 4) and np.all(north_wall != 11):
        stair_dir = north_south[random.randrange(0, len(north_south))]
        stair_location.append(("north", stair_dir))

    if np.all(south_wall != 4) and np.all(south_wall != 11):
        stair_dir = north_south[random.randrange(0, len(north_south))]
        stair_location.append(("south", stair_dir))

    for stair in range(len(stair_location)):
        # loop through all the walls that have no walls
        # and create a stair plot for each  good walls
        s_plot = np.zeros((plot.shape[0], plot.shape[1]), dtype=np.int64)
        stair_wall = stair_location[stair][0]

        # We calculate the possible stair direction for each wall
        # and mark it with a number in the stair plot
        if stair_wall == "north" or stair_wall == "south":
            direction = stair_location[stair][1]
            if direction[0] < 0:
                s_x = np.min(walls[0]) + 3 + floor_height
                rail_x = s_x + 1
            if direction[0] > 0:
                s_x = np.max(walls[0]) - 3 - floor_height
                rail_x = s_x - 1
            if stair_wall == "north":
                s_z = np.min(walls[1]) + 1
            if stair_wall == "south":
                s_z = np.max(walls[1]) - 1
            rail_z = s_z

            for rail in range(floor_height + 3):
                for j in range(3):
                    if rail > floor_height:
                        num = -2
                    else:
                        num = -1
                    if stair_wall == "north":
                        s_plot[rail_x + direction[0] * rail, rail_z + j + direction[1] * rail] = num
                    if stair_wall == "south":
                        s_plot[rail_x + direction[0] * rail, rail_z - j + direction[1] * rail] = num

            for i in range(floor_height):
                for j in range(2):
                    if stair_wall == "north":
                        s_plot[s_x + direction[0] * i, (s_z + j + direction[1] * i)] = 1 + i
                    if stair_wall == "south":
                        s_plot[s_x + direction[0] * i, s_z - j + direction[1] * i] = 1 + i
            all_stairs.append(s_plot)

        if stair_wall == "east" or stair_wall == "west":
            direction = stair_location[stair][1]
            if direction[1] < 0:
                s_z = np.min(walls[1]) + 3 + floor_height
                rail_z = s_z + 1
            if direction[1] > 0:
                s_z = np.max(walls[1]) - 3 - floor_height
                rail_z = s_z - 1
            if stair_wall == "east":
                s_x = np.max(walls[0]) - 1
            if stair_wall == "west":
                s_x = np.min(walls[0]) + 1
            rail_x = s_x
            s_plot[s_x, s_z] = 1

            for rail in range(floor_height + 3):
                for j in range(3):
                    if rail > floor_height:
                        num = -2
                    else:
                        num = -1
                    if stair_wall == "east":
                        s_plot[rail_x - j + direction[0] * rail, rail_z + direction[1] * rail] = num
                    if stair_wall == "west":
                        s_plot[rail_x + j + direction[0] * rail, rail_z + direction[1] * rail] = num

            for i in range(floor_height):
                for j in range(2):
                    if stair_wall == "east":
                        s_plot[s_x - j + direction[0] * i, s_z + direction[1] * i] = 1 + i
                    if stair_wall == "west":
                        s_plot[s_x + j + direction[0] * i, s_z + direction[1] * i] = 1 + i
            all_stairs.append(s_plot)

    return all_stairs


'''
    @furniture_plot: using stair plot we can get the stair location and using plot , we can get the door location 
        of a house, then we use those location to place furniture.
    @param:
        stairs: the array of all the stairs, 
        storey: How many storey the house is,. 
        basement: Boolean, if there a basement
        floor_plot: the plot for floor 
        plot: the main house plot
    @return:
        The array of furniture plot for each floor, and for basement
'''


def furniture_plot(stairs, storey, basement, floor_plot, plot):
    # checking how many storey the houses will be then create initiate furniture plot for each storey
    for s in range(storey):
        if s + 1 == 1:
            main_floor_furniture = np.copy(floor_plot)
        if s + 1 == 2:
            second_floor_furniture = np.copy(floor_plot)
        if s + 1 == 3:
            third_floor_furniture = np.copy(floor_plot)

    # an empty array for all the furniture plots
    furniture_plots = []

    # for the main floor, replacing all the doors into one number for simplification
    main_floor_plot = np.where(plot == 11, 4, plot)

    # Looking for the floors
    available_space = np.where(floor_plot == 2)
    min_x = np.min(available_space[0])
    max_x = np.max(available_space[0])
    min_z = np.min(available_space[1])
    max_z = np.max(available_space[1])

    main_floor_furniture[min_x, min_z] = 8
    main_floor_furniture[min_x, max_z] = 8
    main_floor_furniture[max_x, min_z] = 8
    main_floor_furniture[max_x, max_z] = 8
    walls = np.where(floor_plot == 1)
    west_wall = main_floor_plot[np.min(walls[0]), np.min(walls[1]):np.max(walls[1]) + 1]
    east_wall = main_floor_plot[np.max(walls[0]), np.min(walls[1]):np.max(walls[1]) + 1]
    north_wall = main_floor_plot[np.min(walls[0]):np.max(walls[0]) + 1, np.min(walls[1])]
    south_wall = main_floor_plot[np.min(walls[0]):np.max(walls[0]) + 1, np.max(walls[1])]

    main_floor_furniture[min_x, min_z + 2:max_z - 1] = 4
    main_floor_furniture[max_x, min_z + 2:max_z - 1] = 7
    main_floor_furniture[min_x + 2:max_x - 1, min_z] = 5
    main_floor_furniture[min_x + 2:max_x - 1, max_z] = 6
    if basement:
        basement_furniture = np.copy(main_floor_furniture)
    # Checking if there is no door on that wall
    if np.any(west_wall == 4):
        door = np.where(west_wall == 4)[0][0] + np.min(walls[1])
        main_floor_furniture[min_x:min_x + 2, door - 1:door + 2] = -2
    if np.any(east_wall == 4):
        door = np.where(east_wall == 4)[0][0] + np.min(walls[1])

        main_floor_furniture[max_x - 1:max_x + 1, door - 1:door + 2] = -2
    if np.any(north_wall == 4):
        door = np.where(north_wall == 4)[0][0] + np.min(walls[0])

        main_floor_furniture[door - 1:door + 2, min_z:min_z + 2] = -2
    if np.any(south_wall == 4):
        door = np.where(south_wall == 4)[0][0] + np.min(walls[0])
        main_floor_furniture[door - 1:door + 2, max_z - 1:max_z + 1] = -2

    if basement:
        for x in range(stairs[0].shape[0]):
            for z in range(stairs[0].shape[1]):
                if stairs[0][x, z] != 0:
                    if stairs[0][x, z] == -2:
                        main_floor_furniture[x, z] = -2
                    else:
                        main_floor_furniture[x, z] = -1
                    basement_furniture[x, z] = -1

    if storey > 1:
        for x in range(stairs[1].shape[0]):
            for z in range(stairs[1].shape[1]):
                if stairs[1][x, z] != 0:
                    main_floor_furniture[x, z] = -1
    furniture_plots.append(main_floor_furniture)

    if storey >= 2:

        second_floor_furniture[min_x, min_z] = 8
        second_floor_furniture[min_x, max_z] = 8
        second_floor_furniture[max_x, min_z] = 8
        second_floor_furniture[max_x, max_z] = 8
        walls = np.where(floor_plot == 1)
        west_wall = plot[np.min(walls[0]), np.min(walls[1]):np.max(walls[1]) + 1]
        east_wall = plot[np.max(walls[0]), np.min(walls[1]):np.max(walls[1]) + 1]
        north_wall = plot[np.min(walls[0]):np.max(walls[0]) + 1, np.min(walls[1])]
        south_wall = plot[np.min(walls[0]):np.max(walls[0]) + 1, np.max(walls[1])]

        second_floor_furniture[min_x, min_z + 2:max_z - 1] = 4
        second_floor_furniture[max_x, min_z + 2:max_z - 1] = 7
        second_floor_furniture[min_x + 2:max_x - 1, min_z] = 5
        second_floor_furniture[min_x + 2:max_x - 1, max_z] = 6

        if np.any(west_wall == 11):
            door = np.where(west_wall == 11)[0][0] + np.min(walls[1])
            second_floor_furniture[min_x:min_x + 2, door - 1:door + 2] = -2
        if np.any(east_wall == 11):
            door = np.where(east_wall == 11)[0][0] + np.min(walls[1])

            second_floor_furniture[max_x - 1:max_x + 1, door - 1:door + 2] = -2
        if np.any(north_wall == 11):
            door = np.where(north_wall == 11)[0][0] + np.min(walls[0])

            second_floor_furniture[door - 1:door + 2, min_z:min_z + 2] = -2
        if np.any(south_wall == 11):
            door = np.where(south_wall == 11)[0][0] + np.min(walls[0])
            second_floor_furniture[door - 1:door + 2, max_z - 1:max_z + 1] = -2

        if storey == 3:
            third_floor_furniture = np.copy(second_floor_furniture)
        for x in range(stairs[1].shape[0]):
            for z in range(stairs[1].shape[1]):
                if stairs[1][x, z] != 0:
                    if stairs[1][x, z] == -2:
                        second_floor_furniture[x, z] = -2
                    else:
                        second_floor_furniture[x, z] = -1
        if storey > 2:
            for x in range(stairs[0].shape[0]):
                for z in range(stairs[0].shape[1]):
                    if stairs[0][x, z] != 0:
                        if stairs[0][x, z] == -2:
                            second_floor_furniture[x, z] = -2
                        else:
                            second_floor_furniture[x, z] = -1
        furniture_plots.append(second_floor_furniture)
        if storey == 3:
            for x in range(stairs[0].shape[0]):
                for z in range(stairs[0].shape[1]):
                    if stairs[0][x, z] != 0:
                        if stairs[0][x, z] == -2:
                            third_floor_furniture[x, z] = -2
                        else:
                            third_floor_furniture[x, z] = -1
            furniture_plots.append(third_floor_furniture)

    if basement:
        furniture_plots.append(basement_furniture)

    return furniture_plots


'''
    @getFountain: generate plot for central fountain
    @param:
        none 
    @return:
        2 dimensional array
'''


def fountain_plot():
    fountain = np.zeros((5, 5), dtype=np.int64)
    fountain[0, 0], fountain[0, fountain.shape[1] - 1], fountain[fountain.shape[0] - 1, 0], fountain[
        fountain.shape[0] - 1, fountain.shape[1] - 1] = 1, 1, 1, 1
    fountain[0, 1:fountain.shape[1] - 1] = 2
    fountain[1:fountain.shape[0] - 1, 0] = 2
    fountain[fountain.shape[0] - 1, 1:fountain.shape[1] - 1] = 2
    fountain[1:fountain.shape[0] - 1, fountain.shape[1] - 1] = 2
    fountain[fountain.shape[0] // 2, fountain.shape[1] // 2] = 3
    return fountain

'''
    @plot_rolling: roll all the plots towards a specific direction
    @param:
        plot, roof_plot, floor_plot: plots are used for build houeses
    @return:
        same plot after rolled
'''


def plot_rolling(plot, roof_plot, floor_plot):
    house_loc = np.where(plot != 0)

    max_x = np.max(house_loc[0])
    max_z = np.max(house_loc[1])
    min_x = np.min(house_loc[0])
    min_z = np.min(house_loc[1])

    if np.random.uniform(0, 1) < .99:

        roll_rand = np.random.uniform(0, 1)

        if roll_rand < .125:

            # Roll down
            plot = np.roll(plot, plot.shape[0] - 5 - max_x, 0)
            roof_plot = np.roll(roof_plot, plot.shape[0] - 5 - max_x, 0)
            floor_plot = np.roll(floor_plot, plot.shape[0] - 5 - max_x, 0)

        elif roll_rand < .25:
            # Roll up
            plot = np.roll(plot, 3 - min_x, 0)
            roof_plot = np.roll(roof_plot, 3 - min_x, 0)
            floor_plot = np.roll(floor_plot, 3 - min_x, 0)

        elif roll_rand < .375:
            # Roll left
            plot = np.roll(plot, 3 - min_z, 1)
            roof_plot = np.roll(roof_plot, 3 - min_z, 1)
            floor_plot = np.roll(floor_plot, 3 - min_z, 1)

        elif roll_rand < .5:
            # Roll right
            plot = np.roll(plot, plot.shape[1] - 5 - max_z, 1)
            roof_plot = np.roll(roof_plot, plot.shape[1] - 5 - max_z, 1)
            floor_plot = np.roll(floor_plot, plot.shape[1] - 5 - max_z, 1)

        elif roll_rand < .625:
            # Roll up / right
            plot = np.roll(plot, plot.shape[1] - 5 - max_z, 1)
            roof_plot = np.roll(roof_plot, plot.shape[1] - 5 - max_z, 1)
            floor_plot = np.roll(floor_plot, plot.shape[1] - 5 - max_z, 1)

            plot = np.roll(plot, 3 - min_x, 0)
            roof_plot = np.roll(roof_plot, 3 - min_x, 0)
            floor_plot = np.roll(floor_plot, 3 - min_x, 0)

        elif roll_rand < .75:
            # Roll down / right
            plot = np.roll(plot, plot.shape[0] - 5 - max_x, 0)
            roof_plot = np.roll(roof_plot, plot.shape[0] - 5 - max_x, 0)
            floor_plot = np.roll(floor_plot, plot.shape[0] - 5 - max_x, 0)

            plot = np.roll(plot, plot.shape[1] - 5 - max_z, 1)
            roof_plot = np.roll(roof_plot, plot.shape[1] - 5 - max_z, 1)
            floor_plot = np.roll(floor_plot, plot.shape[1] - 5 - max_z, 1)

        elif roll_rand < .875:
            # Roll up / left
            plot = np.roll(plot, 3 - min_x, 0)
            roof_plot = np.roll(roof_plot, 3 - min_x, 0)
            floor_plot = np.roll(floor_plot, 3 - min_x, 0)

            plot = np.roll(plot, 3 - min_z, 1)
            roof_plot = np.roll(roof_plot, 3 - min_z, 1)
            floor_plot = np.roll(floor_plot, 3 - min_z, 1)
        else:
            # Roll down / left
            plot = np.roll(plot, plot.shape[0] - 5 - max_x, 0)
            roof_plot = np.roll(roof_plot, plot.shape[0] - 5 - max_x, 0)
            floor_plot = np.roll(floor_plot, plot.shape[0] - 5 - max_x, 0)

            plot = np.roll(plot, 3 - min_z, 1)
            roof_plot = np.roll(roof_plot, 3 - min_z, 1)
            floor_plot = np.roll(floor_plot, 3 - min_z, 1)

    return plot, roof_plot, floor_plot

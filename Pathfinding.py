import interfaceUtils
import numpy as np

'''
    @getPath: generate the path location between houses or any walkable structures. 
    @param:
        node: the goal location
    @return:
        list of direction
'''


class Pathfinder:

    def __init__(self, area):
        self.area = area
        self.batching = True

    def heightAt(self, x, z, heightmap):
        """Access height using local coordinates."""
        # Warning:
        # Heightmap coordinates are not equal to world coordinates!
        return heightmap[(x - self.area[0], z - self.area[1])]

    def getPath(self, node):
        path = []
        count = 0
        while node.parent != None:
            count += 1
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path

    '''
        @isOOB: Check if any value x,y is out of the build area 
        @param:
            width, height: the size of build area
            x,y: the value that need to be checked
        @return: 
            boolean , True or False
    '''

    def isOOB(self, width, height, x, z, world_map):
        if (x < 0) or (z < 0) or (x > (width - 1)) or (z > (height - 1)):
            return True

        # if (world_map[x, z] == 1):
        #     return True

        else:
            return False

    # heuristic for Astar search
    def aStarHeuristic(self, x, y, gx, gy):
        return abs(x - gx) + abs(y - gy)

    '''
        @aStarSearch class: path finding algorithm for road generation between houses. 
    '''

    def aStarSearch(self, roads, sx, sy, gx, gy, heightmapGround):
        class Node:
            def __init__(self, cost, parent, x, y, action, f_cost):
                self.cost = cost
                self.parent = parent
                self.x = x
                self.y = y
                self.action = action
                self.f_cost = f_cost

        open_list = []
        grid = np.copy(roads)
        open_check = np.zeros((grid.shape[0], grid.shape[1]))
        root = Node(0, None, sx, sy, None, 0)
        open_list.append(root)
        actions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        searching = True
        count = 0

        while searching:

            count += 1

            if len(open_list) == 0:
                searching = False
                return []
            node = open_list.pop(0)
            if node.x == gx and node.y == gy:
                searching = False
                return self.getPath(node)
            if open_check[node.x, node.y] == 1:
                continue
            open_check[node.x, node.y] = 1
            for i in actions:
                nx = node.x + i[0]
                nz = node.y + i[1]
                if self.isOOB(grid.shape[0], grid.shape[1], nx, nz, grid):
                    continue
                if open_check[nx, nz] == 1:
                    continue
                penalty = 0

                try:
                    node_h = self.heightAt(nx + self.area[0], nz + self.area[1], heightmapGround)
                except:
                    continue

                for window_w in range(-3, 4):
                    for window_h in range(-3, 4):

                        wx = nx + window_w
                        wz = nz + window_h
                        try:
                            wy = self.heightAt(wx + self.area[0], wz + self.area[1], heightmapGround)
                        except:
                            penalty += 100
                            continue

                        height_diff = abs(node_h - wy)

                        if self.isOOB(grid.shape[0], grid.shape[1], wx, wz, grid):
                            continue

                        if height_diff > 1:
                            penalty = 50 * height_diff

                        if (grid[wx, wz] == 1):
                            penalty += 400

                g = 100 + node.cost + penalty
                parent = node
                new_node = Node(g, parent, nx, nz, [i[0], i[1]], g + self.aStarHeuristic(nx, nz, gx, gy))
                open_list.append(new_node)

            open_list = sorted(open_list, key=lambda x: x.f_cost, reverse=False)

    def rectanglesOverlap(self, r1, r2):
        """Check that r1 and r2 do not overlap."""
        if (r1[0] >= r2[0] + r2[2]) or (r1[0] + r1[2] <= r2[0]) or (r1[1] + r1[3] <= r2[1]) or (r1[1] >= r2[1] + r2[3]):
            return False
        else:
            return True

    def drawPath(self, build_area_map, nx, nz, path, heightmapGround, worldSlice, map_w, map_h):

        world = worldSlice

        master_map = np.copy(build_area_map)
        count = 0
        turn = 0
        last_action = [0, 0]
        last_height = (self.heightAt(nx, nz, heightmapGround))
        # Build the path block in the build area between house and intersection
        print("Drawing path.")
        for i in path:

            if i != last_action and last_action != [0, 0]:

                for ww in range(-1, 2):
                    for wh in range(-1, 2):
                        wx = nx + ww
                        wz = nz + wh
                        if (master_map[wx - self.area[0], wz - self.area[1]] == 1 or master_map[
                            wx - self.area[0], wz - self.area[1]] == 3):
                            continue
                        interfaceUtils.placeBlockBatched(wx, last_height - 1, wz, "minecraft:stone_bricks")

            nx = nx + i[0]
            nz = nz + i[1]

            last_action = i

            y = self.heightAt(nx, nz, heightmapGround)
            y1 = self.heightAt(nx - 1, nz, heightmapGround)
            y2 = self.heightAt(nx + 1, nz, heightmapGround)

            min_h = min(y, min(y1, y2))

            if abs(min_h - last_height) > 1:
                p_height = last_height + 1 if min_h > last_height else last_height - 1

            else:
                p_height = min_h

            if i == [1, 0] or i == [-1, 0]:

                for ww in range(-1, 2):
                    for wh in range(-1, 2):
                        wx = nx + ww
                        wz = nz + wh
                        if (master_map[wx - self.area[0], wz - self.area[1]] == 1 or master_map[
                            wx - self.area[0], wz - self.area[1]] == 3):
                            continue

                        for air in range(12):
                            interfaceUtils.placeBlockBatched(wx, p_height + air, wz, "minecraft:air")

                        interfaceUtils.placeBlockBatched(wx, p_height - 1, wz, "minecraft:stone_bricks")

                        master_map[wx - self.area[0], wz - self.area[1]] = 3 if master_map[
                                                                                    wx - self.area[0], wz - self.area[
                                                                                        1]] != 20 else 20

                if count % 21 == 0 and count != 0:

                    try:
                        if np.all(master_map[nx - 7: nx + 8, nz - 7: nz + 8] != 21):

                            for air in range(12):
                                interfaceUtils.placeBlockBatched(nx, p_height + air, nz - 2, "minecraft:air")
                                interfaceUtils.placeBlockBatched(nx, p_height + air, nz + 2, "minecraft:air")

                            for h in range(4):
                                if h == 3:
                                    if turn % 2 == 0 and master_map[nx - self.area[0], nz - self.area[1] + 2] != 3 and \
                                            master_map[nx - self.area[0], nz - self.area[1] - 2] != 3:

                                        interfaceUtils.placeBlockBatched(nx, p_height + h, nz - 2, "minecraft:lantern")
                                        master_map[nx - self.area[0], nz - self.area[1] - 2] = 21

                                    else:
                                        interfaceUtils.placeBlockBatched(nx, p_height + h, nz + 2, "minecraft:lantern")
                                        master_map[nx - self.area[0], nz - self.area[1] + 2] = 21
                                else:
                                    if turn % 2 == 0 and master_map[nx - self.area[0] - 2, nz - self.area[1] + 2] != 3:

                                        interfaceUtils.placeBlockBatched(nx, p_height + h, nz - 2,
                                                                         "minecraft:blackstone")
                                    else:
                                        interfaceUtils.placeBlockBatched(nx, p_height + h, nz + 2,
                                                                         "minecraft:blackstone")
                    except:
                        print("OOB")

            if i == [0, 1] or i == [0, -1]:

                for ww in range(-1, 2):
                    for wh in range(-1, 2):
                        wx = nx + ww
                        wz = nz + wh
                        if (master_map[wx - self.area[0], wz - self.area[1]] == 1 or master_map[
                            wx - self.area[0], wz - self.area[1]] == 3):
                            continue
                        for air in range(12):
                            interfaceUtils.placeBlockBatched(wx, p_height + air, wz, "minecraft:air")

                        interfaceUtils.placeBlockBatched(wx, p_height - 1, wz, "minecraft:stone_bricks")

                        master_map[wx - self.area[0], wz - self.area[1]] = 3 if master_map[
                                                                                    wx - self.area[0], wz - self.area[
                                                                                        1]] != 20 else 20

                if count % 21 == 0 and count != 0:
                    try:
                        if np.all(master_map[nx - 7: nx + 8, nz - 7: nz + 8] != 21):

                            for air in range(12):
                                interfaceUtils.placeBlockBatched(nx - 2, p_height + air, nz, "minecraft:air")
                                interfaceUtils.placeBlockBatched(nx + 2, p_height + air, nz, "minecraft:air")

                            for h in range(4):
                                if h == 3:

                                    if turn % 2 == 0 and master_map[nx - self.area[0] - 2, nz - self.area[1] + 2] != 3:

                                        interfaceUtils.placeBlockBatched(nx - 2, p_height + h, nz, "minecraft:lantern")
                                    else:
                                        interfaceUtils.placeBlockBatched(nx + 2, p_height + h, nz, "minecraft:lantern")

                                    master_map[nx - self.area[0] - 2, nz - self.area[1]] = 21
                                    master_map[nx - self.area[0] + 2, nz - self.area[1]] = 21

                                else:
                                    if turn % 2 == 0 and master_map[nx - self.area[0] - 2, nz - self.area[1] + 2] != 3:

                                        interfaceUtils.placeBlockBatched(nx - 2, p_height + h, nz,
                                                                         "minecraft:cobblestone")
                                    else:
                                        interfaceUtils.placeBlockBatched(nx + 2, p_height + h, nz,
                                                                         "minecraft:cobblestone")
                    except:
                        print("OOB")
            if (count % 10 == 0) and count != 0:
                master_map[nx - self.area[0], nz - self.area[1]] = 20
            count += 1
            turn += 1
            last_height = p_height

            interfaceUtils.sendBlocks()
        print("Finished drawing path.")
        return master_map

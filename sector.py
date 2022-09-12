import numpy as np

class Sector:
    def __init__(self, area):
        self.sectors = np.zeros((area[2], area[3]), dtype=np.int64)

    # checking a block is inside the build area , and walkable form given neighbor(node)
    def islegalAction(self, node, action, height, heightmapGround):
        x = node[0] + action[0]
        y = node[1] + action[1]
        if 0 <= x < heightmapGround.shape[0] and 0 <= y < heightmapGround.shape[1]:
            h = heightmapGround[x, y]
            if height - 1 <= h <= height + 1:
                return True

        return False

    # Cardinal bfs algorithm to create sector.
    def cardinalBFS(self, x, y, height, heightmapGround, water_location, sectorNumber):
        actions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        openlist = []
        openlist.append([x, y])
        while len(openlist) > 0:
            node = openlist.pop()
            node_height = heightmapGround[node[0], node[1]]
            if self.sectors[node[0], node[1]] == 0 and height + 5 >= node_height >= height - 5:
                if water_location[node[0], node[1]] > 0:
                    self.sectors[node[0], node[1]] = -1
                else:
                    self.sectors[node[0], node[1]] = sectorNumber
                for i in range(len(actions)):
                    if self.islegalAction(node, actions[i], node_height, heightmapGround):
                        x = node[0] + actions[i][0]
                        y = node[1] + actions[i][1]
                        openlist.append([x, y])

    '''@calculate_sectors: generate sector using height map,and water location, to divide the build are into different 
                            sectors. 
        @paras: 
            heightmapGround:height map for ground blocks
            water_location: location of water in the build area. 
            sectors: 2 dimensional array with all values equal to 0
        @return:
            completed sector map

    '''

    def calculate_sectors(self, heightmapGround, water_location):
        sectorNumber = 0
        for x in range(self.sectors.shape[0]):
            for y in range(self.sectors.shape[1]):
                if self.sectors[x, y] == 0:
                    height = heightmapGround[x, y]
                    sectorNumber += 1
                    self.cardinalBFS(x, y, height, heightmapGround, water_location, sectorNumber)

        return self.sectors

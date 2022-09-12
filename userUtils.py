import interfaceUtils

class UserUtilities:
    def __init__(self, area):
        self.area = area

    def heightAt(self, x, z, heightmap):
        """Access height using local coordinates."""
        # Warning:
        # Heightmap coordinates are not equal to world coordinates!
        return heightmap[(x - self.area[0], z - self.area[1])]

    """
    This function create a flat surface on a specific area with a given height
    @params:
        area: specific area to work
        init_y: the height we want to use to create plane
        heightmap: array of heights of the top block on a given x , z position
    @return:
        none
"""

    def clean_plot(self, plot, init_y, heightmap):
        for x in range(plot[0], plot[2]):  # loop through each x position in the given range
            for z in range(plot[1], plot[3]):  # loop through each z position in the given range
                y = self.heightAt(x, z, heightmap)  # getting the height of the most top block on x, z position
                if y > init_y:  # checking if the height is larger than our initial height
                    diff_y = y - init_y  # get the height difference
                    for d in range(
                            diff_y + 1):  # replacing all the blocks with air blocks that are above initial height.
                        interfaceUtils.placeBlockBatched(x, init_y + diff_y - d, z, "air")

    '''
        This function fill up the empty places under any structure we built
        in the settlement. 
        @params:
            x1,x2,y1,z1,z2: location in the build area ,that need to be filled.
            heightmapGround: height of ground 
        @return:
            none
    '''

    def fill_plot(self, x1, x2, y1, z1, z2, heightmapGround, block):
        for x in range(x1, x2):
            for z in range(z1, z2):
                y = self.heightAt(x, z, heightmapGround)
                if y < y1:
                    diff = y1 - y
                    for d in range(diff):
                        interfaceUtils.placeBlockBatched(x, y + d, z, block)

    def blockColor(self, x, z, blocks):
        if x % 2 == 0:
            if z % 2 == 0:
                block = blocks[0]
            else:
                block = blocks[1]
        else:
            if z % 2 == 0:
                block = blocks[1]
            else:
                block = blocks[0]
        return block

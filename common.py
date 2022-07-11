#################################################################
# Global Constants
#################################################################

#################################################################
# Coordinates of each tile
#################################################################
GAP = 240

#tile0_coord = (486.04, 417.77, 590.39, 316.37)
#tile0_coord = (486, 419, 589, 316)
tile0_coord = (966, 616, 1189, 849)
tile1_coord = (966+GAP*1, 616+GAP*0, 1189+GAP*1, 849+GAP*0)
tile2_coord = (966+GAP*2, 616+GAP*0, 1189+GAP*2, 849+GAP*0)
tile3_coord = (966+GAP*3, 616+GAP*0, 1189+GAP*3, 849+GAP*0)
tile4_coord = (966+GAP*0, 616+GAP*1, 1189+GAP*0, 849+GAP*1)
tile5_coord = (966+GAP*1, 616+GAP*1, 1189+GAP*1, 849+GAP*1)
tile6_coord = (966+GAP*2, 616+GAP*1, 1189+GAP*2, 849+GAP*1)
tile7_coord = (966+GAP*3, 616+GAP*1, 1189+GAP*3, 849+GAP*1)
tile8_coord = (966+GAP*0, 616+GAP*2, 1189+GAP*0, 849+GAP*2)
tile9_coord = (966+GAP*1, 616+GAP*2, 1189+GAP*1, 849+GAP*2)
tile10_coord = (966+GAP*2, 616+GAP*2, 1189+GAP*2, 849+GAP*2)
tile11_coord = (966+GAP*3, 616+GAP*2, 1189+GAP*3, 849+GAP*2)
tile12_coord = (966+GAP*0, 616+GAP*3, 1189+GAP*0, 849+GAP*3)
tile13_coord = (966+GAP*1, 616+GAP*3, 1189+GAP*1, 849+GAP*3)
tile14_coord = (966+GAP*2, 616+GAP*3, 1189+GAP*2, 849+GAP*3)
tile15_coord = (966+GAP*3, 616+GAP*3, 1189+GAP*3, 849+GAP*3)

coord_list = [tile0_coord, tile1_coord, tile2_coord, tile3_coord,
              tile4_coord, tile5_coord, tile6_coord, tile7_coord,
              tile8_coord, tile9_coord, tile10_coord, tile11_coord,
              tile12_coord, tile13_coord, tile14_coord, tile15_coord]
board = [0]*16

#################################################################
# Useful Values
#################################################################
UP = 500
DOWN = 501
RIGHT = 502
LEFT = 503

valid_dirs = [UP, DOWN, RIGHT, LEFT]
valid_dirs_weights = [1, 40, 40, 19]

#################################################################
# Tile Weights
#################################################################
tile_heuristic_grid = [10, 8, 5, 1,
                       15, 25, 50, 100,
                       800, 600, 500, 200,
                       1000, 2000, 3000, 5000]

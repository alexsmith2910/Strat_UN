import secrets
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
for i in range(7):
    print(i)

def tiles_map(x, y):
    tiles = []
    for i in range(y):
        tiles.append([])
    for i in range(len(tiles)):
        # print("layer" + str(i))
        for j in range(x):
            # b = secrets.randbelow(255)
            num = secrets.randbelow(10)
            if num > 1:
                tiles[i - 1].append(1)
            else:
                tiles[i - 1].append(-1)
    #for i in range(len(tiles)):

    return tiles
print(map := tiles_map(30, 20))

matrix = [
  [1, 1, 1],
  [1, 0, 1],
  [1, 1, 1]
]
grid = Grid(matrix=map)

start = grid.node(0, 0)
end = grid.node(2, 17)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print("Path: ", path)
print(grid.grid_str(path=path, start=start, end=end))
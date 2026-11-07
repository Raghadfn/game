import pygame
import random
from collections import deque
import time
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Define color
# BoarderColor = (190, 110, 80) 
# CellsColor = (180, 110, 80)
# MazeBoarderColor = (200, 160, 110) 
# PathCellsColor = (34, 34, 122) 

BoarderColor = (102, 51, 0)  # بني غامق
CellsColor = (235, 194, 153)  # بني فاتح
MazeBoarderColor = (139, 69, 19)  # بني غامق محمر (يمكن تعديله حسب الرغبة)
PathCellsColor = (153, 102, 51)  # سكري

# Set up the game window
width, height = 1000, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
playerImage = pygame.image.load(".\\robot.jpg")
goalImage = pygame.image.load(".\\box.jpg")
winnerImage = pygame.image.load(".\\robot.jpg")
pygame.display.set_caption("Maze Game")

# Define maze properties

maze_width, maze_height = (20,20)
cell_height = height // maze_height
cell_width = width // maze_width
maze = [[0] * maze_width for _ in range(maze_height)]
typeOfCell = [[0] * maze_width for _ in range(maze_height)] 
path = dict()
start_x, start_y = 1, 1
h=random.randint(2,maze_height-2)
w=random.randint(2,maze_width-2)
goal_x, goal_y = h, w

playerImage = pygame.transform.scale(playerImage, (cell_width - 2, cell_height - 2))
goalImage = pygame.transform.scale(goalImage, (cell_width - 1, cell_height - 1))
winnerImage = pygame.transform.scale(winnerImage, (cell_width - 1, cell_height - 1))

def draw_line(y1, x1, y2, x2):
    pygame.draw.line(screen, 
                     BoarderColor, 
                     (y1 * cell_width, x1 * cell_height), 
                     (y2 * cell_width, x2 * cell_height)
                     )
def draw_rect(color, y, x, add_width, add_height, min_width, min_height):
    pygame.draw.rect(screen, 
                     color, 
                     (y * cell_width + add_width, 
                      x * cell_height + add_height, 
                      cell_width + min_width, 
                      cell_height + min_height
                      ))
        
def generate_maze():
    frontier = []
    def add_frontier(x, y):
        if x >= 1 and y >= 1 and y < maze_width - 1 and x < maze_height - 1 and typeOfCell[x][y] == 0 :
            typeOfCell[x][y] = 1
            frontier.append((x, y))
    def mark(x, y):
        typeOfCell[x][y] = 2
        add_frontier(x-1, y)
        add_frontier(x+1, y)
        add_frontier(x, y-1)
        add_frontier(x, y+1)
    def neighbors(x, y):
        n = []
        if x > 1 and typeOfCell[x - 1][y] == 2:
            n.append((x-1, y))
        if x < maze_height - 2 and typeOfCell[x + 1][y] == 2:
            n.append((x+1, y))
        if y > 1 and typeOfCell[x][y - 1] == 2:
            n.append((x, y - 1))
        if y < maze_width - 2 and typeOfCell[x][y + 1] == 2:
            n.append((x, y+1))
        return n
    x, y = random.randrange(1, maze_height - 1), random.randrange(1, maze_width - 1)
    mark(x, y)
    while len(frontier) != 0:
        random_index = random.randrange(len(frontier))
        x, y = frontier.pop(random_index) 
        n = neighbors(x, y)
        nx, ny = n[random.randrange(len(n))]
        path[((x, y), (nx, ny))] = 1
        path[((nx, ny), (x, y))] = 1
        mark(x, y)
    for i in range(1, maze_height - 1):
        for j in range(1, maze_width - 1):
            if ((i, j), (i, j + 1)) not in path:
                draw_line(j + 1, i + 1, j + 1, i)
            if ((i, j), (i, j - 1)) not in path:
                draw_line(j, i, j, i + 1)
            if ((i, j), (i + 1, j)) not in path:
                draw_line(j, i + 1, j + 1, i + 1)
            if ((i, j), (i - 1, j)) not in path:
                draw_line(j, i, j+1, i)

# Draw the maze
def draw_maze():
    screen.fill(CellsColor)
    for j in range (0, maze_width):
        draw_rect(MazeBoarderColor, j, 0, 0, 0, 0, 0)
        draw_rect(MazeBoarderColor, j, (maze_height - 1), 0, 0, 0, 0)
    for i in range (0, maze_height):
        draw_rect(MazeBoarderColor, 0, i, 0, 0, 0, 0)
        draw_rect(MazeBoarderColor, (maze_width - 1), i, 0, 0, 0, 0)
    generate_maze()

# Maze solver
def calculate_heuristic(cell1, cell2):
    # Manhattan distance heuristic
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

# Apply A* Algorithm for generating solving path
def maze_solver():
    x = 1
    y = 1
    g_score = dict()
    h_score = dict()
    for i in range(1, maze_height - 1):
            for j in range(1, maze_width - 1):
                g_score[(i, j)] = 1000000000
                h_score[(i, j)] = 1000000000
    g_score[(x, y)] = 0
    h_score[(x, y)] = calculate_heuristic([x, y], [goal_x, goal_y])
    open = PriorityQueue()
    open.put((h_score[(x, y)],h_score[(x, y)], [x, y]))
    aPath={}
    while not open.empty():
        currCell = open.get()[2]
        if currCell == [goal_x, goal_y]:
            break
        for d in 'ESNW':
            if d == 'E' and ((currCell[0], currCell[1]), (currCell[0], currCell[1] + 1)) in path:
                childCell = [currCell[0], currCell[1] + 1]
            elif d == 'W' and ((currCell[0], currCell[1]), (currCell[0], currCell[1] - 1)) in path:
                childCell = [currCell[0], currCell[1] - 1]
            elif d == 'N' and ((currCell[0], currCell[1]), (currCell[0] - 1, currCell[1])) in path:
                childCell = [currCell[0] - 1, currCell[1]]
            elif d == 'S' and ((currCell[0], currCell[1]), (currCell[0] + 1, currCell[1])) in path:
                childCell = [currCell[0] + 1, currCell[1]]
            else:
                continue

            temp_g_score = g_score[(currCell[0], currCell[1])] + 1
            temp_h_score = temp_g_score + calculate_heuristic(childCell,[goal_x, goal_y])

            if temp_h_score < h_score[(childCell[0], childCell[1])]:
                g_score[(childCell[0], childCell[1])] = temp_g_score
                h_score[(childCell[0], childCell[1])] = temp_h_score
                open.put((temp_h_score,calculate_heuristic(childCell,[goal_x,goal_y]),childCell))
                aPath[(childCell[0], childCell[1])] = (currCell[0], currCell[1])
    
    return aPath

def drawPath():
    solvePath = maze_solver()
    cell = (goal_x, goal_y)
    while True:
        cell = solvePath[cell]
        if (cell == (1, 1)):
            break
        draw_rect(PathCellsColor, cell[1], cell[0], 5, 5, -10, -10)
        

# Player controls
player_x, player_y = start_x, start_y
def handle_player_movement():
    global player_x, player_y
    old_x, old_y = player_x, player_y
    keys = pygame.key.get_pressed()
    positionChanged = False
    if keys[pygame.K_UP] and player_x > 0 and ((player_x - 1,player_y), (player_x, player_y)) in path:
        positionChanged = True
        player_x -= 1
    elif keys[pygame.K_DOWN] and player_x < maze_height - 1 and ((player_x + 1,player_y), (player_x, player_y)) in path:
        positionChanged = True
        player_x += 1
    elif keys[pygame.K_LEFT] and player_y > 0 and ((player_x,player_y - 1), (player_x, player_y)) in path:
        positionChanged = True
        player_y -= 1
    elif keys[pygame.K_RIGHT] and player_y < maze_width - 1 and ((player_x,player_y + 1), (player_x, player_y)) in path:
        positionChanged = True
        player_y += 1
    if positionChanged:
        draw_rect(CellsColor, old_y, old_x, 1, 1, -1, -1)


# Game loop
running = True
clock = pygame.time.Clock()

draw_maze()
drawPath()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    handle_player_movement()
    screen.blit(playerImage, (player_y *  cell_width + 1, player_x * cell_height + 1))
    screen.blit(goalImage, (goal_y *  cell_width + 1, goal_x * cell_height + 1))
    if player_x == goal_x and player_y == goal_y:
        screen.blit(playerImage, (goal_y *  cell_width + 1, goal_x * cell_height + 1))
    pygame.display.flip()
    clock.tick(60)
    time.sleep(0.1)

pygame.quit()


# change color
# change photo
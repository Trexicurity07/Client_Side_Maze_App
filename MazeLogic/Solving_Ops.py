from random import choice
from customtkinter import CTkImage
from PIL import Image
from time import sleep

class FailSolve(Exception):
    pass
# Creates custom exception class to raise and catch

def Turn(Direction, Anti = False):
    
    if Anti:
        return (Direction[1], -Direction[0])
    else:
        return (-Direction[1], Direction[0])
# Rotates direction pointer is facing 90 degrees

def CheckDeadEnd(Maze, ThisX, ThisY):

    ValidList = []

    try:
        if Maze[ThisY + 1][ThisX] in (0, 'E'):
            ValidList.append((ThisX, ThisY + 1))
    except IndexError:
        None

    # IndexError accept to catch cases where current cell is on the border and checks beyond Maze constraints
    # Only applicable where ThisY = Maze Height or ThisX = Maze Width without passing them seperately

    if Maze[ThisY - 1][ThisX] in (0, 'E') and ThisY > 0:
        ValidList.append((ThisX, ThisY - 1))

    # IndexError doesnt work as List[-1] loops to end of the list
    # If statement work as if ThisY or ThisX == 0, ThisY - 1 or ThisX - 1 equal - 1 and the minimal index of the Maze Height / Width is always 0

    try:
        if Maze[ThisY][ThisX + 1] in (0, 'E'):
            ValidList.append((ThisX + 1, ThisY))
    except IndexError:
        None

    if Maze[ThisY][ThisX - 1] in (0, 'E') and ThisX > 0:
        ValidList.append((ThisX - 1, ThisY))

    return ValidList
# Returns list of path cells neighboring current cell to check

def LeftHand(Maze, ThisX, ThisY, Direction, NumpyArray, MazeLabel):

    try:
        Next = CheckDeadEnd(Maze, ThisX, ThisY)[0]
        Direction = (Next[0] - ThisX, Next[1] - ThisY)
    except IndexError:
        raise FailSolve
        # [][0] raises error when Start cell is blocked up from all sides
    # Finds path cell position from Start cell and calculates direction towards it

    while Maze[ThisY][ThisX] != 'E':
        # While the current cell isnt the End cell

        Maze[ThisY][ThisX] += 1
        NumpyArray[ThisY][ThisX] = (219, 141, 252)
        # Number = amount of visits the path cell had, default is 0
        # Affects CheckDeadEnd search fro available cells

        counter = -1
        while True:

            if counter == 4:
                raise FailSolve
                # Raised if no direction is available to explore
            
            if Maze[ThisY + Direction[1]][ThisX + Direction[0]] in ('w', 4):
                Direction = Turn(Direction)
                counter += 1
            else:
                break
            # Checks if current direction is valid to advance in, if not then turn right
        
        
        ThisX += Direction[0]
        ThisY += Direction[1]
        NumpyArray[ThisY][ThisX] = (179, 0, 255)

        Resized = Resize(NumpyArray)
        MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (200, 200)))
        Window.update()
        sleep(Sleep)

        Direction = Turn(Direction, True)
        # Once an advancement is made, turn left (to catch any possible emerging path to the left) 

def Tremaux(Maze, ThisX, ThisY, NumpyArray, MazeLabel):
    
    SplitList = []
    Options = CheckDeadEnd(Maze, ThisX, ThisY)

    while Maze[ThisY][ThisX] != 'E':
        # While the current cell isnt the End cell
        
        Maze[ThisY][ThisX] += 1
        NumpyArray[ThisY][ThisX] = (219, 141, 252)
        # Number = amount of visits the path cell had, default is 0
        # Affects CheckDeadEnd search for available cells

        try:
            Next = choice(Options)
            ThisX = Next[0]
            ThisY = Next[1]

        except IndexError:
            # choice([]) raises IndexError if Options = [] (No unvisited path to advance to)

            if len(SplitList) == 0:
                raise FailSolve
                # Raised if all available intersections had all their paths checked and End cell wasnt found
            
            else:
                Next = SplitList.pop()
                ThisX = Next[0]
                ThisY = Next[1]
                # Rewinds to last explored intersection

        NumpyArray[ThisY][ThisX] = (179, 0, 255)

        Resized = Resize(NumpyArray)
        MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (200, 200)))
        Window.update()
        sleep(Sleep)

        Options = CheckDeadEnd(Maze, ThisX, ThisY)

        if len(Options) > 1:
            SplitList.append((ThisX, ThisY))
        # If the current cell has more than 1 path leading from it (Intersection) add it to SplitList

def CalCost(Start, Current, End):
    
    Cost = abs(Current[0] - Start[0]) + abs(Current[1] - Start[1])
    HDistance = abs(End[0] - Current[0]) + abs(End[1] - Current[1])
    # Calculates the cost in steps of moving to a cell against how close it gets to the end cell
    # Absolute value deals with negatives and uses only the magnitude of length

    return Cost + HDistance
# Returns the heuristic cost of advancing to a given cell

def AStar(Maze, ThisX, ThisY, End, NumpyArray, MazeLabel):
    
    OptionsList = []
    Options = CheckDeadEnd(Maze, ThisX, ThisY)

    while Maze[ThisY][ThisX] != 'E':
        # While the current cell isnt the End cell

        Maze[ThisY][ThisX] += 1
        NumpyArray[ThisY][ThisX] = (219, 141, 252)
        # Number = amount of visits the path cell had, default is 0
        # Affects CheckDeadEnd search fro available cells

        Options.sort(key = lambda Pos : CalCost((ThisX, ThisY), Pos, End), reverse = True)
        # Instead of creating a seperate list for storing the costs of advancement for calculations or if statements to check which one is the greatest
        # List.sort() can take a key method to run on every element of the list
        # lambda creates a temporary method taking in Pos of the next stop and returning it's heuristic cost

        try:
            Next = Options.pop()
            OptionsList += Options
            ThisX = Next[0]
            ThisY = Next[1]
            # Turn the current position into that of the last element of the reverse sorted list
            # Adds the rest of the sorted options to the back of the OptionsList

        except IndexError:
            if len(OptionsList) == 0:
                raise FailSolve
                # Raises when all options are exhausted and End cell wasn't found
            
            else:
                Next = OptionsList.pop()
                ThisX = Next[0]
                ThisY = Next[1]
                # Turn the current position into that of the next best option

        NumpyArray[ThisY][ThisX] = (179, 0, 255)

        Resized = Resize(NumpyArray)
        MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (200, 200)))
        Window.update()
        sleep(Sleep)

        Options = CheckDeadEnd(Maze, ThisX, ThisY)

Window = None
Sleep = None
Resize = None

# --------------- TESTING ---------------- #

# Height = randint(3, 15)
# Width = randint(3, 15)
# MaxMinDistance = ((Width // 2) + Height - 2) if Width > Height else ((Height // 2) + Width - 2)
# Distance = randint(0, MaxMinDistance)
# Maze = GenerationOps.GenerateGrid(Width, Height, True)
# GenerationOps.Backtracker(Maze, Width, Height, Distance)


# for y, row in enumerate(Maze):
#     for x, cell in enumerate(row):
#         Maze[y][x] = cell.GetType() 

# for y, row in enumerate(Maze):
#     for x, cell in enumerate(row):

#         if cell == 'S':
#             PosX = x
#             PosY = y
#             Direction = (1, 0)
#             Maze[y][x] = 0
        
#         elif cell == ' ':
#             Maze[y][x] = 0

#         elif cell == 'E':
#             End = (x, y)

# try:
#     print(AStar(Maze, PosX, PosY, End))
# except FailSolve:
#     print('Imperfect Maze!')

# print('Done')

# for y, row in enumerate(Maze):
#     for x, cell in enumerate(row):
#         Maze[y][x] = str(Maze[y][x])

# for row in Maze:
#     print(' '.join(row))
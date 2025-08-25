from random import randint, choice
from customtkinter import CTkImage
from PIL import Image
from time import sleep

class Fail(Exception): 
    pass
# Creates custom exception class to raise and catch

class Cell:

    def __init__(self, XPos, YPos, Type, Up = None, Right = None, Down = None, Left = None, Border = False, Colour = None):

        self.__x = XPos
        self.__y = YPos
        self.__neighbors = [Up, Left, Down, Right]
        self.__border = Border
        self.__type = Type
        self.__Visited = False
        self.__Colour = Colour
        # Stores cell maze coordinates, neighboring cells, whether it is on the border, type (start, end, wall, path), and whether it was visited

    def GetCoords(self):
        return (self.__x, self.__y)
    
    def GetNeighbors(self):
        return self.__neighbors
    
    def SetNeighbors(self, Cell, dir):
        self.__neighbors[dir] = Cell
        # dir is an integer value, 0 corresponds to Up, 1 = Left, 2 = Down, 3 = Right
    
    def GetBorder(self):
        return self.__border
    
    def GetType(self):
        return self.__type
    
    def SetType(self, Type):
        self.__type = Type

    def GetColour(self):
        return self.__Colour
    
    def SetColour(self, Colour):
        self.__Colour = Colour

    def ToggleVisited(self):
        self.__Visited = True

    def GetVisited(self):
        return self.__Visited
        
    @staticmethod
    def AddFrontiers(Cell, Maze):

        column, row = Cell.GetCoords()
        # Extracts current cell coordinates

        if row > 0:
            Maze[row - 1][column].SetNeighbors(Cell, 0)
        # Check if row > 0 as when row == 0, row - 1 will loop around to the other end of the maze
        # List[-1] = List[last index]

        try:
            Maze[row][column + 1].SetNeighbors(Cell, 1)
        except IndexError:
            None
        # Catch errors when column + 1 is beyond the maze size
        # Different approach as when column - 1 or row - 1 as loopiing isnt present when index is too large and more variables have to be passed to check column + 1 against maze size
        
        try:
            Maze[row + 1][column].SetNeighbors(Cell, 2)
        except IndexError:
            None

        if column > 0:
            Maze[row][column - 1].SetNeighbors(Cell, 3)

def GenerateGrid(Width, Height, Filled):

    Maze = [[[]for column in range(Width)] for row in range(Height)]
    # List comprehension to generate Maze with Height nested lists, each being Width elements long

    for row in range(Height):
        for column in range(Width):

            if column in (0, Width - 1) or row in (0, Height - 1):
                ThisCell = Cell(column, row, 'w', Border = True, Colour = (0, 0, 0))
                # If cell is on the border, force it to be a wall and set Border = True

            else:
                ThisCell = Cell(column, row, (' ' if Filled == False else 'w'))
                ThisCell.SetColour((255, 255, 255) if Filled == False else (0, 0, 0))
                # If cell isnt on the border set it as a wall or path depending on the value of Filled
            
            Maze[row][column] = ThisCell

    for i, row in enumerate(Maze):
        for z, cell in enumerate(row):
            Maze[i][z].AddFrontiers(cell, Maze)
            # For every cell, add it to it's neighbor's self.__neighbors list

    return Maze
# Generates grid base to execute other algorithms on

def ChooseGates(Maze, Width, Height, Distance):

    sideS = randint(1, 4)
    # Randomly choose side for the starting cell

    match sideS:

        case 1:
            Along = randint(1, Width - 2)
            StartCell = Maze[0][Along]

        case 4:
            Along = randint(1, Width - 2)
            StartCell = Maze[Height - 1][Along]

        case 2:
            Along = randint(1, Height - 2)
            StartCell = Maze[Along][0]

        case 3:
            Along = randint(1, Height - 2)
            StartCell = Maze[Along][Width - 1]

    # Finds random cell along the randomly choen wall of the maze
    # Randint starts at 1 and ends at something - 2 to eliminate chance of start or end being in a corner

    Length = -1
    while Length < Distance:

        sideE = randint(1, 4)
        # Randomly choose side for end cell

        match sideE:

            case all if sideE == sideS:
                # End never on same side as start otherwise mazes are too short
                continue

            case 1:
                Along = randint(1, Width - 2)
                CheckCell = Maze[0][Along]

            case 4:
                Along = randint(1, Width - 2)
                CheckCell = Maze[Height - 1][Along]

            case 2:
                Along = randint(1, Height - 2)
                CheckCell = Maze[Along][0]

            case 3:
                Along = randint(1, Height - 2)
                CheckCell = Maze[Along][Width - 1]
        
        # Finds random cell along the randomly choen wall of the maze
        # Randint starts at 1 and ends at something - 2 to eliminate chance of start or end being in a corner

        Length = abs(StartCell.GetCoords()[0] - CheckCell.GetCoords()[0]) + abs(StartCell.GetCoords()[1] - CheckCell.GetCoords()[1])
        # Length = Difference X + Difference Y between the Start and End
        # Must at least meet the distance parameter provided

    CheckCell.SetType('E')
    CheckCell.SetColour((0, 255, 0))
    StartCell.SetType('S')
    StartCell.SetColour((255, 0, 0))
    return [StartCell, CheckCell]
# Selects Start and End cells from given empty maze (Only for Recursive Division)

def Divide(Maze, TopL, SecWidth, SecHeight, Gaps, NumpyArray, MazeLabel):

    if SecWidth <= 3 or SecHeight <= 3:
        return None
        # Any maze with parameter of 3 or less causes endless loop (impossible to draw any walls)

    if SecHeight + SecWidth > 7 and SecHeight + SecWidth < 11:
        failsafe = 20
    else:
        failsafe = -1
    # There are combination where no walls can be draws usign current logic in 4*4, 4*5 and 5*5 mazes
    # A limit of attempts is given to these sizes to ensure a breakout of the loop is possible

    GapBorder = [0, 1]
    # Filler values for start of loop

    while len(set(GapBorder)) > 1 and failsafe != 0:
        # Set to remove duplicates (Cases where a cell neighbors 2 gaps ends up in duplicate elements)
        
        RayList = []
        GapExcept1 = []
        GapExcept2 = []

        if SecHeight + SecWidth == 8:
            chance = randint(0, 1)
        elif SecWidth == 4:
            chance = 0
        elif SecHeight == 4:
            chance = 1
        else:
            chance = randint(0, 1)

        # Gives priority to generating walls on the same axis a wall with size 4
        # To avoid generating parallel walls with no space in between
        # If no or both walls are size 4, choose randomly

        if chance == 0:
            # Generate X axis wall

            try:
                RayY = randint(TopL[1] + 2, TopL[1] + SecHeight - 3)
            except ValueError:
                RayY = TopL[1] + randint(1, 2)
            # Randomly chooses Y position along wall
            # If size == 4, value error gets raised due to randint(2, 1)
                
            for XPos in range(1, SecWidth - 1):
                RayList.append(Maze[RayY][TopL[0] + XPos])
            # Add every cell between the 2 vertical walls on the chosen Y axis to the list

            for Gap in Gaps:
                if Gap.GetCoords()[1] < RayY:
                    GapExcept1.append(Gap)
                elif Gap.GetCoords()[1] > RayY:
                    GapExcept2.append(Gap)
            # Splits gaps into ones below and above the ray (Sections to recurse next into)
            
            NewTopL = (TopL[0], RayY)

        else:
            # Generate Y axis wall

            try:
                RayX = randint(TopL[0] + 2, TopL[0] + SecWidth - 3)
            except ValueError:
                RayX = TopL[0] + randint(1, 2)
            # Randomly chooses X position along wall
            # If size == 4, value error gets raised due to randint(2, 1)

            for YPos in range(1, SecHeight - 1):
                RayList.append(Maze[TopL[1] + YPos][RayX])
            # Add every cell between the 2 horizontal walls on the chosen Y axis to the list

            for Gap in Gaps:
                if Gap.GetCoords()[0] < RayX:
                    GapExcept1.append(Gap)
                elif Gap.GetCoords()[0] > RayX:
                    GapExcept2.append(Gap)
            # Splits gaps into ones to the right and left the ray (Sections to recurse next into)

            NewTopL = (RayX, TopL[1])

        GapBorder = []
        for cell in RayList:
            for gap in Gaps:
                if gap in cell.GetNeighbors():
                    GapBorder.append(cell)
        # Add every cell that neighbors a gap into a list

        failsafe -= 1

    if failsafe == 0:
        raise Fail
        # Break out of potentially endless loop to restart generation from scratch

    for cell in RayList:
        cell.SetType('w')
        Coords = cell.GetCoords()
        NumpyArray[Coords[1]][Coords[0]] = (0, 0, 0)

    if GapBorder == []:
        GapCell = choice(RayList)
    else:
        if GapBorder[0] == RayList[0]:
            GapCell = RayList[0]
        else:
            GapCell = RayList[-1]
    GapCell.SetType(' ')
    Coords = GapCell.GetCoords()
    NumpyArray[Coords[1]][Coords[0]] = (255, 255, 255)
    # If no cells neighbor gaps, turn a random onle into a gap
    # If a cell neighbors a gap (can only possibly occur on either end), turn that cell into a gap

    Resized = Resize(NumpyArray)
    MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (300, 300)))
    Window.update()
    sleep(Sleep)

    Divide(Maze, TopL, SecWidth if chance == 0 else RayX - TopL[0] + 1, SecHeight if chance == 1 else RayY - TopL[1] + 1, GapExcept1 + [GapCell], NumpyArray, MazeLabel)
    Divide(Maze, NewTopL, SecWidth if chance == 0 else SecWidth - RayX + TopL[0], SecHeight if chance == 1 else SecHeight - RayY + TopL[1], GapExcept2 + [GapCell], NumpyArray, MazeLabel)

    return NumpyArray
    # Recurse further into the 2 sections split by the generated ray

def CheckDeadEnd(Maze, ThisX, ThisY):

    ValidList = []

    try:
        if Maze[ThisY + 2][ThisX].GetVisited() == False:
            ValidList.append((ThisX, ThisY + 2))
    except IndexError:
        if Maze[ThisY + 1][ThisX].GetVisited() == False:
            ValidList.append((ThisX, ThisY + 1))

    # Catch errors in case the cell is near a border where X = Maze Width or Y = Maze Height (If statements require parameter Max Width / Height to be passed too)
    # Dont want to leave space with both SecW and SecH > 1 (causes loop when solving) so check by increment of 1 instead of 2
    
    if Maze[ThisY - 2][ThisX].GetVisited() == False and ThisY > 1:
        ValidList.append((ThisX, ThisY - 2))
    elif Maze[ThisY - 1][ThisX].GetVisited() == False and Maze[ThisY - 1][ThisX].GetBorder():
        ValidList.append((ThisX, ThisY - 1))

    # Instead of catching errors, the minimum ThisX or ThiyY can be without exiting the maze is 1 as 1 - 2 = -1 index
    # Dont want to leave space with both SecW and SecH > 1 (causes loop when solving) so check by increment of 1 instead of 2

    try:
        if Maze[ThisY][ThisX + 2].GetVisited() == False:
            ValidList.append((ThisX + 2, ThisY))
    except IndexError:
        if Maze[ThisY][ThisX + 1].GetVisited() == False:
            ValidList.append((ThisX + 1, ThisY))

    if Maze[ThisY][ThisX - 2].GetVisited() == False and ThisX > 1:
        ValidList.append((ThisX - 2, ThisY))
    elif Maze[ThisY][ThisX - 1].GetVisited() == False and Maze[ThisY][ThisX - 1].GetBorder():
        ValidList.append((ThisX - 1, ThisY))

    return ValidList
# Returns list of potentially valid cell positions to expand into (Only for Backtracker and Prims)

def Backtracker(Maze, Width, Height, Distance, NumpyArray, MazeLabel):
    allowBorder = 2
    CurrentX = randint(1, Width - 2)
    CurrentY = randint(1, Height - 2)
    Maze[CurrentY][CurrentX].SetType(' ')
    Maze[CurrentY][CurrentX].ToggleVisited()
    NumpyArray[CurrentY][CurrentX] = (255, 255, 255)
    steps = 0

    CellList = [Maze[CurrentY][CurrentX]]

    while len(CellList) != 0:
        # len(CellList) == 0 when no cells without dead ends exist

        try:
            posTup = choice(CheckDeadEnd(Maze, CurrentX, CurrentY))
        except IndexError:
            CellList.pop()
            if len(CellList) != 0:
                CurrentX, CurrentY = CellList[-1].GetCoords()
            continue

        # Chooses random available cell to expand into
        # If no cells are available choice([]) raises IndexError
        # Remove latest added cell if possible and try again

        CellMidX = (posTup[0] + CurrentX) // 2
        CellMidY = (posTup[1] + CurrentY) // 2
        CellMid = Maze[CellMidY][CellMidX]
        if CellMid.GetBorder() == False:
            CellMid.SetType(' ')
            NumpyArray[CellMidY][CellMidX] = (255, 255, 255)
        # As the algorithm tries to move in steps of 2 to leave gaps for walls this block calulates the inbetween step cell and fills it in
        # If it moves in 1 step the floor division just returns the 1 step cell position, therefore checking it for being a border before turnign it into a path is crucial

        Cell1 = Maze[posTup[1]][posTup[0]]

        if Cell1.GetBorder():

            if allowBorder == 2:
                Cell1.SetType('S') 
                NumpyArray[posTup[1]][posTup[0]] = (255, 0, 0)
                allowBorder -= 1

                if posTup[1] in (0, Height - 1):
                    SameSide = (-1, posTup[1])
                else:
                    SameSide = (posTup[0], -1)
                # Keeps track of which side the Start cell is generated on
                
                steps = Distance * (Width * Height) / 5
                # Steps is the minimum amount of moves before trying to place an end cell
                # Attempts to distance the Start and End to the users liking as they have a tendency to generate closeby

            elif allowBorder == 1:
                if steps < 0:
                    if posTup[1] != SameSide[1] and posTup[0] != SameSide[0]:
                        Cell1.SetType('E') 
                        NumpyArray[posTup[1]][posTup[0]] = (0, 255, 0)
                        allowBorder -= 1
                # Generates End Cell if the step threshold is met and its not on the same side as the start cell

        else:
            Cell1.SetType(' ')
            NumpyArray[posTup[1]][posTup[0]] = (255, 255, 255)
            CellList.append(Cell1)
            CurrentX = posTup[0]
            CurrentY = posTup[1]
        # If cell isnt on the border turn it into a path and add it to the CellList

        Cell1.ToggleVisited()
        steps -= 1

        Resized = Resize(NumpyArray)
        MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (300, 300)))
        Window.update()
        sleep(Sleep)
    
    while allowBorder == 1:

        Axis = choice(('Hor', 'Vert'))
        if Axis == 'Hor':
            XPos = randint(1, Width - 2)
            YPos = choice((0, -1))
        else:
            XPos = choice((0, -1))
            YPos = randint(1, Height - 2)

        Cell = Maze[YPos][XPos]
        if Cell.GetType() != 'S':

            NeighborTypes = []
            for Neighbor in Cell.GetNeighbors():
                if Neighbor:
                    NeighborTypes.append(Neighbor.GetType())
            
            if ' ' in NeighborTypes:
                Cell.SetType('E')
                NumpyArray[YPos][XPos] = (0, 255, 0)
                allowBorder = 0

    Resized = Resize(NumpyArray)
    MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (300, 300)))
    Window.update()

    return NumpyArray

def Prims(Maze, Width, Height, Distance, NumpyArray, MazeLabel):
    allowBorder = 2
    CurrentX = randint(1, Width - 2)
    CurrentY = randint(1, Height - 2)
    Maze[CurrentY][CurrentX].SetType(' ')
    Maze[CurrentY][CurrentX].ToggleVisited()
    NumpyArray[CurrentY][CurrentX] = (255, 255, 255)
    steps = 0

    FrontierList = [[Coords, CurrentX, CurrentY] for Coords in CheckDeadEnd(Maze, CurrentX, CurrentY)]
    # Stores neighbor cell pos along with cell pos it originates from in a nested list

    while len(FrontierList) != 0:
        # len(FrontierList) == 0 when no cells without dead ends exist

        posTup = choice(FrontierList)
        if Maze[posTup[0][1]][posTup[0][0]].GetVisited() == False:
            # Need to check cell vacancy again as multiple cells can point to the same frontier to expand

            CurrentX = posTup[1]
            CurrentY = posTup[2]

            CellMidX = (posTup[0][0] + CurrentX) // 2
            CellMidY = (posTup[0][1] + CurrentY) // 2
            CellMid = Maze[CellMidY][CellMidX]
            if CellMid.GetBorder() == False:
                CellMid.SetType(' ')
                NumpyArray[CellMidY][CellMidX] = (255, 255, 255)
            # As the algorithm tries to move in steps of 2 to leave gaps for walls this block calulates the inbetween step cell and fills it in
            # If it moves in 1 step the floor division just returns the 1 step cell position, therefore checking it for being a border before turnign it into a path is crucial

            Cell1 = Maze[posTup[0][1]][posTup[0][0]]

            if Cell1.GetBorder():

                if allowBorder == 2:
                    Cell1.SetType('S') 
                    NumpyArray[posTup[0][1]][posTup[0][0]] = (255, 0, 0)
                    allowBorder -= 1

                    if posTup[0][1] in (0, Height - 1):
                        SameSide = (-1, posTup[0][1])
                    else:
                        SameSide = (posTup[0][0], -1)
                    # Keeps track of which side the Start cell is generated on
                    
                    steps = Distance * (Width * Height) / 5
                    # Steps is the minimum amount of moves before trying to place an end cell
                    # Attempts to distance the Start and End to the users liking as they have a tendency to generate closeby

                elif allowBorder == 1:
                    if steps < 0:
                        if posTup[0][1] != SameSide[1] and posTup[0][0] != SameSide[0]:
                            Cell1.SetType('E') 
                            NumpyArray[posTup[0][1]][posTup[0][0]] = (0, 255, 0)
                            allowBorder -= 1
                    # Generates End Cell if the step threshold is met and its not on the same side as the start cell

            else:
                Cell1.SetType(' ')
                NumpyArray[posTup[0][1]][posTup[0][0]] = (255, 255, 255)
                FrontierList = FrontierList + [[Coords, posTup[0][0], posTup[0][1]] for Coords in CheckDeadEnd(Maze, posTup[0][0], posTup[0][1])]
                CurrentX = posTup[0][0]
                CurrentY = posTup[0][1]
                # If cell isnt on the border turn it into a path and add it's available neighbors to FrontierList

            Cell1.ToggleVisited()
            FrontierList.remove(posTup)
            steps -= 1

            Resized = Resize(NumpyArray)
            MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (300, 300)))
            Window.update()
            sleep(Sleep)
    
        else:
            FrontierList.remove(posTup)

    while allowBorder == 1:

        Axis = choice(('Hor', 'Vert'))
        if Axis == 'Hor':
            XPos = randint(1, Width - 2)
            YPos = choice((0, -1))
        else:
            XPos = choice((0, -1))
            YPos = randint(1, Height - 2)

        Cell = Maze[YPos][XPos]
        if Cell.GetType() != 'S':

            NeighborTypes = []
            for Neighbor in Cell.GetNeighbors():
                if Neighbor:
                    NeighborTypes.append(Neighbor.GetType())
            
            if ' ' in NeighborTypes:
                Cell.SetType('E')
                NumpyArray[YPos][XPos] = (0, 255, 0)
                allowBorder = 0

    Resized = Resize(NumpyArray)
    MazeLabel.configure(image = CTkImage(Image.fromarray(Resized), size = (300, 300)))
    Window.update()

    return NumpyArray

Window = None
Sleep = None  
Resize = None

# --------------- Testing ---------------- #

# Height = 20
# Width = 20

# MaxMinDistance = ((Width // 2) + Height - 2) if Width > Height else ((Height // 2) + Width - 2)
# # Calculation to find maximum possible distance between Start and End cell at given Height and Width
# # This distance should be possible for any generated position of the Start cell

# Distance = randint(0, MaxMinDistance)

# Maze = GenerateGrid(Width, Height, True)

# Backtracker(Maze, Width, Height, 10000)
    

# for i, row in enumerate(Maze):
#     for z, cell in enumerate(row):
#         Maze[i][z] = cell.GetType()

# for i in Maze:
#         print(' '.join(i))

# print('Done')
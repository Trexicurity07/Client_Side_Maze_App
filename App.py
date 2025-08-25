import requests
import Pages
import MazeLogic.Generation_Ops as Gen
import MazeLogic.Solving_Ops as Sol
from customtkinter import *
from datetime import datetime, timedelta  # For .isoformat() to string and timing progress
from numpy import ones, uint8, shape, array
from cv2 import resize, INTER_NEAREST
from PIL import Image
from json import dumps, loads
from copy import deepcopy
from subprocess import run
from tempfile import NamedTemporaryFile
from os import remove
from tkinter import filedialog

# ------------------ IMPORTS ------------------


ServerUrl = 'http://127.0.0.1:5000'  #  https://server-side-maze-app.onrender.com/
# Safe as server IP can be found anyways and server performs authentication on requests

Pages.DropdownOptions = {
        'Account' : lambda : ToProfile(SessionInfo['UserName']),
        'Logout' : lambda : Logout()}
Pages.NavigationOptions = {
        'Back' : lambda : Reorder(),
        'Home' : lambda : (SessionInfo['FramesOrder'].remove(HomeInfo['Frame']),
                           SessionInfo['FramesOrder'].insert(0, HomeInfo['Frame']), HomeInfo['Frame'].lift()),
        'Forward' : lambda : Reorder(True)}
# Lambda delays evaluation as methods are wrapped inside another 'method'
# Also allows methods to be stored before definition

SizeDict = {'Any' : (0, 10000),
            'Small\n(0 -> 900)' : (0, 900),
            'Medium\n(900 -> 4.9K)' : (900, 4900),
            'Large\n(4.9K -> 10K)' : (4900, 10000)}

SessionInfo = {'UserName' : None,
               'Token' : None,
               'LastAlgorithm' : None,
               'FramesOrder' : None}
# ------------------ VARIABLES ------------------


def OpenMessage(FailStr):

    Popup = CTkToplevel(Pages.Window)
    Popup.title('Message')
    Popup.geometry('200x100+860+490')
    Popup.attributes('-topmost', True)

    CTkLabel(Popup, text = FailStr).pack(pady = 21)
# Opens popup with message
# Popup.mainloop() is possible but deletes Pages.Window.mainloop() as only 1 mainloop() can exist at once

def RaiseFrame(Frame):

    try:
        SessionInfo['FramesOrder'].remove(Frame)
    except ValueError:
        None
    SessionInfo['FramesOrder'].insert(0, Frame)
    Frame.lift()
# Configures FramesOrder to have passed frame as index 0 with no repeating values

def Reorder(Forward = False):

    Pages.Window.focus_set()
    FramesOrder = SessionInfo['FramesOrder']

    if Forward == False:
        LastPage = FramesOrder[1]

        if LastPage != 'End':
            CurPage = FramesOrder.pop(0)
            FramesOrder.append(CurPage)
    # End acts as stopper (signals that current tab is the furthest possible in that direction)
    # [page1, page2, page3, end] -->  [page2, page3, end, page1]

    else:
        NextPage = FramesOrder.pop()

        if NextPage == 'End':
            FramesOrder.append(NextPage)
        else:
            FramesOrder.insert(0, NextPage)
    # End acts as stopper (signals that current tab is the furthest possible in that direction)
    # [page2, page3, end, page1] --> [page1, page2, page3, end]

    for InfoDict in (GenerationInfo, DrawInfo):
        if InfoDict['Frame'] == FramesOrder[0]:
            InfoDict['SizeX'].configure(text = f'Width : {Pages.WidthVar.get()}')
            InfoDict['SizeY'].configure(text = f'Height : {Pages.WidthVar.get()}')
            break
    # Keeps the DrawInfo and GenerationInfo sliders and label values synchronized

    SessionInfo['FramesOrder'] = FramesOrder
    FramesOrder[0].lift()

def GenerateEmptyMazeImg(Width, Height, ForDraw = False):

    Empty = ones((Height, Width, 3), dtype = uint8) * 255
    Empty[0, :] *= 0
    Empty[-1, :] *= 0
    Empty[: , 0] *= 0
    Empty[: , -1] *= 0
    # Generates maze full of (255, 255, 255) white
    # Changes borders to (0, 0, 0) black

    return (Empty, Resize(Empty, 300)) if ForDraw else Resize(Empty, 300)

def Resize(Array, Size):

    return resize(Array, (Size, Size), interpolation = INTER_NEAREST)
    # INTER_NEAREST enlarges image while keeping edges sharp
    # Causes pixelation however it doesnt matter as we use low res squares anyways in image

def ShowPassword(Button, Entry):
    if Entry.cget('show') == '':
        Button.configure(fg_color = '#257ac4', hover_color = '#61a4df')
        Entry.configure(show = '•')

    else:  # Entry.cget('show') == '•'
        Button.configure(fg_color = 'white', hover_color = '#cacaca')
        Entry.configure(show = '')
    # Scrambles / unscrambles password  when button is pressed

def ToLogin():

    Pages.Window.focus_set()

    LoginInfo['UserName'].delete(0, 'end')
    LoginInfo['Password'].delete(0, 'end')
    LoginInfo['UserName'].configure(placeholder_text = 'Enter username or email', placeholder_text_color = 'grey')
    LoginInfo['Password'].configure(placeholder_text = 'Enter password', placeholder_text_color = 'grey')
    # Labels dont have .set(), instead delete is used to clear all text and placeholder data, then reconfigure the placeholder

    LoginInfo['Frame'].lift()

def AttemptLogin(UserName, Password):
    
    Pages.Window.focus_set()

    JsonPayload = {'UN_Email' : UserName,
                 'Password' : Password}
    Success = requests.post(f'{ServerUrl}/Login', json = JsonPayload).json()

    if Success == False:
        LoginInfo['UserName'].delete(0, 'end')
        LoginInfo['UserName'].configure(placeholder_text = 'Invalid details', placeholder_text_color = '#9a1e1e')

        LoginInfo['Password'].delete(0, 'end')
        LoginInfo['Password'].configure(placeholder_text = 'Invalid details', placeholder_text_color = '#9a1e1e')

    else:
        SessionInfo['UserName'] = Success['UserName']
        SessionInfo['Token'] = Success['Token']
        ToHome()
# Sets UserName and Token for the session, proceeds to homepage if login is successful

def ToSignup():

    Pages.Window.focus_set()

    for Entry in [*SignupInfo][1::]:  #  not including 'Frames' key
        SignupInfo[Entry].delete(0, 'end')
        SignupInfo[Entry].configure(placeholder_text = f'Enter {Entry}', placeholder_text_color = 'Grey')
    # Pages.CreateSignup() returns lowercase keys for the SignupInfo dict
    # Allows *Signup to pass the keys which can then be used directly in the f'' insted of
    # if Entry = 'UName' : Signup[Entry].configure()

    SignupInfo['Frame'].lift()

def ApplySignup():

    Pages.Window.focus_set()

    JsonPayload = {}

    for Entry in ['first name', 'last name']:

        EnteredValue = SignupInfo[Entry].get()
        if len(EnteredValue) > 20 or EnteredValue == '':
            SignupInfo[Entry].delete(0, 'end')
            SignupInfo[Entry].configure(placeholder_text = 'Enter 1 - 20 characters', placeholder_text_color = '#9a1e1e')
            return
        
        JsonPayload[Entry] = EnteredValue
    # Exit signup attempt if FName or LName arent set correctly (cant be empty or >20 length)
        
    for Entry in ['username', 'password']:  #  UName and Password

        EnteredValue = SignupInfo[Entry].get()
        if len(EnteredValue) < 5 or len(EnteredValue) > 20:
            SignupInfo[Entry].delete(0, 'end')
            SignupInfo[Entry].configure(placeholder_text = 'Enter 5 - 20 characters', placeholder_text_color = '#9a1e1e')
            return
        
        JsonPayload[Entry] = SignupInfo[Entry].get()
    # Exit signup attempt if FName or LName arent set correctly (must be between 5 - 20 length)

    JsonPayload['email'] = SignupInfo['email'].get().lower()
    # Database stores all emails in lowercase to make sure no repeats occur
    # Makes sure dummy@gmail.com wont be considered different from DUMMY@gmail.com

    Success = requests.post(f'{ServerUrl}/Signup', json = JsonPayload).json()

    if Success == True:
        ToLogin()

    elif Success == False:
        SignupInfo['email'].delete(0, 'end')
        SignupInfo['email'].configure(placeholder_text = "Email doesn't exist", placeholder_text_color = '#9a1e1e')

    else:
        if Success[0] != 0:
            SignupInfo['username'].delete(0, 'end')
            SignupInfo['username'].configure(placeholder_text = 'Username is taken', placeholder_text_color = '#9a1e1e')

        if Success[1] != 0:
            SignupInfo['email'].delete(0, 'end')
            SignupInfo['email'].configure(placeholder_text = 'Email already registered', placeholder_text_color = '#9a1e1e')

def Logout():

    requests.post(f'{ServerUrl}/Logout/{SessionInfo['Token']}')
    SessionInfo['Token'] = None
    SessionInfo['UserName'] = None
    ToLogin()
    # Will remove current sensitive session info data

def ToHome():

    Pages.Window.focus_set()

    Pages.UName = SessionInfo['UserName']
    Pages.DropdownDefault.set(SessionInfo['UserName'])
    HomeInfo['WelcomeLabel'].configure(text = f'Hello {SessionInfo['UserName']}')
    # Sets commonly used Pages file variables 

    SessionInfo['FramesOrder'] = [HomeInfo['Frame'], 'End']
    HomeInfo['Frame'].lift()

def ToExplore():

    FilterInfo['Name'].delete(0, 'end')
    FilterInfo['Name'].configure(placeholder_text = 'Enter maze name')
    FilterInfo['Algorithm'].set('Any')
    FilterInfo['Size'].set('Any')
    # Resets filter options every time page is called

    GetFilteredMazes()

    RaiseFrame(FilterInfo['Frame'])

def GetFilteredMazes(Page = 1, Name = '', ALgorithm = 'Any', Size = 'Any'):

    Pages.Window.focus_set()

    JsonPayload = {'Pages' : Page}
    if Name != '': JsonPayload['Name'] = Name
    if ALgorithm != 'Any': JsonPayload['Algorithm'] = ALgorithm
    if Size != 'Any': JsonPayload['Size'] = SizeDict[Size]

    Response = requests.post(f'{ServerUrl}/Filter/{SessionInfo['Token']}', json = JsonPayload).json()

    if Response == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:

        WidgetList = FilterInfo['Widgets']
        for Index in range(5):

            AffectedWidgets = WidgetList[Index]
            try:
                Data = Response[Index]

                AffectedWidgets['Frame'].pack(pady = (50, 0))
                AffectedWidgets['Frame'].data = Data['MazeID']
                # Attatches info to frame for <Button-1> bind command

                MazeImg = Resize(array(loads(Data['MazeList']), uint8), 150)
                AffectedWidgets['ButtonSim'].configure(
                    image = CTkImage(Image.fromarray(MazeImg), size = (150, 150)))
                
                AffectedWidgets['Label'].configure(text = f'Name : {Data['MazeName']}\nCompleted : {Data['Completed']}')
                
            except IndexError:
                AffectedWidgets['Frame'].pack_forget()
                # If less than 5 objects are returned in the list, hide the frames of the missing data

        # For each frame representing a maze, get the WidgetList data representing it and configure the widgets with said data

        FilterInfo['ScrollableFrame']._parent_canvas.yview_moveto(0)
        # Scrolls back to top using TkCanvas CTkScrollableFrame inherits from
        # Scrolling on frame also forces widgets packed on it to update and show new images

def ToGeneration():

    GenerationInfo['Distance'][0].set(50)
    GenerationInfo['Distance'][1].configure(text = f'Length : 50')
    Pages.WidthVar.set(30)
    GenerationInfo['SizeX'].configure(text = f'Width : 30')
    Pages.HeightVar.set(30)
    GenerationInfo['SizeY'].configure(text = f'Height : 30')

    GenerationInfo['Name'].delete(0, 'end')
    GenerationInfo['Name'].configure(placeholder_text = 'Enter maze name')
    Pages.Algorithm.set('Division')
    GenerationInfo['Buttons'][0].configure(state = 'disabled')
    # makes sure that the Submit maze button is disabled until a maze has been generated

    EmptyMaze = GenerateEmptyMazeImg(30, 30)
    GenerationInfo['MazeLabel'].configure(image = CTkImage(Image.fromarray(EmptyMaze), size = (300, 300)))
    # Generates PIL form numpy, then generates CTKImage from PIL

    RaiseFrame(GenerationInfo['Frame'])

def GenerateMaze(Width, Height, Algorithm):

    Pages.Window.focus_set()
    
    if Algorithm == 'Custom':

        MiniMaze, ResizeMaze = GenerateEmptyMazeImg(Width, Height, True)
        DrawInfo['Maze'] = [MiniMaze, (Width, Height)]
        DrawInfo['MazeLabel'].configure(image = CTkImage(Image.fromarray(ResizeMaze), size = (300, 300)))

        DrawInfo['Name'].delete(0, 'end')
        DrawInfo['Name'].configure(placeholder_text = 'Enter maze name')

        DrawInfo['SizeX'].configure(text = f'Width : {Width}')
        DrawInfo['SizeY'].configure(text = f'Height : {Height}')

        RaiseFrame(DrawInfo['Frame'])
        return
    # Configures DrawInfo Frame and quits method

    GenerationInfo['SizeX'].configure(text = f'Width : {Width}')
    GenerationInfo['SizeY'].configure(text = f'Height : {Height}')
    
    SessionInfo['LastAlgorithm'] = Algorithm
    # Stores the algorithm used for SubmitMaze() algorithm type verification

    RaiseFrame(GenerationInfo['Frame'])
    
    GenerationInfo['Buttons'][0].configure(state = 'disabled')
    GenerationInfo['Buttons'][1].configure(state = 'disabled')
    # Makes buttons unclickable for the duration of the generation

    if Width * Height < 900:
        Gen.Sleep = 0.05
    elif Width * Height < 4900:
        Gen.Sleep = 0.01
    else:  #  70*70 until 100*100
        Gen.Sleep = 0.001
    # Makes generation faster depending on maze size

    if Algorithm == 'Division':

        if Width > Height:
            Distance = (Width // 2) + Height - 2
        else:
            Distance = (Height // 2) + Width - 2
        Distance *= GenerationInfo['Distance'][0].get() / 100
        # Sets distance as % of the smallest maximum distance the gates can be from one another

        Attempts = 15
        while True:

            try:
                Maze = Gen.GenerateGrid(Width, Height, False)
                Gaps = Gen.ChooseGates(Maze, Width, Height, Distance)

                ColourMazeCopy = map(lambda Row : list(map(lambda Cell : Cell.GetColour(), Row)), Maze)
                NumpyMaze = array(list(ColourMazeCopy), dtype = uint8)
                # Generate a numpy array with each element being the colour attritube of the Maze Cell instance

                GenerationInfo['MazeLabel'].configure(image = CTkImage(Image.fromarray(Resize(NumpyMaze, 300)), size = (300, 300)))
                Pages.Window.update()

                NumpyMaze = Gen.Divide(Maze, (0, 0), Width, Height, Gaps,
                                   NumpyMaze, GenerationInfo['MazeLabel'])
                break

            except Gen.Fail:
                Attempts -= 1
                if Attempts == 0:
                    OpenMessage('Maze generation has failed\nTry again')
                    GenerationInfo['Buttons'][1].configure(state = 'normal')
                    return
                continue
        # Division algorithm can get stuck in unfortunate generation
        # If it fails 15 times, quit generation and report the issue

    elif Algorithm == 'Backtracker':
        
        Distance = GenerationInfo['Distance'][0].get() / 100
        Maze = Gen.GenerateGrid(Width, Height, True)
        # Distance is a % of the steps required value before planting another gate

        ColourMazeCopy = map(lambda Row : list(map(Gen.Cell.GetColour, Row)), Maze)
        NumpyMaze = array(list(ColourMazeCopy), dtype = uint8)
        # Generate a numpy array with each element being the colour attritube of the Maze Cell instance

        NumpyMaze = Gen.Backtracker(Maze, Width, Height,
                            Distance, NumpyMaze, GenerationInfo['MazeLabel'])
        
    else:  #  Algorithm == 'Prims'
        
        Distance = GenerationInfo['Distance'][0].get() / 100
        Maze = Gen.GenerateGrid(Width, Height, True)
        # Distance is a % of the steps required value before planting another gate

        ColourMazeCopy = map(lambda Row : list(map(Gen.Cell.GetColour, Row)), Maze)
        NumpyMaze = array(list(ColourMazeCopy), dtype = uint8)
        # Generate a numpy array with each element being the colour attritube of the Maze Cell instance

        NumpyMaze = Gen.Prims(Maze, Width, Height,
                            Distance, NumpyMaze, GenerationInfo['MazeLabel'])

    GenerationInfo['Maze'] = NumpyMaze
    GenerationInfo['Buttons'][0].configure(state = 'normal')
    GenerationInfo['Buttons'][1].configure(state = 'normal')
    # Enables buttons again

def DrawOnMaze(Event, CursorColour):

    NumpyArray, Size = DrawInfo['Maze']
    # More reliable than pulling Pages.Width , Pages.Height as those variable can change without affecting the size of the array

    SFX = 450 / Size[0]
    SFY = 450 / Size[1]
    # Maze size is 300 * 300, but TKinter stretches Label to 450 * 450

    XPos = int(Event.x / SFX)
    YPos = int(Event.y / SFY)
    NewColour = tuple(map(lambda char : int(char) * 255, CursorColour.get()))
    
    if NewColour == (255, 255, 255) and (YPos in (0, Size[1] - 1) or XPos in (0, Size[0] - 1)):
        return
    # Doesn't allow placing path tiles on borders

    if YPos < 0 or YPos >= Size[1] or XPos < 0 or XPos >= Size[0]:
        return
    # Doesn't allow placing outside of array index

    NewColour = tuple(map(lambda char : int(char) * 255, CursorColour.get()))
    NumpyArray[YPos][XPos] = NewColour
    # Scale factor compensates for image offset im label (from top left) and difference in pixel height, width

    DrawInfo['Maze'][0] = NumpyArray
    DrawInfo['MazeLabel'].configure(image = CTkImage(Image.fromarray(Resize(NumpyArray, 300)), size = (300, 300)))

def SubmitMaze(Name, Draw = False):
    
    Pages.Window.focus_set()

    JsonPayload = {'Table' : 'Mazes'}
    Product = lambda Tuple : Tuple[0] * Tuple[1]

    if Draw == True:  #  Pull info from DrawInfo dict

        FieldsDict = {'Algorithm' : 'Custom'}

        if len(Name) > 20:
            DrawInfo['Name'].delete(0, 'end')
            DrawInfo['Name'].configure(placeholder_text = 'Max 20 characters',
                                      placeholder_text_color = '#9a1e1e')
            return
        elif Name == '':
            FieldsDict['Name'] = 'Default Name'
        else:
            FieldsDict['Name'] = Name

        FieldsDict['Maze'] = dumps(DrawInfo['Maze'][0].tolist())
        FieldsDict['SizeArea'] = Product(shape(DrawInfo['Maze'][0]))
        # Shape returns measured size of array instead of relying on sliders affected by user = safer

    else:   #  Pull info from GenerationInfo dict

        FieldsDict = {'Algorithm' : SessionInfo['LastAlgorithm']}
        # Normal Algorithm var not used as user can change the OptionMenu option without regenerating the maze

        if len(Name) > 20:
            GenerationInfo['Name'].delete(0, 'end')
            GenerationInfo['Name'].configure(placeholder_text = 'Max 20 characters',
                                      placeholder_text_color = '#9a1e1e')
            return
        elif Name == '':
            FieldsDict['Name'] = 'Default Name'
        else:
            FieldsDict['Name'] = Name

        FieldsDict['Maze'] = dumps(GenerationInfo['Maze'].tolist())
        FieldsDict['SizeArea'] = Product(shape(GenerationInfo['Maze']))
        # Shape returns measured size of array instead of relying on sliders affected by user = safer


    JsonPayload['Fields'] = FieldsDict
    Success = requests.post(f'{ServerUrl}/CreateRecord/{SessionInfo['Token']}', json = JsonPayload).json()

    if Success == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:
        HomeInfo['Frame'].lift()

def InspectMaze(MazeID):

    JsonPayload = {'MazeID' : MazeID, 'Pages' : 1}
    Data = requests.post(f'{ServerUrl}/Filter/{SessionInfo['Token']}', json = JsonPayload).json()
    # Reloads data every time maze is opened to update changing info such as comments, likes etc

    if Data == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
        return
    
    Data = Data[0]

    InspectImg = Resize(array(loads(Data['MazeList']), uint8), 200)
    InspectInfo['MazeLabel'].configure(image = CTkImage(Image.fromarray(InspectImg), size = (200, 200)),
                                       text = f'Name : {Data['MazeName']}\n')

    InspectInfo['AssignButtons'][0].configure(
        command = lambda : (InspectInfo['Pages'].set(InspectInfo['Pages'].get() - 1),
                            GetMazeComments(MazeID)))
    InspectInfo['AssignButtons'][1].configure(
        command = lambda : (InspectInfo['Pages'].set(InspectInfo['Pages'].get() + 1),
                            GetMazeComments(MazeID)))
    InspectInfo['AssignButtons'][2].configure(
        command = lambda : PostComment(InspectInfo['PostEntry'], MazeID))
    InspectInfo['AssignButtons'][3].configure(
        command = lambda : ToProfile(Data['UserName']),
        text = f'Creator : {Data['UserName']}')
    InspectInfo['AssignButtons'][4].MazeInfo = [loads(Data['MazeList']), Data['MazeID'], Data['Completed']]
    # Stores MazeData in custom MazeInfo attribute to the button

    InspectInfo['Likes'][0].configure(fg_color = '#eb176f' if Data['Liked'] else 'light grey',
                            command = lambda : LikeToggle(MazeID, *InspectInfo['Likes']))
    InspectInfo['Likes'][1].configure(text = f'Likes  :  {Data['Likes']}')
    InspectInfo['Likes'][1].Count = Data['Likes']

    if Data['Completed']:
        InspectInfo['Progress'][0].configure(text = f'Completed', state = 'disabled')
    else:
        InspectInfo['Progress'][0].configure(text = f'Start time', state = 'normal')

    InspectInfo['Progress'][0].configure(command = lambda : TimePress(*InspectInfo['Progress'], MazeID))
    InspectInfo['Progress'][0].Time = [timedelta(seconds = Data['Time']), None]
    InspectInfo['Progress'][1].configure(text = FormatTimeDelta(Data['Time']))
    # Stores TimeData in custon Time attribute to the button

    GetMazeComments(MazeID)

    RaiseFrame(InspectInfo['Frame'])

def GetMazeComments(MazeID):

    JsonPayload = {'ID' : MazeID,
                   'ByUser' : False,
                   'Pages' : InspectInfo['Pages'].get()}
    Response = requests.post(f'{ServerUrl}/FetchComments/{SessionInfo['Token']}', json = JsonPayload).json()

    if Response == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:

        WidgetList = InspectInfo['Widgets']
        for Index in range(5):

            AffectedWidgets = WidgetList[Index]
            try:
                Data = Response[Index]

                AffectedWidgets['Frame'].pack(pady = (20, 0))
                AffectedWidgets['Button'].configure(text = Data['UserName'],
                            command = lambda : ToProfile(Data['UserName']))
                AffectedWidgets['Label'].configure(text = Data['Text'])
                
            except IndexError:
                AffectedWidgets['Frame'].pack_forget()
                # If less than 5 objects are returned in the list, hide the frames of the missing data

        # For each frame representing a comment, get the WidgetList data representing it and configure the widgets with said data

        InspectInfo['CommentsFrame']._parent_canvas.yview_moveto(0)
        # Scrolls back to top using TkCanvas CTkScrollableFrame inherits from
        # Scrolling on frame also forces widgets packed on it to update and show new comments

def PostComment(Entry, MazeID):

    Pages.Window.focus_set()
    
    JsonPayload = {'Table' : 'Comments'}

    if len(Entry.get()) > 150:
        Entry.delete(0, 'end')
        Entry.configure(placeholder_text = 'Max 150 characters', placeholder_text_color = '#9a1e1e')
        return
    # Doesnt allow comments to be > 150 char (Database Comment = Column(String(150)))
    
    JsonPayload['Fields'] = {'MazeID' : MazeID, 'Comment' : Entry.get()}
    Success = requests.post(f'{ServerUrl}/CreateRecord/{SessionInfo['Token']}', json = JsonPayload).json()

    if Success == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:
        GetMazeComments(MazeID)
        Entry.delete(0, 'end')
        Entry.configure(placeholder_text = 'Enter comment', placeholder_text_color = 'light grey')
        # Erases comment from the entry box
        # GetMazeComments reloads the comments, forcing the user made one to show up

def Solve(MazeList, MazeLabel, Algorithm):

    NumpyArray = array(MazeList, uint8)

    Product = lambda Tuple : Tuple[0] * Tuple[1] 
    if Product(shape(NumpyArray)) < 900:
        Sol.Sleep = 0.10
    elif Product(shape(NumpyArray)) < 4900:
        Sol.Sleep = 0.02
    else:  #  70*70 until 100*100
        Sol.Sleep = 0.002
    # Changes solving algorithm speed based on maze size

    MazeList = deepcopy(MazeList)
    # Creates perfect copy without storing reference to original object
    # If MazeList2 = Mazelist is done instead, any changes to MazeList2 show up on MazeList and vice versa

    StartNum = 0
    End = None
    for y, Row in enumerate(MazeList):
        for x, Cell in enumerate(Row):

            if Cell == [255, 0, 0]:  #  Start
                StartNum += 1
                Start = (y, x)
                MazeList[y][x] = 3

            elif Cell == [255, 255, 255]:  #  Path
                MazeList[y][x] = 0

            elif Cell == [0, 255, 0]:  #  End
                End = (x, y)
                MazeList[y][x] = 'E'

            else:  #  Wall
                MazeList[y][x] = 'w'

    # Casting numpy array for compatibility with solving algorithms
    # RGB stored in lists not tuples due to numpy.tolist when packing to JSON and sending maze data to flask

    if StartNum != 1:
        OpenMessage('Cannot solve maze\nWith 0 or > 1 statring points')
        return

    InspectInfo['AssignButtons'][4].configure(state = 'disabled')
    # Disables SolveMaze button for the duration of the solving

    try:

        if Algorithm == 'Tremaux':
            Sol.Tremaux(MazeList, Start[1], Start[0], NumpyArray, MazeLabel)

        elif Algorithm == 'Left Hand':
            Sol.LeftHand(MazeList, Start[1], Start[0], (1, 0), NumpyArray, MazeLabel)

        elif End:  #  Algorithm == 'A - Star'
            Sol.AStar(MazeList, Start[1], Start[0], End, NumpyArray, MazeLabel)

        else:  # Algorithm == 'A - Star' and end doesnt exist in maze
            raise Sol.FailSolve
        
    except Sol.FailSolve:
        OpenMessage('Failed to solve maze\nMaze must have 1 start\n1+ ends, no loops')
    
    InspectInfo['AssignButtons'][4].configure(state = 'normal')
    InspectInfo['Progress'][0].configure(text = 'Completed', state = 'disabled')
    # Disable StartTime button as maze is now considered solved
    # CompleteMaze() is ran parallel to this script from the button calling it

def LikeToggle(MazeID, LikeButton, LikeLabel):
    
    if LikeButton.cget('fg_color') == 'light grey':
        LikeButton.configure(fg_color = '#eb176f')
        LikeLabel.Count += 1

        JsonPayload = {'Table' : 'Likes', 'Fields' : {'MazeID' : MazeID}}
        FullUrl = f'{ServerUrl}/CreateRecord/{SessionInfo['Token']}'

    else:  # LikeButton.cget('fg_color') == pink ('#eb176f')
        LikeButton.configure(fg_color = 'light grey')
        LikeLabel.Count -= 1

        JsonPayload = {'MazeID' : MazeID}
        FullUrl = f'{ServerUrl}/Unlike/{SessionInfo['Token']}'

    LikeLabel.configure(text = f'Likes  :  {LikeLabel.Count}')
    Success = requests.post(FullUrl, json = JsonPayload).json()

    if Success == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')

def TimePress(TimeButton, TimeLabel, MazeID):
    
    if TimeButton.Time[1] == None:
        TimeButton.Time[1] = datetime.now()
        TimeButton.configure(text = 'Stop time')

    else:
        TimeCommit(TimeButton, TimeLabel, MazeID)
# If button is in start time mode (Time[1] == None) (Start time == None), set the start time
# If button has a start time, Commit the time change from then till now

def TimeCommit(TimeButton, TimeLabel, MazeID):
    
    Elapsed = datetime.now() - TimeButton.Time[1]
    # Time difference

    JsonPayload = {'Table' : 'Progress', 'Fields' : {'MazeID' : MazeID,
                                                    'Time' : Elapsed.total_seconds(),
                                                    'Completed' : False}}
    # Jsons cant store datetime objects, so .total_seconds() returns it as a float

    if TimeButton.Time[0]:
        # Timedelta values with duration > 0.0s are Truthy
        # Add progress (Time[0] > 0.0 indicates record already exists)
        Success = requests.post(f'{ServerUrl}/AddProgress/{SessionInfo['Token']}',
                                 json = JsonPayload['Fields']).json()
    else:
        # Create record (Time[0] == 0.0 indicates record doesnt exists)
        Success = requests.post(f'{ServerUrl}/CreateRecord/{SessionInfo['Token']}',
                                 json = JsonPayload).json()

    if Success == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:
        TimeButton.configure(text = 'Start time')
        TimeButton.Time = [TimeButton.Time[0] + Elapsed, None]
        TimeLabel.configure(text = FormatTimeDelta(TimeButton.Time[0].total_seconds()))
        # Configure .Time to make sure every subsequent call only AddsProgress (Time[0] is set > 0)

def FormatTimeDelta(Time):

    Time = int(Time)  #  Everything past decimal point = microsecnonds

    Hours = Time // 3600
    Minutes = (Time % 3600) //  60
    Seconds = Time % 60

    return f'Time  =  {Hours}h : {Minutes}m : {Seconds}s'

def CompleteMaze(MazeID, Completed, SolveButton, ProgressButton):
    
    if Completed == True:
        return
    
    if 'Stop time' == ProgressButton.cget('text'):
        ProgressButton.invoke()
        # Forces button to TimeCommit() before setting maze to complete

    JsonPayload = {'Table' : 'Progress', 'Fields' : {'MazeID' : MazeID,
                                                    'Time' : 0.0,
                                                    'Completed' : True}}

    if ProgressButton.Time[0]:
        # Timedelta values with no duriation arent considered truthy
        # Add progress (Time[0] > 0.0 indicates record already exists)
        Success = requests.post(f'{ServerUrl}/AddProgress/{SessionInfo['Token']}',
                                 json = JsonPayload['Fields']).json()
    else:
        # Create record (Time[0] == 0.0 indicates record doesnt exists)
        Success = requests.post(f'{ServerUrl}/CreateRecord/{SessionInfo['Token']}',
                                 json = JsonPayload).json()

    if Success == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:
        SolveButton.MazeInfo[2] = True
        ProgressButton.configure(text = 'Completed', state = 'disabled')
        # Disables StartTime button as maze is marked as complete

def PrintMaze(MazeArray):
    
    MazeImg = Image.fromarray(Resize(array(MazeArray, uint8), 4000))
    # A4 is ~8.5 * ~11.5 inches. Avg printer DPI ~450 DPI. Pixels to fill up A4 = 8.5 * 450 = ~4000 pixels in the smallest dimension. Img should be similar size or else resizing in paint causes quality loss.

    with NamedTemporaryFile(suffix = '.png', delete = False) as Temp:
        Path = Temp.name  # Genrate temporary path that doesnt interfere with anything
        MazeImg.save(Path)

    try:
        run(['mspaint', '/p', Path], check = True)
        OpenMessage('Printing job successful')
    except:
        OpenMessage('Printing job failed')
    OpenMessage('If the print didnt go\nAs expected, configure\nYour default printer in setting')
    # Depending on printer (eg printer is too far away or in error state) Printing job successful can be displayed however it fails in the printer itself
    # Or user expected a different printer to be used and must configure

    remove(Path)
    # Print only needs file for short time as it loads it locally for itself -> can delete temp path safely

def SaveMaze(MazeArray):
    
    MazeImg = Image.fromarray(Resize(array(MazeArray, uint8), 512))
    AbsPath = ''

    while AbsPath == '':
        AbsPath = filedialog.asksaveasfilename(title = 'Select a folder',
                                               defaultextension = '.png',
                                               filetypes = [('PNG', '.png')])
    # Fetches chosen file path for saving

    MazeImg.save(AbsPath)

def ToProfile(UserName):

    Pages.Window.focus_set()

    ProfileInfo['UName'] = UserName
    ProfileInfo['TabView'].set('Created Mazes')
    ProfileInfo['UserLabel'].configure(text = UserName)

    for PageVar in ProfileInfo['PageVars']:
        PageVar.set(1)

    UpdateTab('Created Mazes')

    RaiseFrame(ProfileInfo['Frame'])

def UpdateTab(TabPage):

    if TabPage == 'Created Mazes':
        Tab = 0
        ExtraFunc = lambda : f'Likes  :  {Data['Likes']}'
        JsonPayload = {'Pages' : ProfileInfo['PageVars'][0].get(),
                       'UserName' : ProfileInfo['UName']}
        Response = requests.post(f'{ServerUrl}/Filter/{SessionInfo['Token']}', json = JsonPayload).json()

    elif TabPage == 'Created Comments':
        Tab = 1
        ExtraFunc = lambda : f'Comment  :\n\n{Data['Comment']}'
        JsonPayload = {'Pages' : ProfileInfo['PageVars'][1].get(),
                       'ByUser' : True}
        Response = requests.post(f'{ServerUrl}/FetchComments/{SessionInfo['Token']}', json = JsonPayload).json()
        
    else:  #  TabView == 'Progressed Mazes'
        Tab = 2
        ExtraFunc = lambda : f'{FormatTimeDelta(Data['Time'])}\n\nCompleted : {Data['Completed']}'
        JsonPayload = {'Pages' : ProfileInfo['PageVars'][2].get()}
        Response = requests.post(f'{ServerUrl}/UserProgress/{SessionInfo['Token']}', json = JsonPayload).json()
    # Defines important variables depending on current tab and fetches appropriate data fron server

    if Response == False:
        Logout()
        OpenMessage('Your token has changed\nOr the sent / requested\nData had corrupted')
    else:

        WidgetList = ProfileInfo['Widgets'][Tab]
        for Index in range(5):

            AffectedWidgets = WidgetList[Index]
            # Gets correct widgets depending on current tab

            try:
                Data = Response[Index]

                AffectedWidgets['Frame'].pack(pady = (30, 0))
                AffectedWidgets['Frame'].data = Data['MazeID']
                # Attatches info to frame for <Button-1> bind command

                MazeImg = Resize(array(loads(Data['MazeList']), uint8), 150)
                AffectedWidgets['ButtonSim'].configure(
                    image = CTkImage(Image.fromarray(MazeImg), size = (150, 150)))
                
                AffectedWidgets['Completion'].configure(text = f'Name : {Data['MazeName']}\nCompleted : {Data['Completed']}')
                AffectedWidgets['Extra'].configure(text = ExtraFunc())
                
            except IndexError:
                AffectedWidgets['Frame'].pack_forget()
                # If less than 5 objects are returned in the list, hide the frames of the missing data

        # For each frame representing a maze + its info, get the WidgetList data representing it and configure the widgets with said data

        ProfileInfo['ScrollableFrame'][Tab]._parent_canvas.yview_moveto(0)
        # Scrolls back to top using TkCanvas CTkScrollableFrame inherits from
        # Scrolling on frame also forces widgets packed on it to update and show new images
    
# ------------------ METHOD LOGIC ------------------


Gen.Window = Pages.Window
Gen.Resize = lambda Array : Resize(Array, 300)
Sol.Window = Pages.Window
Sol.Resize = lambda Array : Resize(Array, 200)
# Defines important variables and emthods in other scripts

LoginInfo = Pages.CreateLogin(AttemptLogin, ToSignup, ShowPassword)
SignupInfo = Pages.CreateSignup(ApplySignup, ToLogin, ShowPassword)
HomeInfo = Pages.CreateHome(ToGeneration, ToExplore)
FilterInfo = Pages.CreateFilter(GetFilteredMazes, InspectMaze)
GenerationInfo = Pages.CreateGeneration(GenerateMaze, SubmitMaze)
DrawInfo = Pages.CreateDraw(GenerateMaze, DrawOnMaze, SubmitMaze)
InspectInfo = Pages.CreateInspect(Solve, CompleteMaze, PrintMaze, SaveMaze)
ProfileInfo = Pages.CreateProfile(InspectMaze, UpdateTab)
# Creates all CTk widgets and frames

LoginInfo['Frame'].place(x = 0, y = 0)
SignupInfo['Frame'].place(x = 250, y = 220)
HomeInfo['Frame'].place(x = 0, y = 0)
FilterInfo['Frame'].place(x = 0, y = 0)
GenerationInfo['Frame'].place(x = 0, y = 0)
DrawInfo['Frame'].place(x = 0, y = 0)
InspectInfo['Frame'].place(x = 0, y = 0)
ProfileInfo['Frame'].place(x = 0, y = 0)
# Places all CTk widgets and frames

LoginInfo['Frame'].lift()
Pages.Window.mainloop()
# Opens login page and executes
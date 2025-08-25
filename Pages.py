from customtkinter import *
from PIL import Image
# ------------------ IMPORTS ------------------


def CreateWindow():
    Window = CTk()
    # help(CTkLabel.grid)

    Window.title('Mazenta')
    Window.geometry('700x550+250+50')
    Window.resizable(False, False)

    Window.iconbitmap(default = 'App/Images/Logo.ico')  #  Remove App/ path at runtime
    # Only takes .ico images
    # More reliable than iconphoto as CTk runs Tk which runs its own iconbitmap() which may override iconphoto

    Window._set_appearance_mode('Dark')
    # Overrides system default

    return Window
Window = CreateWindow()
# Method only to fold code for code clarity

SmallFont = CTkFont(size = 14)
SmallFontBold = CTkFont(size = 14, weight = 'bold')
XSmallFont = CTkFont(size = 12)
BigFont = CTkFont(size = 24, weight = 'bold')
TitleFont = CTkFont(size = 36, weight = 'bold')
# Font family not specified as it would rely on user installing certain fonts files

LoginImg = CTkImage(Image.open('App/Images/LoginBG.png'), size = (700, 550))
ShowImg = CTkImage(Image.open('App/Images/Show.png'), size = (20, 20))
HomeBGImg = CTkImage(Image.open('App/Images/HomeBG.png'), size = (700, 550))
CreateImg = CTkImage(Image.open('App/Images/Create.png'), size = (95, 95))
ExploreImg = CTkImage(Image.open('App/Images/Explore.png'), size = (95, 95))
SearchImg = CTkImage(Image.open('App/Images/Search.png'), size = (55, 45))
HomeImg = CTkImage(Image.open('App/Images/Home.png'), size = (15, 15))
ForwardImg = CTkImage(Image.open('App/Images/Forward.png'), size = (15, 15))
BackImg = CTkImage(Image.open('App/Images/Back.png'), size = (15, 15))
StartImg = CTkImage(Image.open('App/Images/Start.png'), size = (20, 20))
EndImg = CTkImage(Image.open('App/Images/End.png'), size = (20, 20))
WallImg = CTkImage(Image.open('App/Images/Wall.png'), size = (20, 20))
PathImg = CTkImage(Image.open('App/Images/Path.png'), size = (20, 20))
SendImg = CTkImage(Image.open('App/Images/Send.png'), size = (20, 20))
LikeImg = CTkImage(Image.open('App/Images/Like.png'), size = (30, 30))
# Loading images
# ------------------ VARIABLES ------------------


DropdownOptions = {}
NavigationOptions = {}
UName = ''
DropdownDefault = StringVar()
# DropdownOptions, UName, DropdownDefault ran and assigned in App.py

Algorithm = StringVar()
WidthVar = IntVar()
HeightVar = IntVar()
# For GenerateMazes and DrawMazes tabs to share same slider values
# ------------------ MULTI PAGE WIDGETS ------------------


def CreateUserDropdown(Frame):

    HomeMenuFrame = CTkFrame(Frame, fg_color = 'white', bg_color = 'white')
    HomeMenuFrame.place(x = 10, y = 10)

    CTkOptionMenu(
        HomeMenuFrame,
        0, 30, 15,
        'white', '#367ed1', text_color = 'black',
        values = ['Account', 'Logout'],
        command = lambda CurValue : (DropdownOptions[CurValue](), DropdownDefault.set(UName)),
        variable = DropdownDefault,
        button_color = '#367ed1', button_hover_color = '#93b6de',
        dropdown_fg_color = '#367ed1', dropdown_text_color = 'black', dropdown_hover_color = '#93b6de',
        anchor = 'center').pack()
# TKinter doesnt support moving widgets between parents, so a new one is crated for each page
# DropdownOptions, DropdownDefault and UName all set in App.py

def CreateNavigation(Frame, TimeButton = None):

    HomeNavFrame = CTkFrame(Frame, fg_color = 'white', bg_color = 'white')
    HomeNavFrame.place(x = 570, y = 10)

    StopTime = lambda : None
    if TimeButton:
        StopTime = lambda : TimeButton.invoke() if 'Stop time' == TimeButton.cget('text') else None
        # Packed into lambda so that .cget('text') is evaluated later at runtime
    # If tab is changed from InspectMaze while timer is running, pause timer and add time to database

    CTkButton(
        HomeNavFrame,
        0, 30, 10,
        bg_color = 'white', fg_color = '#367ed1', hover_color = '#93b6de',
        text = '',
        image = BackImg,
        command = lambda : (NavigationOptions['Back'](),
                            StopTime())).pack(side = 'left')
    CTkButton(
        HomeNavFrame,
        0, 30, 10,
        bg_color = 'white', fg_color = '#367ed1', hover_color = '#93b6de',
        text = '',
        image = HomeImg,
        command = lambda : (NavigationOptions['Home'](),
                            StopTime())).pack(side = 'left', padx = 4)
    CTkButton(
        HomeNavFrame,
        0, 30, 10,
        bg_color = 'white', fg_color = '#367ed1', hover_color = '#93b6de',
        text = '',
        image = ForwardImg,
        command = lambda : (NavigationOptions['Forward'](),
                            StopTime())).pack(side = 'left')
# TKinter doesnt support moving widgets between parents, so a new one is crated for each page

def CreateLogin(LoginPress, SignupPress, ShowPassword):

    LoginFrame = CTkFrame(Window, 700, 550)

    CTkLabel(LoginFrame,
             text = '',
             image = LoginImg).place(x = 0, y = 0)

    HomeMainFrame = CTkFrame(LoginFrame, fg_color = 'white', bg_color = 'white')
    HomeMainFrame.place(x = 250, y = 225)

    CTkLabel(HomeMainFrame,
             bg_color = 'white',
             text = 'Welcome Back', font = BigFont).pack()
             
    UNameEntry = CTkEntry(HomeMainFrame,
                          200, 30, 15, 1,
                          placeholder_text = 'Enter username or email')
    UNameEntry.pack(pady = (24, 16))
    PasswordEntry = CTkEntry(HomeMainFrame,
                             200, 30, 15, 1,
                             placeholder_text = 'Enter password', font = SmallFont)
    PasswordEntry.pack()

    ShowButton = CTkButton(HomeMainFrame,
              20, 20, 200,
              fg_color = 'white',
              hover_color = '#cacaca',
              text = '',
              image = ShowImg,
              border_width = 1, border_color = 'grey',
              command = lambda : ShowPassword(ShowButton, PasswordEntry))
    ShowButton.pack(pady = (8, 12))
    CTkButton(HomeMainFrame,
              80, 20, 200,
              fg_color = '#c800ff', hover_color = '#d05bf1',
              text = 'Login', text_color = 'white', font = SmallFont,
              command = lambda : LoginPress(UNameEntry.get(), PasswordEntry.get())).pack(pady = (0, 16))
    CTkButton(HomeMainFrame,
              80, 15, 200,
              fg_color = 'white', hover_color = '#b1cff3',
              text = "Don't have an account ?", text_color = '#2175ca', font = XSmallFont,
              command = SignupPress).pack()

    return {'Frame' : LoginFrame,
            'UserName' : UNameEntry,
            'Password' : PasswordEntry}

def CreateSignup(SignupPress, LoginPress, ShowPassword):

    SignupFrame = CTkFrame(Window, height = 250, fg_color = 'white', bg_color = 'white')
    
    FNameEntry = CTkEntry(SignupFrame,
                          200, 25, 15, 1,
                          placeholder_text = 'Enter first name')
    FNameEntry.pack(side = 'top')
    LNameEntry = CTkEntry(SignupFrame,
                          200, 25, 15, 1,
                          placeholder_text = 'Enter last name')
    LNameEntry.pack(pady = 6)
    EmailEntry = CTkEntry(SignupFrame,
                          200, 25, 15, 1,
                          placeholder_text = 'Enter email')
    EmailEntry.pack()
    UNameEntry = CTkEntry(SignupFrame,
                          200, 25, 15, 1,
                          placeholder_text = 'Enter username')
    UNameEntry.pack(pady = 6)
    PasswordEntry = CTkEntry(SignupFrame,
                             200, 25, 15, 1,
                             placeholder_text = 'Enter password')
    PasswordEntry.pack()

    ShowButton = CTkButton(SignupFrame,
              20, 20, 200,
              fg_color = 'white',
              hover_color = '#cacaca',
              text = '',
              image = ShowImg,
              border_width = 1, border_color = 'grey',
              command = lambda : ShowPassword(ShowButton, PasswordEntry))
    ShowButton.pack(pady = (6, 8))
    CTkButton(SignupFrame,
              80, 20, 200,
              fg_color = '#c800ff', hover_color = '#d05bf1',
              text = 'Signup', text_color = 'white', font = SmallFont,
              command = SignupPress).pack(pady = (8, 12))
    CTkButton(SignupFrame,
              80, 15, 200,
              fg_color = 'white', hover_color = '#b1cff3',
              text = 'Already have an account ?', text_color = '#2175ca', font = XSmallFont,
              command = LoginPress).pack()

    return {'Frame' : SignupFrame,
            'email' : EmailEntry,
            'first name' : FNameEntry,
            'last name' : LNameEntry,
            'username' : UNameEntry,
            'password' : PasswordEntry}

def CreateHome(CreatePress, ExplorePress):

    HomeFrame = CTkFrame(Window, 700, 550)

    CTkLabel(HomeFrame,
             text = '',
             image = HomeBGImg).place(x = 0, y = 0)
    
    CreateUserDropdown(HomeFrame)
    CreateNavigation(HomeFrame)

    HomeMainFrame = CTkFrame(HomeFrame, 400, 300, 40, fg_color = '#cacaca', bg_color = 'white')
    HomeMainFrame.place(x = 150, y = 125)

    WelcomeLabel = CTkLabel(HomeMainFrame,
             bg_color = '#cacaca',
             font = TitleFont)
    WelcomeLabel.pack(pady = 30)
    # Text = parameter configured in App.py ToHome() and is set to UserName

    CTkButton(HomeMainFrame,
              155, 170, 15,
              bg_color = '#cacaca', fg_color = '#367ed1', hover_color = '#93b6de',
              text = '\nCreate\nMazes', font = SmallFontBold,
              command = CreatePress,
              image = CreateImg, compound = 'bottom',
              anchor = 'n').pack(side = 'left', padx = (30, 15), pady = (0, 30), anchor = 'n')
    CTkButton(HomeMainFrame,
              155, 170, 15,
              bg_color = '#cacaca', fg_color = '#367ed1', hover_color = '#93b6de',
              text = '\nExplore\nMazes', font = SmallFontBold,
              command = ExplorePress,
              image = ExploreImg, compound = 'bottom',
              anchor = 'n').pack(side = 'right', padx = (15, 30), pady = (0, 30), anchor = 'n')
    # Compound = parameter determines how image is aligned to the text

    return {'Frame' : HomeFrame,
            'WelcomeLabel' : WelcomeLabel}

def CreateFilter(SearchPress, MazePress):

    FilterFrame = CTkFrame(Window, 700, 550)

    CTkLabel(FilterFrame,
             text = '',
             image = HomeBGImg).place(x = 0, y = 0)
    
    CreateUserDropdown(FilterFrame)
    CreateNavigation(FilterFrame)

    FilterMazesFrame = CTkScrollableFrame(FilterFrame, 500, 380, 40, fg_color = 'black', bg_color = 'white')
    FilterMazesFrame.place(x = 70, y = 50)
    # Pack_propagate(False) would extend the frame to fit all the widgets inside -> no point in scrollable

    FilterOptionsFrame = CTkFrame(FilterFrame, 500, 40, fg_color = 'black', bg_color = 'black')
    FilterOptionsFrame.place(x = 100, y = 60)
    FilterOptionsFrame.pack_propagate(False)  #  Disables scaling with child widget size

    CTkButton(FilterOptionsFrame,
              30, 30, 10,
              bg_color = 'black', fg_color = 'black', hover_color = '#202020',
              text = '',
              command = lambda : (Pages.set(1),
                                SearchPress(1,
                                MazeNameEntry.get(),
                                AlgorithmLocal.get(), Size.get())),
              image = SearchImg).pack(side = 'left')
    
    MazeNameEntry = CTkEntry(FilterOptionsFrame,
            165, 30, 100,
            border_width = 1, border_color = 'white',
            fg_color = 'black',
            text_color = 'white',
            placeholder_text = 'Enter maze name', placeholder_text_color = 'white')
    MazeNameEntry.pack(side = 'left')

    AlgorithmLocal = StringVar()
    CTkOptionMenu(FilterOptionsFrame,
        40, 30, 10,
        'black', 'black', text_color = 'white',
        values = ['Any', 'Custom', 'Division', 'Backtracker', 'Prims'],
        variable = AlgorithmLocal,
        button_color = 'black', button_hover_color = '#202020',
        dropdown_fg_color = 'black', dropdown_text_color = 'white', dropdown_hover_color = '#202020',
        anchor = 'center').pack(side = 'left', padx = (15))
    Size = StringVar()
    CTkOptionMenu(FilterOptionsFrame,
        40, 30, 10,
        'black', 'black', text_color = 'white',
        values = ['Any', 'Small\n(0 -> 900)', 'Medium\n(900 -> 4.9K)', 'Large\n(4.9K -> 10K)'],
        variable = Size,
        button_color = 'black', button_hover_color = '#202020',
        dropdown_fg_color = 'black', dropdown_text_color = 'white', dropdown_hover_color = '#202020',
        anchor = 'center').pack(side = 'left')
    # Variable = parameter forces any change in widget value to update the variable to said value
    # OptionMenu has no .get() function so this is used

    Pages = IntVar(value = 1)

    WidgetList = []

    for i in range(5):

        MazeFrame = CTkFrame(FilterMazesFrame, corner_radius = 20,
                             fg_color = '#cacaca', bg_color = 'black')
        MazeFrame.bind('<Enter>', lambda Event, ThisFrame = MazeFrame : ThisFrame.configure(fg_color = 'grey'))
        MazeFrame.bind('<Leave>', lambda Event, ThisFrame = MazeFrame : ThisFrame.configure(fg_color = '#cacaca'))
        # Lambda delays evaluating expression after : until called
        # Without ThisFrame = MazeFrame (evaluates at creation), the expression would refer to the latest instance of MazeFrame once the loop is finished
        MazeFrame.bind('<Button-1>', lambda Event, ThisFrame = MazeFrame : MazePress(ThisFrame.data))
        # Simulating button functionality
        # Bind always passes the event itself as a parameter

        CompletionLabel = CTkLabel(MazeFrame, text = '', text_color = 'black', font = SmallFontBold)
        CompletionLabel.pack(pady = 10)
        MazeButtonSim = CTkLabel(MazeFrame, text = '')
        MazeButtonSim.pack(padx = 20, pady = (0, 20))
        # Unlike buttons, labels store 'strong pointers' to their images so images do not get garbage collected
        
        WidgetList.append({'Frame' : MazeFrame,
                           'ButtonSim' : MazeButtonSim,
                           'Label' : CompletionLabel})
    # Creates frame and widgets for every maze to be displayed on 1 page (5)

    PagesMenuFrame = CTkFrame(FilterMazesFrame, fg_color = 'black')
    PagesMenuFrame.pack(side = 'bottom', pady = (40, 0))

    CTkButton(PagesMenuFrame,
        0, 30, 10,
        fg_color = '#cacaca', hover_color = 'grey',
        text = '',
        image = BackImg,
        command = lambda : (Pages.set(Pages.get() - 1) if Pages.get() > 1 else None,
                            SearchPress(Pages.get(), MazeNameEntry.get(), AlgorithmLocal.get(), Size.get()))).pack(side = 'left', padx = (0, 15))
    CTkButton(PagesMenuFrame,
        0, 30, 10,
        fg_color = '#cacaca', hover_color = 'grey',
        text = '',
        image = ForwardImg,
        command = lambda : (Pages.set(Pages.get() + 1),
                            SearchPress(Pages.get(), MazeNameEntry.get(), AlgorithmLocal.get(), Size.get()))).pack(side = 'left')
    # Lambda command includes incrementing the PageNumber before calling method
    # Other way around would cause method to use old page number as it hasnt been updated before calling

    return {'Frame' : FilterFrame,
            'ScrollableFrame' : FilterMazesFrame,
            'Name' : MazeNameEntry,
            'Algorithm' : AlgorithmLocal,
            'Size' : Size,
            'Widgets' : WidgetList}

def CreateGeneration(GenerateMazes, SubmitMaze):

    GenerateFrame = CTkFrame(Window, 700, 550)

    CTkLabel(GenerateFrame,
             text = '',
             image = HomeBGImg).place(x = 0, y = 0)
    
    CreateUserDropdown(GenerateFrame)
    CreateNavigation(GenerateFrame)

    GenerateMazesFrame = CTkFrame(GenerateFrame, 550, 450, 40, fg_color = 'black', bg_color = 'white')
    GenerateMazesFrame.pack_propagate(False)  #  Disable frame scaling dependent on child widget size
    GenerateMazesFrame.place(x = 75, y = 50)

    MazeDisplay = CTkLabel(GenerateMazesFrame,
                           300, 330, 15,
                           text = '',
                           fg_color = '#cacaca')
    MazeDisplay.pack(side = 'left', padx = (30, 0))
    # No text, image = configured with CTkImage(PILImage) in App.py

    CTkOptionMenu(GenerateMazesFrame,
        50, 30, 10,
        'black', 'black', text_color = 'white',
        values = ['Division', 'Backtracker', 'Prims', 'Custom'],
        variable = Algorithm,
        button_color = 'black', button_hover_color = '#202020',
        dropdown_fg_color = 'black', dropdown_text_color = 'white', dropdown_hover_color = '#202020',
        anchor = 'center').pack(pady = (35, 10))
    
    WidthLabel = CTkLabel(GenerateMazesFrame, text_color = 'white')
    WidthLabel.pack()
    CTkSlider(GenerateMazesFrame,
        135, 20, 10,
        fg_color = 'white',
        progress_color = '#71adf1',
        from_ = 3,
        to = 100,
        variable = WidthVar,
        command = lambda Width : WidthLabel.configure(text = f'Width : {int(Width)}')).pack(pady = (0, 10))
    # Label takes text = (evaluated at creation) or textvariable = (evaluated always) but the IntVar passed cannot be formatted eg f'Value : {intVar}'
    # Therefore slider must .configure to change text at every value change
    
    HeightLabel = CTkLabel(GenerateMazesFrame, text_color = 'white')
    HeightLabel.pack()
    CTkSlider(GenerateMazesFrame,
        135, 20, 10,
        fg_color = 'white',
        progress_color = '#71adf1',
        from_ = 3,
        to = 100,
        variable = HeightVar,
        command = lambda Height : HeightLabel.configure(text = f'Height : {int(Height)}')).pack(pady = (0, 10))
    # Variable = parameter forces any change in widget value to update the variable to said value
    # Used so that the labels can be configured to the right values when switching between GenerateMaze and DrawMaze frames in App.py
    
    DistanceVar = IntVar()
    DistanceLabel = CTkLabel(GenerateMazesFrame, text_color = 'white')
    DistanceLabel.pack()
    CTkSlider(GenerateMazesFrame,
        135, 20, 10,
        fg_color = 'white',
        progress_color = '#71adf1',
        from_ = 0,
        to = 100,
        variable = DistanceVar,
        command = lambda Distance : DistanceLabel.configure(text = f'Length : {int(Distance)}')).pack()

    Submit = CTkButton(GenerateMazesFrame,
              135, 25, 200,
              fg_color = 'grey', hover_color = '#C6C6C6',
              command = lambda : SubmitMaze(MazeName.get()),
              state = 'disabled',
              text = 'Submit maze', text_color = 'white', font = XSmallFont)
    Submit.pack(side = 'bottom', pady = (12, 35))

    MazeName = CTkEntry(GenerateMazesFrame,
                135, 25, 100,
                border_width = 1, border_color = 'white',
                fg_color = 'black',
                text_color = 'white',
                placeholder_text = 'Enter maze name', placeholder_text_color = 'white')
    MazeName.pack(side = 'bottom')

    Apply = CTkButton(GenerateMazesFrame,
            135, 25, 200,
            fg_color = 'grey', hover_color = '#C6C6C6',
            command = lambda : GenerateMazes(WidthVar.get(), HeightVar.get(), Algorithm.get()),
            text = 'Apply changes', text_color = 'white', font = XSmallFont)
    Apply.pack(side = 'bottom', pady = 12)

    return {'Frame' : GenerateFrame,
            'Distance' : (DistanceVar, DistanceLabel),
            'MazeLabel' : MazeDisplay,
            'SizeX' : WidthLabel,
            'SizeY' : HeightLabel,
            'Name' : MazeName,
            'Buttons' : (Submit, Apply)}

def CreateDraw(GenerateMazes, DrawOnMaze, SubmitMaze):

    DrawFrame = CTkFrame(Window, 700, 550)

    CTkLabel(DrawFrame,
             text = '',
             image = HomeBGImg).place(x = 0, y = 0)
    
    CreateUserDropdown(DrawFrame)
    CreateNavigation(DrawFrame)

    DrawMazesFrame = CTkFrame(DrawFrame, 550, 450, 40, fg_color = 'black', bg_color = 'white')
    DrawMazesFrame.pack_propagate(False)  #  Disable frame scaling dependent on child widget size
    DrawMazesFrame.place(x = 75, y = 50)

    MazeDisplay = CTkLabel(DrawMazesFrame,
                           300, 330, 15,
                           text = '',
                           fg_color = '#cacaca')
    MazeDisplay.pack_propagate(False)
    MazeDisplay.bind('<Button-1>', command = lambda Event : DrawOnMaze(Event, CursorColour))
    MazeDisplay.bind('<B1-Motion>', command = lambda Event : DrawOnMaze(Event, CursorColour))
    MazeDisplay.pack(side = 'left', padx = (30, 0))
    # When pressed on, retrieve button press or hold event (can get x and y pos) and pass it to method

    CTkOptionMenu(DrawMazesFrame,
        50, 30, 10,
        'black', 'black', text_color = 'white',
        values = ['Division', 'Backtracker', 'Prims', 'Custom'],
        variable = Algorithm,
        button_color = 'black', button_hover_color = '#202020',
        dropdown_fg_color = 'black', dropdown_text_color = 'white', dropdown_hover_color = '#202020',
        anchor = 'center').pack(pady = (35, 10))
    
    WidthLabel = CTkLabel(DrawMazesFrame, text_color = 'white')
    WidthLabel.pack()
    CTkSlider(DrawMazesFrame,
        135, 20, 10,
        fg_color = 'white',
        progress_color = '#71adf1',
        from_ = 3,
        to = 100,
        variable = WidthVar,
        command = lambda Width : WidthLabel.configure(text = f'Width : {int(Width)}')).pack(pady = (0, 10))
    # Label takes text = (evaluated at creation) or textvariable = (evaluated always) but the IntVar passed cannot be formatted eg f'Value : {intVar}'
    # Therefore slider must .configure to change text at every value change
    
    HeightLabel = CTkLabel(DrawMazesFrame, text_color = 'white')
    HeightLabel.pack()
    CTkSlider(DrawMazesFrame,
        135, 20, 10,
        fg_color = 'white',
        progress_color = '#71adf1',
        from_ = 3,
        to = 100,
        variable = HeightVar,
        command = lambda Height : HeightLabel.configure(text = f'Height : {int(Height)}')).pack(pady = (0, 10))
    # Variable = parameter forces any change in widget value to update the variable to said value
    # Used so that the labels can be configured to the right values when switching between GenerateMaze and DrawMaze frames in App.py

    CursorColour = StringVar(value = '000')
    CTkButton(DrawMazesFrame,
              135, 25, 200,
              fg_color = 'black',
              image = StartImg, compound = 'right',
              command = lambda : CursorColour.set('100'),
              text = 'Place start', text_color = 'white', font = XSmallFont).pack()
    CTkButton(DrawMazesFrame,
              135, 25, 200,
              fg_color = 'black',
              image = EndImg, compound = 'right',
              command = lambda : CursorColour.set('010'),
              text = 'Place end', text_color = 'white', font = XSmallFont).pack()
    CTkButton(DrawMazesFrame,
              135, 25, 200,
              fg_color = 'black',
              image = WallImg, compound = 'right',
              command = lambda : CursorColour.set('000'),
              text = 'Place wall', text_color = 'white', font = XSmallFont).pack()
    CTkButton(DrawMazesFrame,
              135, 25, 200,
              fg_color = 'black',
              image = PathImg, compound = 'right',
              command = lambda : CursorColour.set('111'),
              text = 'Place path', text_color = 'white', font = XSmallFont).pack()
    # 3 numbers passed to CursolColour.set are split -> [1, 0, 0]
    # Then *255 -> [255, 0, 0] to get a numpy RGB value

    Submit = CTkButton(DrawMazesFrame,
              135, 25, 200,
              fg_color = 'grey', hover_color = 'light grey',
              command = lambda : SubmitMaze(MazeName.get(), True),
              text = 'Submit maze', text_color = 'white', font = XSmallFont)
    Submit.pack(side = 'bottom', pady = (12, 35))

    MazeName = CTkEntry(DrawMazesFrame,
                135, 25, 100,
                border_width = 1, border_color = 'white',
                fg_color = 'black',
                text_color = 'white',
                placeholder_text = 'Enter maze name', placeholder_text_color = 'white')
    MazeName.pack(side = 'bottom')

    Apply = CTkButton(DrawMazesFrame,
              135, 25, 200,
              fg_color = 'grey', hover_color = "#C6C6C6",
              text = 'Apply changes', text_color = 'white', font = XSmallFont,
              command = lambda : GenerateMazes(WidthVar.get(), HeightVar.get(), Algorithm.get()))
    Apply.pack(side = 'bottom', pady = 12)

    return {'Frame' : DrawFrame,
            'MazeLabel' : MazeDisplay,
            'SizeX' : WidthLabel,
            'SizeY' : HeightLabel,
            'Name' : MazeName}

def CreateInspect(SolveMaze, CompleteMaze, PrintMaze, SaveMaze):

    InspectFrame = CTkFrame(Window, 700, 550)

    CTkLabel(InspectFrame,
             text = '',
             image = HomeBGImg).place(x = 0, y = 0)
    
    InspectMazesFrame = CTkFrame(InspectFrame, 680, 450, 40, fg_color = 'black', bg_color = 'white')
    InspectMazesFrame.pack_propagate(False)  #  Disable frame scaling dependent on child widget size
    InspectMazesFrame.place(x = 10, y = 50)

    ProgressButton = CTkButton(InspectMazesFrame,
            135, 25, 200,
            fg_color = 'grey', hover_color = '#C6C6C6',
            text_color = 'white', font = XSmallFont)
    # Must be defined early due to reference in CreateNavigation, packed later with ProgressLabel

    CreateUserDropdown(InspectFrame)
    CreateNavigation(InspectFrame, ProgressButton)

    CommentsFrame = CTkScrollableFrame(InspectMazesFrame, 200, 350, 20, fg_color = '#cacaca')
    CommentsFrame.pack(side = 'left', padx = (20))

    MazeLikeFrame = CTkFrame(InspectMazesFrame, 200, 350, fg_color = 'black')
    MazeLikeFrame.pack(side = 'left')

    MazeDisplay = CTkLabel(MazeLikeFrame,
                           200, 270, 15,
                           text = '', font = SmallFontBold,
                           compound = 'bottom',
                           fg_color = '#cacaca')
    MazeDisplay.pack()

    LikeCount = CTkLabel(MazeLikeFrame,
        0, 0, 0,
        fg_color = 'black',
        text_color = 'white', font = SmallFont)
    LikeCount.pack(side = 'left', padx = (30, 15), pady = (20, 0))

    LikeButton = CTkButton(MazeLikeFrame,
        30, 30, 0,
        fg_color = 'light grey', hover = False,
        image = LikeImg,
        text = '')
    LikeButton.pack(side = 'left', pady = (20, 0))
    # Likes info assigned in ToInspect() and LikeToggle() in App.py
    
    Pages = IntVar(value = 1)

    WidgetList = []

    for i in range(5):

        CommentFrame = CTkFrame(CommentsFrame, corner_radius = 10,
                             fg_color = '#949494', bg_color = '#cacaca')

        UserNameButton = CTkButton(CommentFrame,
                                   60, 30, 10,
                                   fg_color = '#6D6D6D', hover_color = '#7B7B7B',
                                   text = '', font = XSmallFont)
        UserNameButton.pack()

        CommentLabel = CTkLabel(CommentFrame, 200, corner_radius = 10,
                                text = '', text_color = 'black', font = XSmallFont,
                                wraplength = 150, anchor = 'w', justify = 'left')
        CommentLabel.pack(padx = 0, pady = 6)
        # Anchor = parameter determines where the text lines up in the widget (eg centered or against the top)
        # Justify = parameter determines how the text is lined up (on left margin, centered)
        
        WidgetList.append({'Frame' : CommentFrame,
                           'Button' : UserNameButton,
                           'Label' : CommentLabel})
    # Creates frame and widgets for every comment to be displayed on 1 page

    CTkLabel(CommentsFrame, text = 'Comments :', font = SmallFontBold).pack()

    PostCommentFrame = CTkFrame(CommentsFrame, fg_color = '#cacaca')
    PostCommentFrame.pack(side = 'bottom')

    PagesMenuFrame = CTkFrame(CommentsFrame, fg_color = '#cacaca')
    PagesMenuFrame.pack(side = 'bottom', pady = (40, 0))

    PostEntry = CTkEntry(PostCommentFrame,
                         200, 30, 20,
                         placeholder_text = 'Enter comment')
    PostEntry.pack(pady = 6)
    SendButton = CTkButton(PostCommentFrame,
                           0, 20, 10,
                           text = '',
                           fg_color = '#A09E9E', hover_color = 'grey',
                           image = SendImg)
    SendButton.pack()

    MinusPage = CTkButton(PagesMenuFrame,
        0, 30, 10,
        fg_color = '#A09E9E', hover_color = 'grey',
        text = '',
        image = BackImg)
    MinusPage.pack(side = 'left', padx = (0, 15))
    PlusPage = CTkButton(PagesMenuFrame,
        0, 30, 10,
        fg_color = '#A09E9E', hover_color = 'grey',
        text = '',
        image = ForwardImg)
    PlusPage.pack(side = 'left')
    # Command assigned in App.py as the MazeID is needed to be passed to the command method

    CreatorButton = CTkButton(InspectMazesFrame,
            corner_radius = 20,
            fg_color = '#cacaca', hover_color = 'grey',
            text = '', text_color = 'black')
    CreatorButton.pack(pady = (61, 0))
    # Text and command assigned in App.py as UserName is needed for both

    ProgressLabel = CTkLabel(InspectMazesFrame,
            0, 0, 0,
            fg_color = 'black',
            text_color = 'white', font = XSmallFont)
    ProgressLabel.pack(pady = (35, 12))
    ProgressButton.pack()
    # Text assigned in App.py as time data is different from user to user

    SolveMenu = CTkOptionMenu(InspectMazesFrame,
        50, 30, 10,
        fg_color = '#cacaca', text_color = 'black',
        values = ['A - Star', 'Left Hand', 'Tremaux'],
        button_color = '#cacaca', button_hover_color = 'grey',
        dropdown_fg_color = '#cacaca', dropdown_text_color = 'black', dropdown_hover_color = 'grey',
        anchor = 'center')
    SolveMenu.pack(pady = (35, 12))
    # Command assigned in App.py as it depends on whether the maze is already completed

    Solve = CTkButton(InspectMazesFrame,
            135, 25, 200,
            fg_color = 'grey', hover_color = '#C6C6C6',
            command = lambda : (CompleteMaze(*Solve.MazeInfo[1::], Solve, ProgressButton),
                                SolveMaze(Solve.MazeInfo[0], MazeDisplay, SolveMenu.get())),
            text = 'Solve now', text_color = 'white', font = XSmallFont)
    Solve.pack()

    Print = CTkButton(InspectMazesFrame,
            135, 25, 200,
            fg_color = 'grey', hover_color = '#C6C6C6',
            command = lambda : (PrintMaze(Solve.MazeInfo[0])),
            text = 'Print maze', text_color = 'white', font = XSmallFont)
    Print.pack(pady = (55, 10))

    Save = CTkButton(InspectMazesFrame,
            135, 25, 200,
            fg_color = 'grey', hover_color = '#C6C6C6',
            command = lambda : (SaveMaze(Solve.MazeInfo[0])),
            text = 'Save maze', text_color = 'white', font = XSmallFont)
    Save.pack()

    return {'Frame' : InspectFrame,
            'CommentsFrame' : CommentsFrame,
            'MazeLabel' : MazeDisplay,
            'AssignButtons' : (MinusPage, PlusPage, SendButton, CreatorButton, Solve),
            'Pages' : Pages,
            'Likes' : (LikeButton, LikeCount),
            'Progress' : (ProgressButton, ProgressLabel),
            'PostEntry' : PostEntry,
            'Widgets' : WidgetList}

def CreateProfile(MazePress, GetNewData):

    ProfileFrame = CTkFrame(Window, 700, 550)

    CTkLabel(ProfileFrame,
             text = '',
             image = HomeBGImg).place(x = 0, y = 0)
    
    DisplayFrame = CTkFrame(ProfileFrame,
                            500, 480, 40,
                            fg_color = 'black', bg_color = 'white')
    DisplayFrame.pack_propagate(False)
    DisplayFrame.place(x = 100, y = 50)

    CreateUserDropdown(ProfileFrame)
    CreateNavigation(ProfileFrame)

    UserLabel = CTkLabel(DisplayFrame,
                bg_color = 'black', fg_color = 'black',
                text_color = 'white', font = TitleFont)
    UserLabel.pack(pady = (20, 10))

    ProfileTabs = CTkTabview(DisplayFrame,
                             fg_color = 'black', bg_color = 'black',
                             segmented_button_fg_color = '#cacaca',
                             segmented_button_unselected_color = 'grey',
                             segmented_button_selected_color = '#2b2b2b',
                             segmented_button_unselected_hover_color = '#2b2b2b',
                             segmented_button_selected_hover_color = '#2b2b2b',
                             command = lambda : GetNewData(ProfileTabs.get()))
    ProfileTabs.pack()
    # ProfileTabs.get() returns current tabs name

    ProfileTabs.add('Created Mazes')
    ProfileTabs.add('Created Comments')
    ProfileTabs.add('Progressed Mazes')

    WidgetList = [[], [], []]
    PageList = [IntVar(value = 1), IntVar(value = 1), IntVar(value = 1)]
    Scrollables = []

    for Tab in range(3):

        if Tab == 0:
            ThisFrame = ProfileTabs.tab('Created Mazes')
        elif Tab == 1:
            ThisFrame = ProfileTabs.tab('Created Comments')
        else:
            ThisFrame = ProfileTabs.tab('Progressed Mazes')

        InfoFrame = CTkScrollableFrame(ThisFrame, 500, 300, fg_color = 'black', bg_color = 'black')
        InfoFrame.pack()

        Scrollables.append(InfoFrame)

        for i in range(5):

            MazeFrame = CTkFrame(InfoFrame, corner_radius = 20,
                                fg_color = '#cacaca', bg_color = 'black')
            MazeFrame.bind('<Enter>', lambda Event, ThisFrame = MazeFrame : ThisFrame.configure(fg_color = 'grey'))
            MazeFrame.bind('<Leave>', lambda Event, ThisFrame = MazeFrame : ThisFrame.configure(fg_color = '#cacaca'))
            # Lambda delays evaluating expression after : until called
            # Without ThisFrame = MazeFrame (evaluates at creation), the expression would refer to the latest instance of MazeFrame in MazeFrame.configure()
            MazeFrame.bind('<Button-1>', lambda Event, ThisFrame = MazeFrame : MazePress(ThisFrame.data))
            # Simulating button functionality

            ExtraData = CTkLabel(MazeFrame,
                                 text = '', text_color = 'black', font = XSmallFont,
                                 wraplength = 100, justify = 'left')
            ExtraData.pack(side = 'right', padx = (0, 20))

            CompletionLabel = CTkLabel(MazeFrame, text = '', text_color = 'black', font = SmallFontBold)
            CompletionLabel.pack(pady = 10)
            MazeButtonSim = CTkLabel(MazeFrame, text = '')
            MazeButtonSim.pack(padx = 20, pady = (0, 20))
            # Unlike buttons, labels store 'strong pointers' to their images so images do not get garbage collected
            
            WidgetList[Tab].append({'Frame' : MazeFrame,
                            'ButtonSim' : MazeButtonSim,
                            'Completion' : CompletionLabel,
                            'Extra' : ExtraData})
        
        PagesMenuFrame = CTkFrame(InfoFrame, fg_color = 'black')
        PagesMenuFrame.pack(side = 'bottom', pady = (40, 0))

        Back = CTkButton(PagesMenuFrame,
            0, 30, 10,
            fg_color = '#cacaca', hover_color = 'grey',
            text = '',
            image = BackImg,
            command = lambda Tab = Tab : (PageList[Tab].set(PageList[Tab].get() - 1) 
                                        if PageList[Tab].get() > 1 else None,
                                        GetNewData(ProfileTabs.get())))
        Back.pack(side = 'left', padx = (0, 15))
        Forward = CTkButton(PagesMenuFrame,
            0, 30, 10,
            fg_color = '#cacaca', hover_color = 'grey',
            text = '',
            image = ForwardImg,
            command = lambda Tab = Tab : (PageList[Tab].set(PageList[Tab].get() + 1),
                                GetNewData(ProfileTabs.get())))
        Forward.pack(side = 'left')
    # For every tab : creates frames and widgets for each object to be displayed on a page (max 5)
    # Can't reuse frames and widgets as ProfileTabs.tabs count as frames and changing widget parent frame at runtime isnt supported

    return {'Frame' : ProfileFrame,
            'TabView' : ProfileTabs,
            'UName' : None,
            'UserLabel' : UserLabel,
            'ScrollableFrame' : Scrollables,
            'PageVars' : PageList,
            'Widgets' : WidgetList}
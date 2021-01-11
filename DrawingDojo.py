#Title of game: Drawing Dojo
#Created by: Kevin Hu
#Class: ICS3UI

from tkinter import *
from math import *
from time import *
from PIL import Image, ImageTk
from pyscreenshot import grab

# tkinter global variables
root = Tk()
root.title("Drawing Dojo")
screenWidth = 1200
screenHeight = 600
screen = Canvas(root,width=screenWidth, height=screenHeight, highlightthickness=0)
screen.pack()


#SET INITIAL VALUES
def setInitialValues():
    global paintColours, numColours, colourBoxSize, spacing
    global xPaletteMin, xPaletteMax, yPaletteMin, yPaletteMax
    global xMouse, yMouse, mouseDown, Qpressed, numColours
    global xPaintDishMin,xPaintDishMax,yPaintDishMin,yPaintDishMax
    global currPaintColour, outlineColour, backgroundColour, lineThickness 
    global timeStart, c, gameTime, clockDisplay, timerStillRunning
    global imageWidth, imageHeight, img, resized, photo, score

    paintColours=["black", "white"] #paint colour options
    numColours = len(paintColours) 
    colourBoxSize = 30 #constant values
    spacing = 5
    xPaletteMin = 10 #starting x-coordinate of paint palette
    xPaletteMax = xPaletteMin + (spacing + colourBoxSize)*2 #ending x-coordinate of paint palette
    yPaletteMin = 40 #starting y-coordinate of paint palette
    yPaletteMax = yPaletteMin + (spacing + colourBoxSize)*numColours #starting y-coordinate of paint palette
    timerStillRunning = False #the timer is not currently running unless stated otherwise

    #arrays to hold dimensions of each palette
    xPaintDishMin = [] 
    xPaintDishMax = []
    yPaintDishMin = []
    yPaintDishMax = []

    #filling the arrays with each palette's dimensions:
    for i in range(0, numColours ):
        xPaintDishMin.append(0)
        xPaintDishMax.append(0)
        yPaintDishMin.append(0)
        yPaintDishMax.append(0)

        xPaintDishMin[i] = xPaletteMin 
        xPaintDishMax[i] = xPaintDishMin[i]  + colourBoxSize
        yPaintDishMin[i] = yPaletteMin + i * (spacing + colourBoxSize)
        yPaintDishMax[i] = yPaintDishMin[i] + colourBoxSize


    #determining difficulty and level
    if level == "level1": #if player chose level 1:
        #chooses image for level 1
        img = Image.open("level1.gif")
        resized = img.resize((500,500))
        photo = ImageTk.PhotoImage(resized)

        if difficulty == "novice":
            gameTime = 80 #the amount of time (s) novices get to complete the level

        elif difficulty == "amateur":
            gameTime = 40 #the amount of time (s) amateurs get to complete the level
            
        elif difficulty == "master":
            gameTime = 20 #the amount of time (s) masters get to complete level

    elif level == "level2": #if player chose level 2:
        #chooses image for level 2
        img = Image.open("level2.gif")
        resized = img.resize((500,500))
        photo = ImageTk.PhotoImage(resized)
        
        if difficulty == "novice":
            gameTime = 115

        elif difficulty == "amateur":
            gameTime = 75 
            
        elif difficulty == "master":
            gameTime = 50 

    elif level == "level3": #if player chose level 3:
        #chooses image for level 3
        img = Image.open("level3.gif")
        resized = img.resize((500,500))
        photo = ImageTk.PhotoImage(resized)
        
        if difficulty == "novice":
            gameTime = 150 

        elif difficulty == "amateur":
            gameTime = 100
            
        elif difficulty == "master":
            gameTime = 75 

    #assigning values to variables to avoid reference before assignment error
    xMouse = 300
    yMouse = 300
    
    currPaintColour = "black"
    outlineColour = "black"
    backgroundColour = "white"

    mouseDown = False
    Qpressed = False

    lineThickness = 4

    timeStart = time()
    c = 0
    clockDisplay = screen.create_text( 200, 200, text=str( round(gameTime,1) ) + "   " + str(c), font="Times 48", fill="black")

    #dimensions of image to be put on right half of the screen
    imageWidth = 600 
    imageHeight = 600

    score = 0
    
    newScreen() #displays the user interface


#THE USER INTERFACE - WHAT THE PLAYER WILL SEE WHEN THEY START PLAYING THE GAME
def newScreen():
    global background, divider, currentLevel, brushWidthLabel, brushWidthSlider, palettes

    palettes = [] #array to hold the multiple paint palettes 
    
    screen.delete(all) #delete any objects currently on the screen
    
    background = screen.create_rectangle(0, 0, screenWidth, screenHeight, fill="white", outline = "white" ) #background to draw on
    divider = screen.create_rectangle(imageWidth - lineThickness, 0, imageWidth + lineThickness, imageHeight, fill = "black") #divides the screen into respective halves
    currentLevel = screen.create_image( 900, 300, image = photo ) #displays current level based on what user selected

    #creating a label and slider for brush width
    brushWidthLabel = Label(root, text="Brush size")
    brushWidthLabel.place( x=450, y=40)
    
    brushWidthSlider = Scale( root, from_ = 2, to=20, orient=HORIZONTAL, length=100, width = 10, resolution = 2  )
    brushWidthSlider.pack()
    brushWidthSlider.place( x = 450, y = 10 )
    brushWidthSlider.set( 80 )

    #create all the different colour palettes
    for i in range(0, numColours):
        palette = screen.create_rectangle( xPaintDishMin[i], yPaintDishMin[i], xPaintDishMax[i], yPaintDishMax[i], fill=paintColours[i], width = 2 )
        palettes.append(palette)


#INTRO SCREEN - APPEARS WHEN USER RUNS PROGRAM, ALLOWS THE PLAYER TO SELECT A LEVEL
def introScreen():
    global dojo, level1Button, level2Button, level3Button, instructionButton

    #create the background
    dojo = PhotoImage(file = "dojo.gif")
    screen.create_image(600,300,image=dojo)
    
    #create button for level 1
    level1Button = Button(root,text = "Level 1", font = "Times 30", command = level1ButtonPressed, anchor = CENTER) 
    level1Button.pack()
    level1Button.place(x = 50, y = 400, width = 220 , height = 100 )

    #create button for level 2
    level2Button = Button(root,text = "Level 2", font = "Times 30", command = level2ButtonPressed, anchor = CENTER)  
    level2Button.pack()
    level2Button.place(x = 350, y = 400, width = 220 , height = 100 )

    #create button for level 3
    level3Button = Button(root,text = "Level 3", font = "Times 30", command = level3ButtonPressed, anchor = CENTER)  
    level3Button.pack()
    level3Button.place(x = 650, y = 400, width = 220 , height = 100 )

    #create button for instructions
    instructionButton = Button(root,text = "How to play", font = "Times 30", command = instructionButtonPressed, anchor = CENTER) 
    instructionButton.pack()
    instructionButton.place(x = 950, y = 400, width = 220 , height = 100 )


#WHEN THE USER SELECTS LEVEL 1
def level1ButtonPressed():
    global level
    
    level = "level1"
    difficultySelect() #after choosing a level, allow player to choose a difficulty
    

#WHEN THE USER SELECTS LEVEL 2
def level2ButtonPressed():
    global level
    
    level = "level2"
    difficultySelect()


#WHEN THE USER SELECTS LEVEL 3
def level3ButtonPressed():
    global level
    
    level = "level3"
    difficultySelect()


#WHEN THE USER CLICKS HOW TO PLAY
def instructionButtonPressed():
    global intropicture, instructions, backButton

    #gets rid of previous screen's buttons
    level1Button.destroy()  
    level2Button.destroy()
    level3Button.destroy()
    instructionButton.destroy()

    #uploads image containing instructions to the screen
    intropicture = PhotoImage(file = "intropicture.gif")
    screen.create_image(630,300,image=intropicture)

    #upload image containing instructions
    instructions = PhotoImage(file = "instructions.gif")
    screen.create_image(600,200,image=instructions)

    #creates button to go back to the introscreen                                   
    backButton = Button(root,text = "Back", font = "Times 30", command = backButtonPressed, anchor = CENTER)  
    backButton.pack()
    backButton.place(x = 500, y = 400, width = 220 , height = 100)
    

#WHEN THE USER CLICKS BACK BUTTON
def backButtonPressed():
    backButton.destroy() #get rid of the back button
    
    introScreen() #send the user back to the intro screen

#LETTING THE PLAYER SELECT A DIFFICULTY
def difficultySelect():
    global dojo, noviceButton, amateurButton, masterButton, instructionButton

    #gets rid of all the buttons from the intro screen
    level1Button.destroy()  
    level2Button.destroy()
    level3Button.destroy()
    instructionButton.destroy()

    #create button for novice difficulty
    noviceButton = Button(root,text = "Novice", font = "Times 30", command = noviceButtonPressed, anchor = CENTER) 
    noviceButton.pack()
    noviceButton.place(x = 200, y = 400, width = 220 , height = 100 )

    #create button for amateur difficulty
    amateurButton = Button(root,text = "Amateur", font = "Times 30", command = amateurButtonPressed, anchor = CENTER)  
    amateurButton.pack()
    amateurButton.place(x = 500, y = 400, width = 220 , height = 100 )

    #create button for master difficulty
    masterButton = Button(root,text = "Master", font = "Times 30", command = masterButtonPressed, anchor = CENTER)  
    masterButton.pack()
    masterButton.place(x = 800, y = 400, width = 220 , height = 100 )


#WHEN THE USER SELECTS NOVICE DIFFICULTY
def noviceButtonPressed():
    global difficulty
    
    difficulty = "novice"
    runGame() #after the user has specified all game settings, run the game!


#WHEN THE USER SELECTS AMATEUR DIFFICULTY
def amateurButtonPressed():
    global difficulty
    
    difficulty = "amateur"
    runGame()


#WHEN THE USER SELECTS MASTER DIFFICULTY
def masterButtonPressed():
    global difficulty
    
    difficulty = "master"
    runGame()
    
    
#UPDATES THE COUNTDOWN TIMER         
def redrawGameClock(c):
      global clockDisplay
      
      screen.delete( clockDisplay ) #delete the clock display to prevent multiple clock displays on top of each other

      #clockDisplay takes the gameTime and displays it as text to the screen
      clockDisplay = screen.create_text( 320, 50, text=str( round(gameTime,1) ) + "   " + str(c), font="Times 36 bold", fill="black")
      screen.update() #update the screen
        

#SETS THE COLOUR OF THE PAINTBRUSH
def setColour():
    global currPaintColour
    #tests to see if mouse is inside a palette and switches paint colour to said palette
    
    for i in range(0,numColours):
        
        if xMouse <= xPaintDishMax[i] and xMouse >= xPaintDishMin[i] and yMouse <= yPaintDishMax[i] and yMouse >= yPaintDishMin[i]:
            currPaintColour = paintColours[i]
            setOutlineColour()
            break


#SETS THE OUTLINE COLOUR OF THE PAINTBRUSH
def setOutlineColour():
    global outlineColour

    outlineColour = currPaintColour

    
#DETERMINES IF MOUSE IS INSIDE PAINT PALETTE
def mouseInsidePalette():
    #if the mouse is within the borders of the palette:
    if xMouse <= (colourBoxSize+10) and yMouse <= yPaletteMax: 
        return True
    
    else:
        return False


#GETS CALLED WHENEVER THE MOUSE IS CLICKED DOWN
def mouseClickHandler( event ):
    global xMouse, yMouse, mouseDown, currentShape, currPaintColour, xStart, yStart, pointsOnParabola, pointsInPolygon
    
    xMouse = event.x #determining current location of mouse
    yMouse = event.y

    mouseDown = True #signifies that mouse is pressed down
    
    if timerStillRunning == True: #as long as the timer is still going
        if mouseInsidePalette() == True: #change the colour if mouse clicks on palette
            setColour()

        else: #otherwise, draw a dot wherever the mouse is
            xStart = xMouse
            yStart = yMouse
            paintOneStroke()


#GETS CALLED WHEN MOUSE MOVES
def mouseMotionHandler( event ):
    global xMouse, yMouse, xEnd, yEnd, currentShape
    
    xMouse = event.x #determines current location of mouse
    yMouse = event.y
    
    #if the mouse clicked down, is not inside a palette, and the player still has time left:
    if mouseInsidePalette() == False and mouseDown == True and timerStillRunning == True:
        paintOneLine()

    
#GETS CALLED WHENEVER MOUSE IS CLICKED
def paintOneStroke(): 
    width = int( brushWidthSlider.get()) / 2 #determine the brush size from the slider value
    
    if xMouse + width <= imageWidth - lineThickness: #if the mouse is within the drawing space:
        #create a splotch of paint to the screen
        dot = screen.create_oval( xMouse-width, yMouse-width, xMouse+width, yMouse+width, fill=currPaintColour, outline=outlineColour )
        
    screen.update() #update the screen


#GETS CALLED WHENEVER MOUSE IS HELD DOWN AND MOVED
def  paintOneLine():
    global xStart, yStart

    #determines the number of paint splotches to make by determining the distance between point A of a mouse and point B
    numPoints = max(2, int(distance( [xMouse, yMouse], [xStart, yStart]))) #minimum two paint splotches to make a "line" (otherwise just call above function)
    
    #determines direction and speed mouse is moving in in order to obtain x- and y-coordinates of paint splotches
    deltaX = (xMouse-xStart)/numPoints 
    deltaY = (yMouse-yStart)/numPoints

    r = int(brushWidthSlider.get()) / 2 #determine the brush size from the slider value

    x = xStart #starting coordinates of mouse
    y = yStart
    
    for i in range(1, numPoints):
        y = y + deltaY #creating new coordinates for every new point the mouse moves to
        x = x + deltaX
        if x + r <= imageWidth - lineThickness: #if the mouse is within the drawing space:
            #create multiple splotches of paint to the screen that follows the mouse
            dot = screen.create_oval(x-r, y-r, x+r, y+r, fill=currPaintColour, outline=currPaintColour)

    xStart = xMouse #current location of mouse
    yStart = yMouse


#DISTANCE FORMULA USED IN ABOVE FUNCTION
def distance( pointA, pointB ):
    #Just calculates distance with the distance formula
    x1=pointA[0]
    y1=pointA[1]
    x2=pointB[0]
    y2=pointB[1]

    return sqrt( (x2-x1)**2 + (y2-y1)**2 )


#GETS CALLED WHENEVER THE MOUSE IS RELEASED
def mouseReleaseHandler( event ):
    global mouseDown
    
    mouseDown = False #the mouse is not currently pressed down


#GETS CALLED WHENEVER ANY KEY IS PRESSED DOWN
def keyDownHandler( event ):
    global Qpressed

    if event.keysym == "q" or event.keysym == "Q": #close window if q is pressed
        root.destroy() 


#COUNTDOWN FROM 3 SECONDS
def countdown():
    global timerStillRunning
    #3, 2, 1 countdown before beginning the game
    for i in range(3,-1,-1):
        if i == 0:
            countdown = screen.create_text( 300,275, text = "START!", font = "Times 64 bold", fill = "red" )
            
        else:
            countdown = screen.create_text( 300,275, text = i, font = "Times 64 bold", fill = "red" )

        screen.update()
        sleep(1)
        screen.delete(countdown)
        
    timerStillRunning = True


#CONVERT TKINTER CANVAS TO IMAGE FILE BY TAKING SCREENSHOT
def takeScreenshots():

    global leftScreenshot, rightScreenshot, lPx, rPx

    #screenshot of the player drawing half of the screen
    x1 = root.winfo_rootx() #get the x-coordinate of uppermost leftmost pixel of the canvas
    y1 = root.winfo_rooty() #get the y-coordinate of uppermost leftmost pixel of the canvas
    #grab the left hand portion of the screen for checking
    leftScreenshot = grab(bbox=(x1, y1, x1 + imageWidth, y1 + imageHeight), childprocess=False) #IDLE has a problem with multiprocessing, so it is turned off

    #screenshot of the image half of the screen
    x2 = root.winfo_rootx() + imageWidth #similar the the x-coordinate above, but starting at the halfway point of the screen
    #grab the right hand portion of the screen for checking
    rightScreenshot = grab(bbox=(x2, y1, x2 + imageWidth, y1 + imageHeight), childprocess=False) 

    lPx = leftScreenshot.load() #load the image to obtain pixel values
    rPx = rightScreenshot.load()
    
    bindingRectangle() #call the binding rectangle procedure

    
#CREATE A BINDING RECTANGLE AROUND THE USER DRAWING TO INCREASE ACCURACY OF THE COMPARISON
#By creating a binding rectangle, the unnecessary outer white pixels are cropped out of the drawing.
#This is intended to prevent accuracy errors, such as if the player drew a perfect image but it was offset by 1 pixel.    
def bindingRectangle():

    global leftResized, rightResized
    
    #LEFT SIDE
    #the goal of the following algorithm is to crop the exterior white borders from the screenshot of the player's drawing: 
    xValuesLeft = [] #creating arrays for the x- and y-coordinates of pixels
    yValuesLeft = []

    for x in range(leftScreenshot.size[0]): # for every pixel in the image:
        for y in range(leftScreenshot.size[1]):
            
            if lPx[x,y] < (200,200,200,200): #if pixel colour value is below specified shade (a.k.a. not white)
                xValuesLeft.append(x) #append pixel coordinates
                yValuesLeft.append(y)

    #these four values will be the coordinates for the binding rectangle: the furthest points outward to which a non-white pixel value exists
    if len(xValuesLeft) == 0: #if the user didn't draw anything to the screen, end the game with a score of 0%
        endGame()

    else: #if the user DID draw something:
        xSmallestLeft = xValuesLeft[0] #starting values are set as first index of array
        ySmallestLeft = yValuesLeft[0]

        xLargestLeft = xValuesLeft[0]
        yLargestLeft = yValuesLeft[0]

    #sorting through the array:
    for i in range(0, len(xValuesLeft)):
        
        if xValuesLeft[i] < xSmallestLeft: #runs through the xValuesLeft array to find any smaller x-values
            xSmallestLeft = xValuesLeft[i]
            
        elif xValuesLeft[i] > xLargestLeft: #runs through the xValuesLeft array to find any larger x-values
            xLargestLeft = xValuesLeft[i]

    for i in range(0, len(yValuesLeft)):
        
        if yValuesLeft[i] < ySmallestLeft: #runs through the yValuesLeft array to find any smaller y-values
            ySmallestLeft = yValuesLeft[i]
            
        elif yValuesLeft[i] > yLargestLeft: #runs through the yValuesLeft array to find any larger y-values
            yLargestLeft = yValuesLeft[i]
            
    #RIGHT SIDE
    #The exact same thing is done to the screenshot of the image:
    xValuesRight = [] 
    yValuesRight = []

    for x in range(rightScreenshot.size[0]): 
        for y in range(rightScreenshot.size[1]):
            
            if rPx[x,y] < (200,200,200,200): 
                xValuesRight.append(x) 
                yValuesRight.append(y)


    xSmallestRight = xValuesRight[0] 
    ySmallestRight = yValuesRight[0]

    xLargestRight = xValuesRight[0]
    yLargestRight = yValuesRight[0]

    for i in range(0, len(xValuesRight)):
        
        if xValuesRight[i] < xSmallestRight:
            xSmallestRight = xValuesRight[i]
            
        elif xValuesRight[i] > xLargestRight:
            xLargestRight = xValuesRight[i]

    for i in range(0, len(yValuesRight)):
        
        if yValuesRight[i] < ySmallestRight:
            ySmallestRight = yValuesRight[i]
            
        elif yValuesRight[i] > yLargestRight:
            yLargestRight = yValuesRight[i]

    leftCropped = leftScreenshot.crop((xSmallestLeft, ySmallestLeft, xLargestLeft, yLargestLeft))
    rightCropped = rightScreenshot.crop((xSmallestRight, ySmallestRight, xLargestRight, yLargestRight))

    #leftCropped.show() #<----- uncomment to see the result of creating a binding rectangle on the player's drawing
    #rightCropped.show() #<----- uncomment to see the result of creating a binding rectangle on the image

    leftResized = leftCropped.resize((100,100))
    rightResized = rightCropped.resize((100,100))


#FUNCTION TO RETURN THE SIMILARITY OF ANY TWO PIXEL VALUES
def compareRGB(px1,px2):
    #this algorithm helps with accuracy immensely, but when colour is added, its effectiveness falters (hence why the available colour palettes are only black and white).
    #this algorithm returns a float from 1 to 0, which represents the similarity of px1 and px2: 1 being the most similar, 0 being the least similar.

    #calculates maximum difference between two pixels
    maxDiff = 255*3
    
    #get the positive difference between px1 and px2
    diff = abs(sum(px1) - sum(px2))
    
    #take the positive difference, divide it by the maximum difference, and subtract from 1 to obtain the float value
    score = 1-(diff / maxDiff)
    
    return score #return float value


#SCORES THE SIMILARITY OF THE PLAYER'S DRAWING TO THE LEVEL IMAGE USING THE ABOVE FUNCTION
def scoreImage(user, image):

    global im
    
    score = 0
    maxScore = user.size[0] * user.size[1] #set to the size of the user drawing 
    
    for x in range(user.size[0]): #loops through every pixel of the drawing
        for y in range(user.size[1]):
            
            # check the similarity of the two pixels
            leftPixel = user.getpixel((x,y))
            rightPixel = image.getpixel((x,y))
            colourScore = compareRGB(leftPixel, rightPixel) #call the function to receive the float value for similarity
            
            # record the differences, if there are any
            if colourScore < 0.5: #0.5 being the margin to determine whether or not two pixels are different
                user.putpixel((x,y),(255,0,0))
                
            score += colourScore #add float value to total score
            
    #show the differences between player drawing and reference image in an image file, to be displayed in the end screen
    resize = user.resize((200,200))
    im = ImageTk.PhotoImage(resize)

    
    # return the total percentage of similarity between user drawing and image
    return score / maxScore * 100 


#RUN THE GAME AFTER THE INTRO SCREEN
def runGame():
    global score, user, perfect, gameTime, timeStart

    #get rid of all the buttons
    noviceButton.destroy()  
    amateurButton.destroy()
    masterButton.destroy()

    #set the initial values
    setInitialValues()
    countdown()
    
    while gameTime > 0.1: #if set to 0 instead of 0.1, timer counts down to -0.1 
        timeNow = time()
        timeElapsedSinceLastCheck = timeNow - timeStart #checks how much time passed between the starting and current time
            
        if timeElapsedSinceLastCheck >= 0.1: #if 0.1 seconds have passed since the last check 
                
            gameTime = gameTime - 0.1 #reduce the game time
            redrawGameClock("") #redraws a new game clock
                  
            timeStart = time()  #The most important step: reset timeStart to the current time as soon as the game clock has updated

    #delete palettes, timer and screen divider to just display player's drawing and the image
    for i in range(0, len(palettes)):
        screen.delete(palettes[i])
        
    screen.delete(clockDisplay, divider)
    brushWidthLabel.destroy()
    brushWidthSlider.destroy()

    #update the screen
    screen.update()

    timerStillRunning = False #set timerStillRunning to False to signify that time has run out

    takeScreenshots() #take screenshots in order to convert drawings to image files

    #convert screenshots to RGB images
    user =  leftResized.convert('RGB')
    perfect = rightResized.convert('RGB')

    score = scoreImage(user,perfect) #compare the two images by running the comparison function 
    
    endGame() #goes to the endgame screen
        

#END SCREEN THAT GETS CALLED AFTER RUNGAME FINISHES
def endGame():
    global playAgainButton, intropicture

    intropicture = PhotoImage(file = "intropicture.gif")
    screen.create_image(600,300,image=intropicture) #display image of dojo to the screen

    #text to show player's score/statistics
    screen.create_text(475, 175,anchor=N, font="Times 40 italic bold", text="Your Score:")
    screen.create_text(475, 250,anchor=N, font="Times 80 italic bold", text=str(round(score, 2)) + "%")
    screen.create_text(600, 525,anchor=N, font="Times 40 italic bold", text="Press Q to quit") 

    #button to allow the player to play again                                   
    playAgainButton = Button(root,text = "Play Again", font = "Times 30", command =  playAgainButtonPressed, anchor = CENTER)  
    playAgainButton.pack
    playAgainButton.place(x = 500, y = 400, width = 220 , height = 100 )

    screen.create_image(725, 250, image = im) #image that shows player's drawing superimposed on the image; the red pixels signify pixels with non-matching values

def playAgainButtonPressed():
    
    playAgainButton.destroy()  #gets rid of the previous screen's button
    introScreen()  #goes back to the intro screen

        
#STARTS THE GAME BY PASSING CONTROL TO THE PROCEDURE introScreen() 
root.after(0, introScreen)

#BINDS THE PROCEDURE mouseClickHandler TO ALL MOUSE-CLICK EVENTS
screen.bind("<Button-1>", mouseClickHandler)

#BINDS THE PROCEDURE mouseMotionHandler TO ALL MOUSE-MOTION EVENTS
screen.bind("<Motion>", mouseMotionHandler) 

#BINDS THE PROCEDURE mouseReleaseHandler TO ALL MOUSE-RELEASE EVENTS
screen.bind("<ButtonRelease-1>", mouseReleaseHandler) 

#BINDS THE PROCEDURE keyDownHandler TO ALL KEY-DOWN EVENTS
screen.bind("<Key>", keyDownHandler)

screen.focus_set()
root.mainloop()

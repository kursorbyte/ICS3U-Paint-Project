'''
Evan Sun
ICS3U McKenzie
Paint Project
'''
#modules
from pygame import *
from random import *
from math import *
from time import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
font.init()

#managing tkinter
root = Tk()
root.withdraw()
tkinterIcon = PhotoImage(file = "assets/titlebar_icon.png")
root.iconphoto(False,tkinterIcon)

#window title and icon
display.set_caption("Springtime Sketch")
titlebarIcon = image.load("assets/titlebar_icon.png")
display.set_icon(titlebarIcon)

width,height = 1600,900                 #window dimensions
canvasWidth,canvasHeight = 1140,790
canvasCornerX,canvasCornerY = 162,90       #coordinates of top left corner of canvas
screen = display.set_mode((width,height))
#standard colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0)
WHITE = (255,255,255)
#theme colors light
LBLUE = (192, 217, 231)
LGREEN = (199, 220, 163)
LPINK = (241, 206, 216)
LBEIGE = (241, 233, 223)
#theme colors dark
DBLUE = (31, 63, 81)
DGREEN = (80,102,39)
DPINK = (123,35,57)
DBEIGE = (109,83,47)

#logical rects
canvasRect = Rect(canvasCornerX,canvasCornerY,canvasWidth,canvasHeight)

pencilRect = Rect(20,175,50,50)
brushRect = Rect(90,175,50,50)
highlighterRect = Rect(20,245,50,50)
inkBrushRect = Rect(90,245,50,50)
pixelBrushRect = Rect(20,315,50,50)
sprayRect = Rect(90,315,50,50)
eyedropperRect = Rect(20,385,50,50)
eraserRect = Rect(90,385,50,50)
lineRect = Rect(20,455,50,50) 
polygonRect = Rect(90,455,50,50)
rectangleFRect = Rect(20,525,50,50)    #filled square
rectangleUFRect = Rect(90,525,50,50)   #unfilled square
circleFRect = Rect(20,595,50,50)
circleUFRect = Rect(90,595,50,50)
selectRect = Rect(20,665,50,50)
fillRect = Rect(90,665,50,50)
flipHRect = Rect(20,735,50,50)      #horiz flip
flipVRect = Rect(90,735,50,50)      #vert flip
textRect = Rect(20,805,50,50)
clearRect = Rect(90,805,50,50)

undoRect = Rect(1324,20,50,50)
redoRect = Rect(1392,20,50,50)
saveRect = Rect(1460,20,50,50)
loadRect = Rect(1528,20,50,50)

#alpha surface to work with transparency (highlighter tool)
alphaSurf = Surface((canvasWidth,canvasHeight))
alphaSurf.fill(WHITE)
alphaSurf.set_colorkey(WHITE)       #makes everything the color WHITE on alphaSurf transparent

#layer for showing brush cursor (previews brush width)
cursorSurf = Surface((canvasWidth,canvasHeight))
cursorSurf.fill(WHITE)
cursorSurf.set_colorkey(WHITE)

#background image
backgroundimg = image.load("assets/background.jpg")
screen.blit(backgroundimg, (0,0))

#create canvas
draw.rect(screen, DBLUE, (160,88,1144,794))     #canvas outline
draw.rect(screen, WHITE, canvasRect)
screencopy = screen.subsurface(canvasRect).copy()   #copy blank canvas to avoid screencopy undefined

#draw tool rects
toolRects = [pencilRect,highlighterRect,pixelBrushRect,eyedropperRect,lineRect,rectangleFRect,circleFRect,selectRect,flipHRect,textRect,brushRect,inkBrushRect,sprayRect,eraserRect,
             polygonRect,rectangleUFRect,circleUFRect,fillRect,flipVRect,clearRect]
toolCols = [LBLUE,LGREEN,LPINK,LBEIGE]*5
toolOutlines = [DBLUE,DGREEN,DPINK,DBEIGE]*5
for i in range(len(toolRects)):
    draw.rect(screen,toolCols[i],toolRects[i])          #buttons
    draw.rect(screen,toolOutlines[i],toolRects[i],2)    #button outlines

#draw color palette picker
colorpickerRect = Rect(1326,90,250,257)     #top corner and dimensions of color gradient image
draw.rect(screen,DBLUE,(1324,88,254,261))   #outline
colorpicker = image.load("assets/colorpicker.png")
screen.blit(colorpicker,colorpickerRect)
  
#draw top bar buttons rects
topRects = [undoRect,redoRect,saveRect,loadRect]
for i in range(len(topRects)):
    draw.rect(screen,LBLUE,topRects[i])
    draw.rect(screen,DBLUE,topRects[i],2)

#UI fonts with fixed size
lFont = font.Font("assets/font.ttf",50)      #large UI font 50px
sFont = font.Font("assets/font.ttf",30)      #small UI font 30px
ssFont = font.Font("assets/font.ttf",20)     #smaller UI font 20px
sssFont = font.Font("assets/font.ttf",15)     #smallest UI font 15px

#title "Springtime Sketch"
titleRect = Rect(20,25,420,50)
titlePic = lFont.render("Springtime Sketch",True,DBLUE)
screen.blit(titlePic,(titleRect[0],titleRect[1]))

#"Tools" title
toolsTRect = Rect(20,115,120,40)
draw.rect(screen,LBLUE,toolsTRect)
draw.rect(screen,DBLUE,toolsTRect,2)
toolsTPic = sFont.render("Tools",True,DBLUE)
screen.blit(toolsTPic,(toolsTRect[0]+20,toolsTRect[1]+10))

#program variables
tool = ""                   #what tool is selected
undoList = [screencopy]     #previous screencopies to go back to (starts with 1 item in it (the blank canvas))
redoList = []               #items removed from undo list go here to be redone if needed
omx,omy = 0,0               #position of old mouse location
oax,oay = 0,0               #position of old click location
r = 0
g = 0
b = 0
col = (r,g,b)
thick = 10    #thickness/size of tools
ax,ay = 0,0   #at position of mouse click
usedUndo = False    #is the last tool used undo? (used to clear redoList)
recCol = [(DBLUE)]*8     #list of recent colors used (DBLUE is empty state)
                         #7 spots for recent colors and an additional spot for current color
#R,G,B textbox user input
rInput = str(r)
gInput = str(g)
bInput = str(b)
#thickness textbox user input
thickInput = str(thick)
#for polygon tool
polygonList = []            #polygon points
polygonClosed = False       #tracks if polygon is closed (means user finished drawing)
#for text tool
writingText = False     #differentiate btwn the text tool being selected and actually typing text (true - actually typing text)(false - clicked off text box, awaiting next click to type in a different location)
textInput = ""          #user's typed text
#flags for selection tool
drawSelectBox = False       #tracks if the selection box should be drawn
selectionMade = False       #tracks if a selection is being made (the selection box has area > 0)
readyToMove = False         #tracks if a selection has been made and mouse has been released (the selection area has been set and is ready to be moved by dragging)
moving = False              #tracks if user dragging on the selected area and is actively moving it
firstMoveDone = False       #tracks if user translated selected area and released (the initial move is done)
copied = False              #tracks if selection has been copied with ctrl+c to determine if paste should be available

#for stamps
#import stamp images
stamp1 = image.load("assets/stamps/1.png")
stamp2 = image.load("assets/stamps/2.png")
stamp3 = image.load("assets/stamps/3.png")
stamp4 = image.load("assets/stamps/4.png")
stamp5 = image.load("assets/stamps/5.png")
stamp6 = image.load("assets/stamps/6.png")
stamp7 = image.load("assets/stamps/7.png")
stamp8 = image.load("assets/stamps/8.png")
stamp9 = image.load("assets/stamps/9.png")
stamp10 = image.load("assets/stamps/10.png")
stamp11 = image.load("assets/stamps/11.png")
stamp12 = image.load("assets/stamps/12.png")
stamp13 = image.load("assets/stamps/13.png")
stamp14 = image.load("assets/stamps/14.png")
stamp15 = image.load("assets/stamps/15.png")
stamp16 = image.load("assets/stamps/16.png")
stamp17 = image.load("assets/stamps/17.png")
stamp18 = image.load("assets/stamps/18.png")
stamp19 = image.load("assets/stamps/19.png")
stamp20 = image.load("assets/stamps/20.png")
stampsList = [stamp1,stamp2,stamp3,stamp4,stamp5,stamp6,stamp7,stamp8,stamp9,stamp10,stamp11,stamp12,stamp13,stamp14,stamp15,stamp16,stamp17,stamp18,stamp19,stamp20] #list of stamp images
#stamp quick selection buttons (2 rows of 10 buttons)
stampSelectRects = []                       #list of 20 stamp button rects
for i in range(20):
    if i < 10:
        stampSelectRect = Rect(1324+i*26,809,20,20) #top row
    else:
        stampSelectRect = Rect(1064+i*26,835,20,20) #bottom row
    stampSelectRects.append(stampSelectRect)
#left and right arrow region for flipping through stamps
leftArrowRect = Rect(1324,694,30,40)
rightArrowRect = Rect(1548,694,30,40)
currentStampInd = 0                         #index of current stamp in stampsList being shown
stampPreviewRect = Rect(1376,639,150,150)   #rect that stamp previews will be shown in

#load tool icons
pencilicon = image.load("assets/pencil.png")
brushicon = image.load("assets/brush.png")
highlightericon = image.load("assets/highlighter.png")
inkbrushicon = image.load("assets/inkbrush.png")
pixelbrushicon = image.load("assets/pixelbrush.png")
spraypainticon = image.load("assets/spraypaint.png")
eyedroppericon = image.load("assets/eyedropper.png")
erasericon = image.load("assets/eraser.png")
lineicon = image.load("assets/line.png")
polygonicon = image.load("assets/polygon.png")
rectangleFicon = image.load("assets/rectangleF.png")
rectangleUFicon = image.load("assets/rectangleUF.png")
circleFicon = image.load("assets/circleF.png")
circleUFicon = image.load("assets/circleUF.png")
selecticon = image.load("assets/select.png")
fillicon = image.load("assets/fill.png")
flipHicon = image.load("assets/flipH.png")
flipVicon = image.load("assets/flipV.png")
texticon = image.load("assets/text.png")
clearicon = image.load("assets/clear.png")
undoicon = image.load("assets/undo.png")
redoicon = image.load("assets/redo.png")
saveicon = image.load("assets/save.png")
loadicon = image.load("assets/load.png")

#load tool description images
initialDesc = image.load("assets/tool_descriptions/initial_desc.png")       #intial message shown on startup when no tool is selected
pencilDesc = image.load("assets/tool_descriptions/pencil_desc.png")
brushDesc = image.load("assets/tool_descriptions/brush_desc.png")
highlighterDesc = image.load("assets/tool_descriptions/highlighter_desc.png")
inkbrushDesc = image.load("assets/tool_descriptions/inkbrush_desc.png")
pixelbrushDesc = image.load("assets/tool_descriptions/pixelbrush_desc.png")
spraypaintDesc = image.load("assets/tool_descriptions/spraypaint_desc.png")
eyedropperDesc = image.load("assets/tool_descriptions/eyedropper_desc.png")
eraserDesc = image.load("assets/tool_descriptions/eraser_desc.png")
lineDesc = image.load("assets/tool_descriptions/line_desc.png")
polygonDesc = image.load("assets/tool_descriptions/polygon_desc.png")
rectangleFDesc = image.load("assets/tool_descriptions/rectangleF_desc.png")
rectangleUFDesc = image.load("assets/tool_descriptions/rectangleUF_desc.png")
circleFDesc = image.load("assets/tool_descriptions/circleF_desc.png")
circleUFDesc = image.load("assets/tool_descriptions/circleUF_desc.png")
selectDesc = image.load("assets/tool_descriptions/select_desc.png")
fillDesc = image.load("assets/tool_descriptions/fill_desc.png")
flipHDesc = image.load("assets/tool_descriptions/flipH_desc.png")
flipVDesc = image.load("assets/tool_descriptions/flipV_desc.png")
textDesc = image.load("assets/tool_descriptions/text_desc.png")
clearDesc = image.load("assets/tool_descriptions/clear_desc.png")
stampsDesc = image.load("assets/tool_descriptions/stamps_desc.png")
undoDesc = image.load("assets/tool_descriptions/undo_desc.png")
redoDesc = image.load("assets/tool_descriptions/redo_desc.png")
saveDesc = image.load("assets/tool_descriptions/save_desc.png")
loadDesc = image.load("assets/tool_descriptions/load_desc.png")
toolDesc = [pencilDesc,highlighterDesc,pixelbrushDesc,eyedropperDesc,lineDesc,rectangleFDesc,circleFDesc,selectDesc,flipHDesc,textDesc,brushDesc,inkbrushDesc,spraypaintDesc,eraserDesc,
            polygonDesc,rectangleUFDesc,circleUFDesc,fillDesc,flipVDesc,clearDesc]  #list of description images
descRect = Rect(650,10,654,68)      #rect where tool description will be shown

running = True

while running:
    
    click = False           #check for left click down (used for single click buttons (ex:undo,redo) so clicking them doesn't spam action); each loop around resets click state
    release = False         #check for left click release
    #tkinter dialogs
    openSaveDialog = False      #should the save dialog open?
    openLoadDialog = False      #should the load dialog open?
    #are these keys pressed (for undo, redo, copy, paste shortcuts)?
    z = False
    y = False
    c = False
    v = False
    for evt in event.get():
        if evt.type == QUIT:
            confirmQuit = messagebox.askyesno(title = "Springtime Sketch", message = "Are you sure you want to quit? Any unsaved changes will be lost.\nThe flowers might wilt too...")    #quit warning when closing program
            if confirmQuit:
                running = False
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:                 #left mouse button
                ax,ay = evt.pos                 #store mouse position at the moment of left click down
                click = True                    #tracks single mouse click down event, only way to make True again is reclick (ensures click does not spam)
        if evt.type == MOUSEBUTTONUP:
            if evt.button == 1 and canvasRect.collidepoint(ax,ay) and tool not in ["eyedropper","text","polygon","flipH","flipV","clear","select","fill"]:          #if left mb released (i.e. drawing tool has made an edit), copy the canvas and add it to undoList (doesn't add new item each time program loops)
                                                                                                            #certain tools like those that draw preview shapes handle copying differently in their own if statement to avoid preview shapes being included in actual drawing
                screencopy = screen.subsurface(canvasRect).copy()   #upon mouse release (edit was made), copy the canvas to update the drawing and add last edit to undoList
                undoList.append(screencopy)
                if usedUndo == True:            #if undo was just used and then an edit was made, user should not be able to redo again (in accordance to how undo works in other programs) 
                    redoList.clear()
                    usedUndo = False
            if evt.button == 1:
                bx,by = evt.pos                     #store mouse position at the moment of left click release
                release = True                      #track single mouse release event
                if saveRect.collidepoint(ax,ay):    #tkinter dialog box stops responding and hangs after subsequent uses when coded to open with "click" but works with MOUSEBUTTONUP (dk why :/)
                    openSaveDialog = True
                if loadRect.collidepoint(ax,ay):
                    openLoadDialog = True
        if evt.type == KEYDOWN:                 #track key press event for each frame (avoid key down being registered multiple times in a row)
            if evt.key == K_z:
                z = True
            if evt.key == K_y:
                y = True
            if evt.key == K_c:
                c = True
            if evt.key == K_v:
                v = True
            #manage user input for R textbox
            if rInputRect.collidepoint(ax,ay):
                if evt.key == K_BACKSPACE:
                    rInput = rInput[:-1]            #remove last char
                if evt.key in [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_KP0,K_KP1,K_KP2,K_KP3,K_KP4,K_KP5,K_KP6,K_KP7,K_KP8,K_KP9] and len(rInput) < 3:    #only allow numeric input, max length of 3 chars
                    rInput += evt.unicode
                    if int(rInput) > 255:           #numbers out of range return to max val of 255
                        rInput = "255"
                    if rInput[0] == "0" and len(rInput) > 1:    #nums like '005' are not valid, return to min val of 0
                        rInput = "0"
            #manage user input for G textbox
            if gInputRect.collidepoint(ax,ay):
                if evt.key == K_BACKSPACE:
                    gInput = gInput[:-1]
                if evt.key in [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_KP0,K_KP1,K_KP2,K_KP3,K_KP4,K_KP5,K_KP6,K_KP7,K_KP8,K_KP9] and len(gInput) < 3:
                    gInput += evt.unicode
                    if int(gInput) > 255:
                        gInput = "255"
                    if gInput[0] == "0" and len(gInput) > 1:
                        gInput = "0"
            #manage user input for B textbox
            if bInputRect.collidepoint(ax,ay):
                if evt.key == K_BACKSPACE:
                    bInput = bInput[:-1]
                if evt.key in [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_KP0,K_KP1,K_KP2,K_KP3,K_KP4,K_KP5,K_KP6,K_KP7,K_KP8,K_KP9] and len(bInput) < 3:
                    bInput += evt.unicode
                    if int(bInput) > 255:
                        bInput = "255"
                    if bInput[0] == "0" and len(bInput) > 1:
                        bInput = "0"
            #manage user input for thickness textbox
            if thickInputRect.collidepoint(ax,ay):
                if evt.key == K_BACKSPACE:
                    thickInput = thickInput[:-1]
                if evt.key in [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_KP0,K_KP1,K_KP2,K_KP3,K_KP4,K_KP5,K_KP6,K_KP7,K_KP8,K_KP9]:    #only allow numeric input
                    thickInput += evt.unicode
                    if int(thickInput) > 2000:          #restrict valid thicknesses 1 minimum to 2000 maxiumum
                        thickInput = "2000"
                    if int(thickInput) == 0:
                        thickInput = "1"
            #manage user input for text tool
            if writingText == True:
                if evt.key == K_BACKSPACE:
                    textInput = textInput[:-1]
                elif evt.key not in [K_RETURN,K_KP_ENTER,K_TAB,K_ESCAPE,K_DELETE]:      #disable incompatible characters
                    textInput += evt.unicode
        if evt.type == MOUSEWHEEL:                                  #change thickness with scrollwheel (up > bigger, down > smaller)
            if thick + evt.y >= 1 and thick + evt.y <= 2000:        #thickness restricted 1-2000
                thick += evt.y
                thickInput = str(thick)                             #update thickness textbox value
                
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    keys = key.get_pressed()    #get keyboard input

    #variable fonts - in loop so size can change
    varFont = font.Font("assets/font.ttf",thick)   #text tool uses variable font size controlled by thickness
    
    #mouse coordinates display
    mouseCoordsRect = (470,40,155,30)
    if canvasRect.collidepoint(mx,my):
        mouseCoordsPic = sFont.render("(%d,%d)"%(mx-canvasCornerX,my-canvasCornerY),True,DBLUE)
    else:
        mouseCoordsPic = sFont.render("(x,y)",True,DBLUE)
    screen.blit(backgroundimg.subsurface(mouseCoordsRect),(mouseCoordsRect[0],mouseCoordsRect[1]))
    screen.blit(mouseCoordsPic,(mouseCoordsRect[0],mouseCoordsRect[1]))

    #tool selection
    if pencilRect.collidepoint(ax,ay) and mb[0]:
        tool = "pencil"
    if brushRect.collidepoint(ax,ay) and mb[0]:
        tool = "brush"
    if highlighterRect.collidepoint(ax,ay) and mb[0]:
        tool = "highlighter"    
    if inkBrushRect.collidepoint(ax,ay) and mb[0]:
        tool = "inkbrush"
    if pixelBrushRect.collidepoint(ax,ay) and mb[0]:
        tool = "pixelbrush"
    if sprayRect.collidepoint(ax,ay) and mb[0]:
        tool = "spraypaint"
    if eyedropperRect.collidepoint(ax,ay) and mb[0]:
        tool = "eyedropper"
    if eraserRect.collidepoint(ax,ay) and mb[0]:
        tool = "eraser"
    if lineRect.collidepoint(ax,ay) and mb[0]:
        tool = "line"
    if polygonRect.collidepoint(ax,ay) and mb[0]:
        tool = "polygon"
    if rectangleFRect.collidepoint(ax,ay) and mb[0]:
        tool = "rectangleF"
    if rectangleUFRect.collidepoint(ax,ay) and mb[0]:
        tool = "rectangleUF"
    if circleFRect.collidepoint(ax,ay) and mb[0]:
        tool = "circleF"
    if circleUFRect.collidepoint(ax,ay) and mb[0]:
        tool = "circleUF"
    if selectRect.collidepoint(ax,ay) and mb[0]:
        tool = "select"
    if fillRect.collidepoint(ax,ay) and mb[0]:
        tool = "fill"
    if flipHRect.collidepoint(ax,ay) and mb[0]:
        tool = "flipH"
    if flipVRect.collidepoint(ax,ay) and mb[0]:
        tool = "flipV"
    if textRect.collidepoint(ax,ay) and mb[0]:
        tool = "text"
    if clearRect.collidepoint(ax,ay) and mb[0]:
        tool = "clear"

    #startup tool description placeholder (when no tool selected)
    screen.blit(backgroundimg.subsurface(descRect),descRect)
    if tool == "":
        screen.blit(initialDesc,descRect)

    #hover and click indication for tools
    activeTool = ["pencil","highlighter","pixelbrush","eyedropper","line","rectangleF","circleF","select","flipH","text","brush","inkbrush","spraypaint","eraser","polygon","rectangleUF","circleUF","fill","flipV","clear"]
    for i in range(20):
        #click indication
        if activeTool[i] == tool:
            draw.rect(screen,WHITE,toolRects[i])
            draw.rect(screen,toolOutlines[i],toolRects[i],2)
            screen.blit(toolDesc[i],descRect)               #show tool description for selected tool
        #when tool not selected, redraw unclicked button
        else:
            draw.rect(screen,toolCols[i],toolRects[i])
            #draw hover outlines
            if toolRects[i].collidepoint(mx,my):
                draw.rect(screen,WHITE,toolRects[i],2)
            else:
                draw.rect(screen,toolOutlines[i],toolRects[i],2)
                
    #hover and click indication for top bar buttons (undo,redo,save,load) - these buttons do not persist (do not stay selected like a tool)
    for i in range(4):
        if topRects[i].collidepoint(ax,ay) and mb[0]:
            draw.rect(screen,WHITE,topRects[i])
            draw.rect(screen,DBLUE,topRects[i],2)
        else:
            draw.rect(screen,LBLUE,topRects[i])
            if topRects[i].collidepoint(mx,my):
                draw.rect(screen,WHITE,topRects[i],2)
            else:
                draw.rect(screen,DBLUE,topRects[i],2)

    #descriptions for hovering over undo button, redo button, save button, load button, and stamp preview
    if tool == "stamps":
        screen.blit(stampsDesc,descRect)
    if undoRect.collidepoint(mx,my) or redoRect.collidepoint(mx,my) or saveRect.collidepoint(mx,my) or loadRect.collidepoint(mx,my) or stampPreviewRect.collidepoint(mx,my):
        screen.blit(backgroundimg.subsurface(descRect),descRect)
        if undoRect.collidepoint(mx,my):
            screen.blit(undoDesc,descRect)
        if redoRect.collidepoint(mx,my):
            screen.blit(redoDesc,descRect)
        if saveRect.collidepoint(mx,my):
            screen.blit(saveDesc,descRect)
        if loadRect.collidepoint(mx,my):
            screen.blit(loadDesc,descRect)
        if stampPreviewRect.collidepoint(mx,my):
            screen.blit(stampsDesc,descRect)
                
    #draw the tool icons
    screen.blit(pencilicon,pencilRect)
    screen.blit(brushicon,brushRect)
    screen.blit(highlightericon,highlighterRect)
    screen.blit(inkbrushicon,inkBrushRect)
    screen.blit(pixelbrushicon,pixelBrushRect)
    screen.blit(spraypainticon,sprayRect)
    screen.blit(eyedroppericon,eyedropperRect)
    screen.blit(erasericon,eraserRect)
    screen.blit(lineicon,lineRect)
    screen.blit(polygonicon,polygonRect)
    screen.blit(rectangleFicon,rectangleFRect)
    screen.blit(rectangleUFicon,rectangleUFRect)
    screen.blit(circleFicon,circleFRect)
    screen.blit(circleUFicon,circleUFRect)
    screen.blit(selecticon,selectRect)
    screen.blit(fillicon,fillRect)
    screen.blit(flipHicon,flipHRect)
    screen.blit(flipVicon,flipVRect)
    screen.blit(texticon,textRect)
    screen.blit(clearicon,clearRect)
    
    screen.blit(undoicon,undoRect)
    screen.blit(redoicon,redoRect)
    screen.blit(saveicon,saveRect)
    screen.blit(loadicon,loadRect)


    #color palette picker
    screen.blit(colorpicker,colorpickerRect)        #blit color palette so crosshair can update 
    if colorpickerRect.collidepoint(mx,my):
        #crosshair
        screen.set_clip(colorpickerRect)            #crosshair drawn only in the color palette region
        draw.line(screen,BLACK,(mx-1,my),(mx-8,my),1)
        draw.line(screen,BLACK,(mx+1,my),(mx+8,my),1)
        draw.line(screen,BLACK,(mx,my-1),(mx,my-8),1)
        draw.line(screen,BLACK,(mx,my+1),(mx,my+8),1)
        screen.set_clip(None)
    #using color palette picker    
    if colorpickerRect.collidepoint(ax,ay) and click:     #'click' so doesn't spam and add color to recent list many times
        grabCol = (screen.get_at((ax,ay)))                #get color of pixel at mouse location
        #update rgb vals
        r = grabCol[0]
        g = grabCol[1]
        b = grabCol[2]
        rInput = str(r)
        gInput = str(g)
        bInput = str(b)
        col = (r,g,b)
        recCol.append(col)                                #add to list of recent colors (it becomes current color)

    #current color indicator box    
    draw.rect(screen,col,(1324,355,254,20))
    draw.rect(screen,DBLUE,(1324,355,254,20),2)
    
    #recent colors
    #recent color rects (from left to right)
    recCol1 = Rect(1324,381,20,20)
    recCol2 = Rect(1363,381,20,20)
    recCol3 = Rect(1402,381,20,20)
    recCol4 = Rect(1441,381,20,20)
    recCol5 = Rect(1480,381,20,20)
    recCol6 = Rect(1519,381,20,20)
    recCol7 = Rect(1558,381,20,20)
    recColRects = [recCol1,recCol2,recCol3,recCol4,recCol5,recCol6,recCol7]     #list of recent color rectangles
    if len(recCol) > 8:                                  #update recent color list so only the last 7 colors and current color are stored
        del recCol[0]
    #drawing recent color rects
    for i in range(7):
        draw.rect(screen,recCol[6-i],recColRects[i])     #current color will always be at index 7 so last used colors are index 0~6
        #hover indication outlines
        if recColRects[i].collidepoint(mx,my):
            draw.rect(screen,WHITE,recColRects[i],2)
        else:
            draw.rect(screen,DBLUE,recColRects[i],2)
    #clicking on recent color selects that color
    for i in range(7):
        if recColRects[i].collidepoint(ax,ay) and click:
            #get color info for the color in the clicked square
            r = recCol[6-i][0]
            g = recCol[6-i][1]
            b = recCol[6-i][2]
            rInput = str(r)
            gInput = str(g)
            bInput = str(b)
            col = (r,g,b)
            del recCol[6-i]         #remove color from recent color boxes since it is now displayed in the current color box
            recCol.append(col)      #color added to end of recent color list (it becomes current color)


    #RGB input textboxes
    #R input
        #outer box
    rRect = Rect(1324,407,130,40)
    draw.rect(screen,LPINK,rRect)
    draw.rect(screen,DPINK,rRect,2)
        #"R" label
    redLabelPic = sFont.render("R:",True,DPINK)
    screen.blit(redLabelPic,(rRect[0]+12,rRect[1]+10))
        #input box
    rInputRect = Rect(1374,411,76,32)
    if rInputRect.collidepoint(ax,ay):      #input box is active
        draw.rect(screen,WHITE,rInputRect)
        if time() % 1 > 0.5:                #text cursor blinks every 0.5 seconds
            draw.rect(screen,DPINK,(rInputRect[0]+rInputPic.get_width()+5,rInputRect[1]+5,2,22))    #position text cursor at the end of text input image
    else:                                   #input box is inactive
        draw.rect(screen,DPINK,rInputRect,2)
    if rInputRect.collidepoint(mx,my):      #hover indication
        draw.rect(screen,WHITE,rInputRect,2)
        #blitting the input text
    rInputPic = sFont.render(rInput,True,DPINK)
    screen.blit(rInputPic,(rInputRect[0]+5,rInputRect[1]+5))
        #update the R value only when the user clicks off input box
    if rInputRect.collidepoint(ax,ay) == False and rInputRect.collidepoint(oax,oay):    #oax,oay is the last position where mouse was clicked
        if rInput == "":            #if the textbox is left blank, default to value of 0
            rInput = "0"
        r = int(rInput)
        col = (r,g,b)
        recCol.append(col)          #add to list of recent colors (it becomes current color)

    #G input
        #outer box
    gRect = Rect(1324,453,130,40)
    draw.rect(screen,LGREEN,gRect)
    draw.rect(screen,DGREEN,gRect,2)
        #"G" label
    greenLabelPic = sFont.render("G:",True,DGREEN)
    screen.blit(greenLabelPic,(gRect[0]+12,gRect[1]+10))
        #input box
    gInputRect = Rect(1374,457,76,32)
    if gInputRect.collidepoint(ax,ay):
        draw.rect(screen,WHITE,gInputRect)
        if time() % 1 > 0.5:
            draw.rect(screen,DGREEN,(gInputRect[0]+gInputPic.get_width()+5,gInputRect[1]+5,2,22))
    else:
        draw.rect(screen,DGREEN,gInputRect,2)
    if gInputRect.collidepoint(mx,my):
        draw.rect(screen,WHITE,gInputRect,2)
        #blitting the input text
    gInputPic = sFont.render(gInput,True,DGREEN)
    screen.blit(gInputPic,(gInputRect[0]+5,gInputRect[1]+5))
        #updating the G value
    if gInputRect.collidepoint(ax,ay) == False and gInputRect.collidepoint(oax,oay):
        if gInput == "":
            gInput = "0"
        g = int(gInput)
        col = (r,g,b)
        recCol.append(col)

    #B input
        #outer box
    bRect = Rect(1324,499,130,40)
    draw.rect(screen,LBLUE,bRect)
    draw.rect(screen,DBLUE,bRect,2)
        #"B" label
    blueLabelPic = sFont.render("B:",True,DBLUE)
    screen.blit(blueLabelPic,(bRect[0]+12,bRect[1]+10))
        #input box
    bInputRect = Rect(1374,503,76,32)
    if bInputRect.collidepoint(ax,ay):
        draw.rect(screen,WHITE,bInputRect)
        if time() % 1 > 0.5:
            draw.rect(screen,DBLUE,(bInputRect[0]+bInputPic.get_width()+5,bInputRect[1]+5,2,22))
    else:
        draw.rect(screen,DBLUE,bInputRect,2)
    if bInputRect.collidepoint(mx,my):
        draw.rect(screen,WHITE,bInputRect,2)
        #blitting the input text
    bInputPic = sFont.render(bInput,True,DBLUE)
    screen.blit(bInputPic,(bInputRect[0]+5,bInputRect[1]+5))
        #updating the B value
    if bInputRect.collidepoint(ax,ay) == False and bInputRect.collidepoint(oax,oay):
        if bInput == "":
            bInput = "0"
        b = int(bInput)
        col = (r,g,b)
        recCol.append(col)

    #thickness input texbox
        #outer box
    thickRect = Rect(1460,407,118,132)
    draw.rect(screen,LBEIGE,thickRect)
    draw.rect(screen,DBEIGE,thickRect,2)
        #"Thickness" label
    thickLabelPic = ssFont.render("Thickness",True,DBEIGE)
    screen.blit(thickLabelPic,(thickRect[0]+10,thickRect[1]+10))
        #info labels
    thickSubLabel1Pic = sssFont.render("(or adjust with",True,DBEIGE)
    screen.blit(thickSubLabel1Pic,(thickRect[0]+5,thickRect[1]+35))
    thickSubLabel2Pic = sssFont.render("scroll wheel)",True,DBEIGE)
    screen.blit(thickSubLabel2Pic,(thickRect[0]+5,thickRect[1]+50))
    thickSubLabel3Pic = sssFont.render("1-2000px",True,DBEIGE)
    screen.blit(thickSubLabel3Pic,(thickRect[0]+5,thickRect[1]+80))
        #input box
    thickInputRect = Rect(1464,503,110,32)
    if thickInputRect.collidepoint(ax,ay):      #input box is active
        draw.rect(screen,WHITE,thickInputRect)
        if time() % 1 > 0.5:                    #text cursor blinks every 0.5 seconds
            draw.rect(screen,DBEIGE,(thickInputRect[0]+thickInputPic.get_width()+5,thickInputRect[1]+5,2,22))
    else:                                       #input box is inactive
        draw.rect(screen,DBEIGE,thickInputRect,2)
    if thickInputRect.collidepoint(mx,my):      #hover indication
        draw.rect(screen,WHITE,thickInputRect,2)
        #blitting the input text
    thickInputPic = sFont.render(thickInput,True,DBEIGE)
    screen.blit(thickInputPic,(thickInputRect[0]+5,thickInputRect[1]+5))
        #update the thickness once the user clicks off input box
    if thickInputRect.collidepoint(ax,ay) == False and thickInputRect.collidepoint(oax,oay):
        if thickInput == "":        #if field is left empty, default to min thickness of 1
            thickInput = "1"
        thick = int(thickInput)
    


    #using tools
    screen.set_clip(canvasRect)                             #restrict all drawings to canvas rect
    screen.blit(screencopy,(canvasCornerX,canvasCornerY))   #always blit existing drawing onto canvas
    if mb[0] and canvasRect.collidepoint(ax,ay):
        
        #pencil
        if tool == "pencil":
            draw.line(screen,col,(omx,omy),(mx,my),1)
            screencopy = screen.subsurface(canvasRect).copy()   #copy what was just drawn so it can be blit back
            
        #brush, highlighter, inkbrush, eraser
        if tool == "brush" or tool == "highlighter" or tool == "inkbrush" or tool == "eraser":          #these tools draw intermittently when drawing fast that needs to be fixed by drawing consistently in between (mx,my) and (omx,omy)
            distx = mx-omx
            disty = my-omy
            steps = hypot(distx,disty)                          #minimum number of circles to draw in between current mouse pos and old mouse pos
            #for intermediary drawing
            for i in range(1,int(steps+1)):
                stepX = omx+(i*distx/steps)                     #x pos of intermediary shapes
                stepY = omy+(i*disty/steps)                     #y pos of intermediary shapes
                if tool == "brush":
                    draw.circle(screen,col,(stepX,stepY),max(1,thick//2))                           #radius fix - does not draw if thickness < 2
                if tool == "highlighter":
                    if mx > omx:                #when using highlighter and drawing left to right, there are artifacts caused by distx/steps < 1 and pixel locations round down if given float
                                                #stepX does not increment and gets rounded down, causing 'gaps'
                        stepX = ceil(stepX)     #fix by rounding stepX and stepY up always
                        stepY = ceil(stepY)                      
                    draw.rect(alphaSurf,col,(stepX-canvasCornerX,stepY-canvasCornerY-thick//2,1,thick))     #chisel tip
                if tool == "inkbrush":
                    draw.circle(screen,col,(stepX,stepY),max(1,thick//10,thick//2-steps//4))     #simulates ink - thicker when drawing slowly by relating thickness to steps
                if tool == "eraser":
                    draw.circle(screen,WHITE,(stepX,stepY),max(1,thick//2))                 
            #allow single clicking to draw for some tools above (handles drawing single click circles or if steps are 0 (no intermediary circles drawn))
            if tool=="brush":
                draw.circle(screen,col,(mx,my),max(1,thick//2))
            if tool == "highlighter":
                if click:                       #only draw on single click, don't draw incrementally when drawing line (causes darker intermittent lines in alpha)
                    draw.rect(alphaSurf,col,(mx-canvasCornerX,my-canvasCornerY-thick//2,1,thick))
                alphaSurf.set_alpha(30)                                 #after drawing in btwn with highlighter, change translucency of highlighter layer
                screen.blit(alphaSurf,(canvasCornerX,canvasCornerY))
                alphaSurf.fill(WHITE)                                   #reset layer to key color (transparent again)
            if tool == "inkbrush" and click:    #only draw on single click, don't draw incrementally when drawing line
                draw.circle(screen,col,(mx,my),max(1,thick//2))
            if tool=="eraser":
                draw.circle(screen,WHITE,(mx,my),max(1,thick//2))
            screencopy = screen.subsurface(canvasRect).copy()
            
        #pixel brush    
        if tool == "pixelbrush":
            draw.rect(screen,col,((mx//thick)*thick,(my//thick)*thick,thick,thick))
            screencopy = screen.subsurface(canvasRect).copy()
            
        #spraypaint    
        if tool == "spraypaint":
            for i in range(10):                                      #makes spray faster
                rx = randint(-thick//2,thick//2)
                ry = randint(-thick//2,thick//2)
                if hypot(rx,ry) <= thick//2:                        #restrain to circular region
                    draw.circle(screen,col,(mx+rx,my+ry),1)
                    screencopy = screen.subsurface(canvasRect).copy()
        #line        
        if tool == "line":
            draw.line(screen,col,(ax,ay),(mx,my),thick)

        #rectangle filled    
        if tool == "rectangleF":
            squareRect = Rect(ax,ay,mx-ax,my-ay)
            squareRect.normalize()                              #flips w or h of rect if side lengths are negative (allows drag in any direction)
            draw.rect(screen,col,squareRect)

        #rectangle unfilled    
        if tool == "rectangleUF":
            squareRect = Rect(ax,ay,mx-ax,my-ay)
            squareRect.normalize()
            draw.rect(screen,col,squareRect,thick)

        #circle filled
        if tool == "circleF":
            circleRect = Rect(ax,ay,mx-ax,my-ay)
            circleRect.normalize()
            draw.ellipse(screen,col,circleRect)
            
        #circle unfilled
        if tool == "circleUF":
            circleRect = Rect(ax,ay,mx-ax,my-ay)
            circleRect.normalize()
            draw.ellipse(screen,col,circleRect,thick)
            

    #polygon
    if tool == "polygon":
        if keys[K_ESCAPE]:                                              #escape to restart polygon
            screen.blit(screencopy,(canvasCornerX,canvasCornerY))       #blit the image before polygon preview was drawn to remove the preview points, reset all flags back to original state
            polygonList.clear()
            polygonClosed = False
        if canvasRect.collidepoint(ax,ay):
            if click:                                                       #each click adds new point to polygon
                polygonList.append((ax,ay))
                startPoint = Rect(polygonList[0][0]-10,polygonList[0][1]-10,20,20)      #first point of the polygon is important so we know when to close the shape
            if len(polygonList) > 1 and startPoint.collidepoint(ax,ay) and click:       #if user clicks back on the first point, close and draw polygon permanently with right colors
                polygonList[-1] = polygonList[0]                                        #last point of polygon is exactly the same as first point
                screen.blit(screencopy,(canvasCornerX,canvasCornerY))                   #blit image before polygon preview was drawn to remove the preview points
                draw.polygon(screen,col,(polygonList),thick)
                screencopy = screen.subsurface(canvasRect).copy()                       #this polygon is now part of the drawing
                undoList.append(screencopy)
                polygonClosed = True
                #if drawing polygon after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
                if usedUndo == True:
                    redoList.clear()
                    usedUndo = False
            if polygonClosed:                                               #when user is done drawing polygon, reset everything so new polygon can be drawn
                polygonClosed = False
                polygonList.clear()
        #draw preview points
        for i in range(len(polygonList)):
            if i > 0:
                draw.line(screen,BLACK,polygonList[i],polygonList[i-1],thick)   #joint points with lines
        for i in range(len(polygonList)):
            draw.circle(screen,WHITE,polygonList[i],10)
            draw.circle(screen,RED,polygonList[i],10,3)


    #text
    #catch when user is actively using text tool
    if tool == "text":
        if canvasRect.collidepoint(ax,ay) and click and writingText == False:  #clicking on canvas with text tool to begin typing 
            writingText = True
        elif click:                           #user finished typing, click again anywhere to get off current text box
            writingText = False
    #text tool behaviour
        if keys[K_ESCAPE]:                  #escape to cancel current text
            writingText = False
            textInput = ""
        if writingText and canvasRect.collidepoint(ax,ay):               #actively writing text
            textInputPic = varFont.render(textInput,True,col)
            textInputRect = Rect(ax,ay,textInputPic.get_width()+15,textInputPic.get_height())
            draw.rect(screen,BLACK,textInputRect,1)                                         #text bounding box
            screen.blit(textInputPic,(textInputRect[0],textInputRect[1]))
            if time() % 1 > 0.5:                                                            #text cursor blinks every 0.5 seconds
                draw.rect(screen,BLACK,(textInputRect[0]+textInputPic.get_width(),textInputRect[1],2,thick*0.9))
        if writingText == False and textInput != "":                     #finished typing text, blit onto canvas permanently
            screen.blit(textInputPic,(oax,oay))                                             #blit text at location of the last click (bc user clicks off to permanently set text)
            screencopy = screen.subsurface(canvasRect).copy()
            undoList.append(screencopy)
            textInput = ""                                      #clear textInput so user can start again when typing more text
            #if setting more text after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
            if usedUndo == True:
                redoList.clear()
                usedUndo = False



    #select        
    if tool == "select":
        #no current selection, begin drawing selection box when user clicks on canvas:
        if canvasRect.collidepoint(ax,ay) and drawSelectBox == False:
            drawSelectBox = True
        #if selection has been made, user can cancel selection by single clicking on the canvas outside the selection; revert flags back to default state of False so new selection can be made
        if selectionMade:
            if drawSelectBox == True and selectionRect.collidepoint(ax,ay) == False and canvasRect.collidepoint(ax,ay) and release and ax == bx and ay == by:
                drawSelectBox = False
                selectionMade = False
                readyToMove = False
                firstMoveDone == False
                copied = False
        #user can also cancel selection with esc
        if keys[K_ESCAPE]:
            drawSelectBox = False
            selectionMade = False
            readyToMove = False
            firstMoveDone = False
            copied = False
        #if the user is dragging on the canvas and readyToMove is false, that means they are still drawing the selection area
        #determine properties of the selection area they are making
        if mb[0] and canvasRect.collidepoint(ax,ay) and readyToMove == False:
            selectX = abs(mx-ax)        #width of selection
            selectY = abs(my-ay)        #height of selection
            #selection is valid if it has a non-zero area and does not go off the canvas
            #any selection area that goes off the canvas causes subsurface blit issues later
            if selectX > 0 and selectY > 0 and mx > canvasCornerX and mx < canvasCornerX+canvasWidth and my > canvasCornerY and my < canvasCornerY+canvasHeight:
                selectionRect = Rect(ax,ay,mx-ax,my-ay)         #selection area
                selectionRect.normalize()
                selectionPic = screen.subsurface(selectionRect).copy()      #copy selected area as an image
                selectionMade = True                                        #selection has been made (i.e. the selection rect and pic have been made)
            else:                                               #otherwise, selection is invalid so reset flags
                drawSelectBox = False
                selectionMade = False
                readyToMove = False
                firstMoveDone = False
                copied = False
        if selectionMade:
            if release:
                readyToMove = True                              #as the user releases mouse after drawing the selection area, the selection is now ready to be manipulated
            if drawSelectBox and keys[K_LCTRL] == False:        #only draw the selection box if ctrl key isnt being pressed (if ctrl is being pressed, the select box must be hidden so user can ctrl+c/v to copy/paste without the selection box being copied in the drawing)
                draw.rect(screen,BLACK,selectionRect,1)
        if readyToMove:
            if selectionRect.collidepoint(ax,ay):               #if user clicks in the selection area, they are intending to drag and move it
                if click:                                       #get click location distance from the left and top edge of selection area
                    grabDistX = ax-selectionRect[0]
                    grabDistY = ay-selectionRect[1]
                #actually in the process of dragging and moving 
                if mb[0]:
                    if firstMoveDone == False:                  #if the selection is being moved for the first time, what should be left behind in the selected area is the canvas (white)
                        draw.rect(screen,WHITE,selectionRect)
                        behindcopy = screen.subsurface(canvasRect).copy()   #copy the canvas below (including the white square)(selected area is drawn after a few lines below so that isn't copied)
                    if firstMoveDone == True:                   #if the selection is being moved multiple times in a row, subsequent moves should not alter the drawing underneath (use the behindcopy pic)
                        screen.blit(behindcopy.subsurface(selectionRect[0]-canvasCornerX,selectionRect[1]-canvasCornerY,selectionRect[2],selectionRect[3]),(selectionRect[0],selectionRect[1])) #blit behindcopy in right place
                    screen.blit(selectionPic,(mx-grabDistX,my-grabDistY))       #translate the selection
                    draw.rect(screen,BLACK,(mx-grabDistX,my-grabDistY,selectionPic.get_width(),selectionPic.get_height()),1)    #translate the visual selection box
                    moving = True

        #permanently drawing on canvas
        if moving == True and release and ax != ay and ay != by:
            #if selection was dragged a non-zero distance
            if firstMoveDone == False:
                draw.rect(screen,WHITE,selectionRect)
                behindcopy = screen.subsurface(canvasRect).copy()
            if firstMoveDone == True:
                screen.blit(behindcopy.subsurface(selectionRect[0]-canvasCornerX,selectionRect[1]-canvasCornerY,selectionRect[2],selectionRect[3]),(selectionRect[0],selectionRect[1]))
            screen.blit(selectionPic,(bx-grabDistX,by-grabDistY))       #drawn the moved selection
            selectionRect = Rect(bx-grabDistX,by-grabDistY,selectionPic.get_width(),selectionPic.get_height())  #redefine the selection area at the new placement (allows subsequent translations from the new position)
            screencopy = screen.subsurface(canvasRect).copy()   #make it a permanent part of the image
            undoList.append(screencopy)
            moving = False              #no longer actively moving
            firstMoveDone = True
            #if new placement of the selection box and translated selection is partially/totally off the canvas, do not allow subsequent translations
            #additonal moves causes issues with subsurface blit
            #reset all flags (await next NEW selection)
            if selectionRect[0] < canvasCornerX or selectionRect[0]+selectionRect[2] > canvasCornerX+canvasWidth or selectionRect[1] < canvasCornerY or selectionRect[1]+selectionRect[3] > canvasCornerY+canvasHeight:
                drawSelectBox = False
                selectionMade = False
                readyToMove = False
                firstMoveDone = False
                copied = False
            #if moving after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
            if usedUndo == True:
                redoList.clear()
                usedUndo = False

        #copying and pasting
        if selectionMade:
            if keys[K_LCTRL] and c:
                copypastePic = screen.subsurface(selectionRect).copy()  #copy currently selected area
                copied = True
            if keys[K_LCTRL] and v and copied:  #only allow paste if user already did ctrl+c
                behindcopy = screen.subsurface(canvasRect).copy()   #copy the drawing below to keep drawing intact when moving pasted selection (doesn't reveal the white canvas below)
                screen.blit(copypastePic,(mx-copypastePic.get_width()/2,my-copypastePic.get_height()/2))            #paste in middle of mouse position
                selectionRect = Rect(mx-copypastePic.get_width()/2,my-copypastePic.get_height()/2,copypastePic.get_width(),copypastePic.get_height())   #set selection area to new pasted region (so user may manipulate what they just pasted)
                screencopy = screen.subsurface(canvasRect).copy()   #keep it visible upon paste
                undoList.append(screencopy)
                firstMoveDone = True
                #if pasting after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
                if usedUndo == True:
                    redoList.clear()
                    usedUndo = False

        #delete selection with delete key
        if keys[K_DELETE] and selectionMade:
            #if selection was just made, deleting it should expose the white canvas underneath
            if firstMoveDone == False:
                draw.rect(screen,WHITE,selectionRect)
            #deleting a selection that has been moved deletes the selection but keeps what was underneath intact 
            if firstMoveDone == True:
                screen.blit(behindcopy,canvasRect)
            screencopy = screen.subsurface(canvasRect).copy()   #make it a permanent part of the image
            undoList.append(screencopy)
            #if deleting after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
            if usedUndo == True:
                redoList.clear()
                usedUndo = False
            #reset all flags for select tool - ready for new selection
            drawSelectBox = False
            selectionMade = False
            readyToMove = False
            firstMoveDone = False
            copied = False

            

    #eyedropper
    if tool == "eyedropper" and canvasRect.collidepoint(mx,my):
        #eyedropper crosshair
        draw.line(screen,BLACK,(mx,my-2),(mx,my-10),3)
        draw.line(screen,WHITE,(mx,my-3),(mx,my-9),1)
        draw.line(screen,BLACK,(mx,my+2),(mx,my+10),3)
        draw.line(screen,WHITE,(mx,my+3),(mx,my+9),1)
        draw.line(screen,BLACK,(mx-2,my),(mx-10,my),3)
        draw.line(screen,WHITE,(mx-3,my),(mx-9,my),1)
        draw.line(screen,BLACK,(mx+2,my),(mx+10,my),3)
        draw.line(screen,WHITE,(mx+3,my),(mx+9,my),1)
        if mb[0] and click:
            grabCol = screen.get_at((mx,my))            #get color of pixel at mouse location
            #update rgb vals
            r = grabCol[0]
            g = grabCol[1]
            b = grabCol[2]
            rInput = str(r)
            gInput = str(g)
            bInput = str(b)
            col = (r,g,b)
            recCol.append(col)                          #add to list of recent colors

    #flood fill
    #logic: get color of target pixel and check surrounding pixels if they are the same color then fill with fill color and continue checking surrounding pixels until different color is met (indicates a border)
    if tool == "fill" and canvasRect.collidepoint(ax,ay):
        if click:
            targetX = ax
            targetY = ay
            pixels = [(targetX,targetY)]                #add the clicked on pixel (target) to list
            oldCol = screen.get_at((targetX,targetY))   #old color to replace with fill color
            if oldCol != col:                           #only fill area if fill color is different than target pixel color
                while len(pixels) > 0:
                    #check the last pixel in list and fill if needed
                    targetX,targetY = pixels.pop()
                    if screen.get_at((targetX,targetY)) == oldCol:
                        screen.set_at((targetX,targetY),col)
                        #if the pixel was filled, add the pixels to the left, right, above, and below to the list to check them
                        pixels.append((targetX+1,targetY))
                        pixels.append((targetX-1,targetY))
                        pixels.append((targetX,targetY+1))
                        pixels.append((targetX,targetY-1))
                screencopy = screen.subsurface(canvasRect).copy()
                undoList.append(screencopy)
                #if filling after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
                if usedUndo == True:
                    redoList.clear()
                    usedUndo = False
                
    #flip horizontal
    if tool == "flipH" and flipHRect.collidepoint(ax,ay) and click:
        screencopy = transform.flip(screen.subsurface(canvasRect).copy(),True,False)
        undoList.append(screencopy)
        #if flipping after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
        if usedUndo == True:
            redoList.clear()
            usedUndo = False

    #flip vertical
    if tool == "flipV" and flipVRect.collidepoint(ax,ay) and click:
        screencopy = transform.flip(screen.subsurface(canvasRect).copy(),False,True)
        undoList.append(screencopy)
        #if flipping after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
        if usedUndo == True:
            redoList.clear()
            usedUndo = False

    #clear
    if tool == "clear" and clearRect.collidepoint(ax,ay) and click:
        confirmClear = messagebox.askyesno(title = "Springtime Sketch", message = "Are you sure you want to clear the canvas?\nSpring is the perfect time for a fresh start!")
        if confirmClear:
            screen.fill(WHITE)
            screencopy = screen.subsurface(canvasRect).copy()
            undoList.append(screencopy)
            #if clearing after undo was used, clear the redo list (similar to how drawing with brush after undo clears redo list)
            if usedUndo == True:
                redoList.clear()
                usedUndo = False

    #using stamps
    if tool == "stamps" and canvasRect.collidepoint(ax,ay) and mb[0]:
        screen.blit(stampsList[currentStampInd],(mx-stampsList[currentStampInd].get_width()/2,my-stampsList[currentStampInd].get_height()/2))


    #these tools are not activated using 'tool' var and run each action once per click        
    #undo
    if (undoRect.collidepoint(ax,ay) and click) or (keys[K_LCTRL] and z):                                   #ctrl is allowed to constantly be True when held down
        if len(undoList) > 1:                               #only allow undo if something is drawn
            transCopy = undoList.pop()                      #move last item to transfer to redoList
            redoList.append(transCopy)
            screencopy = undoList[-1]                       #go back to previous copied canvas
            usedUndo = True

            #using undo with select tool should deselect any selected regions when undo is used (since the image is changing now and select area may no longe be where the user wants it)
            drawSelectBox = False
            selectionMade = False
            readyToMove = False
            firstMoveDone == False
            copied = False

    #redo
    if (redoRect.collidepoint(ax,ay) and click) or (keys[K_LCTRL] and y):
        if len(redoList) > 0:
            transCopy = redoList.pop()
            undoList.append(transCopy)
            screencopy = undoList[-1]

    #save
    if openSaveDialog:
        saveName = filedialog.asksaveasfilename(title = "Save Drawing", filetypes = (("PNG Files", "*.png"), ("JPEG Files", "*.jpg *.jpeg"), ("Bitmap Files", "*.bmp")), defaultextension = ".png") #save path with save name
        if saveName != "":          #avoid crashing if user cancels operation
            image.save(screen.subsurface(canvasRect).copy(),saveName)
            messagebox.showinfo(title = "Springtime Sketch", message = "Your drawing was saved successfully!\nLook at all those beautiful colors...")

    #load
    if openLoadDialog:
        fileName = filedialog.askopenfilename(title = "Load Image", filetypes = (("PNG Files", "*.png"), ("JPEG Files", "*.jpg *.jpeg"), ("Bitmap Files", "*.bmp"))) #path of file to open
        if fileName != "":      #check if user canceled load
            loadedPic = image.load(fileName)
            picX,picY = loadedPic.get_width(),loadedPic.get_height()      #get dimensions of loaded image
            aspectRatio = picX/picY                                         #calc aspect ratio x/y for scaling purposes
            if picX > 1140:                                                 #scale image down if width larger than canvas
                picX,picY = 1140,1140/aspectRatio 
                loadedPic = transform.scale(loadedPic,(picX,picY))
            if picY > 790:                                                  #scale image down if height larger than canvas
                picX,picY = 790*aspectRatio,790
                loadedPic = transform.scale(loadedPic,(picX,picY))
            screen.blit(loadedPic,(canvasCornerX,canvasCornerY))
            screencopy = screen.subsurface(canvasRect).copy()
            undoList.append(screencopy)


    #brush custom cursors (they preview width and brush shape)
    #only show cursors when left click is not down so it does not interfere with screencopying while drawing
    #cursor previews thickness, looks best above 6px
    if (mb[0] == False and canvasRect.collidepoint(mx,my) and thick >= 6 and (tool == "pencil" or tool == "brush" or tool == "inkbrush" or tool == "spraypaint" or tool == "eraser" or tool == "highlighter" or tool == "pixelbrush" or tool == "eyedropper")) or colorpickerRect.collidepoint(mx,my):
        if tool == "pencil":                                                                                                #pencil cursor has a crosshair 1px
            draw.line(cursorSurf,BLACK,(mx-1-canvasCornerX,my-canvasCornerY),(mx-8-canvasCornerX,my-canvasCornerY),1)
            draw.line(cursorSurf,BLACK,(mx+1-canvasCornerX,my-canvasCornerY),(mx+8-canvasCornerX,my-canvasCornerY),1)
            draw.line(cursorSurf,BLACK,(mx-canvasCornerX,my-1-canvasCornerY),(mx-canvasCornerX,my-8-canvasCornerY),1)
            draw.line(cursorSurf,BLACK,(mx-canvasCornerX,my+1-canvasCornerY),(mx-canvasCornerX,my+8-canvasCornerY),1)
        if tool == "brush" or tool == "inkbrush" or tool == "spraypaint" or tool == "eraser":                               #round brushes have a circle cursor
            draw.circle(cursorSurf,BLACK,(mx-canvasCornerX,my-canvasCornerY),thick//2,1)
        if tool == "highlighter":                                                                                           #highlighter has a chisel cursor
            draw.rect(cursorSurf,BLACK,(mx-1-canvasCornerX,my-thick//2-canvasCornerY,3,thick),1)
        if tool == "pixelbrush":                                                                                            #pixel has a square cursor
            draw.rect(cursorSurf,BLACK,(mx-thick//2-canvasCornerX,my-thick//2-canvasCornerY,thick,thick),1)
        screen.blit(cursorSurf,(canvasCornerX,canvasCornerY))       #blit the cursor surface
        cursorSurf.fill(WHITE)                                      #reset cursor surface by making it transparent (so the cursor can "move")
        mouse.set_visible(False)
    elif mb[0] == False and canvasRect.collidepoint(mx,my) and tool == "stamps":        #for using stamps draw translucent preview of stamp
        stampPreviewSurf = Surface((stampsList[currentStampInd].get_width(),stampsList[currentStampInd].get_height()))      #surface to show translucent stamp preview on
        stampPreviewSurf.fill((200,200,200))                                    #since stamp image has per pixel transparency, to make it so the entire stamp shows up with some opacity, must fill the transparent background with color otherwise there is an ugly black square
        stampPreviewSurf.blit(stampsList[currentStampInd],(0,0))
        stampPreviewSurf.set_colorkey((200,200,200))                            #make the background transparent
        stampPreviewSurf.set_alpha(50)                                          #set opacity
        screen.blit(stampPreviewSurf,(mx-stampsList[currentStampInd].get_width()/2,my-stampsList[currentStampInd].get_height()/2))    
    else:                                           #mouse cursor should return if custom cursor not in use or tool doesn't have a custom cursor                         
        mouse.set_visible(True)

    screen.set_clip(None)       #stop canvas restriction


    #choosing stamps UI
    if stampPreviewRect.collidepoint(ax,ay) and mb[0]:      #if click on stamp preview, change tool to stamp tool
        tool = "stamps"
    #"Stamps" title
    stampsTRect = Rect(1324,579,254,40)
    draw.rect(screen,LBLUE,stampsTRect)
    draw.rect(screen,DBLUE,stampsTRect,2)
    stampsTPic = sFont.render("Stamps",True,DBLUE)
    stampNumPic = sFont.render("%d/20" % (currentStampInd+1),True,DBLUE)    #display stamp number
    screen.blit(stampsTPic,(stampsTRect[0]+10,stampsTRect[1]+10))
    screen.blit(stampNumPic,(1578-stampNumPic.get_width()-10,stampsTRect[1]+10))
    #left arrow
    draw.polygon(screen,LBLUE,[(1324,714),(1354,694),(1354,734)])
    draw.polygon(screen,DBLUE,[(1324,714),(1354,694),(1354,734)],2)
    #right arrow
    draw.polygon(screen,LBLUE,[(1578,714),(1548,694),(1548,734)])
    draw.polygon(screen,DBLUE,[(1578,714),(1548,694),(1548,734)],2)
    #stamp quick selection buttons
    for i in range(len(stampSelectRects)):
        #clicking on a rectangle switches to corresponsing stamp
        if click and stampSelectRects[i].collidepoint(ax,ay):
            currentStampInd = i
        else:
            draw.rect(screen,LBLUE,stampSelectRects[i])
            #hover indication
            if stampSelectRects[i].collidepoint(mx,my):
                draw.rect(screen,WHITE,stampSelectRects[i],2)
            else:
                draw.rect(screen,DBLUE,stampSelectRects[i],2)
        #selected button indicator
        if currentStampInd == i:
            draw.rect(screen,WHITE,stampSelectRects[i])
            draw.rect(screen,DBLUE,stampSelectRects[i],2)
    #arrow hover and click indication
    if leftArrowRect.collidepoint(mx,my):
        draw.polygon(screen,WHITE,[(1324,714),(1354,694),(1354,734)],2)
        if leftArrowRect.collidepoint(ax,ay) and mb[0]:
            draw.polygon(screen,WHITE,[(1324,714),(1354,694),(1354,734)])
            draw.polygon(screen,DBLUE,[(1324,714),(1354,694),(1354,734)],2)
        #go to last stamp when clicking on left arrow
        if click:
            if currentStampInd == 0:
                currentStampInd = 19
            else:
                currentStampInd -= 1
    if rightArrowRect.collidepoint(mx,my):
        draw.polygon(screen,WHITE,[(1578,714),(1548,694),(1548,734)],2)
        if rightArrowRect.collidepoint(ax,ay) and mb[0]:
            draw.polygon(screen,WHITE,[(1578,714),(1548,694),(1548,734)])
            draw.polygon(screen,DBLUE,[(1578,714),(1548,694),(1548,734)],2)
        #go to next stamp when clicking on right arrow
        if click:
            if currentStampInd == 19:
                currentStampInd = 0
            else:
                currentStampInd += 1
    screen.blit(backgroundimg.subsurface(stampPreviewRect[0]-4,stampPreviewRect[1]-4,stampPreviewRect[2]+8,stampPreviewRect[3]+8),(stampPreviewRect[0]-4,stampPreviewRect[1]-4))    #blit background image in stamp preview region so stamps don't overlap
    screen.blit(stampsList[currentStampInd],stampPreviewRect)
    #draw box outline around stamp preview to show hover and if stamp tool is selected
    if tool == "stamps":
        draw.rect(screen,DBLUE,(stampPreviewRect[0]-4,stampPreviewRect[1]-4,stampPreviewRect[2]+8,stampPreviewRect[3]+8),2)
    if stampPreviewRect.collidepoint(mx,my):
        draw.rect(screen,WHITE,(stampPreviewRect[0]-4,stampPreviewRect[1]-4,stampPreviewRect[2]+8,stampPreviewRect[3]+8),2)

  
    omx,omy = mx,my             #store previous mouse position (1 step behind)
    oax,oay = ax,ay             #store position of previous (old) click down
    display.flip()

quit()

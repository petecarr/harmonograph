# Harmonograph
# Two coupled, damped pendulums.
# x = exp(-pt)*(b1*sin(w1*t) + c1*cos(w1*t)) + 
#     exp(-qt)*(b2*sin(w2*t) + c2*cos(w2*t))
# 

# Slider controlled values for ai and bi.
# Slider is in slider.py
# Cycle through colors each time we come back to initial condition

import os, random, pygame; from pygame.locals import *
import sys
from math import sin, cos, pi, exp

import slider
from slider import Slider
Scale = slider.Slider

# Abbreviations for commands
pdl=pygame.draw.line 

#Constants
WINDOWWIDTH = 1100
WINDOWHEIGHT = 900

FPS = 100

BLACK = (0,0,0)
BLUEGREEN = (0,64,64)
BRIGHTBLUE = (0,50,255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255,255,0)
ORANGE = (255, 84,0)
GREEN = (0,255,0)
CYAN = (0,255,255)
BLUE = (0,0,255)
MAGENTA = (255, 0, 255)


BUTTONCOLOR = BLACK      #WHITE
BUTTONTEXTCOLOR = WHITE  #BLACK
MESSAGECOLOR = WHITE
TEXTCOLOR = WHITE
BGCOLOR = BLACK          #BLUEGREEN
LINECOLOR = [RED, ORANGE,YELLOW, GREEN, CYAN, BLUE, MAGENTA]
LCMAX = 6

BASICFONTSIZE = 20
SCALEFONTSIZE = 12

SCALELENGTH = 500
SCALETHICKNESS = 20
BORDERCOLOR = WHITE
BORDERWIDTH = 1

INITA = 4
INITB = 5

TITLE = 'Harmonograph: x = exp(-pt)*(B*sin(wt) +C*cos(wt)) + another damped pendulum.'

global cindx, CINDX_MAX, A1, A2, B1, B2, C1, C2, D1, D2, E1, E2, F1, F2
CINDX_MAX = 11
cindx = 0

A1=0; B1=1; C1=2; D1=3; E1=4; F1=5; A2=6; B2=7; C2=8; D2=9; E2=10; F2=11
cfs = [
    # A1    B1   C1    D1    E1   F1   A2    B2    C2    D2    E2    F2
    
    # no decay
    [0.0,  1.5, 1.5, 3.5,  1.5,  2.8, 0.0,  1.55, 1.55, 2.55, 1.55,-2.864],
    #with decay
    [1.0,  1.5, 1.5, -1.5,  1.5, 2.8, 0.1,  1.55, 1.55, 1.55, 1.55,-2.864],
    [0.3,  1.5, 1.5, -1.5,  1.5, 2.8, 0.1,  1.55, 1.55, 1.55, 1.55, 2.864],
    #spirographs
    [1.0,  3.0, 0.0,  0.0,  3.0, 0.2, 1.0,  0.0,  0.3, -0.3,  0.0,  5.0],
    [1.0,  2.0, 2.0,  2.0, -2.0, 0.5, 3.0, -1.0,  1.0, -1.0, -1.0,  5.0],
    #2 lobes
    [0.25, 4.0, 0.0,  0.0,  0.0, 1.0, 2.0,  0.0,  0.0,  4.0,  0.0,  2.03],
    [0.25, 4.0, 0.0,  0.0,  0.0, 1.0, 2.0,  0.0,  0.0,  4.0,  0.0,  2.0],
    # oddities
    [1.0, -1.0,-1.0,  1.0,  1.0, 2.0, 2.0, -2.0,  2.0,  2.0,  2.0,  1.0],
    # should be 4 lobes
    [1.0,  2.0, 2.0, -2.0, -2.0, 1.0, 0.3, -0.65, 0.65, 0.65, 0.65, 3.01],
    # 3 lobes
    [1.0,  1.0, 1.0, -1.0,  1.0, 2.0, 2.0, -2.0,  2.0,  2.0,  2.0,  1.0],
    # 5 lobes
    [0.4,  1.4, 1.4, -1.4,  1.4, 2.0, 1.0, -1.5,  1.5,  1.5,  1.5,  3.0],
    # 7 lobes
    [1.0,  1.0, 1.0, -1.0,  1.0, 2.0, 2.0, -2.0,  2.0,  2.0,  2.0,  1.5],
    [0.1,  1.0, 1.0, -1.0,  1.0, 2.0, 2.0, -2.0,  2.0,  2.0,  2.0,  1.5],
    # cardoid
    [1.0, -1.0, 1.0,  1.0,  1.0, 2.0, 2.0, -2.0,  2.0,  2.0,  2.0,  1.0] 

    ]
"""   
A1 = ( 1.0,  0.3,  0.4,  1.0,  1.0,  0.25,  1.0,  0.25, 1.0,  1.0,  1.0)
B1 = (-1.0,  1.5,  1.4,  3.0,  2.0,  4.0,   2.0,  4.0, -1.0,  1.0,  1.0)
C1 = ( 1.0,  1.5,  1.4,  0.0,  2.0,  0.0,   2.0,  0.0, -1.0,  1.0,  1.0)
D1 = ( 1.0, -1.5, -1.4,  0.0, -2.0,  0.0,   2.0,  0.0,  1.0, -1.0, -1.0)
E1 = ( 1.0,  1.5,  1.4,  3.0, -2.0,  0.0,  -2.0,  0.0,  1.0,  1.0,  1.0)
F1 = ( 2.0,  2.8,  2.0,  0.2,  1.0,  1.0,   0.5,  1.0,  2.0,  2.0,  2.0)

A2 = ( 2.0,  0.1,  1.0,  1.0,  0.3,  2.0,   3.0,  2.0,  2.0,  2.0,  2.0)
B2 = (-2.0,  1.55,-1.5,  0.0, -0.65, 0.0,  -1.0,  0.0, -2.0, -2.0, -2.0)
C2 = ( 2.0,  1.55, 1.5,  0.3,  0.65, 0.0,   1.0,  0.0,  2.0,  2.0,  2.0)
D2 = ( 2.0,  1.55, 1.5, -0.3,  0.65, 4.0,  -1.0,  4.0,  2.0,  2.0,  2.0)
E2 = ( 2.0,  1.55, 1.5,  0.0,  0.65, 0.0,  -1.0,  0.0,  2.0,  2.0,  2.0)
F2 = ( 1.0,  2.864,3.0,  5.0,  3.01, 2.03,  5.0,  2.0,  1.0,  1.0,  1.5) 
"""

cx=WINDOWWIDTH/2; cy=WINDOWHEIGHT/2 # Centre of the screen

def harmonograph(t):
    coeffs = cfs[cindx]
    a1 = coeffs[A1]; b1 = coeffs[B1]; c1 = coeffs[C1]
    d1 = coeffs[D1]; e1 = coeffs[E1]; f1 = coeffs[F1]
    a2 = coeffs[A2]; b2 = coeffs[B2]; c2 = coeffs[C2]
    d2 = coeffs[D2]; e2 = coeffs[E2]; f2 = coeffs[F2] 
    
    r1 = 100.0*exp(-a1*0.01*t)
    r2 = 100.0*exp(-a2*0.01*t)
    s1 = r1*sin(f1*t)
    s2 = r2*sin(f2*t)
    t1 = r1*cos(f1*t)
    t2 = r2*cos(f2*t)
    x = cx + b1*s1 + b2*s2 + c1*t1 + c2*t2
    y = cy + d1*s1 + d2*s2 + e1*t1 + e2*t2
    return (x,y)

def makeText(font, text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
        
def checkForPrint():
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_PRINT: 
            pygame.image.save(screen, "Pictures/harmonograph%d.png"%cindx)
        else:
            pygame.event.post(event) # put the other KEYUP event objects back  
        
       
def nextPlot():
    global t, initx, inity, lastx, lasty , start_display , full_cycle, cindx
    cindx = cindx + 1
    if cindx > CINDX_MAX: cindx = 0
         
    t = 0.0
    lastx, lasty = harmonograph(t)
    initx = lastx; inity = lasty
    #full_cycle = 0 
    full_cycle = full_cycle + 1
    if full_cycle > LCMAX: full_cycle = 0                 
    start_display = True
    bk.fill((BGCOLOR)) 
    
#-------------------------------------------------------------------

global screen, BASICFONT, Start_Surf, Start_Rect, Restart_Surf, Restart_Rec
global Quit_Surf, Quit_Rect
global t, initx, inity, lastx, lasty



pygame.init()

clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
pygame.display.set_caption(TITLE)
screen=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
SCALEFONT = pygame.font.SysFont("Ariel", size = 20, bold=False, italic=False)

bk=pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT)); bk.fill((BGCOLOR))
dot=pygame.Surface((4,4)); dot.set_colorkey([0,0,0])
pygame.draw.circle(dot,WHITE,(2,2),2,0)

# Buttons and messages
Start_Surf, Start_Rect = makeText(BASICFONT, 'Start', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
Restart_Surf, Restart_Rect = makeText(BASICFONT, 'Restart', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
Next_Surf, Next_Rect = makeText(BASICFONT, 'Next', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
Quit_Surf,   Quit_Rect   = makeText(BASICFONT, 'Quit', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 60)


# Initial Screen  
screen.blit(bk,(0,0)) # Draw the background surface
screen.blit(Start_Surf, Start_Rect)
screen.blit(Quit_Surf, Quit_Rect)

pygame.display.update()

t = 0.0
color_changed = False
done = False
start_display = False
while not done:
    checkForQuit()
    checkForPrint()

    for event in pygame.event.get(): # User did something
        if event.type == MOUSEBUTTONUP:
            # check if the user clicked on an option button
            if Quit_Rect.collidepoint(event.pos):
                terminate()       
            elif Restart_Rect.collidepoint(event.pos):  # same as Start
                t = 0.0
                lastx, lasty = harmonograph(t)
                initx = lastx; inity = lasty
                full_cycle = 0            
                start_display = True
                bk.fill((BGCOLOR))
            elif Next_Rect.collidepoint(event.pos):
                nextPlot()

            
    if start_display:         # User selected Start Button     
        screen.blit(bk,(0,0)) # Draw the background surface
        screen.blit(Next_Surf, Next_Rect)
        screen.blit(Restart_Surf, Restart_Rect)
        screen.blit(Quit_Surf, Quit_Rect)
      
        x,y = harmonograph(t)
        if not color_changed:
            pdl(bk, LINECOLOR[full_cycle], (lastx, lasty), (x,y))
        else:
            color_changed = False
        t = t + 0.05
      
        lastx = x
        lasty = y
          
        #screen.blit(dot, (x,y))
        clock.tick(FPS)
        pygame.display.update()
      
        if t >= 150.0:
            event = pygame.event.wait()
            checkForPrint()
            t = 0.0
            bk.fill(BGCOLOR)
            full_cycle = full_cycle + 1
            if full_cycle > LCMAX: nextPlot()
            """
                full_cycle = 0
                cindx = cindx + 1
                if cindx >= CINDX_MAX: cindx = 0  
            """
            color_changed = True
      

pygame.quit()



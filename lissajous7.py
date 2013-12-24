# Lissajous figure
# x = 120 * sin (at)
# y = 120 * cos (bt)   -- or sin(bt + pi/2) - or sin(bt+delta)
#  
# Slider controlled values for ai and bi.
# Slider is in slider.py
# Cycle through colors each time we come back to initial condition

import os, random, pygame; from pygame.locals import *
import sys
from math import sin, cos, pi
import slider
from slider import Slider
Scale = slider.Slider

# Abbreviations for commands
pdl=pygame.draw.line 

#Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

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

TITLE = 'Lissajous Figure - slider controlled frequencies and delta.'

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
            pygame.image.save(screen, "lissajous7.png")
       else:
          pygame.event.post(event) # put the other KEYUP event objects back  

#-------------------------------------------------------------------

global screen, BASICFONT, Start_Surf, Start_Rect, Restart_Surf, Restart_Rec
global Quit_Surf, Quit_Rect



pygame.init()

clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
pygame.display.set_caption(TITLE)
screen=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
SCALEFONT = pygame.font.SysFont("Ariel", size = 20, bold=False, italic=False)
#SCALEFONT = pygame.font.Font('freesansbold.ttf', SCALEFONTSIZE)

bk=pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT)); bk.fill((BGCOLOR))
dot=pygame.Surface((4,4)); dot.set_colorkey([0,0,0])
pygame.draw.circle(dot,WHITE,(2,2),2,0)

# Buttons and messages
Start_Surf, Start_Rect = makeText(BASICFONT, 'Start', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
Restart_Surf, Restart_Rect = makeText(BASICFONT, 'Restart', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
Quit_Surf,   Quit_Rect   = makeText(BASICFONT, 'Quit', TEXTCOLOR, BGCOLOR, 
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
Message_Surf, Message_Rect = makeText(BASICFONT, TITLE, TEXTCOLOR, 
                                      BGCOLOR, 20, 20)
ascale_Surf, ascale_Rect = makeText(SCALEFONT, "ai=%d"%INITA, TEXTCOLOR, 
                                    BGCOLOR, 20, 10)
bscale_Surf, bscale_Rect = makeText(SCALEFONT, "bi=%d"%INITB, TEXTCOLOR, 
                                    BGCOLOR, 20, 120)
dscale_Surf, dscale_Rect = makeText(SCALEFONT, "d=%d"%180, TEXTCOLOR, 
                                    BGCOLOR, 20, 120)

ascale = Scale(screen, color = BLUE, horiz = True, init_value = INITA, 
                min_value = 1, max_value = 20,
                length = SCALELENGTH, thickness = SCALETHICKNESS,
                bordercolor = BORDERCOLOR, borderwidth = BORDERWIDTH) 
# for ascale slider label
YOFFSET = int(SCALETHICKNESS/2 + 5)

bscale = Scale(screen, color = BLUE, horiz = False, init_value = INITB, 
                min_value = 1, max_value = 20,
                length = SCALELENGTH, thickness = SCALETHICKNESS,
                bordercolor = BORDERCOLOR, borderwidth = BORDERWIDTH) 
# for bscale slider label
XOFFSET = int(SCALETHICKNESS/2 + 5)

dscale = Scale(screen, color = GREEN, horiz = False, init_value = 90, 
                min_value = 0, max_value = 360,
                length = SCALELENGTH, thickness = SCALETHICKNESS,
                bordercolor = BORDERCOLOR, borderwidth = BORDERWIDTH) 


 

bigradius = 240.0; points = 720 #360
angleStep = pi *2.0 / points
"""
# Variable Arrays To Store X&Y points for a small and big circle
smcx = []; smcy = []
# Calculate the X&Y points and put values into the array
for a in range(0,points):
   smcx.append(sin(a * angleStep)*bigradius)
   smcy.append(cos(a * angleStep)*bigradius)
   
   """
cx=WINDOWWIDTH/2; cy=WINDOWHEIGHT/2 # Centre of the screen

# Lissajous values to be controlled by a slider
ai, bi = INITA, INITB
delta = pi/2.0
delta_changed = False


# Initial Screen  
screen.blit(bk,(0,0)) # Draw the background surface
screen.blit(Message_Surf, Message_Rect)
screen.blit(Start_Surf, Start_Rect)
screen.blit(Quit_Surf, Quit_Rect)

pygame.display.update()

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
            ai = ascale.get_slider_value()
            bi = bscale.get_slider_value()
            vals = "ai = %d, bi = %d"% (ai, bi)
            Val_Surf, Val_Rect = makeText(BASICFONT, vals, TEXTCOLOR, BGCOLOR, 
                                          WINDOWWIDTH - 140, WINDOWHEIGHT - 150)
            di = dscale.get_slider_value()
            dels = "delta = %d"% (di)
            Del_Surf, Del_Rect = makeText(BASICFONT, dels, TEXTCOLOR, BGCOLOR, 
                                          WINDOWWIDTH - 140, WINDOWHEIGHT - 120)             
            bk.fill((BGCOLOR))

            a = 0; b = 0

            delta = (di*pi/180.0)
            delta_changed = True     
            #lastx = smcx[a]+cx; a = a + ai
            #lasty = smcy[b]+cy; b = b + bi            
            lastx = cx + sin(0.0)*bigradius; a = a + ai
            lasty = cy + sin(0.0 + delta)*bigradius; b = b + bi  
            
            initx = lastx; inity = lasty
            full_cycle = 0            
            start_display = True
            
      ascale.mouse_actions(event)
      bscale.mouse_actions(event)
      dscale.mouse_actions(event)
      
      # this could migrate into slider - at least show the value next to the 
      # circle
      aval = "ai = %d" % (ascale.get_slider_value())
      aloc = ascale.get_slider_screen_coords()
      xoffset = int(SCALEFONT.size(aval)[0]/2)
      yoffset = YOFFSET + SCALEFONT.size(aval)[1]

      ascale_Surf, ascale_Rect = makeText(SCALEFONT, aval, TEXTCOLOR, BGCOLOR, 
                                           aloc[0]-xoffset, aloc[1]-yoffset)            
      
      bval = "bi = %d" % (bscale.get_slider_value())
      bloc = bscale.get_slider_screen_coords()
      xoffset = XOFFSET + SCALEFONT.size(bval)[0]
      yoffset = int(SCALEFONT.size(bval)[1]/2-SCALETHICKNESS/2)
      
      bscale_Surf, bscale_Rect = makeText(SCALEFONT, bval, TEXTCOLOR, BGCOLOR, 
                                          bloc[0]-xoffset, bloc[1])      
            
      dval = "d = %d" % (dscale.get_slider_value())
      dloc = dscale.get_slider_screen_coords()
      xoffset = XOFFSET + SCALEFONT.size(dval)[0]
      yoffset = int(SCALEFONT.size(dval)[1]/2-SCALETHICKNESS/2)
            
      dscale_Surf, dscale_Rect = makeText(SCALEFONT, dval, TEXTCOLOR, BGCOLOR, 
                                                dloc[0]-xoffset, dloc[1])  
      
   if start_display:        # User selected Start Button     
      screen.blit(bk,(0,0)) # Draw the background surface
      ascale.draw_scale(150, 20)
      screen.blit(ascale_Surf, ascale_Rect)
      bscale.draw_scale(120, 50)
      screen.blit(bscale_Surf, bscale_Rect)
      dscale.draw_scale(55, 50)
      screen.blit(dscale_Surf, dscale_Rect)
      
      screen.blit(Val_Surf, Val_Rect)
      screen.blit(Del_Surf, Del_Rect)
      screen.blit(Restart_Surf, Restart_Rect)
      screen.blit(Quit_Surf, Quit_Rect)
             
      #x = smcx[a]+cx
      #y = smcy[b]+cy
      x = cx + sin(a * angleStep)*bigradius
      y = cy + sin(b * angleStep + delta)*bigradius
      
      if not delta_changed:
         pdl(bk, BGCOLOR, (lastx, lasty), (x,y), 2)  # colors mix
         pdl(bk, LINECOLOR[full_cycle], (lastx, lasty), (x,y))
      else:
         delta_changed = False
      lastx = x
      lasty = y
          
      screen.blit(dot, (x,y))
      clock.tick(FPS)
      pygame.display.update()
      
      a = a+ai; b = b+bi
      if b >= points: 
         b = b % points
           
      if a >= points: 
         a = a % points
           
      # 360/7 doesn't match up exactly
      if abs(x - initx)< 2 and abs(y - inity)< 2: full_cycle = full_cycle + 1
      if full_cycle > LCMAX: full_cycle = 0
     
           

pygame.quit()



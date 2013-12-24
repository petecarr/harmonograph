import pygame

class Slider():
    global BLACK, WHITE
    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
 
    
    def __init__(self, screen, color = (127, 127, 127), horiz=True, 
                 init_value=127, min_value=0, max_value=255, 
                 length=100, thickness=10, 
                 borderwidth = 1, bordercolor = (0,0,0)):
        self.screen = screen
        if not horiz:
            w = thickness
            h = length
        else:
            w = length
            h = thickness
        
        self.horiz = horiz
        self.length = length
        self.thickness = thickness
        self.width = w
        self.height = h 
        
        self.min_value = min_value
        self.max_value = max_value
        self.value_range = max_value-min_value
        self.mousedown = False
        self.mouseposx = -1
        self.mouseposy = -1
        self.slidervalue = init_value

        self.xorigin = 0
        self.yorigin = 0  
        self.color = color
        
        self.borderwidth = borderwidth
        if borderwidth*2 > thickness:
            borderwidth = 1
        self.bordercolor = bordercolor
    
        self.surface =  pygame.surface.Surface((w , h ))
        self.draw_slider(self)
        
    @staticmethod
    def draw_slider(self):
        pygame.draw.rect(self.surface, self.bordercolor, 
                         pygame.Rect(0, 0, self.width, self.height ))
        pygame.draw.rect(self.surface, self.color, 
                         pygame.Rect(self.borderwidth, self.borderwidth, 
                              self.width-self.borderwidth*2 , 
                              self.height-self.borderwidth*2))
     
    @staticmethod
    def limit_pos(self, x,y): 
        if self.horiz:
            if x > self.xorigin+self.length: x = self.xorigin+self.length
            elif x < self.xorigin: x =self.xorigin
        else:
            if y > self.yorigin+self.length: y = self.yorigin+self.length
            elif y < self.yorigin: y =self.yorigin 
        return x,y
    
    @staticmethod
    def getsv(self, x,y):
        if self.horiz:
            return int((x-self.xorigin)*self.value_range/self.length + 
                        self.min_value)
        else:
            return int((y-self.yorigin)*self.value_range/self.length + 
                        self.min_value)
     
    @staticmethod   
    def get_slider_coords(self):
        if self.horiz:
            if self.mouseposx < 0:
                self.mouseposx =  self.xorigin + \
                            int(self.slidervalue*self.length/self.value_range)
            pos = (self.mouseposx - self.xorigin, int(self.thickness/2))
        else:
            if self.mouseposy < 0:
                self.mouseposy =  self.yorigin +  \
                          int(self.slidervalue*self.length/self.value_range)
            pos = (int(self.thickness/2), self.mouseposy - self.yorigin)          
        return pos
                    
    def draw_scale(self, x, y):
        self.xorigin = x
        self.yorigin = y
        self.screen.blit(self.surface, (x, y))
        radius1 = int((self.thickness-2*self.borderwidth)/2)
        radius2 = radius1-1
        pos = self.get_slider_coords(self)
    
        self.draw_slider(self)
        pygame.draw.circle(self.surface, BLACK, pos, radius1)
        pygame.draw.circle(self.surface, WHITE, pos, radius2)
        
    def in_scale(self, x, y):
        if (x >= self.xorigin) and (x < self.xorigin+self.width):
            if (y >= self.yorigin) and (y < self.yorigin+self.height):
                return True
        return False
    
    def mouse_down(self, x, y):
        self.mousedown = True
        self.mouseposx = x
        self.mouseposy = y
        self.slidervalue = self.getsv(self, x,y)
        
    def mouse_is_down(self):
         return self.mousedown;
    
    def mouse_up(self, x, y):
        self.mousedown = False
    
    def mouse_motion(self,x,y):
        x1, y1 = self.limit_pos(self, x,y)
        if self.horiz:
            if x1 >= 0:
                 self.mouseposx=x1
        else:
            if y1 >= 0:
                self.mouseposy = y1
        self.slidervalue = self.getsv(self, self.mouseposx, self.mouseposy)
    
    def get_slider_screen_coords(self):
        x,y = self.get_slider_coords(self)
        x = x + self.xorigin
        y = y + self.yorigin
        return (x,y)
        
    def get_slider_value(self):
         return self.slidervalue
             
             
    def mouse_actions(self, event):        
        if event.type == pygame.MOUSEBUTTONUP:
            # slider relinquished
            x,y = event.pos
            if self.mouse_is_down():
                self.mouse_up(x,y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            if self.in_scale(x,y):
               self.mouse_down(x,y)        

        elif event.type == pygame.MOUSEMOTION:
            # as long as the button is down, keep sliding
            x,y = event.pos
            if self.mouse_is_down():
                self.mouse_motion(x,y)
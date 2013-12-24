from tkinter import *
from math import pi, sin, cos, exp

#----------------------------------------------------------------------------
# Things to try:
# Display equations being shown - possibly in a small window - 
# controlled by a button
# Gray out scales not applicable to a display like Lissajous
# Add Spiral Envelopes
# Change scales for Potted displays which use a different formula
# Save button for printing (make background white!!)
# Load ??
# More object oriented. Separate modules.
# Source control.
# Handle window resizing.
# Try PyQt  (-> PySide), OpenGL
# Generalize plotting
#----------------------------------------------------------------------------



CANVASWIDTH=1000
CANVASHEIGHT=800

BGCOLOR="black"
LINECOLOR="red"
linecolor=LINECOLOR
colors = ("red", "orange", "yellow", "green", "cyan", "blue", "magenta")

Ax1,Fx1,Px1,Ax2,Fx2,Px2 = 0.0,0.0,0.0,0.0,0.0,0.0
Ay1,Fy1,Py1,Ay2,Fy2,Py2 = 0.0,0.0,0.0,0.0,0.0,0.0
Dkx, Dky = 0.0, 0.0
cx = CANVASWIDTH/2
cy = CANVASHEIGHT/2

NO_DK_LIMIT = 2.0*pi
drawing_limit = NO_DK_LIMIT


#----------------------------------------------------------------------------
# Different plots
spirograph = False
lissajous = True
damped_pends = False
#----------------------------------------------------------------------------
print_equation = False
#----------------------------------------------------------------------------
# Animation control
ani = False
#----------------------------------------------------------------------------
# multicolor control
multcol = False
#----------------------------------------------------------------------------
# Potted Displays
potted_draw=False
potted_index=0
global cindx, CINDX_MAX, A1, A2, B1, B2, C1, C2, D1, D2, E1, E2, F1, F2
CINDX_MAX = 13
 
A1=0; B1=1; C1=2; D1=3; E1=4; F1=5; A2=6; B2=7; C2=8; D2=9; E2=10; F2=11
cfs = [
    # A1   B1   C1    D1    E1   F1   A2    B2    C2    D2    E2    Fx2

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
    # should be 4 lobes,  but isn't
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

#x=cx+(b1*sin(f1*t)+c1*cos(f1*t))*100.0*exp(-a1*0.01*t)+  #note was 100.0
#     (b2*sin(f2*t)+c2*cos(f2*t))*100.0*exp(-a2*0.01*t)
#y=cy+(d1*sin(f1*t)+e1*cos(f1*t))*100.0*exp(-a1*0.01*t)+
#     (d2*sin(f2*t)+e2*cos(f2*t))*100.0*exp(-a2*0.01*t)
def _harmonograph_(t):
    global print_equation
    coeffs = cfs[potted_index]
    a1 = coeffs[A1]; b1 = coeffs[B1]; c1 = coeffs[C1]
    d1 = coeffs[D1]; e1 = coeffs[E1]; f1 = coeffs[F1]
    a2 = coeffs[A2]; b2 = coeffs[B2]; c2 = coeffs[C2]
    d2 = coeffs[D2]; e2 = coeffs[E2]; f2 = coeffs[F2]
    DSCALE=80.0

    if a1 != 0.0: r1 = DSCALE*exp(-a1*0.01*t)
    else: r1 = DSCALE
    if a2 != 0.0: r2 = DSCALE*exp(-a2*0.01*t)
    else: r2 = DSCALE
    
    s1 = sin(f1*t)
    s2 = sin(f2*t)
    t1 = cos(f1*t)
    t2 = cos(f2*t)
    x = cx + r1*(b1*s1 + c1*t1) + r2*(b2*s2 + c2*t2)
    y = cy + r1*(d1*s1 + e1*t1) + r2*(d2*s2 + e2*t2)
    
    if print_equation:
        try:
            if a1 != 0.0: r1_="80.0*exp(-"+repr(a1)+"*0.01*t)*"
            else : r1_ = "80.0*"
            if a2 != 0.0: r2_="80.0*exp(-"+repr(a2)+"*0.01*t)*"
            else: r2_ = "80.0*"
            s1_="*sin("+repr(f1)+"*t)"
            s2_="*sin("+repr(f2)+"*t)"
            t1_="*cos("+repr(f1)+"*t)"
            t2_="*cos("+repr(f2)+"*t)"
            print("x = "+repr(cx)+ "+"+
                  r1_+"("+repr(b1)+s1_+"+"+repr(c1)+t1_+")+"+
                  r2_+"("+repr(b2)+s2_+"+"+repr(c2)+t2_+")")
            print("y = "+repr(cy)+ "+"+
                  r1_+"("+repr(d1)+s1_+"+"+repr(e1)+t1_+")+"+
                  r2_+"("+repr(d2)+s2_+"+"+repr(e2)+t2_+")")            
        except TypeError:
            print("Error in show equation")
        print_equation = False
    return (x,y)

#-------------------------------------------------------------------------
# R is outer radius, r is inner. Rho is pen radius relative to inner wheel.
# Added decay factors for extra spectacle
R=0.0
r = 0.0
Rrr = 0.0
Rpr = 0.0
Rho = 0.0

def _spirograph_(t):
    global spirograph, Ax1, Ax2, Ay1, Dkx, Dky, cx, cy
    global R, R, Rrr, Rpr, Rho
    global print_equation
    if t == 0.0:
        R=Ax1; r = Ax2
        Rrr = (R-r)/r
        Rpr = R-r
        Rho = Ay1
    if print_equation:
        try:
            print("x = "+repr(cx)+" + ("+repr(Rpr)+"* cos(t) - "+
                         repr(Rho)+" * cos("+repr(Rrr)+"*t))*exp(-"+
                         repr(Dkx)+"*t)")
            print("y = "+repr(cy)+" + ("+repr(Rpr)+"* sin(t) - "+
                   repr(Rho)+" * sin("+repr(Rrr)+"*t))*exp(-"+
                   repr(Dky)+"*t)")             
        except TypeError:
            print(cx,Rpr,Rho,Rrr,Dkx)
                  
        print_equation = False
        
    x = cx + (Rpr*cos(t) -Rho*cos(Rrr*t))*exp(-Dkx*t)
    y = cy + (Rpr*sin(t) -Rho*sin(Rrr*t))*exp(-Dky*t)
    return (x,y)
#-------------------------------------------------------------------------

def harmonograph_draw(canvas):
    global Ax1, Fx1, Px1, Ax2, Fx2, Px2, Ay1, Fy1, Py1, Ay2, Fy2, Py2, cx, cy
    global linecolor, spirograph, potted_draw, multcol
    global print_equation
    
    x=0.0; y = 0.0
    
    canvas.delete(ALL)

    if Dkx > 0.0 or Dky > 0.0:
        drawing_limit = Dlimit   # a slider
    elif potted_draw:
        drawing_limit = 100.0
    else:
        drawing_limit = NO_DK_LIMIT
           
    t = 0.0
    while t < drawing_limit:
        try:
            if spirograph:
                x,y = _spirograph_(t)
            elif potted_draw:
                x,y = _harmonograph_(t)
            else:
                if print_equation:
                    try:
                        if Dkx == 0.0: 
                            Dkx_ = ""
                        else: 
                            Dkx_ = "*exp(-"+repr(Dkx)+"*t)"
                        if Px1 == 0.0:
                            Px1_ = ""
                        else:
                            Px1_ = "+"+repr(Px1)
                        if Px2 == 0.0:
                            Px2_ = ""
                        else:
                            Px2_ = "+"+repr(Px2)           
                        if Py1 == 0.0:
                            Py1_ = ""
                        else:
                            Py1_ = "+"+repr(Py1)
                        if Py2 == 0.0:
                            Py2_ = ""
                        else:
                            Py2_ = "+"+repr(Py2)
                        if Ax1 == 0.0:
                            Ax1_ = ""
                        else:
                            Ax1_ = repr(Ax1)+"*sin("+repr(Fx1)+"*t"+Px1_+")"
                        if Ax2 == 0.0:
                            Ax2_ = ""
                        else:
                            Ax2_ = "+"+repr(Ax2)+"*sin("+repr(Fx2)+"*t+"+repr(Px2) 
                            
                        print("x="+repr(cx)+"+("+Ax1_+Ax2_+")"+Dkx_)
                        if Dky == 0.0: 
                            Dky_ = ""
                        else: 
                            Dky_ = "*exp(-"+repr(Dky)+"*t)" 
                        if Ay1 == 0.0:
                            Ay1_ = ""
                        else:
                            Ay1_ = repr(Ay1)+"*sin("+repr(Fy1)+"*t+"+repr(Py1)+")"
                        if Ay2 == 0.0:
                            Ay2_ = ""
                        else:
                            Ay2 = "+"+repr(Ay2)+"*sin("+repr(Fy2)+"*t+"+repr(Py2) 
                                                        
                        print("y="+repr(cy)+"+("+Ay1_+Ay2_+")"+Dky_)                            
                 
                    except TypeError:
                        print(cx, Ax1, Fx1, Px1)
                    print_equation = False       
                x = cx + int(Ax1*sin(Fx1*t+Px1) +
                             Ax2*sin(Fx2*t+Px2))*exp(-Dkx*t)
                y = cy + int(Ay1*sin(Fy1*t+Py1) +
                             Ay2*sin(Fy2*t+Py2))*exp(-Dky*t)
        except TypeError:
            pass
        if multcol:
            if (t -float(int(t))) < 0.00000000001:
                lineindex = colors.index(linecolor)
                lineindex = lineindex+1
                if lineindex >=  len(colors): lineindex = 0
                linecolor = colors[lineindex]

        if t > 0.0:
            canvas.create_line(lastx,lasty,x,y, width=1, fill=linecolor)
            
        lastx=x; lasty=y
        t = t + 0.01
        #print(lastx, lasty, x,y)



class Scales():
    def __init__(self, root, orient, label, from_, to, resolution = 1,
                 variable=0.0):
        self.value = 0
        self.root = root
        self.orient = orient
        self.label = label
        self.from_ = from_
        self.to = to
        self.resolution = resolution
        self.variable= variable

        self.scale=Scale(self.root, orient = self.orient, label = self.label,
                         from_=self.from_, to = self.to,
                         resolution = self.resolution,
                         command = self.update_value)
        self.scale.pack()
        self.scale.set(variable)


    def update_value(self, scaleValue):
        self.variable = scaleValue
        self.scale.set(scaleValue)
        refresh_now()

    def get(self):
        #print("Scales val="+str(self.val))
        return self.variable

    def set(self, scaleValue):
        self.variable = scaleValue
        self.scale.set(scaleValue)


def refresh_now():
    global Ax1, Fx1, Px1, Ax2, Fx2, Px2, Ay1, Fy1, Py1, Ay2, Fy2, Py2
    global Dkx, Dky, Dlimit
    Ax1 = float(Ax1scale.get())
    Fx1 = float(Fx1scale.get())
    Px1 = float(Px1scale.get())*pi/180.0
    Ax2 = float(Ax2scale.get())
    Fx2 = float(Fx2scale.get())
    Px2 = float(Px2scale.get())*pi/180.0
    Dkx = float(Dkxscale.get())
    Ay1 = float(Ay1scale.get())
    Fy1 = float(Fy1scale.get())
    Py1 = float(Py1scale.get())*pi/180.0
    Ay2 = float(Ay2scale.get())
    Fy2 = float(Fy2scale.get())
    Py2 = float(Py2scale.get())*pi/180.0
    Dky = float(Dkyscale.get())
    Dlimit  = float(Dlimitscale.get())
    harmonograph_draw(canvas)


def quitNow():
    global tk
    tk.destroy()
    #sys.exit(None)

#--------------------------------------------------------------------------

tk = Tk()
lf = Frame(tk, borderwidth=2, relief=RAISED)
lf.pack(fill = BOTH, side =LEFT)
lf.master.title("Harmonograph")
cf = Frame(tk, borderwidth=2, relief=RAISED)
cf.pack(side =LEFT)
rf = Frame(tk, borderwidth=2, relief=RAISED)
rf.pack(fill = BOTH, side =RIGHT)
bottomleftframe = Frame(lf)
bottomleftframe.pack(fill = BOTH, side = BOTTOM )
bottomrightframe = Frame(rf)
bottomrightframe.pack(fill = BOTH, side = BOTTOM )

leftLabel= Label(lf, text="X-coefficients", borderwidth=2, relief=RAISED)
leftLabel.pack(side=TOP)
Ax1scale = Scales(lf, orient=HORIZONTAL, label = "Ax1",
                  from_=0, to=CANVASWIDTH/2, variable=Ax1)
Fx1scale = Scales(lf, orient=HORIZONTAL, label = "Fx1",
                  from_=0, to=15, variable=Fx1)
Px1scale = Scales(lf, orient=HORIZONTAL, label = "Px1",
                  from_=0, to=360, resolution = 1, variable=Px1)
Ax2scale = Scales(lf, orient=HORIZONTAL, label = "Ax2",
                  from_=0, to=CANVASWIDTH/2, variable=Ax2)
Fx2scale = Scales(lf, orient=HORIZONTAL, label = "Fx2",
                  from_=0, to=15, variable=Fx2)
Px2scale = Scales(lf, orient=HORIZONTAL, label = "Px2",
                  from_=0, to=360, resolution = 10, variable=Px2)
Dkxscale = Scales(lf, orient=HORIZONTAL, label = "Decay rate",
                  from_=0.0, to=0.5, resolution = 0.01, variable=Dkx)
Dlimitscale = Scales(lf, orient=HORIZONTAL, label = "Plot Length (secs)",
                     from_=0.01, to=100.0, resolution = 0.01,
                     variable=drawing_limit)
Dlimitscale.set(drawing_limit)
    
#--------------------------------------------------------------------------
#centerLabel= Label(cf, text="Harmonograph", borderwidth=2, relief=RAISED)
#centerLabel.pack(side=TOP, fill=BOTH)

global canvas
canvas = Canvas(cf, width = CANVASWIDTH, height = CANVASHEIGHT, bg=BGCOLOR)
canvas.pack()

def key(event):
    if (event.keysym == 'Escape'):
        print("Pressed Escape, quitting")
        quitNow()
    #elif (event.keycode == <Print>):  #doesn't work
        #print("Print")
    else:
        print ("pressed", repr(event.keysym))
        print ("pressed", repr(event.keycode))


def callback(event):
    canvas.focus_set()
    #print ("clicked at", event.x, event.y)


canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)

#--------------------------------------------------------------------------
rightLabel= Label(rf, text="Y-coefficients", borderwidth=2, relief=RAISED)
rightLabel.pack(side=TOP)
Ay1scale = Scales(rf, orient=HORIZONTAL, label = "Ay1",
                  from_=0, to=CANVASHEIGHT/2, variable=Ay1)
Fy1scale = Scales(rf, orient=HORIZONTAL, label = "Fy1",
                  from_=0, to=15, variable=Fy1)
Py1scale = Scales(rf, orient=HORIZONTAL, label = "Py1",
                  from_=0, to=360, resolution = 10, variable=Py1)
Ay2scale = Scales(rf, orient=HORIZONTAL, label = "Ay2",
                  from_=0, to=CANVASHEIGHT/2, variable=Ay2)
Fy2scale = Scales(rf, orient=HORIZONTAL, label = "Fy2",
                  from_=0, to=15, variable=Fy2)
Py2scale = Scales(rf, orient=HORIZONTAL, label = "Py2",
                  from_=0, to=360,resolution = 10, variable=Py2)
Dkyscale = Scales(rf, orient=HORIZONTAL, label = "Decay rate",
                  from_=0.0, to=0.5, resolution = 0.01, variable=Dky)
#--------------------------------------------------------------------------
buttonframe = Frame(bottomrightframe, borderwidth=2)
buttonframe.pack(fill = BOTH, side = TOP )

# Options.
#--------------------------------------------------------------------------

# Show the current equations being plotted
def show_equation():
    global print_equation
    print_equation =True
    refresh_now()


equation = Button(buttonframe, text = "Show equation",
                  command=show_equation)
equation.pack(anchor=W)

#--------------------------------------------------------------------------

# Animate display by incrementing Px1 to rotate the display'

def animate_display():
    global ani
    if ani: ani=False
    else: ani = True
    # move Py1 at intervals to rotate the display
    if ani:
        try:
            while ani:
                Px1 = int(Px1scale.get())
                Px1 = Px1+5
                if Px1 >=360: Px1 = 0
                Px1scale.set(Px1)
                refresh_now()

                tk.update_idletasks()
                tk.update()
        except TclError:
            pass   # avoid errors when window is closed


animate = Checkbutton(buttonframe, text = "Animate",
                      command=animate_display)
animate.config(indicatoron=1)
animate.pack(anchor=W)

#--------------------------------------------------------------------------
# load up potted values that make nice pictures

def potted_display():
    global potted_draw
    # saved values for cool display
    if potted_draw:
        potted_draw=False
    else: 
        potted_draw = True
        Dlimitscale.set(float(100.0))    
    refresh_now()
    
def next_display(): 
    global potted_draw, potted_index
    if potted_draw:
        potted_index= potted_index+1
        if potted_index > CINDX_MAX:
            potted_index= 0
        Dlimitscale.set(float(100.0))
        refresh_now()
        
def last_display(): 
    global potted_draw, potted_index
    if potted_draw:
        potted_index= potted_index-1
        if potted_index < 0:
            potted_index= CINDX_MAX
        Dlimitscale.set(float(100.0))
        refresh_now()
        
pbuttonframe = Frame(bottomrightframe, borderwidth=2)
pbuttonframe.pack(fill = BOTH, side = TOP )

potted = Checkbutton(pbuttonframe, text = "Potted displays",
                     command=potted_display)
potted.config(indicatoron=1)
potted.pack(anchor=W)

potted_last = Button(pbuttonframe, text = "Last plot",
                     command=last_display)
potted_last.pack(side=LEFT)

potted_next = Button(pbuttonframe, text = "Next plot",
                     command=next_display)
potted_next.pack(side=RIGHT)
#--------------------------------------------------------------------------
# Multicolor - switch colors every time t goes through a multiple of 2*pi

def multicolor_display():
    global multcol
    # saved values for cool displays
    if multcol: multcol= False
    else: multcol = True
    refresh_now()

multicolor = Checkbutton(bottomrightframe, text = "Multicolor",
                         command=multicolor_display)
multicolor.config(indicatoron=1)
multicolor.pack(anchor=W)
#--------------------------------------------------------------------------
# Select between 3 modes of display: Lissajous, Spirograph or harmonograph
def clear_scales():
    CLR = float(0.0)
    Ax1scale.set(CLR)
    Ax2scale.set(CLR)
    Ay1scale.set(CLR)
    Ay2scale.set(CLR)
    Fx1scale.set(CLR)
    Fx2scale.set(CLR)
    Fy1scale.set(CLR)
    Fy2scale.set(CLR)
    Px1scale.set(CLR)
    Px2scale.set(CLR)
    Py1scale.set(CLR)
    Py2scale.set(CLR)
    Dkxscale.set(CLR)
    Dkyscale.set(CLR)
    Dlimitscale.set(CLR)

def set_mode():
    global Ax1, Fx1, Px1, Ax2, Fx2, Px2, Ay1, Fy1, Py1, Ay2, Fy2, Py2
    global Dkx, Dky, Dlimit, lissajous, spirograph, damped_pends
    global which_plot
    mode = str(which_plot.get())
    if mode =="LI":
        lissajous = True
        spirograph = False
        damped_pends = False
    elif mode == "SP":
        spirograph = True
        damped_pends = False
        lissajous = False
    elif mode == "DP":
        damped_pends = True
        spirograph = False
        lissajous = False

    clear_scales()
    if lissajous:
        Ax1scale.set(float(CANVASWIDTH/4.0))
        Fx1scale.set(float(8.0))
        Px1scale.set(float(0.0))
        Ay1scale.set(float(CANVASHEIGHT/4.0))
        Fy1scale.set(float(7.0))
        Py1scale.set(float(90.0))
        Dlimitscale.set(float(2.0*pi/8.0))  # should be moved into harmonograph
    elif spirograph:
        R = CANVASHEIGHT/4.0      # Outer circle radius
        r = CANVASHEIGHT/40.0     # Inner circle radius
        Rho = CANVASHEIGHT/4.0    # Pen radius
        Ax1scale.set(float(R))
        Ay1scale.set(float(Rho))
        Ax2scale.set(float(r))
        Dlimitscale.set(float(2.0*pi))
    elif damped_pends:
        Ax1scale.set(float(CANVASWIDTH/4.0))
        Fx1scale.set(float(4.0))
        Px1scale.set(float(0.0))
        Ay1scale.set(float(CANVASHEIGHT/4.0))
        Fy1scale.set(float(8.0))
        Py1scale.set(float(90.0))
        Dkxscale.set(float(0.1))
        Dkyscale.set(float(0.0))
        Dlimitscale.set(float(2.0*pi))

    refresh_now()

MODES = [
  ("Damped Pendulums", "DP"),
  ("Lissajous", "LI"),
  ("Spirograph", "SP")
  ]

which_plot = StringVar()
which_plot.set("LI") # initialize

for text, mode in MODES:
    b = Radiobutton(bottomrightframe, text=text,
                    variable=which_plot, value=mode, command=set_mode)
    b.config(indicatoron=1)
    b.pack(anchor=W)


set_mode()
#--------------------------------------------------------------------------
# This radiobox stuff doesn't like to appear before Tk is defined

def select_color():
    global which_color, linecolor
    #print(which_color.get())
    linecolor=which_color.get()
    refresh_now()

which_color = StringVar()
rb = []


def rbox(colors):
    for color in (colors):     
        r = Radiobutton(bottomleftframe, width=8, 
                        text=color, variable=which_color,
                        borderwidth=4,
                        bg=color, fg="black",
                        activebackground=color, activeforeground="white",
                        selectcolor=color, 
                        highlightbackground=color,
                        value=color,
                        command=select_color)

        r.config(indicatoron=0)
        r.pack(anchor=CENTER, fill=X)
        rb.append(r)

rbox(colors)
which_color.set("red")

#-----------------------------------------------------------------------------
refrbutton = Button(bottomleftframe, text="Refresh", fg="blue",
                    command = refresh_now)
refrbutton.pack(side = LEFT)
quitbutton = Button(bottomleftframe, text="Quit", fg="red",
                    command = quitNow)
quitbutton.pack(side = RIGHT)

tk.mainloop()

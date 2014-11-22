
numEnds = 24;
numShafts = 8;
numTreadles = 8
t_end = 24

import Tkinter as tk
import numpy as np

width_end = 22  #pixel width of each rectangle in drawup
width_pick = 20 #pixel height of each rectange in drawup

class WeavingDraft:
    def __init__(self, win):

	self.makeThreadingGUI(win)
	self.makeTreadlingGUI(win)
	self.makeTieupGUI(win)
	self.makeThreadingOptions(win)
	self.makeTreadlingOptions(win)
	self.makeTieupOptions(win)
	#self.makeGeneralOptions(win)
	#win2=tk.Toplevel()
	self.makeDrawdownGUI(win)
	self.manageLayout(win)

	self.loadTieup()
	self.drawDown()


    def makeThreadingGUI(self,win):
        self.shaftsEndsAreOn = []

        threadingFrame = tk.Frame(win, borderwidth=1, relief=tk.RAISED)

	labels = [];
	buttons = []
	for end in range(numEnds):
	        endFrame = tk.Frame(threadingFrame, borderwidth=1, relief=tk.FLAT)
		endFrame.grid(row=0, column=end)
		label = tk.Label(endFrame, text=numEnds-end)
		label.grid(row=0,column=0)

		v = tk.IntVar(win)
		v.set(end%numShafts) #selected by default
		self.shaftsEndsAreOn.append(v)
		for shaft in range(numShafts):
		    if end == numEnds-1:
			label = str(numShafts-shaft)
		    else:
			label = str(numShafts-shaft)#""
		    rb = tk.Radiobutton(endFrame, text=label, variable=v, value=shaft,command=self.drawDown,padx=0, pady=0, borderwidth=1,indicatoron=0,selectcolor='black',width=2)			
		    rb.grid(row=shaft+1, column=0)
		    buttons.append(rb)
	self.threadingFrame = threadingFrame

    def makeTreadlingGUI(self,win):
        self.treadlesAtEachTimeStep = []

        treadlingFrame = tk.Frame(win, borderwidth=1, relief=tk.RAISED)
	labels = [];
	buttons = []
	for t in range(t_end):
	        tFrame = tk.Frame(treadlingFrame, borderwidth=1, relief=tk.RAISED)
		tFrame.grid(row=t, column=0)
		v = tk.IntVar(win)
		v.set(t%numTreadles) #selected by default
		self.treadlesAtEachTimeStep.append(v)
		for treadle in range(numTreadles):
		    if t == 0:
			label = str(treadle+1)
		    else:
			label = str(treadle+1)#""
		    rb = tk.Radiobutton(tFrame, text=label, variable=v, value=treadle,command=self.drawDown,padx=0, pady=0, borderwidth=1,indicatoron=0,width=2,selectcolor='black')	
		    rb.grid(row=0, column=treadle)
		    buttons.append(rb)
        self.treadlingFrame = treadlingFrame

    def makeTieupGUI(self,win):
        self.shaftsOnEachTreadle = []

        tieupFrame = tk.Frame(win, borderwidth=1, relief=tk.RAISED)
	labels = [];
	buttons = []
	for treadle in range(numTreadles):
	        treadleFrame = tk.Frame(tieupFrame, borderwidth=1, relief=tk.RAISED)
		treadleFrame.grid(row=0, column=treadle)
		
		vars=[]
		self.shaftsOnEachTreadle.append(vars)
		for shaft in range(numShafts):
		    v = tk.IntVar(win)
		    rb = tk.Checkbutton(treadleFrame, text="", variable=v, command=self.drawDown,padx=7, pady=0, borderwidth=1,indicatoron=0,selectcolor='black')	
		    rb.grid(row=shaft, column=0)
		    buttons.append(rb)
		    vars.append(v)
        self.tieupFrame = tieupFrame

    def makeDrawdownGUI(self, win):
	drawdownFrame = tk.Frame(win, width=numEnds*width_end, height=t_end*width_pick)
        drawdownFrame.pack()
	self.drawdownFrame = drawdownFrame

    def manageLayout(self, win):
	#put frames in a grid
	#left column
	self.threadingFrame.grid(row=0, column=0)
	self.drawdownFrame.grid(row=1, column=0, rowspan=3)

	#centre column
	self.tieupFrame.grid(row=0, column=1,sticky=tk.S)
	self.treadlingFrame.grid(row=1, column=1, rowspan=3)

	#right column
	self.threadingOptionsFrame.grid(row=0,column=2)
	self.tieupOptionsFrame.grid(row=1, column=2)
	self.treadlingOptionsFrame.grid(row=2,column=2)
	#self.generalOptionsFrame.grid(row=3, column=2)

    def makeGeneralOptions(self,win):
	generalOptionsFrame = tk.Frame(win, borderwidth=3, relief=tk.RAISED)

	label = tk.Label(generalOptionsFrame, text="# ends")
	label.grid(row=0,column=0)

	self.var_numEnds = tk.StringVar(win)
	e = tk.Entry(generalOptionsFrame, textvariable=self.var_numEnds)
	e.grid(row=0,column=1)
	
	self.var_numEnds.set("15")

	b = tk.Button(generalOptionsFrame, text="Update", command=self.updateGeneralOptions)
	b.grid(row=1,column=0,columnspan=2)


	self.generalOptionsFrame = generalOptionsFrame

    def updateGeneralOptions(self):
	numEnds = self.var_numEnds.get()
	print(numEnds)
	'''
	self.updateThreadingGUI(win)
	self.makeTreadlingGUI(win)
	self.makeTieupGUI(win)
	self.makeThreadingOptions(win)
	self.makeTreadlingOptions(win)
	self.makeTieupOptions(win)
	self.makeGeneralOptions(win)
	self.makeDrawdownGUI(win)
	#self.drawDown()
	'''

    def makeTieupOptions(self,win):
	tieupOptionsFrame = tk.Frame(win, borderwidth=3, relief=tk.RAISED)

	b = tk.Button(tieupOptionsFrame, text="Clear tieup", command=self.clearTieup)
	b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

	b = tk.Button(tieupOptionsFrame, text="Fill tieup", command=self.fillTieup)
	b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

	b = tk.Button(tieupOptionsFrame, text="Inverse tieup", command=self.inverseTieup)
	b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

	b = tk.Button(tieupOptionsFrame, text="Save tieup", command=self.saveTieup)
	b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

	self.tieupOptionsFrame = tieupOptionsFrame

    def saveTieup(self):
	filename = 'tieup.txt'
	f = open(filename,'w')
	f.write(str(numShafts)+'\n')
	f.write(str(numTreadles)+'\n')
        for shaft in range(numShafts):
            for treadle in range(numTreadles):
	        f.write(str(self.shaftsOnEachTreadle[treadle][shaft].get()) + ' ')
	    f.write('\n')
        f.close();    

    def loadTieup(self):
	filename = 'tieup.txt'
	f = open(filename)
        numShafts = int(f.readline().strip());
        numTreadles = int(f.readline().strip());
        if(not (numShafts and numTreadles) ):
            print 'Ignoring load request because file is not appropriate'
            
        else:
       	    for shaft in range(numShafts):
                line = f.readline().strip();
                values = line.split(' ');
                #if(not (len(values) == numTreadles) ):
                #    print 'Quitting load request because file doesn't add up'
                        
                values = map(int,values); 
		for treadle in range(numTreadles):
		   self.shaftsOnEachTreadle[treadle][shaft].set(values[treadle])
        f.close();    


    def clearTieup(self):
	
        for treadle in range(numTreadles):
	    for shaft in range(numShafts):
                self.shaftsOnEachTreadle[treadle][shaft].set(0)
	self.drawDown()

    def fillTieup(self):
        for treadle in range(numTreadles):
	    for shaft in range(numShafts):
                self.shaftsOnEachTreadle[treadle][shaft].set(1)
	self.drawDown()

    def inverseTieup(self):
        for treadle in range(numTreadles):
	    for shaft in range(numShafts):
		currentVal = self.shaftsOnEachTreadle[treadle][shaft].get()
                self.shaftsOnEachTreadle[treadle][shaft].set(1-currentVal)
	self.drawDown()



    def makeThreadingOptions(self,win):
	threadingOptionsFrame = tk.Frame(win, borderwidth=3, relief=tk.RAISED)

        b = tk.Button(threadingOptionsFrame, text="Pointed threading", command=self.pointedThreading)
        b.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

	b = tk.Button(threadingOptionsFrame, text="Straight threading", command=self.straightThreading)
        b.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

	b = tk.Button(threadingOptionsFrame, text="Inverse threading", command=self.inverseThreading)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

	self.threadingOptionsFrame = threadingOptionsFrame

    def pointedThreading(self):
	direction = 1; #initially incrementing shafts
	shaft = 0; #start closest to weaver

	for end in reversed(range(numEnds)): #start at right hand side
	    self.shaftsEndsAreOn[end].set(numShafts-1-shaft) #update radio button
	    if direction == 1:
		shaft += 1
                if shaft > numShafts-1: #reached upper point - switch directions
		    shaft = numShafts - 2
		    direction = 0
	    else:
		shaft -= 1
		if shaft < 0: #reached lower point - switch directions
		    shaft = 1
		    direction = 1
	self.drawDown()

    def straightThreading(self):
	for end in range(numEnds):
	    self.shaftsEndsAreOn[end].set(numShafts-1-((numEnds-1-end)%numShafts)) #update radio button
	self.drawDown()

    def inverseThreading(self):
	for end in range(numEnds):
	    currentShaft = self.shaftsEndsAreOn[end].get()	
	    self.shaftsEndsAreOn[end].set(numShafts-1-currentShaft) #update radio button
	self.drawDown()



    def makeTreadlingOptions(self,win):
	treadlingOptionsFrame = tk.Frame(win, borderwidth=3, relief=tk.RAISED)

        b = tk.Button(treadlingOptionsFrame, text="Pointed treadling", command=self.pointedTreadling)
        b.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

	b = tk.Button(treadlingOptionsFrame, text="Straight treadling", command=self.straightTreadling)
        b.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

	b = tk.Button(treadlingOptionsFrame, text="Inverse treadling", command=self.inverseTreadling)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

	self.treadlingOptionsFrame = treadlingOptionsFrame

    def pointedTreadling(self):
	direction = 1; #initially incrementing treadles
	treadle = 0;

	for t in range(t_end): 
	    self.treadlesAtEachTimeStep[t].set(treadle) #update radio button
	    if direction == 1:
		treadle += 1
                if treadle > numTreadles - 1: #reached upper point - switch directions
		    treadle = numTreadles - 2
		    direction = 0
	    else:
		treadle -= 1
		if treadle < 0: #reached lower point - switch directions
		    treadle = 1
		    direction = 1
	self.drawDown()

    def straightTreadling(self):
	for t in range(t_end):
	    self.treadlesAtEachTimeStep[t].set(t%numTreadles) #update radio button
	self.drawDown()

    def inverseTreadling(self):
	for t in range(t_end):
	    currentTreadle = self.treadlesAtEachTimeStep[t].get()	
	    self.treadlesAtEachTimeStep[t].set(numTreadles-1-currentTreadle) #update radio button
	self.drawDown()



    def drawDown(self):

	threading = np.zeros((numShafts, numEnds))
        for end in range(numEnds):
	    threading[self.shaftsEndsAreOn[end].get(),end] = 1

	tieup = np.zeros((numShafts, numTreadles))
        for treadle in range(numTreadles):
	    for shaft in range(numShafts):
                tieup[shaft,treadle] = self.shaftsOnEachTreadle[treadle][shaft].get()

	treadling = np.zeros((t_end, numTreadles))
	for t in range(t_end):
	    treadling[t,self.treadlesAtEachTimeStep[t].get()] = 1
	
        dd=np.zeros((t_end,numEnds))
        for t in range(t_end):      
	    treadle = treadling[t,:].tolist().index(1)
            shaftsLifted=tieup[:,treadle]
            for j in range(len(shaftsLifted)):
                if shaftsLifted[j]==1:
                    for i in range(numEnds):
                        if threading[j,i] == 1:
                            dd[t,i]=1

	self.displayDrawdown(dd)

    def displayDrawdown(self,drawdown):
	drawdown=np.array(drawdown*100,dtype=int)
	data = np.repeat(np.repeat(drawdown, width_pick, axis=0), width_end, axis=1)

	from PIL import Image, ImageTk
        canvas = tk.Canvas(self.drawdownFrame, width=numEnds*width_end, height=t_end*width_pick)
	canvas.place(x=-2,y=-2)

	self.im=Image.fromstring('L', (data.shape[1],\
                        data.shape[0]), data.astype('b').tostring())

        self.imTk = ImageTk.PhotoImage(image=self.im)
        canvas.create_image(0,0,image=self.imTk,anchor=tk.NW)


mw = tk.Tk()
win=mw
app = WeavingDraft(mw)
mw.mainloop()


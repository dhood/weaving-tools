

import Tkinter as tk
import tkFileDialog
import numpy as np

width_end = 22   # pixel width of each rectangle in drawup
width_pick = 20  # pixel height of each rectange in drawup


class WeavingDraft:
    def __init__(self, win, numEnds, numShafts, numTreadles, t_end):
        self.win = win

        self.threadingFrame = None
        self.treadlingFrame = None
        self.tieupFrame = None
	self.drawdownFrame = None

        self.numEnds = numEnds
        self.numShafts = numShafts
        self.numTreadles = numTreadles
        self.t_end = t_end

        self.makeThreadingGUI(win)
        self.makeTreadlingGUI(win)
        self.makeTieupGUI(win)
        self.makeThreadingOptions(win)
        self.makeTreadlingOptions(win)
        self.makeTieupOptions(win)
        self.makeGeneralOptions(win)
        self.makeDrawdownGUI(win)

        self.manageLayout(win)

        self.loadDraft()
        self.drawDown()


    def makeThreadingGUI(self,win):
        self.shaftsEndsAreOn = []

	if self.threadingFrame is None:
            self.threadingFrame = tk.Frame(win, borderwidth=1, relief=tk.RAISED)
        else:
            for i in range(len(self.threadingFrame.winfo_children())):
                self.threadingFrame.winfo_children()[0].destroy()
            
        warpColoursFrame = tk.Frame(self.threadingFrame,borderwidth=0)
        warpColoursFrame.grid(row=0, columnspan=self.numEnds)
        self.warpColours = []


        buttons = []
        for end in range(self.numEnds):
                endFrame = tk.Frame(self.threadingFrame, borderwidth=1, relief=tk.FLAT)
                endFrame.grid(row=1, column=end)

                v = tk.IntVar(win)
                cb = tk.Checkbutton(warpColoursFrame, text="", variable=v, \
                    command=self.drawDown, padx=9, pady=0, borderwidth=1, \
                    indicatoron=0,background='black')
                v.set(0) #default warp to black, weft to white
                cb.grid(row=0,column=end)
                self.warpColours.append(v)

                label = tk.Label(endFrame, text=self.numEnds-end,fg='red')
                label.grid(row=0,column=0)

                v = tk.IntVar(win)
                v.set(end%self.numShafts) #selected by default
                self.shaftsEndsAreOn.append(v)
                for shaft in range(self.numShafts):
                    if end == self.numEnds-1:
                        label = str(self.numShafts-shaft)
                    else:
                        label = str(self.numShafts-shaft)#""
                    rb = tk.Radiobutton(endFrame, text=label, variable=v, \
                        value=shaft, command=self.drawDown, padx=0, pady=0, \
                        borderwidth=1, indicatoron=0,selectcolor='black',width=2)
                    rb.grid(row=shaft+1, column=0)
                    buttons.append(rb)


    def makeTreadlingGUI(self,win):
        self.treadlesAtEachTimeStep = []

	if self.treadlingFrame is None:
            self.treadlingFrame = tk.Frame(win, borderwidth=1, relief=tk.RAISED)
        else:
            for i in range(len(self.treadlingFrame.winfo_children())):
                self.treadlingFrame.winfo_children()[0].destroy()

        weftColoursFrame = tk.Frame(self.treadlingFrame, borderwidth=0)
        weftColoursFrame.grid(column=1, rowspan=self.t_end)
        self.weftColours = []

        labels = [];
        buttons = []
        for t in range(self.t_end):
                tFrame = tk.Frame(self.treadlingFrame, borderwidth=1, relief=tk.RAISED)
                tFrame.grid(row=t, column=0)


                #Allow for binary colour selection in weft
                v = tk.IntVar(win)
                cb = tk.Checkbutton(weftColoursFrame, text="", variable=v, \
                    command=self.drawDown, padx=7, pady=1, borderwidth=1, \
                    indicatoron=0, background='black', selectcolor='white')
                v.set(1) #default weft to white, warp to black
                cb.grid(row=t,column=0)
                self.weftColours.append(v)


                v = tk.IntVar(win)
                v.set(t%self.numTreadles) #selected by default
                self.treadlesAtEachTimeStep.append(v)
                for treadle in range(self.numTreadles):
                    if t == 0:
                        label = str(treadle+1)
                    else:
                        label = str(treadle+1)#""
                    rb = tk.Radiobutton(tFrame, text=label, variable=v, \
                        value=treadle, command=self.drawDown, padx=0, pady=0, \
                        borderwidth=1,indicatoron=0,width=2,selectcolor='black')
                    rb.grid(row=0, column=treadle)
                    buttons.append(rb)

                    label = tk.Label(tFrame, text=t+1, width=2, fg='red')
                    label.grid(row=0,column=treadle+1)


    def makeTieupGUI(self,win):
        self.shaftsOnEachTreadle = []

	if self.tieupFrame is None:
            self.tieupFrame = tk.Frame(win, borderwidth=1, relief=tk.RAISED)
        else:
            for i in range(len(self.tieupFrame.winfo_children())):
                self.tieupFrame.winfo_children()[0].destroy()

        labels = [];
        buttons = []
        for treadle in range(self.numTreadles):
                treadleFrame = tk.Frame(self.tieupFrame, borderwidth=1, relief=tk.RAISED)
                treadleFrame.grid(row=0, column=treadle)

                vars=[]
                self.shaftsOnEachTreadle.append(vars)
                for shaft in range(self.numShafts):
                    v = tk.IntVar(win)
                    rb = tk.Checkbutton(treadleFrame, text="", variable=v, \
                        command=self.drawDown, padx=7, pady=0, borderwidth=1, \
                        indicatoron=0, selectcolor='black')
                    rb.grid(row=shaft, column=0)
                    buttons.append(rb)
                    vars.append(v)

    def makeDrawdownGUI(self, win):
	if self.drawdownFrame is None:
            self.drawdownFrame = tk.Frame(win, width=self.numEnds*width_end, height=self.t_end*width_pick)
            self.drawdownFrame.pack()
        else:
            for i in range(len(self.drawdownFrame.winfo_children())):
                self.drawdownFrame.winfo_children()[0].destroy()
            self.drawdownFrame.config(width=self.numEnds*width_end, height=self.t_end*width_pick)

    def manageLayout(self, win):
        #put frames in a grid
        #left column
        self.threadingFrame.grid(row=0, column=0)
        self.drawdownFrame.grid(row=1, column=0, rowspan=3)

        #centre column
        self.tieupFrame.grid(row=0, column=1,sticky=tk.S+tk.W)
        self.treadlingFrame.grid(row=1, column=1, rowspan=3)

        #right column
        self.threadingOptionsFrame.grid(row=0,column=2)
        self.tieupOptionsFrame.grid(row=1, column=2)
        self.treadlingOptionsFrame.grid(row=2,column=2)
        self.generalOptionsFrame.grid(row=3, column=2)

    def makeGeneralOptions(self,win):
        generalOptionsFrame = tk.Frame(win, borderwidth=3, relief=tk.RAISED, width=0)

	# ends
        label = tk.Label(generalOptionsFrame, text="# ends", width=0)
        label.grid(row=0,column=0)
        self.var_numEnds = tk.StringVar(win)
        e = tk.Entry(generalOptionsFrame, textvariable=self.var_numEnds, width=3)
        e.grid(row=0,column=1)
        self.var_numEnds.set(str(self.numEnds))

        # shafts
        label = tk.Label(generalOptionsFrame, text="# shafts", width=0)
        label.grid(row=1,column=0)
        self.var_numShafts = tk.StringVar(win)
        e = tk.Entry(generalOptionsFrame, textvariable=self.var_numShafts, width=3)
        e.grid(row=1,column=1)
        self.var_numShafts.set(str(self.numShafts))

        # treadles
        label = tk.Label(generalOptionsFrame, text="# treadles", width=0)
        label.grid(row=2,column=0)
        self.var_numTreadles = tk.StringVar(win)
        e = tk.Entry(generalOptionsFrame, textvariable=self.var_numTreadles, width=3)
        e.grid(row=2,column=1)
        self.var_numTreadles.set(str(self.numTreadles))

	# time
        label = tk.Label(generalOptionsFrame, text="# picks", width=0)
        label.grid(row=3,column=0)
        self.var_t_end = tk.StringVar(win)
        e = tk.Entry(generalOptionsFrame, textvariable=self.var_t_end, width=3)
        e.grid(row=3,column=1)
        self.var_t_end.set(str(self.t_end))

        b = tk.Button(generalOptionsFrame, text="Update", command=self.updateGeneralOptions, width=0)
        b.grid(row=4,column=0,columnspan=2)


        self.generalOptionsFrame = generalOptionsFrame

    def updateGeneralOptions(self):
        self.numEnds = int(self.var_numEnds.get())
        self.numShafts = int(self.var_numShafts.get())
        self.numTreadles = int(self.var_numTreadles.get())
        self.t_end = int(self.var_t_end.get())
        
        self.makeThreadingGUI(self.win)
	self.makeTreadlingGUI(self.win)
        self.makeTieupGUI(self.win)
        self.makeDrawdownGUI(self.win)
        self.drawDown()
        
    def makeTieupOptions(self,win):
        tieupOptionsFrame = tk.Frame(win, borderwidth=3, relief=tk.RAISED)

        b = tk.Button(tieupOptionsFrame, text="Clear tieup", command=self.clearTieup)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        b = tk.Button(tieupOptionsFrame, text="Fill tieup", command=self.fillTieup)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        b = tk.Button(tieupOptionsFrame, text="Inverse tieup", command=self.inverseTieup)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        b = tk.Button(tieupOptionsFrame, text="Save draft", command=self.saveDraft)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        b = tk.Button(tieupOptionsFrame, text="Load draft", command=self.loadDraft)
        b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.tieupOptionsFrame = tieupOptionsFrame

    def saveDraft(self):
        f = tkFileDialog.asksaveasfile(defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return

        # write dimensions
        f.write(str(self.numEnds)+'\n')
        f.write(str(self.numShafts)+'\n')
        f.write(str(self.numTreadles)+'\n')
        f.write(str(self.t_end)+'\n')

        # write threading
        for end in range(self.numEnds):
            f.write(str(self.shaftsEndsAreOn[end].get()) + ' ')
        f.write('\n')

        # write warp colours
        for end in range(self.numEnds):
            f.write(str(self.warpColours[end].get()) + ' ')
        f.write('\n')

        # write tieup
        for shaft in range(self.numShafts):
            for treadle in range(self.numTreadles):
                f.write(str(self.shaftsOnEachTreadle[treadle][shaft].get()) + ' ')
            f.write('\n')

        # write treadling
        for t in range(self.t_end):
            f.write(str(self.treadlesAtEachTimeStep[t].get()) + ' ')
        f.write('\n')

        # write weft colours
        for t in range(self.t_end):
            f.write(str(self.weftColours[t].get()) + ' ')
        f.write('\n')

        f.close();

    def loadDraft(self):
        f = tkFileDialog.askopenfile(defaultextension=".txt")
        if f is None:
            return

        try:
        
            # read dimensions
            self.numEnds = int(f.readline().strip())
            self.numShafts = int(f.readline().strip())
            self.numTreadles = int(f.readline().strip())
            self.t_end = int(f.readline().strip())
	
            if(not (self.numEnds and self.numShafts and self.numTreadles and self.t_end) ):
                print 'Ignoring load request because file is not appropriate'
                return

            else:
                # update sizes of GUIs/vars
                self.makeThreadingGUI(self.win)
                self.makeTreadlingGUI(self.win)
                self.makeTieupGUI(self.win)
                self.makeDrawdownGUI(self.win)

                # read threading
                line = f.readline().strip();
                values = line.split(' ');
                values = map(int,values);
                for end in range(self.numEnds):
                    self.shaftsEndsAreOn[end].set(values[end])

                # read warp colours
                line = f.readline().strip();
                values = line.split(' ');
                values = map(int,values);
                for end in range(self.numEnds):
                    self.warpColours[end].set(values[end])
  
                # read tieup
                for shaft in range(self.numShafts):
                    line = f.readline().strip();
                    values = line.split(' ');
                    values = map(int,values);
                    for treadle in range(self.numTreadles):
                       self.shaftsOnEachTreadle[treadle][shaft].set(values[treadle])
 
                # read treadling
                line = f.readline().strip();
                values = line.split(' ');
                values = map(int,values);
                for t in range(self.t_end):
                    self.treadlesAtEachTimeStep[t].set(values[t])
  
                # read weft colours
                line = f.readline().strip();
                values = line.split(' ');
                values = map(int,values);
                for t in range(self.t_end):
                    self.weftColours[t].set(values[t])
  
            f.close();


            self.var_numEnds.set(numEnds)
            self.var_numShafts.set(numShafts)
            self.var_numTreadles.set(numTreadles)
            self.var_t_end.set(t_end)
            self.drawDown()

        except:
            print('Draft not read properly')

    def clearTieup(self):

        for treadle in range(self.numTreadles):
            for shaft in range(self.numShafts):
                self.shaftsOnEachTreadle[treadle][shaft].set(0)
        self.drawDown()

    def fillTieup(self):
        for treadle in range(self.numTreadles):
            for shaft in range(self.numShafts):
                self.shaftsOnEachTreadle[treadle][shaft].set(1)
        self.drawDown()

    def inverseTieup(self):
        for treadle in range(self.numTreadles):
            for shaft in range(self.numShafts):
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

        for end in reversed(range(self.numEnds)): #start at right hand side
            self.shaftsEndsAreOn[end].set(self.numShafts-1-shaft) #update radio button
            if direction == 1:
                shaft += 1
                if shaft > self.numShafts-1: #reached upper point - switch directions
                    shaft = self.numShafts - 2
                    direction = 0
            else:
                shaft -= 1
                if shaft < 0: #reached lower point - switch directions
                    shaft = 1
                    direction = 1
        self.drawDown()

    def straightThreading(self):
        for end in range(self.numEnds):
            self.shaftsEndsAreOn[end].set(self.numShafts-1-((self.numEnds-1-end)%self.numShafts)) #update radio button
        self.drawDown()

    def inverseThreading(self):
        for end in range(self.numEnds):
            currentShaft = self.shaftsEndsAreOn[end].get()
            self.shaftsEndsAreOn[end].set(self.numShafts-1-currentShaft) #update radio button
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

        for t in range(self.t_end):
            self.treadlesAtEachTimeStep[t].set(treadle) #update radio button
            if direction == 1:
                treadle += 1
                if treadle > self.numTreadles - 1: #reached upper point - switch directions
                    treadle = self.numTreadles - 2
                    direction = 0
            else:
                treadle -= 1
                if treadle < 0: #reached lower point - switch directions
                    treadle = 1
                    direction = 1
        self.drawDown()

    def straightTreadling(self):
        for t in range(self.t_end):
            self.treadlesAtEachTimeStep[t].set(t%self.numTreadles) #update radio button
        self.drawDown()

    def inverseTreadling(self):
        for t in range(self.t_end):
            currentTreadle = self.treadlesAtEachTimeStep[t].get()
            self.treadlesAtEachTimeStep[t].set(self.numTreadles-1-currentTreadle) #update radio button
        self.drawDown()



    def drawDown(self):

        threading = np.zeros((self.numShafts, self.numEnds))
        for end in range(self.numEnds):
            threading[self.shaftsEndsAreOn[end].get(),end] = 1

        tieup = np.zeros((self.numShafts, self.numTreadles))
        for treadle in range(self.numTreadles):
            for shaft in range(self.numShafts):
                tieup[shaft,treadle] = self.shaftsOnEachTreadle[treadle][shaft].get()

        treadling = np.zeros((self.t_end, self.numTreadles))
        for t in range(self.t_end):
            treadling[t,self.treadlesAtEachTimeStep[t].get()] = 1

        dd=np.zeros((self.t_end,self.numEnds))
        for t in range(self.t_end):
            dd[t,:] = self.weftColours[t].get() #unlifted threads show the weft's colour
            treadle = treadling[t,:].tolist().index(1)
            shaftsLifted=tieup[:,treadle]
            for j in range(len(shaftsLifted)):
                if shaftsLifted[j]==1:
                    for i in range(self.numEnds):
                        if threading[j,i] == 1:
                            dd[t,i]=self.warpColours[i].get() #lifted threads show warp's colour

        self.displayDrawdown(dd)

    def displayDrawdown(self,drawdown):
        drawdown=np.array(drawdown*255,dtype=int)
        data = np.repeat(np.repeat(drawdown, width_pick, axis=0), width_end, axis=1)

        from PIL import Image, ImageTk
        canvas = tk.Canvas(self.drawdownFrame, width=self.numEnds*width_end, height=self.t_end*width_pick)
        canvas.place(x=-2,y=-2)

        self.im=Image.fromstring('L', (data.shape[1],\
                        data.shape[0]), data.astype('b').tostring())

        self.imTk = ImageTk.PhotoImage(image=self.im)
        canvas.create_image(0,0,image=self.imTk,anchor=tk.NW)


mw = tk.Tk()
numEnds = 20
numShafts = 4
numTreadles = 10
t_end = 20
app = WeavingDraft(mw, numEnds, numShafts, numTreadles, t_end)
mw.mainloop()


# Alexander Shelton
#
#
#
#



import matplotlib
matplotlib.use("TkAgg") #MPL backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #canvas & nav
from matplotlib.figure import Figure
import matplotlib.animation as animation #
from matplotlib import style
from matplotlib import pyplot

import tkinter as tk #GUI
from tkinter import ttk #styling

import urllib
import json

import pandas as pd #csv work
import numpy as np #number crunching


LARGE_FONT = ("Verdana", 12)
NORMAL_FONT= ("Verdana", 10)#normal text info
SMALL_FONT= ("Verdana", 18)#Captions etc


style.use("ggplot") #styling for matplotlib

# Figure subplot
f = Figure() #matplotlib figure
a = f.add_subplot(111)

exchange = 'BTC Markets' #Starting exchange
programName='btcmarkets'
dataCounter = 9000 #Number will force update


def changeExchange(whatExchange, pn):
    global exchange #Default exchange
    global programName #What the program variable is
    global dataCounter #counter force update

# Changing base vars that determine exchanges
    programName = pn
    exchange = whatExchange
    dataCounter = 9000




def popupmsg(msg):
    popup = tk.Tk() #creating a new tk instance
    
    popup.wm_title('!')
    label = ttk.Label(popup,text=msg, font=NORMAL_FONT)
    label.pack(side="top", fill='x', pady=10)

    b1= ttk.Button(popup, text='Okay', command=popup.destroy)
    b1.pack()
    popup.mainloop()


#animate function for live graphing core of data crunch
def animate(rate):


    #TODO FIx this animate with from the day data pull from web server json

    dataLink = 'https://api.btcmarkets.net/market/ETH/BTC/trades?limit=100'
    data = urllib.request.urlopen(dataLink) #Accessing the link using requests
    data = data.read().decode("utf-8") #deocde to utf8 and read into a json
    data = json.loads(data) #size = 500

    data = pd.DataFrame(data) #use pandas to create a csv
    buys = data #dictionary
    buys["datestamp"] = np.array(buys["date"]).astype("datetime64[s]") #Take the buys from the keyvalue in json
    buyDates = (buys["datestamp"]).tolist() #Take the dates from buys key value

    a.clear()
    a.plot_date(buyDates, buys["price"],'#00A3E0', label='Buys') #plotting

    #Creating a map legend, inside params are just so data cant be covered by legend
    a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=3,ncol=2,borderaxespad=0)

    
    title = 'ETH USD Prices\nLast Price in BTC: '+str(buys['price'][499]) #Title for graph
    a.set_title(title) #initializing title


class EtherBody(tk.Tk):#Inherits tk class
    def __init__(self, *args, **kwargs): #Self implied, *args = arguments, **kewargs = key words args(dictionaries)
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self,default='ether.ico') #icon
        tk.Tk.wm_title(self, 'Ethereum Client')

        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand=True)
        container.grid_rowconfigure(0, weight=1) #0 = min size
        container.columnconfigure(0,weight=1)

        #Creating a menu bar
        menuBar = tk.Menu(container)
        #creating a sub menu inside of the menu bar, 'tearoff' allows you to seperate menu bar to its on window
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label='Save Settings', command= lambda: popupmsg('not supported yet')) #gives a label to allow user to save settings they have created
        fileMenu.add_separator() #Adds a bar to serperate menu options
        fileMenu.add_command(label='exit', command=quit)
        menuBar.add_cascade(label='FIle', menu=fileMenu) #adds the dropdown menu to the original Menu holder


        exchangeChoice = tk.Menu(menuBar, tearoff=1) #creating a menu that can be torn off, allows user to choose which exchange they want
        #Adding menu items, inside changeExchange function params are: (Display Name, variable name) to be used in the function
        exchangeChoice.add_command(label='Coinbase', command = lambda: changeExchange('Coinbase','coinbase'))
        exchangeChoice.add_command(label='Coinmama', command = lambda: changeExchange('Coinmama','coinmama'))
        exchangeChoice.add_command(label='CEX.io', command = lambda: changeExchange('CEX.io','cexio'))
        exchangeChoice.add_command(label='BTC Markets', command = lambda: changeExchange('BTC Markets','btcmarkets'))




        tk.Tk.config(self,menu=menuBar) #Configures window to hold ->  menu: 'menubar'

        self.frames = {} #Empty dictionary of franes
        # Add new pages to the list
        for F in (StartPage,EtherPage):  #for loop of tuple of page names
            frame = F(container, self) # creating a value
            self.frames[F] = frame #Putting key value into dictionary 
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont] #Takes key value from frames dict
        frame.tkraise() #tkraise raises to the front page
    


class StartPage(tk.Frame):#inherits from frame 
    def __init__(self, parent, controller): #parent = parent class such as EtherBody
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text='Ethereum trading application', font='LARGE_FONT')
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text='Agree', command=lambda: controller.show_frame(EtherPage))
        button.pack()

        button1 = ttk.Button(self, text='Disagree', command=quit)
        button1.pack()

        
class PageOne(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text='Page 1', font='LARGE_FONT')
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text='Back to home', command=lambda: controller.show_frame(StartPage))
        button.pack()



class EtherPage(tk.Frame):
     def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text='Graph Page', font='LARGE_FONT')
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text='Back to home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # outputting
        canvas = FigureCanvasTkAgg(f, self) 
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        #nav bar
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack()

## Running ##
app = EtherBody()
app.geometry('1280x720') # Setting the window size to 1280x720 res          Default use 800x600 if no 720p
ani = animation.FuncAnimation(f,animate, interval=2000 ) #animation instance (figure, animate, interval -ms-)
app.mainloop()
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
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker #modify dates and ticker in the data

import tkinter as tk #GUI
from tkinter import ttk #styling

import urllib
import json

import pandas as pd #csv work
import numpy as np #number crunching


LARGE_FONT = ("Verdana", 12)
NORMAL_FONT= ("Verdana", 10)#normal text info
SMALL_FONT= ("Verdana", 18)#Captions etc

ABOUT_TEXT = '''Program contributers: Alex Shelton
This program is free to use and alter for any purposes
Created to learn more about tkinter and make me some money'''

style.use("ggplot") #styling for matplotlib

# Figure subplot
f = Figure() #matplotlib figure
a = f.add_subplot(111)


#Default settings:
exchange = 'BTC Markets' #Starting exchange
programName='btcmarkets'
forceUpdate = 9000 #Number will force update
paneCount = 1 #Number of windows

resampleSize = '15min' #default sample size = 15min
dataPace  ='tick' #default graph has a days worth of pricing data
candleWidth = '.008' #default candle width

topIndicator = 'none'
bottomIndicator = 'none'
mainIndicator = 'none'

EMAS = [] #Exponential moving average
SMAS = [] #Simple moving average

chartLoad = True
## End default settings




def tutorial():
    
    #Sucsession of tutorial pages. once user leaves one page button takes them to the next page destroying old page
    
    def page2():
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            tut2.destroy()
            tut3 = tk.Tk()

            tut3.wm_title('part 3')
            label = ttk.Label(tut3, text='Part 3', font = NORMAL_FONT)
            label.pack(side='top', fill='x', pady=10)
            nextB = ttk.Button(tut3, text='Done', command = tut3.destroy)
            nextB.pack()

            tut3.mainloop()

        tut2.wm_title('part 2')
        label = ttk.Label(tut2, text='Part 2', font = NORMAL_FONT)
        label.pack(side='top', fill='x', pady=10)
        nextB = ttk.Button(tut2, text='Next', command = page3)
        nextB.pack()

        tut2.mainloop()
    
    tut = tk.Tk()
    tut.wm_title('Tutorial')
    label = ttk.Label(tut, text='What do you need help with? ', font = NORMAL_FONT)
    label.pack(side='top', fill='x', pady=10)

    overviewButton = ttk.Button(tut, text="Overview of the application", command = page2)
    overviewButton.pack()

    howTrade = ttk.Button(tut, text="How do I trade with this client?", command = lambda: popupmsg('not yet completed'))
    howTrade.pack()

    helpIndicator = ttk.Button(tut, text="Indicator question/help", command = lambda: popupmsg('not yet completed'))
    helpIndicator.pack()

    tut.mainloop()
    



def loadChart(run):
    global chartLoad
    if run == 'start':
        chartLoad = True
    elif run == 'stop':
        chartLoad = False

# About inside of help menu gives info about author(s) and program
def about():
    about = tk.Tk()
    about.wm_title('About this application')
    about.geometry('600x600')
    label = ttk.Label(about, text = ABOUT_TEXT)
    label.pack(side='top')



#Indicators for top and bottom
def addIndicator(option, where):
    global topIndicator
    global bottomIndicator
    global mainIndicator
    global forceUpdate

    #Adding indicators to the top:
    if where != 'main':
        if dataPace == 'tick':
            popupmsg('Indicators in tick data is not available')
        elif option == 'none':
            if where == 'top':
                topIndicator = option
            else:
                bottomIndicator = option
            forceUpdate = 9000 #Forcing an update after the indicator change
        elif option == 'rsi':
            #Must create a window to ask user by what period do they want rsi calculated in: default = 14 days
            rsiQuestion = tk.Tk()
            rsiQuestion.wm_title('Period?')

            label = ttk.Label(rsiQuestion, text='Choose how many periods you want each RSI calculation to consider ')
            label.pack(side='top')

            answer = ttk.Entry(rsiQuestion) #Placing the entry inside of the widnow rsiQuestion
            answer.insert(0,14) #inserting 14 into the first index for a default value:
            answer.pack()
            answer.focus_set()

            def callBack(where):
                global topIndicator
                global bottomIndicator
                global forceUpdate

                periods = answer.get()
                group = []
                group.append('rsi')
                group.append(periods)

                if where == 'top':
                    topIndicator = group
                    print("Set top indicator to: ", group)
                elif where == 'bottom':
                    bottomIndicator = group
                    print("Set bottom indicator to: ", group)
                else:
                    print("Error")
                #Forcing a reset
                forceUpdate = 9000
                rsiQuestion.destroy()
            
            b = ttk.Button(rsiQuestion, text='Submit', width=10, command= lambda: callBack(where))
            b.pack()
            tk.mainloop()
        
        elif option =='macd':
            if where == 'top':
                topIndicator = 'macd'
            elif where == 'bottom':
                bottomIndicator = 'macd'
            forceUpdate = 9000 #Forcing update


# Middle / Main indicator change/adds
def addMainIndicator(option, where):
    global mainIndicator
    global forceUpdate

    if dataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')
    
    if option != 'none':
        question = tk.Tk()
        question.wm_title('Periods?')
        label = ttk.Label(question, text='Choose how many periods for '+option.upper())
        label.pack(side='top', fill='x', pady=10)
        answer = ttk.Entry(question)
        answer.insert(0,10)
        answer.pack()
        answer.focus_set()

        def callBack(option):
            global mainIndicator
            global forceUpdate

            if(mainIndicator == 'none'):
                mainIndicator = []
            
            periods = answer.get()
            group = []
            group.append(option)
            group.append(int(periods))
            mainIndicator.append(group)
            forceUpdate = 9000
            print('Middle indicator set to: ', mainIndicator)
            question.destroy()
        
        button = ttk.Button(question, text='Submit', width=10, command = lambda: callBack(option))
        button.pack()
        tk.mainloop()

    else:
        mainIndicator = 'none'





def changeTimeFrame(timeFrame):
    global dataPace
    global forceUpdate

    if timeFrame == '7d' and resampleSize == '1min': #Will be too ugly
        popupmsg('Too much data selected, choose a smaller time frame or OHLC')
    else:
        dataPace = timeFrame
        forceUpdate = 9000 #Forces an update

def changeSampleSize(size, width):
    global resampleSize
    global forceUpdate
    global candleWidth

    if dataPace == '7d' and resampleSize == '1min': #Will be too ugly
        popupmsg('Too much data selected, choose a smaller time frame or OHLC')
    elif dataPace == 'tick':
        popupmsg("You're curently viewing tick data not OHLC")
    else:
        resampleSize = size
        forceUpdate = 9000 #force update
        candleWidth = width



def changeExchange(whatExchange, pn):
    global exchange #Default exchange
    global programName #What the program variable is
    global forceUpdate #counter force update

# Changing base vars that determine exchanges
    programName = pn
    exchange = whatExchange
    forceUpdate = 9000



# Pop up msg will be used to give the user an important info or throw an error
def popupmsg(msg):
    popup = tk.Tk() #creating a new tk instance
    
    popup.wm_title('!') #title on window will be '!'
    label = ttk.Label(popup,text=msg, font=NORMAL_FONT) #Creating the label: The text will be whats passed through and in normal font
    label.pack(side="top", fill='x', pady=10)

    b1= ttk.Button(popup, text='Okay', command=popup.destroy) #Creating a button on the popup window once clicked will close popup
    b1.pack()
    popup.mainloop() #run main loop of pop up


#animate function for live graphing core of data crunch
def animate(rate):
    global refreshRate
    global forceUpdate

    if chartLoad == True:
        if paneCount == 1:
            if dataPace == 'tick':
                try:
                    
                    a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4) #Full grid size, starting point, row span, column span
                    a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=a) #sharex shares x intercept with subplot 'a'


                    dataLink = 'https://api.btcmarkets.net/market/ETH/BTC/trades?limit=100'
                    data = urllib.request.urlopen(dataLink) #Accessing the link using requests
                    data = data.read().decode("utf-8") #deocde to utf8 and read into a json
                    data = json.loads(data) #size = 500

                    data = pd.DataFrame(data) #use pandas to create a csv


                    buys = data #dictionary
                    buyDates = data["date"].tolist()
                    #buys["datestamp"] = np.array(buys["date"]).astype("datetime64[s]") #Take the buys from the keyvalue in json
                    buyDates = (buys["datestamp"]).tolist() #Take the dates from buys key value
                    volume = data['amount']

                    a.clear()
                    a.plot_date(buyDates, buys["price"],'#00A3E0', label='Buys') #plotting
                    a2.fill_between(buyDates,0, volume, facecolor='#183A54' ) #specify min point, data plotted, face color
                    
                    a.xaxis.set_major_locator(mticker.MaxNLocator(5)) #
                    a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%D %H:M:S'))
                    
                    
                    #Creating a map legend, inside params are just so data cant be covered by legend
                    a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=3,ncol=2,borderaxespad=0)

                    
                    title = 'ETH USD Prices\nLast Price in BTC: '+str(buys['price'][499]) #Title for graph  ## Price index is pulling the last given index of a trade in json for latest data
                    a.set_title(title) #initializing title
                
                except Exception as e:
                    print("Failed because of ", e)




    # #TODO FIx this animate with from the day data pull from web server json

    # dataLink = 'https://api.btcmarkets.net/market/ETH/BTC/trades?limit=100'
    # data = urllib.request.urlopen(dataLink) #Accessing the link using requests
    # data = data.read().decode("utf-8") #deocde to utf8 and read into a json
    # data = json.loads(data) #size = 500

    # data = pd.DataFrame(data) #use pandas to create a csv
    # buys = data #dictionary
    # buys["datestamp"] = np.array(buys["date"]).astype("datetime64[s]") #Take the buys from the keyvalue in json
    # buyDates = (buys["datestamp"]).tolist() #Take the dates from buys key value

    # a.clear()
    # a.plot_date(buyDates, buys["price"],'#00A3E0', label='Buys') #plotting

    # #Creating a map legend, inside params are just so data cant be covered by legend
    # a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=3,ncol=2,borderaxespad=0)

    
    # title = 'ETH USD Prices\nLast Price in BTC: '+str(buys['price'][499]) #Title for graph  ## Price index is pulling the last given index of a trade in json for latest data
    # a.set_title(title) #initializing title









class EtherBody(tk.Tk):#Inherits tk class
    def __init__(self, *args, **kwargs): #Self implied, *args = arguments, **kewargs = key words args(dictionaries)
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self,default='ether.ico') #icon
        tk.Tk.wm_title(self, 'Ethereum Client')

        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand=True)
        container.grid_rowconfigure(0, weight=1) #0 = min size
        container.columnconfigure(0,weight=1)

#####     BEGINNING OF MENU CREATIONS     #####

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
        # Adding the menu to the overall menu
        menuBar.add_cascade(label='Exchange', menu = exchangeChoice)

        dataTimeFrame = tk.Menu(menuBar, tearoff=1)
        dataTimeFrame.add_command(label="Tick", command = lambda: changeTimeFrame("tick"))
        dataTimeFrame.add_command(label="1 Day", command = lambda: changeTimeFrame("1d"))
        dataTimeFrame.add_command(label="3 Day", command = lambda: changeTimeFrame("3d"))
        dataTimeFrame.add_command(label="1 Week", command = lambda: changeTimeFrame("7d"))
        #Adding time frame menu to overall menu
        menuBar.add_cascade(label='Time Frame',menu=dataTimeFrame)

        ## OHLC = Open High Low Close    OHLC conflicts with functions -> added an x
        OHLCX = tk.Menu(menuBar, tearoff=1)
        OHLCX.add_command(label="Tick", command = lambda: changeTimeFrame("tick"))

        #Change sample size takes the program name and 2nd param = candlestick width
        OHLCX.add_command(label="1 Minute", command = lambda: changeSampleSize("1min",0.0005))
        OHLCX.add_command(label="5 Minute", command = lambda: changeSampleSize("5min",0.003))
        OHLCX.add_command(label="15 Minute", command = lambda: changeSampleSize("15min",0.008))
        OHLCX.add_command(label="30 Minute", command = lambda: changeSampleSize("30min",0.016))
        OHLCX.add_command(label="1 Hour", command = lambda: changeSampleSize("1h",0.032))
        OHLCX.add_command(label="3 Hour", command = lambda: changeSampleSize("3h",0.096))
        #Adding the open high low close menu to the menuBar menu
        menuBar.add_cascade(label='OHLC Index', menu=OHLCX)
        
        #Indicator menu:
        topIndicator = tk.Menu(menuBar, tearoff=1)
        topIndicator.add_command(label='None', command= lambda: addIndicator('none', 'top'))
        topIndicator.add_command(label='RSI', command= lambda: addIndicator('rsi', 'top')) #Relative strength index: default = 14
        topIndicator.add_command(label='MACD', command= lambda: addIndicator('macd', 'top'))

        menuBar.add_cascade(label = 'Top Indicator', menu= topIndicator)

        #Main graph Indicator
        mainIndicator = tk.Menu(menuBar, tearoff=1)
        mainIndicator.add_command(label='None', command= lambda: addMainIndicator('none', 'main'))
        mainIndicator.add_command(label='SMA', command= lambda: addMainIndicator('sma', 'main')) #Simple moving average
        mainIndicator.add_command(label='EMA', command= lambda: addMainIndicator('ema', 'main')) #Exponential moving average

        menuBar.add_cascade(label = 'Main / Middle Indicator', menu= mainIndicator)

        # Bottom indicator 
        bottomIndicator = tk.Menu(menuBar, tearoff=1)
        bottomIndicator.add_command(label='None', command= lambda: addIndicator('none', 'bottom'))
        bottomIndicator.add_command(label='RSI', command= lambda: addIndicator('rsi', 'bottom')) #relative strength index
        bottomIndicator.add_command(label='MACD', command= lambda: addIndicator('macd', 'bottom'))

        menuBar.add_cascade(label = 'Bottom Indicator', menu= bottomIndicator)

        #Trading menu for buy & sell
        tradeButton = tk.Menu(menuBar, tearoff=1)
        tradeButton.add_command(label='Manual trading',
        command = lambda: popupmsg('This is not running yet'))

        tradeButton.add_command(label='Automated trading',
        command = lambda: popupmsg('This is not running yet'))

        tradeButton.add_separator()

        tradeButton.add_command(label='Quick buy',
        command = lambda: popupmsg('This is not running yet'))

        tradeButton.add_command(label='Quick sell',
        command = lambda: popupmsg('This is not running yet'))

        tradeButton.add_separator()

        tradeButton.add_command(label='Set-up quick buy/sell',
        command = lambda: popupmsg('This is not running yet'))

        menuBar.add_cascade(label='Trading', menu = tradeButton)

        #Start and stop menu:
        startStop = tk.Menu(menuBar, tearoff=1)
        startStop.add_command(label = 'Resume', command = lambda: loadChart('start') )
        startStop.add_command(label = 'Pause', command = lambda: loadChart('stop') )

        menuBar.add_cascade(label = 'Reusme / Pause', menu = startStop)


        helpMenu = tk.Menu(menuBar, tearoff = 1)
        helpMenu.add_command(label = 'Tutorial', command = tutorial)
        helpMenu.add_command(label = 'About', command = about)

        menuBar.add_cascade(label = 'Help', menu = helpMenu)

        #####     END MENU     #####






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

        button1 = ttk.Button(self, text='Exit', command=quit)
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

#TODO: Plot limits
#TODO: get average distance between each nm and plot it
#TODO: fix colors for neuromasts to deal with different numbers (TNM always same color)
#TODO: Statistics for nm number



#imports

from tkinter import filedialog
from tkinter import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import scipy as scipy
from PyPDF2 import PdfFileMerger
import plotly
import os
import sys
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
import glob
import datetime as dt

#DEF FUNCTIONS

#default color array
colorArray = [(0.6313725490196078, 0.788235294117647, 0.9568627450980393),
 (1.0, 0.7058823529411765, 0.5098039215686274),
 (0.5529411764705883, 0.8980392156862745, 0.6313725490196078),
 (1.0, 0.6235294117647059, 0.6078431372549019),
 (0.8156862745098039, 0.7333333333333333, 1.0),
 (0.8705882352941177, 0.7333333333333333, 0.6078431372549019),
 (0.9803921568627451, 0.6901960784313725, 0.8941176470588236),
 (0.8117647058823529, 0.8117647058823529, 0.8117647058823529),
 (1.0, 0.996078431372549, 0.6392156862745098),
 (0.7254901960784313, 0.9490196078431372, 0.9411764705882353)]

#default line styles
lineStyleArray = ["-", "-", "-","-", "-", "-","-", "-", "-","-"]



def makeKDEPlot(dataArray, title, cols = colorArray, lines = lineStyleArray):

    plt.close()

    f, ax = plt.subplots(figsize=(22, 6))

    for idx, col, line in zip(dataArray, cols, lines):
        if len(myData[idx].dropna()) < 3:
            continue;
        else:
            sns.kdeplot(myData[idx].dropna(), bw=100, color=col, label=idx, linestyle=line, lw=3)
            plt.xlim(0, 2500)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.set_title(title)
    ax.set_ylabel("Probability")
    ax.set_xlabel("Neuromast Distance from Otic Vesicle (um)")



    return f, ax

def quitUI():
    root.quit()
    root.destroy()

def makeList():
    values = [listbox.get(idx) for idx in listbox.curselection()]
    myFig, ax = makeKDEPlot(values, "title")

    newwin = Toplevel(root)
    display = Label(newwin, text="Plot")

    canvas = FigureCanvasTkAgg(myFig, master=newwin)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, root)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

def clearList():
    listbox.selection_clear(0, END)

def myTest():
    print("test")


def makeBoxAndWhiskerPlot(Neuromast_DataFrame, nameArray):

    #print(Neuromast_DataFrame)
    #print(nameArray)
    f, ax = plt.subplots(figsize=(22, 6))
    #sns.boxplot(x="variable", data=Neuromast_DataFrame.melt(Neuromast_DataFrame))
    #

    newdf = pd.melt(Neuromast_DataFrame, value_vars=nameArray)

    nm_plot=sns.boxplot(x="variable", y="value", data=newdf, color='lightgrey')
    nm_plot=sns.swarmplot(x='variable', y='value',
              data=newdf,
              color='black',
              alpha=0.75)

    ax.set_title("Number of Neuromasts, Excluding Terminal Cluster")
    ax.set_ylabel("Number of Non-Terminal Neuromasts")
    ax.set_xlabel("Condition")

    #sns.boxplot(Neuromast_DataFrame[['DMSO', '1uM', '5uM']])
    #plt.show()
    #sns.boxplot(Neuromast_DataFrame[nameArray].dropna())
    return f, ax

def doStats(values, my_dataframe):
    df = pd.DataFrame(columns=values)
    df.set_index(values)
    print(type(df.index))
    for idx in values:
         statRowArray = []
         x = my_dataframe.loc[:,idx]#.dropna()
         for indx in values:
             y = my_dataframe.loc[:,indx]#.dropna()
             pvalue = scipy.stats.ttest_ind(x, y)[1]
             pvalue_round = round(pvalue, 5)
             statRowArray.append(pvalue_round)
         df.loc[len(df)] = statRowArray

    df[''] = values
    df.set_index('',inplace=True)

    fig, ax = plt.subplots()
    ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.axis('off')

    return fig




def merge_PDF(filelist):



    pdf_merger = PdfFileMerger()
    file_handles = []
    print(os.getcwd())
    input_paths = (glob.glob(os.getcwd() + "/*.pdf"))

    #myFiles = []

    #for filename in os.listdir(os.getcwd()):
    #    if filename.endswith('.pdf'):
    #        myFiles.append(filename)

    print(filelist)

    for path in filelist:
        pdf_merger.append(path)



    with open("merge.pdf", 'wb') as fileobj:
        pdf_merger.write(fileobj)

def MegaAnalyze(colnames):

    file_list = []
    graph_index = 0;

    time = dt.datetime.now();
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    path = (os.getcwd())
    os.mkdir(path + "\\output_" + timestamp)
    savePath = path + "\\output_" + timestamp
    os.chdir(savePath)

    myMatrix, nameArray = getConditions(colnames)


    #print(colnames)
    for idx, condition in enumerate(nameArray):
        myList = []
        for colname in colnames:
            if colname.split('_')[0] == condition:
                myList.append(colname)
        myFig, ax = makeKDEPlot(myList, condition)
        if ax.lines:
            filename = str(graph_index) + "_" + condition + ".pdf"
            myFig.savefig(filename)
            file_list.append(filename)
            graph_index = graph_index + 1


    #make plot of number of nm
    neuromastNumberArray = pd.DataFrame()
    for idx, condition in enumerate(nameArray):
        myList = []
        for colname in colnames:
            if colname.split('_')[0] == condition:
                myList.append(colname)
        tempList = (countNM(myList))
        tempSeries = pd.Series(tempList)
        neuromastNumberArray[condition] = tempSeries.values
    neuromastNumberArray[neuromastNumberArray < 0] = np.nan
    neuromastNumberArray = neuromastNumberArray.astype(float)
    #print("neuromast Array before dropna()")
    #print(neuromastNumberArray)
    #neuromastNumberArray = neuromastNumberArray.dropna()
    #print("neuromastArray = ")
    #print(neuromastNumberArray)
    Fig, ax = makeBoxAndWhiskerPlot(neuromastNumberArray, nameArray)
    filename = str(graph_index) +  "_neuromast_number.pdf"
    Fig.savefig(filename)
    file_list.append(filename)
    graph_index = graph_index + 1
    statPlot = doStats(nameArray, neuromastNumberArray)
    filename = str(graph_index)  + "nmnumber_stats.pdf"
    statPlot.savefig(filename)



    # find the longest lists
    maxListSize = 0;
    for list in myMatrix:
        if len(list) > maxListSize:
            maxListSize = len(list)
    #print("max list length is " + str(maxListSize) + " which is " + str(maxListSize-2) + " neuromasts")

    #make a matrx of all neuromasts for each condition
    Neuromast_List = []
    for lists in myMatrix:
        for i in range (1, maxListSize):
            current_nm = "L" + str(i)
            if current_nm in lists:
                Neuromast_List.append(lists[0] + "_" + current_nm)

    #make plots for each inidividual neuromast
    for i in range (1, maxListSize-1):
        myPlots = []
        for nm in Neuromast_List:
            if "L" + str(i) in nm:
                myPlots.append(nm)
        myFig, ax = makeKDEPlot(myPlots, "L" + str(i))
        if ax.lines:
            filename = str(graph_index) + "_L" + str(i) + ".pdf"
            myFig.savefig(filename)
            file_list.append(filename)
            graph_index = graph_index + 1
            statPlot = doStats(myPlots, myData)
            filename = str(graph_index)  + "_L" + str(i) + "_stats.pdf"
            statPlot.savefig(filename)
            file_list.append(filename)
            graph_index = graph_index + 1
        print(myPlots)

    #get the terminal neuromasts
    terminal_array = []
    for condition in nameArray:
        terminal_array.append(condition + "_TNM")
    myFig, ax = makeKDEPlot(terminal_array, "Terminal Neuromast Cluster")
    if ax.lines:
        filename = str(graph_index) + "_TNM.pdf"
        myFig.savefig(filename)
        file_list.append(filename)
        graph_index = graph_index + 1
        statPlot = doStats(terminal_array, myData)
        filename = str(graph_index) + "_TNM_stats.pdf"
        statPlot.savefig(filename)
        file_list.append(filename)
        graph_index = graph_index + 1

    merge_PDF(file_list)






#colnames = ["DMSO_L1", "DMSO_L2", "DMSO_L3", "DMSO_L4", "DMSO_L5", "DMSO_L6", "DMSO_L7"]

def countNM(colnames):
    df2 = pd.DataFrame()
    for name in colnames:
        df2[name] = myData[name]
    #print(df2)

    return (df2.count(axis=1)-1)
    #df2['number'] = (df2.count(axis=1))
    #print(df2)


def getConditions(colnames):
    nameArray = []
    for name in colnames:
        if name.split('_')[0] not in nameArray:
            nameArray.append(name.split('_')[0])

    myMatrix = []

    for condition in nameArray:
        myNewList = []
        myNewList.append(condition)
        for colname in colnames:
            if colname.split('_')[0] == condition:
                myNewList.append(colname.split('_')[1])
        myMatrix.append(myNewList)
    return myMatrix, nameArray




dataToPlot = []
myFig = None;


root = Tk()
root.wm_title("Neuromast Analysis")
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 0, padx = 0)

#root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
#myData = pd.read_csv(root.filename, encoding='utf-8-sig')

#myData = pd.read_csv("C:/Users/damia/github/Neuromast_Analyzer/Ck66_Compiled Data.csv", encoding='utf-8-sig')
myData = pd.read_csv("C:/Users/dalledam/neuromast_analyzer/Ck66_Compiled Data.csv",encoding='utf-8-sig')

colNames = myData.columns.tolist()




b_quit = Button(root, text="Quit", command=quitUI)
b_quit.pack()

b_stats = Button(root, text="Run Statistics", command = doStats)
b_stats.pack()

b_gen = Button(text="Generate Plot", command = makeList)
b_gen.pack()

b_clear = Button(text="Clear Selection", command = clearList)
b_clear.pack()

b_test = Button(text="Mega Analysis!", command = lambda arg = colNames : MegaAnalyze(colNames))
b_test.pack()

b_clear = Button(text="Test", command = countNM)
b_clear.pack()


# Create a Tkinter variable
tkvar = StringVar(root)

listbox = Listbox(root, selectmode=MULTIPLE, height = 20)
listbox.pack()



for item in colNames:
    listbox.insert(END, item)




root.mainloop()

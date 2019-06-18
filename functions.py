
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *

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



def makeKDEPlot(myData, dataArray, cols = colorArray, lines = lineStyleArray):

    plt.close()


    #myPal = sns.color_palette(sns.color_palette(), n_colors=len(dataArray))

    f, ax = plt.subplots(figsize=(22, 6))

    for idx, col, line in zip(dataArray, cols, lines):
        if len(myData[idx].dropna()) < 3:

            errorwin = Toplevel(root)
            display = Label(errorwin, text="Insufficient data error")
            T = Text(errorwin, height=20, width=50)
            T.pack()
            T.insert(END, "Insufficient Data Points (" + str(len(myData[idx].dropna())) + ") at index "  + idx + ". Need at least three data points. Skipping this column")
            #print("Insufficient Data Points (" + str(len(myData[idx].dropna())) + ") at index "  + idx + ". Need at least three data points. Skipping this column")
        else:
            sns.kdeplot(myData[idx].dropna().astype(int), bw=100, color=col, label=idx, linestyle=line, lw=3)
            plt.xlim(0, 2500)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    return f

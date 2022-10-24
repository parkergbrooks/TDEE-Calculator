import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *
 
 
class Window:
    def __init__(self, master):
        self.master = master
 
        self.Main = Frame(self.master)
        self.master.title('TDEE Calculator')
 
         
 
        
        self.middle = Frame(self.Main)
 
        self.row = 9
        self.col = 8
 
        self.cells = [[None for i in range(self.col+1)] for j in range(self.row+1)]
        
        #Generate the labels for the days of week row
        self.days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for i in range(len(self.days)):
            self.cells[0][i+1] = Label(self.middle, text = self.days[i])
            self.cells[0][i+1].grid(row = 0, column = i+1)

        #generate the labels for the instruction/description col
        self.weightCal = ['Weight','Calories','Weight','Calories','Weight','Calories','Weight','Calories']
        for i in range(len(self.weightCal)):
            self.cells[i+1][0] = Label(self.middle, text = self.weightCal[i])
            self.cells[i+1][0].grid(row = i+1, column = 0)        
            
        #Create the entries avoinf the labels in the grid just made    
        for i in range(1,self.row):
           for j in range(1,self.col):
                self.cells[i][j] = Entry(self.middle, width = 10)
                self.cells[i][j].grid(row = i, column = j)
 
         
        self.middle.pack(padx = 10, pady = 10)

 
        self.bottom = Frame(self.Main)
        
        self.clearButton = Button(self.bottom, text = "Calculate", command = self.calculate)
        self.clearButton.pack(padx = 5, pady = 5, side = RIGHT) 
         
        self.saveButton = Button(self.bottom, text = "Save", command = self.save)
        self.saveButton.pack(padx = 5, pady = 5, side = RIGHT)
 
        self.loadButton = Button(self.bottom, text = "Load", command = self.load)
        self.loadButton.pack(padx = 5, pady = 5, side = RIGHT)
        
        self.clearButton = Button(self.bottom, text = "Clear", command = self.clear)
        self.clearButton.pack(padx = 5, pady = 5, side = LEFT)
         
        self.bottom.pack(padx = 5, pady = 5, expand = True, fill = X)
         
        self.Main.pack(padx = 5, pady = 5, expand = True, fill = X)
 
    def save(self):
        
        #Make a temp Array to hold values
        self.tempTest = np.zeros(shape=(self.row-1,self.col-1))
        
        #Go through all non label cells (any index above [0][n]) and put the data in the array to save as spreadsheet
        for i in range(1,self.row):
                for j in range(1,self.col):
                    if(self.cells[i][j].get() == ''):
                        self.tempTest[i-1][j-1] = -1
                    else:
                        self.tempTest[i-1][j-1] = float(self.cells[i][j].get())
        
        np.savetxt('data.csv', self.tempTest,delimiter=',')
        
    def load(self):
        #Clear to avoid double entries
        self.clear()
        #load in the spreadsheet
        arr = np.loadtxt('data.csv',delimiter=",")
        
        #GO through all the entries in cell and insert data
        for i in range(1,self.row):
            for j in range(1,self.col):
                if(arr[i-1][j-1] != -1):
                    self.cells[i][j].insert(0, arr[i-1][j-1])
                 
    def clear(self):
        #Go through all the entries in cell and delete content
        for i in range(1,self.row):
            for j in range(1,self.col):
                self.cells[i][j].delete(0, 'end')
 
    def calculate(self):
        
        self.weightCal = np.zeros(shape=(self.row-1,self.col-1))
        for i in range(1,self.row):
                for j in range(1,self.col):
                    if(self.cells[i][j].get() == ''):
                        self.weightCal[i-1][j-1] = -1
                    else:
                        self.weightCal[i-1][j-1] = float(self.cells[i][j].get())
        
        self.weight = np.zeros(shape=(4,7))
        self.calories = np.zeros(shape=(4,7))
        self.currWRow = 0
        self.currCRow = 0
        
        for i in range(len(self.weightCal)):
            if i % 2 != 0:
                self.calories[self.currCRow] = self.weightCal[i]
                self.currCRow +=1
            else:
                self.weight[self.currWRow] = self.weightCal[i]
                self.currWRow +=1
        #flatten the weight data from 2d array into 1d array and remove placeholder -1
        
        self.processWeeks(self.weight,self.calories)
        
        self.weight = [i for i in self.weight.flatten() if i != -1]
        self.calories = [i for i in self.calories.flatten() if i != -1]
        
        figWeight, weightPoints = plt.subplots()
        weightPoints.scatter(range(len(self.weight)),self.weight)
        trend = np.polyfit(range(len(self.weight)),self.weight,1)
        p = np.poly1d(trend)
        weightPoints.plot( range(len(self.weight)) , p(range(len(self.weight))) , color="red", linewidth=3, linestyle="--")
        weightPoints.set_title("Weight Trends")
        weightPoints.set_xlabel("Day")
        weightPoints.set_ylabel("Weight")
        figWeight.show()
        
        figCal, calPoints = plt.subplots()
        calPoints.scatter(range(len(self.calories)),self.calories)
        calPoints.set_title("Calories Consumed")
        calPoints.set_xlabel("Day")
        calPoints.set_ylabel("Calories")
        figCal.show()
    
    def processWeeks(self,weight,calories):
        
        #create array to get count of entries in each week row
        self.weekWeightEntries = np.zeros(4)
        self.weekCalEntries = np.zeros(4)
        self.weekSumsWeight = np.zeros(4)
        self.weekSumsCal = np.zeros(4)
        
        #for the weeks in the grid, go through and check count of non -1 entries
        for i in range(4):
            self.weekWeightEntries[i] = 7 - np.count_nonzero(weight[i] == -1)
            self.weekCalEntries[i] = 7 - np.count_nonzero(calories[i]==-1)
            for item in weight[i]:
                if item != -1:
                    self.weekSumsWeight[i] += item
            for item in calories[i]:
                if item != -1:
                    self.weekSumsCal[i] += item

        #Go through and make sure there are no zero entries to avoid Div by Zero Error
        for i in range(4):
            if self.weekWeightEntries[i] == 0:
                self.weekWeightEntries[i] = 1
            if self.weekCalEntries[i] == 0:
                self.weekCalEntries[i] = 1     
                
                       
        #calculate averages based on data and number of entries
        self.weekAvgWeight = self.weekSumsWeight/self.weekWeightEntries
        self.weekAvgCal = self.weekSumsCal/self.weekCalEntries
        
        self.estimatedTdee = np.zeros(4)
        self.startWeight = weight[0][0]
        self.avgTDEE = 0
        self.countTDEE = 0
        
        f = open("tdeeData.txt","w")
        for i in range(4):
            self.weightChange = round((self.startWeight - self.weekAvgWeight[i]),2)
            self.startWeight = self.weekAvgWeight[i]
            
            
            
            #Weight Gain
            if(self.weightChange < 0 and self.weekAvgWeight[i]!= 0):
                #calculate and add estimated TDEE   
                #                        weekly calories - weightChange (lbs) / .001 (lbs)  multiplied by .5 calories per day which causes (.001 lb) weight gain
                self.estimatedTdee[i] = round(self.weekAvgCal[i] - ((abs(self.weightChange) / .001) * (.5)))
                
                #User input Calories
                if(self.estimatedTdee[i] > 0):
                    self.data = "During Week "+ str(i+1) + " you gained "+str(abs(self.weightChange))+" pounds. "+ " Your estimated TDEE is: "+str(self.estimatedTdee[i])+" calories\n"
                    f.write(self.data)
                #No user calorie input
                else:
                    self.data = "During Week "+str(i+1)+" you gained "+str(abs(self.weightChange))+" pounds. "+ "Your estimated surplus is: "+str(abs(self.estimatedTdee[i]))+" calories\n"
                    f.write(self.data)
            
            
                    
            #Weight Loss
            if(self.weightChange > 0and self.weekAvgWeight[i]!= 0):
                #calculate and add estimated TDEE   
                #                        weekly calories - weightChange (lbs) / .001 (lbs)  multiplied by .5 calories per day which causes (.001 lb) weight loss
                self.estimatedTdee[i] = round(self.weekAvgCal[i] + ((abs(self.weightChange) / .001) * (.5)))
                
                #No user calorie input
                if(self.weekAvgCal[i] == 0):
                    self.data = "During Week "+str(i+1)+" you lost "+str(abs(self.weightChange))+" pounds. "+" Your estimated defecit is: "+str(self.estimatedTdee[i]) +" calories\n"
                    f.write(self.data)
                #User input Calories
                else:
                    self.data = "During Week "+str(i+1)+" you lost "+str(abs(self.weightChange))+" pounds. "+" Your estimated TDEE is: "+str(self.estimatedTdee[i]) +" calories\n"
                    f.write(self.data)
                    
            if(self.weekAvgCal[i] != 0):
                self.avgTDEE += self.estimatedTdee[i]
                self.countTDEE += 1
        
        if(self.countTDEE != 0):
            self.final = "Your overall estimated TDEE from all data provided is: "+str(self.avgTDEE/self.countTDEE) + "\n"
            f.write(self.final)
        f.close()
                
                
        
#driver         
root = Tk()
window = Window(root)
root.mainloop()
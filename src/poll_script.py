#Innovation Day Poll Script by Victor Stolle

import sys
import tkinter
import os



class TextRedirector(object):
    def __init__(self, widget, tag="cout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.insert("end", str, (self.tag,))

class SurveyCounter:

    def __init__(self, filename):

        self.score = 0.0
        self.title = filename.strip(".csv")
        
        self.file = open(filename, 'r')
        self.data = dict()

        self.count = 0
        self.items = self.file.readline().split(',')[1:5]
        for i in range(len(self.items)):
            self.items[i] = self.items[i].strip('"')
            self.data[self.items[i]] = float(0)

        for line in self.file:
            self.count +=1
            self.item = line.split(',')[1:5]
            for i in range(0, 4):
  
                if(self.item[i] == 'Yes' or self.item[i] == 'Excellent' or self.item[i]== 'On Target'):
                    self.data[self.items[i]] += float(1)
                elif(self.item[i] == 'Good' or 'High' or 'Low'):
                    self.data[self.items[i]] += float(0.5)
                elif(self.item[i] == 'Incomplete (Needs More Investigation)' or self.item[i] == "Don't Know"):
                    self.data[self.items[i]] += float(0.25)
                elif(self.item[i] == 'No' or self.item[i] == 'Not Good'):
                    self.data[self.items[i]] += float(0.0)

        self.setScore()

    def setScore(self):
        self.score = 0.3*(self.data[self.items[0]] + self.data[self.items[1]] + self.data[self.items[2]]) + 0.1*self.data[self.items[3]]

root = tkinter.Tk()
root.title("Poll Results")
root.config(width = 600, height = 400)
datalabel = tkinter.Text(root, bg = "#293134", foreground = "#C0C0C0", font = ("Arial", 18))
datalabel.pack(side = "left", fill = "both", expand = 1)
sys.stdout = TextRedirector(datalabel, "cout")
print("Innovation Day Poll Script")
print("by Victor Stolle\n")

surveys = []
print("Survey Titles:")
for file in os.listdir(os.getcwd()):
    if file.endswith(".csv"):
        print("Title:", file)
        surveys.append(SurveyCounter(file))
print()
if len(surveys) > 0:
    winners = []
    for survey in surveys:
        winners.append((survey.title, survey.score))

    winners = sorted(winners, key= lambda winner: winner[1], reverse=True)      
    print("Rankings:\t\t\t\tScore:")
    for i in range(len(winners)):
        print(str(i+1) + ": Team", winners[i][0],"\t\t\t\t{:.2f}".format(winners[i][1]))

    if(winners[0][1] == winners[1][1]):
        print("Result: Tie")
    else:
        print("Result: Winner Team", winners[0][0])
        
root.mainloop()

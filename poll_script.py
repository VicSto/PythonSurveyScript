#Innovation Day Poll Script by Victor Stolle

import sys
import tkinter
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


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


        self.q1_responses = dict()
        self.q2_responses = dict()
        self.q3_responses = dict()
        self.q4_responses = dict()
        
        for i in range(len(self.items)):
            self.items[i] = self.items[i].strip('"')
            self.data[self.items[i]] = float(0)

        for line in self.file:
            self.count +=1
            self.item = line.split(',')[1:5]

            #Q1 Responses
            if self.item[0] in self.q1_responses.keys():
                self.q1_responses[self.item[0]] += 1
            else:
                self.q1_responses[self.item[0]] = 1
            #Q2 Responses
            if self.item[1] in self.q2_responses.keys():
                self.q2_responses[self.item[1]] += 1
            else:
                self.q2_responses[self.item[1]] = 1
            #Q3 Responses
            if self.item[2] in self.q3_responses.keys():
                self.q3_responses[self.item[2]] += 1
            else:
                self.q3_responses[self.item[2]] = 1
            #Q4 Responses
            if self.item[3] in self.q4_responses.keys():
                self.q4_responses[self.item[3]] += 1
            else:
                self.q4_responses[self.item[3]] = 1

            
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
        self.file.close()

    def setScore(self):
        self.score = 0.3*(self.data[self.items[0]] + self.data[self.items[1]] + self.data[self.items[2]]) + 0.1*self.data[self.items[3]]

    def print_results(self):
        print("\nQuestion 1 Results: ")
        for k , v in self.q1_responses.items():
            print("Key:", k, "Value: ", v)
        print("\nQuestion 2 Results: ")
        for k , v in self.q2_responses.items():
            print("Key:", k, "Value: ", v)
        print("\nQuestion 3 Results: ")
        for k , v in self.q3_responses.items():
            print("Key:", k, "Value: ", v)
        print("\nQuestion 4 Results: ")
        for k , v in self.q4_responses.items():
            print("Key:", k, "Value: ", v)

class pollScriptUI:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Poll Results")
        self.root.config(width = 600, height = 400)
        self.datalabel = tkinter.Text(self.root, bg = "#293134", foreground = "#C0C0C0", font = ("Arial", 18))
        self.datalabel.pack(side = "left", fill = "both", expand = 1)
        sys.stdout = TextRedirector(self.datalabel, "cout")
        print("Innovation Day Poll Script")
        print("by Victor Stolle\n")
        self.calc()
        self.run()

    def calc(self):
        self.surveys = []
        print("Survey Titles:")
        for file in os.listdir(os.getcwd()):
            if file.endswith(".csv"):
                print("Title:", file)
                self.surveys.append(SurveyCounter(file))
        print()
        if len(self.surveys) > 0:
            self.winners = []
            for survey in self.surveys:
                self.winners.append((survey.title, survey.score))
                survey.print_results()

            self.winners = sorted(self.winners, key= lambda winner: winner[1], reverse=True)      
            print("Rankings:\t\t\t\tScore:")
            for i in range(len(self.winners)):
                print(str(i+1) + ": Team", self.winners[i][0],"\t\t\t\t{:.2f}".format(self.winners[i][1]))

            if(self.winners[0][1] == self.winners[1][1]):
                print("Result: Tie")
            else:
                print("Result: Winner Team", self.winners[0][0])

    def hist_q1(self):
        x = self.surveys[0].data[self.surveys[0].items[0]]
        y = self.surveys[1].data[self.surveys[1].items[0]]
        num_bins = len(self.surveys)
        n1, bins1, patches1 = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
        n2, bins2, patches2 = plt.hist(y, num_bins, facecolor='red', alpha=0.5)
        plt.show()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    p = pollScriptUI()
    p.hist_q1()

#Innovation Day Poll Script by Victor Stolle

import sys

from tkinter import Button, Tk, Text

import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

q1_choices = ["Excellent", "Good", "Incomplete (Needs More Investigation)", "Not Good"]
q23_choices = ["Yes", "No", "Don't Know"]
q4_choices = ["High", "On Target", "Low"]




class TextRedirector(object):
    def __init__(self, widget, tag="cout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.insert("end", str, (self.tag,))

class SurveyCounter:

    def __init__(self, filename):

        self.score = 0.0
        print(filename)
        self.title = filename.split(".csv")[0]
        
        self.file = open(filename, 'r')
        self.data = dict()
        self.num_votes = 0
        self.items = self.file.readline().split(',')[1:5]


        self.q1_responses = dict()
        self.q2_responses = dict()
        self.q3_responses = dict()
        self.q4_responses = dict()


        for choice in q1_choices:
            self.q1_responses[choice] = 0

        for choice in q23_choices:
            self.q2_responses[choice] = 0
            self.q3_responses[choice] = 0

        for choice in q4_choices:
            self.q4_responses[choice] = 0
            
        
        for i in range(len(self.items)):
            self.items[i] = self.items[i].strip('"')
            self.data[self.items[i]] = float(0)

        for line in self.file:
            self.num_votes +=1
            self.item = line.split(',')[1:5]
            
            #Q1 Responses
            if self.item[0] in self.q1_responses.keys():
                self.q1_responses[self.item[0]] += 1
                
            #Q2 Responses
            if self.item[1] in self.q2_responses.keys():
                self.q2_responses[self.item[1]] += 1

            #Q3 Responses
            if self.item[2] in self.q3_responses.keys():
                self.q3_responses[self.item[2]] += 1

            #Q4 Responses
            if self.item[3] in self.q4_responses.keys():
                self.q4_responses[self.item[3]] += 1

            
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
        self.root = Tk()
        self.root.title("Poll Results")
        self.root.config(width = 600, height = 400)
        self.datalabel = Text(self.root, bg = "#293134", foreground = "#C0C0C0", font = ("Arial", 18))
        self.datalabel.grid(row = 0, column = 0, rowspan=2, sticky="nsw")

        self.histbutton = Button(self.root, text="Visualize Results", font = "Arial", command = self.hist_generate).grid(row=0, column=1)

        self.exitbutton = Button(self.root, text="Exit", font = "Arial", command = self.root.destroy).grid(row=1,column=1)
        
        sys.stdout = TextRedirector(self.datalabel, "cout")
        
        print("Innovation Day Poll Script")
        print("by Victor Stolle\n")
        self.surveys = []
        print("Survey Titles:")
        for file in os.listdir(os.getcwd()):
            if file.endswith(".csv"):
                print("Title:", file)
                self.surveys.append(SurveyCounter(file))
        print()
        self.calc()
        self.run()

    def calc(self):
        if len(self.surveys) > 1:
            self.winners = []
            for survey in self.surveys:
                self.winners.append((survey.title, survey.score))
                survey.print_results()

            self.winners = sorted(self.winners, key= lambda winner: winner[1], reverse=True)      
            print("Rankings:\t\t\t\tScore:")
            for i in range(len(self.winners)):
                print(str(i+1) + ": Team", self.winners[i][0],"\t\t\t\t{:.0f}".format(self.winners[i][1]) + "%")

            if(self.winners[0][1] == self.winners[1][1]):
                print("Result: Tie")
            else:
                print("Result: Winner Team", self.winners[0][0])

    def hist_q1(self):
        N = len(list(self.surveys[0].q1_responses.values()))
        rects = []
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        
        ind = np.arange(N)  # the x locations for the groups
        width = 0.15       # the width of the bars

        fig, ax = plt.subplots()
        ax.set_ylabel('# of Votes')
        ax.set_title('Question 1 Results: How Well Did the Group Demonstrate the Opportunity?')
        ax.set_xticks(ind + width / 4)
        ax.set_xticklabels(('Excellent', 'Good', 'Incomplete', 'Not Good'))
        
        for i in range(len(self.surveys)):
            rects.append(ax.bar(ind + i * width, (list(self.surveys[i].q1_responses.values())), width, color=colors[i]))
   
        ax.legend((rects[i] for i in range(len(rects))), (self.surveys[j].title for j in range(len(rects))))


    def hist_q2(self):
        N = len(list(self.surveys[0].q2_responses.values()))
        rects = []
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        
        ind = np.arange(N)  # the x locations for the groups
        width = 0.15       # the width of the bars

        fig, ax = plt.subplots()
        ax.set_ylabel('# of Votes')
        ax.set_title('Question 2 Results: Did the Presenter Send a Clear Message on Conclusions and Recommendations?')
        ax.set_xticks(ind + width / 3)
        ax.set_xticklabels(('Yes', 'No', "Don't Know"))
        
        for i in range(len(self.surveys)):
            rects.append(ax.bar(ind + i * width, (list(self.surveys[i].q2_responses.values())), width, color=colors[i]))
   
        ax.legend((rects[i] for i in range(len(rects))), (self.surveys[j].title for j in range(len(rects))))


    def hist_q3(self):
        N = len(list(self.surveys[0].q3_responses.values()))
        rects = []
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        
        ind = np.arange(N)  # the x locations for the groups
        width = 0.15       # the width of the bars

        fig, ax = plt.subplots()
        ax.set_ylabel('# of Votes')
        ax.set_title('Question 3 Results: Do You Find that the Project is Compelling to the Business and Should be a Priority to Halyard Health Acute Pain?')
        ax.set_xticks(ind + width / 3)
        ax.set_xticklabels(('Yes', 'No', "Don't Know"))
        
        for i in range(len(self.surveys)):
            rects.append(ax.bar(ind + i * width, (list(self.surveys[i].q3_responses.values())), width, color=colors[i]))
   
        ax.legend((rects[i] for i in range(len(rects))), (self.surveys[j].title for j in range(len(rects))))

    def hist_q4(self):
        N = len(list(self.surveys[0].q4_responses.values()))
        rects = []
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        
        ind = np.arange(N)  # the x locations for the groups
        width = 0.15       # the width of the bars

        fig, ax = plt.subplots()
        ax.set_ylabel('# of Votes')
        ax.set_title("Question 4 Results: Rate the Accuracy of the Group's Scoring Based on the Prioritization Matrix")
        ax.set_xticks(ind + width / 3)
        ax.set_xticklabels(('High', 'On Target', "Low"))
        
        for i in range(len(self.surveys)):
            rects.append(ax.bar(ind + i * width, (list(self.surveys[i].q4_responses.values())), width, color=colors[i]))
   
        ax.legend((rects[i] for i in range(len(rects))), (self.surveys[j].title for j in range(len(rects))))

    def hist_generate(self):
        self.hist_q1()
        self.hist_q2()
        self.hist_q3()
        self.hist_q4()
        plt.show()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    p = pollScriptUI()

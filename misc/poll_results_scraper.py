import sys
import os

q1_responses = dict()
q2_responses = dict()
q3_responses = dict()
q4_responses = dict()

def extract (file):

    infile = open(file, 'r')
    items = infile.readline().split(',')[1:5]
    for i in range(len(items)):
        items[i] = items[i].strip('"')

    for line in infile:
        item = line.split(',')[1:5]
        #Q1 Responses
        if item[0] in q1_responses.keys():
            q1_responses[item[0]] += 1
        else:
            q1_responses[item[0]] = 1
        #Q2 Responses
        if item[1] in q2_responses.keys():
            q2_responses[item[1]] += 1
        else:
            q2_responses[item[1]] = 1
        #Q3 Responses
        if item[2] in q3_responses.keys():
            q3_responses[item[2]] += 1
        else:
            q3_responses[item[2]] = 1
        #Q4 Responses
        if item[3] in q4_responses.keys():
            q4_responses[item[3]] += 1
        else:
            q4_responses[item[3]] = 1
    infile.close()

def print_results():
    print("\nQuestion 1 Results: ")
    for k , v in q1_responses.items():
        print("Key:", k, "Value: ", v)
    print("\nQuestion 2 Results: ")
    for k , v in q2_responses.items():
        print("Key:", k, "Value: ", v)
    print("\nQuestion 3 Results: ")
    for k , v in q3_responses.items():
        print("Key:", k, "Value: ", v)
    print("\nQuestion 4 Results: ")
    for k , v in q4_responses.items():
        print("Key:", k, "Value: ", v)        


if __name__ == "__main__":
    
    for file in os.listdir(os.getcwd()):
        if file.endswith(".csv"):
            print("Title:", file)
            extract(file)
            print_results()
            break

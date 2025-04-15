#!usr/bin/env python3


import csv
import sys

def read_file(FILENAME):
    list_data = []
    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                list_data.append(row)
            return list_data
    except EOFError:
        list_data=[]
        return list_data
    except FileNotFoundError:
        list_data=[]
        return list_data
        

def write_file(FILENAME, list_data):
    try:
        with open(FILENAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(list_data)
    except OSError:
        print("Could not write to file due to operating system error. Quitting applicaiton...")
        sys.exit()

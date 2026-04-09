# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 10:00:49 2025

@author: balboni
"""

import pandas as pd

# Read the Excel file
df = pd.read_excel('D:/Balboni/Downloads/Liste sito.xlsx')  # Change to your file name

# Open the output text file
with open('insegnanti.txt', 'w', encoding='utf-8') as f:
    for _, row in df.iterrows():
        name = str(row[0])
        surname = str(row[1])
        third = str(row[2])
        fourth = str(row[3])

        line = f"{name} {surname}. {third}, {fourth}"
        f.write(line + "\n")

print("D:/balboni/Documents/MEGA/SciComm/penne/2025-26/sito scicomm/insegnanti.txt")
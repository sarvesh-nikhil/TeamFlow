import csv
import os
from typing import List


csv_file_path = "user_details.csv"

if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "email", "age", "skills","department","designation","yearsofexp","status"]) 

def write_to_csv(id: str, name: str, email: str, age: int, skills: List[str], 
                 department: str, designation: str,yearsofexp: int, status: str):
    with open('user_details.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, name, email, age, ",".join(skills), department, designation, yearsofexp, status]) 

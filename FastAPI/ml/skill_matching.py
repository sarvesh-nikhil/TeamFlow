import pandas as pd
import numpy as np
def match_skills(required_skills, user_data):
    required_skills_set = set(required_skills)

    match_data = []

    for emp in user_data:
        emp_skills_set = set(emp.skills)

        matches = len(required_skills_set.intersection(emp_skills_set))
        match_data.append({
            'id': emp.id,
            'name': emp.name,
            'email': emp.email,
            'age': emp.age,
            'skills': emp.skills,
            'department': emp.department,
            'designation': emp.designation,
            'yearsofexp':emp.yearsofexp,
            'status': emp.status,
            'matches': matches
        })

    df = pd.DataFrame(match_data)
    df_sorted = df.sort_values(by='matches', ascending=False)
    return df_sorted.to_dict(orient='records')
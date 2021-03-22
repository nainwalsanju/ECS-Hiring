"""Routines associated with the application data.
"""
import json

courses = {}
final_id=0

def load_data():
    """Load the data from the json file.
    """
    data = []
    try :
        with open('./json/course.json') as course_data :
            data = json.loads(course_data.read())
    except Exception as e:
        print(e,"\nError opening course.json file.\n")
        return
    
    global courses
    courses = { dict_data['id'] : dict_data for dict_data in data }
    final_id = max(courses.keys())



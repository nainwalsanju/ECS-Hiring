"""Routes for the course resource.
"""

from run import app
from flask import request
from http import HTTPStatus
import data
import datetime


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    course = data.courses.get(id)
    if(not course):
        message = "Course {} does not exist".format(id)
        return {"message": message}, 404
    ret_course = course.copy()
    ret_course.pop('id')
    return {'data' : ret_course}

@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    page_number = request.args.get('page-number', type=int, default=1)
    page_size = request.args.get('page-size', type=int, default=10)
    title_words = request.args.get('title_words')

    title_words_list = []
    if(title_words):
        title_words_list = [ word.strip() for word in title_words.split(",") ]
    
    keys = list(data.courses.keys())

    record_count = len(keys)
    page_count = record_count // page_size

    start_page_index = page_size * (page_number -1)
    end_page_index = start_page_index + page_size
    
    ret_courses = [ data.courses.get(key) for key in keys[start_page_index:end_page_index]]
    
    metadata = {
                "page_count" : page_count,
                "page_number" : page_number,
                "page_size" : page_size,
                "record_count": record_count
                }

    return { "data" : ret_courses , "metadata" : metadata}, 200



@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    date_created = datetime.datetime.now().isoformat()
    date_updated = date_created

    title = request.json.get('title')
    image_path = request.json.get('image_path')
    price = request.json.get('price')
    on_discount = request.json.get('on_discount')
    discount_price = request.json.get('discount_price')
    description = request.json.get('description')
    
    data.final_id = data.final_id +1
    _id = data.final_id

    course = {
        'date_created': date_created,
        'date_updated': date_updated,
        'description': description,
        'discount_price': discount_price,
        'id': _id,
        'image_path': image_path,
        'on_discount': on_discount,
        'price': price,
        'title': title
        }
    
    data.courses[_id] = course

    return {"data": course}, 201


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    _id = request.json.get('id')
    title = request.json.get('title')
    image_path = request.json.get('image_path')
    price = request.json.get('price')
    on_discount = request.json.get('on_discount')
    discount_price = request.json.get('discount_price')
    description = request.json.get('description')

    if(id != _id):
        message =  "The id does match the payload"
        return {"message": message}, 400

    course = data.courses.get(id)
    if(not course):
        message = "Course {} does not exist".format(id)
        return {"message": message}, 404
    
    course['description'] = description
    course['discount_price'] = discount_price
    course['image_path'] = image_path
    course['on_discount'] = on_discount
    course['price'] = price
    course['title'] = title

    ret_course = course.copy()
    ret_course.pop('date_created')
    return {"data": ret_course}


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    message = ""
    course = data.courses.get(id)

    if not course :
        message = "Course {} does not exist".format(id)
        return {"message": message}, 404

    del data.courses[id]
    message = "The specified course was deleted"
    return {"message": message}, 200


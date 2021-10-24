from flask import Flask, request, g
from requests.models import Response
from data_proccessing import get_posts_with_tags, condense_posts, sort_posts

import time

app = Flask(__name__)

#defaults/constants 

SORT_BY_FIELDS = ['id', 'reads', 'likes', 'popularity']
DEFAULT_SORT_BY = 'id'
DIRECTIONS = ['desc', 'asc']
DEFAULT_DIRECTION = 'asc'





# the following 2 functions were found here "https://stackoverflow.com/questions/12273889/calculate-execution-time-for-every-page-in-pythons-flask"
# they track the response time
@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(f"Request Execution time : {diff}")
    return response


def error_response(message) -> Response:
    return {'error': message}, 400


        

@app.route("/api/ping")
def ping() -> Response: #simple ping response
    return {'success' : True} , 200

#/api/posts route uses Query parameters in the form "api/posts?param1=x,y,z&param2=a,b,c ..."
@app.route("/api/posts", methods=['GET'])
def posts() -> Response:
    tags = request.args.get('tags').split(',')
    sort_by = request.args.get('sortBy')
    direction = request.args.get('direction')

    if not tags: #if tags arent suplied send error
        return error_response('tags parameter is required')

    if not sort_by: #no sortBy set as default
        sort_by = DEFAULT_SORT_BY
    elif sort_by not in SORT_BY_FIELDS: #sortBy invalid send error
        return error_response('sortBy parameter is invalid')

    if not direction:#no direction set as default
        direction = DEFAULT_DIRECTION
    elif direction not in DIRECTIONS: #direction invalid send error
        return error_response('direction parameter is invalid')
    
    raw_posts = get_posts_with_tags(tags) #get
    condensed_posts = condense_posts(raw_posts) #flattened
    sorted_posts = sort_posts(condensed_posts, sort_by, direction) #sort

    return {'posts' : sorted_posts} , 200 #send our organized posts


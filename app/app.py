from types import resolve_bases
from flask import Flask, request, g
from requests.models import Response
from multiprocessing import Pool, TimeoutError
from api_access import get_posts
from caching import PostCacher
import time

app = Flask(__name__)

SORT_BY_FIELDS = ['id', 'reads', 'likes', 'popularity']
DEFAULT_SORT_BY = 'id'
DIRECTIONS = ['desc', 'asc']
DEFAULT_DIRECTION = 'asc'

SORTERS = {
    'id': lambda elem : elem['id'],
    'reads' : lambda elem : elem['reads'],
    'likes': lambda elem : elem['likes'],
    'popularity' : lambda elem : elem['popularity']
}



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


post_cacher = PostCacher()

def get_posts_with_tags(tags):
    results = []
    posts = []
    uncached_tags = []

    for i, tag in enumerate(tags):
        cached_posts = post_cacher.retrieve(tag)
        if cached_posts:
            posts.append(cached_posts)
        else:
            uncached_tags.append(tag)

    if len(uncached_tags):
        with Pool(processes=len(uncached_tags)) as pool:
            results = pool.map(get_posts, uncached_tags)

    for result, tag in zip(results, uncached_tags):
        post_cacher.store(tag, result['posts'])
        posts.append(result['posts'])
    return posts

def condense_posts(posts):
    posts = [post for list_of_posts in posts for post in list_of_posts] #flatten the posts
    # new_posts = [] 
    # for list_of_posts in posts:
    #    for post in list_of_posts:
    #        new_posts.append(item)
    unique_ids = []
    unique_posts = []
    #print(posts)
    for post in posts: 
        if post['id'] not in unique_ids:
            #print(post)
            unique_ids.append(post['id'])
            unique_posts.append(post)
    return unique_posts

def get_and_condense_posts(tags):
    return condense_posts(get_posts_with_tags(tags))

def sort_posts(posts, sort_by, direction):
    return sorted(posts, key=SORTERS[sort_by], reverse=(direction == 'asc'))

        

@app.route("/api/ping")
def ping() -> Response:
    return {'success' : True} , 200


@app.route("/api/posts", methods=['GET'])
def posts() -> Response:
    tags = request.args.get('tags').split(',')
    sort_by = request.args.get('sortBy')
    direction = request.args.get('direction')

    if not tags:
        return error_response('tags parameter is required')

    if not sort_by:
        sort_by = DEFAULT_SORT_BY
    elif sort_by not in SORT_BY_FIELDS:
        return error_response('sortBy parameter is invalid')

    if not direction:
        direction = DEFAULT_DIRECTION
    elif direction not in DIRECTIONS:
        return error_response('direction parameter is invalid')
    
    raw_posts = get_posts_with_tags(tags)
    condensed_posts = condense_posts(raw_posts)
    sorted_posts = sort_posts(condensed_posts, sort_by, direction)

    return {'posts' : sorted_posts} , 200


from api_access import get_posts
from multiprocessing import Pool, TimeoutError
from caching import PostCacher


POST_SORTING_KEYS = {
    'id': lambda elem : elem['id'],
    'reads' : lambda elem : elem['reads'],
    'likes': lambda elem : elem['likes'],
    'popularity' : lambda elem : elem['popularity']
}

#insatintiate a PostCacher for use in the get posts function
post_cacher = PostCacher()

# used to get the posts based on the given tags
# gets posts either from the hatchways api via the get_posts function
# or from the post cacher if the tag has recently been retrieved
def get_posts_with_tags(tags):
    results = []
    posts = []
    uncached_tags = []

    for tag in tags:
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

# flattens the list of lists that is the posts and removes duplicates
def condense_posts(posts):
    posts = [post for list_of_posts in posts for post in list_of_posts] #flatten the posts
    # new_posts = [] 
    # for list_of_posts in posts:
    #    for post in list_of_posts:
    #        new_posts.append(item)
    unique_ids = [] #these should probably be sets of some kind
    unique_posts = []
    #print(posts)
    for post in posts: # capturing the unique posts
        if post['id'] not in unique_ids:
            #print(post)
            unique_ids.append(post['id'])
            unique_posts.append(post)
    return unique_posts

    #sort the posts
def sort_posts(posts, sort_by, direction):
    return sorted(posts, key=POST_SORTING_KEYS[sort_by], reverse=(direction == 'asc'))

if __name__ == '__main__': 
    pass
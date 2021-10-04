
# not used but could be in the future
class CacheError():
    def __init__(self, message) -> None:
        self.message = message


# a post caching object that stores posts that have recently been
# retrieved from the API
class PostCacher():

    def __init__(self) -> None:
        self.my_cache = {} #  a dict to store the cached data

    # get the cached data if it exists in the cache
    # if the tag does not exist in the cache return false
    def retrieve(self, tag):
        if tag in self.my_cache.keys():
                return self.my_cache[tag]
        return False

    # add the tag, post pair to the cached data
    def store(self, tag, posts):
        self.my_cache[tag] = posts

    # clear the cache
    def refresh(self):
        self.my_cache = {}
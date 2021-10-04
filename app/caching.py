

class CacheError():
    def __init__(self, message) -> None:
        self.message = message



class PostCacher():

    def __init__(self) -> None:
        self.my_cache = {}


    def retrieve(self, tag):
        if tag in self.my_cache.keys():
                return self.my_cache[tag]
        return False

    def store(self, tag, posts):
        self.my_cache[tag] = posts

    def refresh(self):
        self.my_cache = {}
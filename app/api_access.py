import requests

class ApiAccessError:
    def __init__(self, requested_tag) -> None:
        self.requested_tag = requested_tag

class ApiAccessErrorStatus(ApiAccessError):
    def __init__(self, requested_tag, status_code, response) -> None:
        super().__init__(requested_tag)
        self.status_code = status_code
        self.response = response

class ApiAccessJSONError(ApiAccessError):
    def __init__(self, requested_tag, json_error) -> None:
        super().__init__(requested_tag)
        self.json_error = json_error



def get_posts(tag):
    r = requests.get('https://api.hatchways.io/assessment/blog/posts', params={'tag': tag}, timeout=5)
    if r.status_code != requests.codes.ok :
        raise ApiAccessErrorStatus(tag, r.status_code, r)

    try: 
        r = r.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ApiAccessJSONError(tag, e)
    return r


    




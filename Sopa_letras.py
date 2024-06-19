import urllib3
from urllib3.exceptions import RequestError

try:
    http = urllib3.PoolManager()
    res = http.request(
        method="GET", 
        url="https://pokeapi.co/api/v2"
    )
    print(res.data.decode())
except RequestError as ex:
    print("error1", ex)
except Exception as ex:
    print("name_error", type(ex).__name__)
    print("error2", ex)

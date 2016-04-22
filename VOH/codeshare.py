import requests
from pprint import pprint

if __name__ == "__main__":
    r = requests.get("https://codeshare.io/new", allow_redirects=False).text
    print (r.split(" ")[-1])
    exit(0)


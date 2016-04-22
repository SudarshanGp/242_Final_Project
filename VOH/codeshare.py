import requests

if __name__ == "__main__":
    # Use an HTTP GET request to generate a unique codeshare id and get the response header
    r = requests.get("https://codeshare.io/new", allow_redirects=False).text
    # Parse the header to get the unique URL and output it to the console
    print (r.split(" ")[-1])
    exit(0)


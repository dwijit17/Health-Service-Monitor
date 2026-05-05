import requests
d = {
  "test_urls": [
    "https://example.com",
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/posts",
    
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/5",
    
    "https://httpbin.org/bytes/1024",
    "https://httpbin.org/bytes/20480",
    "https://jsonplaceholder.typicode.com/photos",
    
    "https://httpbin.org/post",
    "https://httpbin.org/put",
    "https://httpbin.org/delete",
    
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    
    "https://api.github.com",
    "https://catfact.ninja/fact"
  ]
}
for url in d["test_urls"]:
    data = {
    "url_link": url,
    "url_name": "string",
    "user_id": 1
    }
    requests.post(url="http://localhost:8000/urls",json=data)
print("Done")
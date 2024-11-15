import requests

test_url = 'http://127.0.0.1:8000/mesh/new'
file = {'file':open('examples/bird.jpg', 'rb')}
resp = requests.post(url=test_url, files=file)
print(resp._content)
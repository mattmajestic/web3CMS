import requests

# Test the GET / route
response = requests.get("http://localhost:8000/")
print(response.json())

# Test the POST /posts/ route
post = {"id": 1, "title": "Test Post", "content": "This is a test post."}
response = requests.post("http://localhost:8000/posts/", json=post)
print(response.json())

# Test the GET /posts/ route
response = requests.get("http://localhost:8000/posts/")
print(response.json())

# Test the PUT /posts/{post_id} route
updated_post = {"id": 1, "title": "Updated Test Post", "content": "This is an updated test post."}
response = requests.put("http://localhost:8000/posts/1", json=updated_post)
print(response.json())

# Test the DELETE /posts/{post_id} route
response = requests.delete("http://localhost:8000/posts/1")
print(response.json())
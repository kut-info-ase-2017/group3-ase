import requests
r = requests.post('http://localhost:3000', files = {"data": ("photo.jpg", open("./unknown/who0.jpg", "rb"), "image/jpeg")
})
print(r.text)

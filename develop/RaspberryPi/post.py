import requests
r = requests.post('https://localhost:3000',
                  files = {
                    "data": ("photo.jpg", open("./unknown/who0.jpg", "rb"),
                    "image/jpeg")
                  }, verify=False)
print(r.text)

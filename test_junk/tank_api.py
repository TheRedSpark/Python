import requests
from package import variables as v
res = requests.get(v.tanke_api)

print(res.content)
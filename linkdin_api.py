import requests
from packages import UA

headers = {'User-Agent': UA.random}
res = requests.get('https://www.linkedin.com/jobs/view/3178195306/?alternateChannel=search&refId=tgmk4oXUZXyC7UYXIYXUXA%3D%3D&trackingId=T0ZnmLjb4Z7EQSnXSq7vyw%3D%3D', 
                   headers = headers)
print(res.status_code)

with open('data.html', 'w', encoding='utf-8') as f:
    f.write(str(res.text))
    

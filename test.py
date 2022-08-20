from packages.utils import _get_job_ids
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
res = session.get('https://www.linkedin.com/jobs/search/?currentJobId=3220849104&f_TPR=r86400&geoId=103644278&keywords=python&location=United%20States&refresh=true')
print(res.status_code)
res.html.render(sleep=1, wait=2, timeout=30)



soup = BeautifulSoup(res.html.html, 'lxml')
ids = _get_job_ids(soup)
print(len(ids))
print(ids)

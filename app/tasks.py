import requests
import mechanize
from bs4 import BeautifulSoup

BASE = "https://www.linkedin.com"

browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]

get_soup = lambda url: BeautifulSoup(requests.get(url).text)
get_soup = lambda url: BeautifulSoup(browser.open(url).read())

def main_task(Recruit, db_session, published=False):
    for recruit in get_list():
        instance = Recruit.query.filter_by(id=recruit[5]).first()
        if instance:
            print "[@] %s already exists" % instance
            pass
        else:
            recruit = Recruit(recruit[0],
                              recruit[1],
                              recruit[2],
                              recruit[3],
                              recruit[4],
                              recruit[5],
                              published)

            db_session.add(recruit)
            db_session.commit()

def get_list():
    urls = [#BASE + "/job/computer-jobs-seoul/?sort=date&trk=jserp_sort_date",
            BASE + "/job/engineer-jobs-seoul/?sort=date&trk=jserp_sort_date",
            BASE + "/job/intern-jobs-seoul/?sort=date&trk=jserp_sort_date",
            BASE + "/job/computer-science-intern-jobs/?sort=date&trk=jserp_sort_date"]

    job_elems = []
    for url in urls:
        soup = get_soup(url)

        job_elems.extend(soup.select("li.job"))
        job_elems.reverse()
    #company_elems = soup.select("a.company")
    #content_elems = soup.select(".hr_list .hr_text_2")
    #href_elems = soup.select(".hr_list .hr_hover_bg a")

    #zipped = zip(job_elems, company_elems, content_elems, href_elems)

    #zipped.reverse()

    #for (job, company, content, a_link) in zipped:
    for job in job_elems:
        url = job.select(".title")[0]['href']
        job_title = job.select(".title")[0].text
        job_content = job.select(".abstract")[0].text
        company = job.select(".company")[0].text
        detail = ' '.join(job.select(".details")[0].text.split())
        jid = int(url.split("/")[-1].split("?")[0])

        yield [job_title,
               company,
               job_content,
               url,
               detail,
               jid]

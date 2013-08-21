from bs4 import BeautifulSoup
import urllib, re, MySQLdb

langs = ['php', 'java', 'c++', 'ruby', 'django', 'python', 'android', '.NET', 'javascript']
jobscz = 'http://www.jobs.cz/search/?section=positions&srch%5Bq%5D='
pracecz = 'https://www.prace.cz/search/?srch%5Blocal%5D=&srch%5Bkey%5D='

def jobsStr(soup):
    return soup.body.find_all(id='joblist')[0].find_all(class_='list')[0].h4.span.string

def praceStr(soup):
    return soup.find_all(id='content')[0].find_all(class_='result')[0].text

def get(lang, url, f):
    jobs = urllib.urlopen(url+urllib.quote_plus(lang)).read()
    soup = BeautifulSoup(jobs)
    s = ''
    try:
        s = f(soup)
    except:
        print "Document malformed."
        return 0
   
    if (re.search('[0-9]+', s)):
        return re.search('[0-9]+', s).group(0)
    else:
        return 0

db = MySQLdb.connect(host="localhost", db='prace', user='root')
c = db.cursor()

print ''.ljust(10), 'jobs'.ljust(10), 'prace'.ljust(10)
for l in langs:
    gj = get(l, jobscz, jobsStr)
    gp = get(l, pracecz, praceStr)
    c.execute('INSERT INTO nabidky VALUES(%d, %d, CURDATE(), "%s")' % (int(gj), int(gp), l))
    print l.ljust(10), gj.ljust(10), gp.ljust(10)

db.commit()
db.close()
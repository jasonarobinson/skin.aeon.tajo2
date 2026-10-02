import re, html, json, sys, time, subprocess, datetime
def get(url):
    for i in range(3):
        r = subprocess.run(["curl","-sS","-m","30","-L",url],capture_output=True,text=True)
        if r.returncode==0 and r.stdout: return r.stdout
        time.sleep(2)
    return ""
def text(x): return html.unescape(re.sub(r'<[^>]+>','',x)).strip()
def parse_article(s):
    title = text(re.search(r'<title>(.*?)</title>',s,re.S).group(1)).split(' — ')[0].split(' — ')[0].strip()
    pn = [int(x) for x in re.findall(r'class="parNum"[^>]*data-pnum="(\d+)"',s)]
    groups=[]
    for q in re.findall(r'<p[^>]*class="qu"[^>]*>(.*?)</p>',s,re.S):
        m = re.match(r'(\d+)\s*[-–]\s*(\d+)\.', text(q))
        if m: groups.append([int(m.group(1)),int(m.group(2))])
    review=None
    m = re.search(r'class="boxTtl[^"]*"[^>]*>\s*<h2>(.*?)</h2>(.*?)</aside>',s,re.S)
    for m in re.finditer(r'class="boxTtl[^"]*"[^>]*>\s*<h2>(.*?)</h2>(.*?)</aside>',s,re.S):
        if 'Your answer' in m.group(2) or 'gen-field' in m.group(2):
            review=len(re.findall(r'<li\b',m.group(2))); break
    return dict(title=title, paragraphs=max(pn) if pn else None, review=review, groups=groups)
def week(year, wk):
    s = get(f"https://wol.jw.org/en/wol/meetings/r1/lp-e/{year}/{wk}")
    i = s.find('Watchtower Study')
    if i < 0: return None
    m = re.search(r'href="(/en/wol/d/r1/lp-e/\d+)"', s[i:])
    if not m: return None
    url = "https://wol.jw.org"+m.group(1)
    a = parse_article(get(url))
    a['url']=url
    return a
if __name__=="__main__":
    out={}
    start=datetime.date.fromisocalendar(int(sys.argv[1]),int(sys.argv[2]),1)
    n=int(sys.argv[3])
    for k in range(n):
        d=start+datetime.timedelta(weeks=k); y,w,_=d.isocalendar()
        try: a=week(y,w)
        except Exception as e: a={'error':str(e)}
        print(d.isoformat(), json.dumps(a, ensure_ascii=False), flush=True)
        if a: out[d.isoformat()]=a
        time.sleep(1)
    json.dump(out,open(sys.argv[4],'w'),ensure_ascii=False,indent=1)

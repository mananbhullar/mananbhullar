"""Tell Bing (and other IndexNow engines) which pages changed, so they re-crawl in hours, not days.

Run after a push that has gone live:   python3 indexnow.py            (pages changed in the last commit)
                                       python3 indexnow.py HEAD~3     (pages changed since that commit)
                                       python3 indexnow.py --all      (every page in sitemap.xml)
The key file /c3f4ac60083b05d9eba775a579132b3c.txt at the site root proves ownership; don't delete or rename it.
"""
import json, re, subprocess, sys, urllib.request

KEY = "c3f4ac60083b05d9eba775a579132b3c"
SITE = "https://www.mananbhullar.com"

def changed_urls(since):
    files = subprocess.run(['git', 'diff', '--name-only', since, 'HEAD'], capture_output=True, text=True, check=True).stdout.split()
    urls = []
    for f in files:
        if f == 'index.html':
            urls.append(SITE + '/')
        elif f.endswith('/index.html') and not f.startswith('assets/'):
            urls.append(f"{SITE}/{f[:-len('index.html')]}")
    return urls

def all_urls():
    return re.findall(r'<loc>([^<]+)</loc>', open('sitemap.xml').read())

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'HEAD~1'
    urls = all_urls() if arg == '--all' else changed_urls(arg)
    if not urls:
        sys.exit('No changed pages to submit.')
    body = json.dumps({"host": "www.mananbhullar.com", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req) as r:
        print(f"IndexNow: HTTP {r.status} for {len(urls)} URL(s)")

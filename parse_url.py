import urllib.parse
s = 'http://search.xxxx.xxx.co.jp/sitesearch/jyo?Q=%98_&SITE=jyo&LANG=JA&PL=JA&SC=jyo'
s2 = urllib.parse.unquote(s, encoding='shift-jis')
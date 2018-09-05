def create_route_tree(path_list):
    root = Node("")
    path_sorted = sorted(path_list)
    for path in path_sorted:
        path_str = path.split("/")
        current = root
        for p in path_str:
            child = find_child(current.children, p)
            if child == Node:



def find_child(children, data):
    return None
        
class Node(object):
    def __init__(self, data):
        self.data = data
        self.value = 0
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_value(self, value):
        self.value = self.value + 1


import urllib.parse
s = 'http://search.xxxx.xxx.co.jp/sitesearch/jyo?Q=%98_&SITE=jyo&LANG=JA&PL=JA&SC=jyo'
s2 = urllib.parse.unquote(s, encoding='shift-jis')

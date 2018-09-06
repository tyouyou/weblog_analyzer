class Node(object):
    def __init__(self, data):
        self.data = data
        self.value = 0
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_value(self):
        self.value = self.value + 1

    def get_data(self):
        return self.data

    def __str__(self, level=0):
        string = " "*level + "|" + "_"*level + "data: %s, value: %s \n" %(self.data, self.value)
        for child in self.children:   
            string += child.__str__(level+1)
        return string

def find_child(children, data):
    for child in children:
        if child.get_data() == data:
            return child
    return None

def create_route_tree(path_list):
    root = Node("")
    path_sorted = sorted(path_list)
    for path in path_sorted:
        path_str = list(filter(None, path.split("/")))
        current = root
        for i in range(0, len(path_str)):
            child = find_child(current.children, path_str[i])
            if child == None:
                path_node = Node(path_str[i])
                current.add_child(path_node)
                current = path_node
            else:
                current = child
                
            if i == len(path_str) - 1:
                current.add_value()
    return root

path_list = ["/home/index", "/home/index/question", "/home/index/question", "/home/index/question", 
"/home/index/question", "/home/index/question", "/home/info", "/home/index/PPS/se", "/home/info","/home/info",
"/homepage/ex","/home/index/question", ]
root = create_route_tree(path_list)
print(root)
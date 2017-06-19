from pygraphviz import *
g = AGraph(ranksep = '0.7', strict = False)
node = ['5', '4', '6', '7', '8']
#g.add_node()
'''
for it in node[:]:
    num = (node.index(it)+1) * 2
    if num < len(node) and node[num-1] is not None:
        g.add_edge(it, node[num-1])
    if num < len(node) and node[num] is not None:
        g.add_edge(it, node[num])
'''
#g.add_edge('5', '10')
#g.add_edge('a', 'b')
g.add_node('a', label = 'a')
g.add_node('b', label = 'a')
g.add_edge('a', 'b')
g.add_edge('1':{label='s'}, 2:{label:'s'})

#g.graph_attr['label']='comma01'
g.node_attr['shape'] = 'box'
g.edge_attr['color'] = 'red'
g.node_attr['fontsize'] = 16
g.layout(prog='dot')
g.draw('first_pygraphviz.jpg')
print(g)
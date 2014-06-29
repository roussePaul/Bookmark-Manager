import matplotlib.pyplot as plt
import networkx as nx
import pprint

def community(G):
    dict = nx.edge_betweenness_centrality(G)
    
    list=[]
    m = max(dict.values())
    
    for edge, val in dict.items():
        if val==m:
            list.append(edge)

    G.remove_edges_from(list)
    
    return nx.connected_component_subgraphs(G)
    
def getMostConnectedNodes(G):
    nodes = nx.betweenness_centrality(G)
    
    list=[]
    m = max(nodes.values())
    
    for node, val in nodes.items():
        if val==m:
            list.append(node)
    return list
    
def drawGraph(g):
    pos=nx.spring_layout(g)
    nx.draw_networkx_nodes(g,pos,node_size=700)
    nx.draw_networkx_labels(g,pos,font_size=8,font_family='sans-serif')
    nx.draw_networkx_edges(g,pos)

G = nx.barabasi_albert_graph(30,1)
drawGraph(G)
plt.savefig('img/path.png')

S = community(G)

i=0
for g in S:
    i=i+1
    plt.clf()
    drawGraph(g)
    plt.savefig('img/path'+str(i)+'.png')
    print(getMostConnectedNodes(g))
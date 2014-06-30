import matplotlib.pyplot as plt
import networkx as nx
import pprint
from bdd import *
from tagger import *

# Trouve des groupes dans le graphe et renvoi l'ensemble de graphes extraits
def community(G):
    dict = nx.edge_betweenness_centrality(G)
    
    list=[]
    
    if not dict:
        return G
        
    m = max(dict.values())
    
    for edge, val in dict.items():
        if val==m:
            list.append(edge)

    G.remove_edges_from(list)
    
    return nx.connected_component_subgraphs(G)

# renvoi les noeuds les plus connectés donc les mots qui "décrivent" le groupe de mots
def getMostConnectedNodes(G):
    nodes = nx.betweenness_centrality(G)
    
    list=[]
    m = max(nodes.values())
    
    for node, val in nodes.items():
        if val==m:
            list.append(node)
    return list
    
# dessine le graphe
def drawGraph(g):
    pos=nx.spring_layout(g,iterations=1000)
    nx.draw_networkx_nodes(g,pos,node_size=700)
    nx.draw_networkx_labels(g,pos,font_size=8,font_family='sans-serif')
    nx.draw_networkx_edges(g,pos)

    
# construit le graphe à partir de la base de donnée
def buildGraph():
    G = nx.Graph()
    G.add_nodes_from(getListTag())
    edges = getListTagsWithWeigth()
    
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(edges)
    
    moyenne = 0
    for (u,v,w) in edges:
        moyenne += w
    moyenne = moyenne/ len(edges)
    edges = [(u,v,w) for (u,v,w) in edges if w>moyenne and u!=v]
    
    
    G.add_weighted_edges_from(edges)
    
    return G

initBDD()

G = buildGraph()

drawGraph(G)
plt.savefig('img/path.png')

S = community(G)
while True:
    A=[]
    for g in S:
        if g.number_of_nodes() > 1:
            A.extend(community(g))
        else:
            A.append(g)
    nbre = list(map(lambda g: g.number_of_nodes(),A))
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(nbre)
    if max(nbre)<10:
        break
    S = A
print(A)
S=A

i=0
for g in S:
    i=i+1
    plt.clf()
    drawGraph(g)
    plt.savefig('img/path'+str(i)+'.png')
    print(getMostConnectedNodes(g))
    
closeBDD()
from graphviz import Graph


def createGraph(adjlist, textlist, sizelist, filename=""):
   g = Graph(format='jpg')
   gtext = []
   
   for i in range(0, len(textlist)):
      t = str(i+1) + ". " + textlist[i]
      g.node(t)
      gtext.append(t)

   for e, v in adjlist.items():
     if (v == 1):
        color1 = "black"
     elif (v == 2):
        color1 = "red"
     elif (v == 3):
        color1 = "blue"
     print(e[0])
     #g.edge_attr(color=color1)
     g.edge(gtext[e[0]], gtext[e[1]], color=color1) 
   print(str(g))
   if (len(filename) > 0):
     g.save(filename)
   return g

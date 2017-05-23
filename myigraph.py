import igraph
import numpy as np
from random import randint

def _plot(g, membership=None,filename='temp.png',lout="lgl",versize=10):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout(lout)
        g.es["color"] = edges_colors
    else:
        layout = g.layout(lout)
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    # visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = versize
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    #visual_style["edge_label"] = g.es["weight"]
    #for vertex in g.vs():
    #    vertex["label"] = vertex.index
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]
    igraph.plot(g,rescale=False,target=filename, **visual_style)
	
	
def _plot2(g, categories=None,filename='temp.png',lout="lgl",versize=5,intraprob=0.75,fload=False):
    if categories is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        gcopy.delete_edges(gcopy.es)
        nadded=0
				
        u, membership = np.unique(categories, return_inverse=True)
        u, index = np.unique(categories, return_index=True)
        u,c=np.unique(categories,return_counts=True)		
        minimum=np.min(c);
        

        if fload==False:
		
          for n1 in gcopy.vs:
	    for n2 in gcopy.vs:
	      if (membership[n1.index] == membership[n2.index]) and (np.random.rand()<=intraprob):
		gcopy.add_edges([(n1.index,n2.index)])
		edges_colors.append("gray")
	      else:
		#if (membership[n1.index] != membership[n2.index]) and (np.random.rand()<interprob):
		if (membership[n1.index] != membership[n2.index]) and (nadded<10*minimum):
		  gcopy.add_edges([(n1.index,n2.index)])
		  nadded=nadded+1
		  #edges_colors.append("black")
	  gcopy.write_gml('gcopy.gml')
        else:
	  gcopy = igraph.Graph.Read_GML('gcopy.gml');
	  
        layout = gcopy.layout(lout)
        g.es["color"] = "gray"
    else:
        layout = g.layout(lout)
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = versize
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    visual_style["label_size"]=36;
    #visual_style["edge_label"] = g.es["weight"]
	# Plot label for each representative
    if index is not None:
		for i in range(len(index)):
			g.vs[index[i]]["label"] = categories[index[i]]
			print categories[index[i]]
    if categories is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]
    igraph.plot(g,rescale=False,target=filename, **visual_style)

import sys
import networkx

def read_edges(file_name):
        try:
                file = open(file_name, 'r')
        except IOError:
                sys.exit('Could not open file: {}'.format(file_name))
        edges = []
        for line in file.readlines():
                cols = line.split(' ')
                edges.append((cols[0], cols[1].rstrip()))
        file.close()

        g = networkx.Graph()
        g.add_edges_from(edges)
	g = max(networkx.biconnected_component_subgraphs(g), key=len)
        g.remove_edges_from(g.selfloop_edges())
        return g

def DMP(g):
        v = g.number_of_nodes()
        e = g.number_of_edges()
        h = networkx.Graph()
	h.add_edges_from(networkx.find_cycle(g))
	b = []
	b.append((h.copy()))
	b.append((h.copy()))
        
	#Handles trivial cases
	if (v < 5):
                planar()
        if (3 * v - 6 < e):
                nonplanar()
        if (h is None):
                planar()
	
	#Upper bound determined by Euler's Formula f = e - v + 2
	for r in range(0, e - v):
		add_face(g, h, b)
	planar()

def add_face(g, h, b):
	nodes = list(h.nodes())
	path = None
	face = None

	#All unique vertex combos
	for i in range(0, len(nodes) - 1):
		start = nodes[i]
		for j in range(i + 1, len(nodes)):
			end = nodes[j]
			
			#Graph that is g - h except start and end
			copy = g.copy()
                       	copy.remove_edges_from(h.edges())
			copy.remove_nodes_from(n for n in list(h.nodes) if n not in {start, end})
			
			if networkx.has_path(copy, start, end):
				#List of regions for path to be embedded in
				regions = []
				for f in b:
               				if start in f.nodes() and end in f.nodes():
                       				regions.append(f)
				
				if len(regions) == 0:
					nonplanar()
				elif (len(regions) == 1):
					path = networkx.shortest_path(copy, source = start, target = end)
					face = regions[0]
					add_path(path, face, h, b)
					return
				else:
					path = networkx.shortest_path(copy, source = start, target = end)
					face = regions[0]
	add_path(path, face, h, b)

def add_path(path, face, h, b):
	start = path[0]
	end = path[len(path)-1]
	neighbors = list(face.neighbors(start))
	
	#Constructing the 2 new faces from path splitting face
	subface1 = networkx.Graph()
	n1 = start
	ne1 = neighbors[0]
	while n1 != end:
		subface1.add_edge(n1, ne1)
		temp = list(face.neighbors(ne1))
		temp.remove(n1)
		n1 = ne1
		ne1 = temp[0]

	subface2 = networkx.Graph()
	n2 = start
	ne2 = neighbors[1]
	while n2 != end:
		subface2.add_edge(n2, ne2)
		temp = list(face.neighbors(ne2))
		temp.remove(n2)
		n2 = ne2
		ne2 = temp[0]
       	
	#Updating structures with path
	for k in range (0, len(path) - 1):
        	h.add_edge(path[k], path[k+1])
                subface1.add_edge(path[k], path[k+1])
               	subface2.add_edge(path[k], path[k+1])
				
	#Restoring basis		
	b.append(subface1)
	b.append(subface2)
	b.remove(face)
	

def planar():
	sys.exit('PLANAR')

def nonplanar():
	sys.exit('NONPLANAR')

def main(argv):
        graph = read_edges(argv[1])
        result = DMP(graph)
        if result:
                print 'PLANAR'
	else:
                print 'NONPLANAR'


if __name__ == '__main__':
        main(sys.argv)


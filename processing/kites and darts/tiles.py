'''
this is different from the pentagon version
because we need to grow the tiling out
we will need ways of telling which tiles are on the border
and which of those are adjacent


probably the best will be to have edge and vertex objects
with methods to compare if they are the same.
then the tiles will have edges and vertices

the edges and vertices will be used to decide which shape to put
'''


class Vertex(object):
    ''' A vertex has coordinates, and colour'''
    def __init__(self, coords, colour):
        self.coords = coords
        self.colour = colour

    def __repr__(self):
        colour = "White" if self.colour == 'w' else 'Black'
        return colour+' vertex at '+str(self.coords)

    def __hash__(self):
        return hash((self.coords, self.colour))

    def __eq__(self, other):
        ''' Two vertices are the same if they share
            coordinates and colour'''
        if self.colour == other.colour :
            return self.coords == other.coords
        else: return False


class  Edge(object):
    ''' An edge has two edges and a colour'''
    def __init__(self, vertex1, vertex2, colour):
        if vertex1 == vertex2:
            print('Same vertices!!')
        self.vertices = set([vertex1, vertex2])
        self.colour = colour

    def __repr__(self):
        colour = "Green" if self.colour == 'g' else 'Red'
        coords = [v.coords for v in self.vertices]
        return colour+' edge between '+str(coords[0])+' and '+str(coords[1])

    def __hash__(self):
        return hash(self.vertices, self.colour)

    def __eq__(self, other):
        '''Two edges are the same if they share colour
            and vertices
        '''
        if self.colour == other.colour :
            return self.vertices == other.vertices
        else: return False

    def __contains__(self, vertex):
        return vertex in self.vertices
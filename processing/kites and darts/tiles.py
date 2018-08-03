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

import math

ROTATION_MATRICES ={
        72 : (math.cos(.4*math.pi), math.sin(.4*math.pi)),
        144: (math.cos(.8*math.pi), math.sin(.8*math.pi)),
        -72 : (math.cos(-.4*math.pi), math.sin(-.4*math.pi)),
        -144: (math.cos(-.8*math.pi), math.sin(-.8*math.pi)),
        }

FACTORS= {
    'green_kite': math.tan(0.1*math.pi),
    'red_kite': 1./math.tan(0.2*math.pi),
    'green_dart': -math.tan(0.1*math.pi),
    'red_dart': -math.cos(0.1*math.pi)
}



class Vector(list):

    def __init__(self, l=[]):
        ''' converts to float to avoid surprises later on'''
        if type(l) not in (list, tuple):
            inner_list = list(l)
        else: inner_list = l
        float_list = [float(x) for x in l]
        super(Vector, self).__init__(float_list)

    def __neg__(self):
        return Vector([-x for x in self])

    def __abs__(self):
        return math.sqrt(sum([x**2 for x in self]))

    def __eq__(self, other):
        if type(self) is not type(other):
            raise ValueError
        return list(self) == list(other)

    def __add__(self, other):
        if type(other) in (int, float):
            return self.scalar_addition(other)
        else:
            return self.vector_addition(other)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(self) is type(other):
            return self.vector_multiplication(other)
        elif type(other) in (int,float):
            return self.scalar_multiplication(other)
        else:
            raise ValueError

    def __truediv__(self, other):
        return self*float(1/other)

    def __radd__(self, other):
        return self+other

    def __rmul__(self, other):
        return self*other

    def rotate_vector(self, other, angle):
        diff = other - self
        if angle in ROTATION_MATRICES.keys():
            cos, sin = ROTATION_MATRICES[angle]
        else:
            cos, sin = math.cos(angle), math.sin(angle)
        rotated = [cos*diff[0] - sin*diff[1], sin*diff[0] + cos*diff[1]]
        return self + Vector(rotated)
        

    def vector_addition(self, other):
        return Vector([x1+x2 for x1, x2 in zip(self,other)])
    def scalar_addition(self, other):
        return Vector([x1 + float(other) for x1 in self])
    def vector_multiplication(self, other):
        return Vector([x1*x2 for x1, x2 in zip(self,other)])
    def scalar_multiplication(self, other):
        return Vector([x1 * float(other) for x1 in self])


class Vertex(Vector):
    ''' A vertex is a vector with colour'''
    def __init__(self, coords, colour):
        super(Vertex, self).__init__(coords)
        self.colour = colour

    @property
    def coords(self):
        return tuple(self)
    
    def __repr__(self):
        colour = "White" if self.colour == 'w' else 'Black'
        return colour+' vertex at '+super(Vertex, self).__repr__()

    def __hash__(self):
        return hash((self.coords, self.colour))

    def __eq__(self, other):
        ''' Two vertices are the same if they share
            coordinates and colour
            Probably need to have a lenient version'''
        if self.colour == other.colour :
            return self.coords == other.coords
        else: return False

    @property
    def vector(self):
        return Vector(list(self.coords))

    def rotate_vertex(self, other, angle):
        ''' Returns a vertex same colour as other, 
        rotated about self by angle'''
        return Vertex(self.rotate_vector(other, angle), other.colour)

    def bisect(self, v1, v2):
        return 0.5*sum([v1-self, v2-self])




class  Edge(object):
    ''' An edge has two vertices and a colour'''
    def __init__(self, vertex1, vertex2, colour):
        if vertex1 == vertex2:
            print('Same vertices!!')
        self.vertices = (vertex1, vertex2)
        self.colour = colour

    def __repr__(self):
        colour = "Green" if self.colour == 'g' else 'Red'
        coords = [v.coords for v in self.vertices]
        return colour+' edge between '+str(coords[0])+' and '+str(coords[1])

    def __hash__(self):
        return hash((self.vertices, self.colour))

    def __eq__(self, other):
        '''Two edges are the same if they share colour
            and vertices
        '''
        if self.colour == other.colour :
            return self.vertices == other.vertices
        else: return False

    def __contains__(self, vertex):
        return vertex in self.vertices

    @property
    def white_vertex(self):
        for v in self.vertices:
            if v.colour == 'w':
                return v
    @property
    def black_vertex(self):
        for v in self.vertices:
            if v.colour == 'b':
                return v

    @property
    def white_black(self):
        return (self.white_vertex, self.black_vertex)
    


''' Can make basic tiles, then make 'aware' tiles later'''

class Tile(object):

    def __init__(self, edge,clockwise=False):
        if edge.colour == 'g':
            self.build_from_green(edge,clockwise)
        else: self.build_from_red(edge,clockwise)

    def build_from_green(edge):
        raise NotImplemented

    def build_from_red(edge):
        raise NotImplemented

    #this will be overridden for the aware tile
    def assign(self, vertices, edges):
        self.vertices = tuple(vertices)
        self.edges = tuple(edges)

    def __hash__(self):
        return hash((self.vertices, self.edges))

    def bisect_and_scale(self, centre, v1, v2, factor):
        ''' This is handy in building the last vertex.
            Obtains the vector bisecting the angle v1_self_v2
            Scales it by (1+height/bisector*factor)
            and returns a new vertex, same colour as self, there.
        '''
        bisector = centre.bisect(v1, v2)
        height = 0.5*abs(v1-v2)
        additonal_distance = height/abs(bisector)*factor
        displacement = (1.0+additonal_distance)*bisector
        return Vertex(displacement+centre, centre.colour)

class Kite(Tile):

    def build_from_green(self, edge, clockwise=False):
        white, black = edge.white_black
        # getting the other black edge
        # need only to rotate the first one through 72 degrees
        angle = 72 if not clockwise else -72
        new_black = white.rotate_vertex(black, angle)
        new_white = self.bisect_and_scale(white, black, new_black, FACTORS['green_kite'])

        # assign
        vertices = white, black, new_white, new_black
        edges = (  edge, 
                        Edge(black, new_white,'r'), 
                        Edge(new_white,new_black,'r'),
                        Edge(new_black, white, 'g')
                    )
        self.assign(vertices, edges)

    def build_from_red(self, edge, clockwise=False):
        white, black = edge.white_black
        # getting the other black edge
        # need only to rotate the first one through 144 degrees
        angle = 144 if not clockwise else -144
        new_black = white.rotate_vertex(black, angle)
        new_white = self.bisect_and_scale(white, black, new_black, FACTORS['red_kite'])

        # assign
        vertices = white, black, new_white, new_black
        edges = (  edge, 
                        Edge(black, new_white,'g'), 
                        Edge(new_white,new_black,'g'),
                        Edge(new_black, white, 'r')
                    )
        self.assign(vertices, edges)

    def __rep__(self):
        return 'Kite with '+str(self.vertices)


class Dart(Tile):

    def build_from_green(self, edge, clockwise=False):
        white, black = edge.white_black
        # getting the other black edge
        # need only to rotate the first one through 72 degrees
        angle = 72 if not clockwise else -72
        new_white = black.rotate_vertex(white, angle)
        new_black = self.bisect_and_scale(black, white, new_white, FACTORS['green_dart'])

        # assign
        vertices = black, white, new_black, new_white
        edges = (  edge, 
                        Edge(white, new_black,'r'), 
                        Edge(new_black, new_white,'r'),
                        Edge(new_white, black, 'g')
                    )
        self.assign(vertices, edges)


    def build_from_red(self, edge, clockwise=False):
        white, black = edge.white_black
        # getting the other black edge
        # need only to rotate the first one through 72 degrees
        angle = 144 if not clockwise else -144
        new_white = black.rotate_vertex(white, angle)
        bisector = black.bisect(white, new_white)
        height = 0.5*abs(white-new_white)
        scale = height/abs(bisector)*FACTORS['red_dart']
        new_black = Vertex(black+scale*bisector, 'b')

        # assign
        vertices = black, new_white, new_black, white
        edges = (  edge, 
                        Edge(black, new_white,'r'), 
                        Edge(new_white, new_black,'g'),
                        Edge(new_black, white, 'g')
                    )
        self.assign(vertices, edges)


    def __rep__(self):
        return 'Dart with '+str(self.vertices)


class BetterKite(Kite):
    pass



def star(edge):
    '''returns a list of tiles in the shape of a star'''
    if edge.colour != 'g':
        raise ValueError
    tile_list = []
    current_edge = edge
    for i in range(5):
        current_tile = Dart(current_edge)
        tile_list.append(current_tile)
        current_edge = current_tile.edges[-1]
    return tile_list

def sun(edge):
    '''returns a list of tiles in the shape of a star'''
    if edge.colour != 'g':
        raise ValueError
    tile_list = []
    current_edge = edge
    for i in range(5):
        current_tile = Kite(current_edge)
        tile_list.append(current_tile)
        current_edge = current_tile.edges[-1]
    return tile_list

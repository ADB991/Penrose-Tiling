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


    def __rmul__(self, other):
        return self*other



    def rotate_vector(self, other, angle):
        diff = other - self
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
    ''' A vertex has coordinates, and colour'''
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
            coordinates and colour'''
        if self.colour == other.colour :
            return self.coords == other.coords
        else: return False

    @property
    def vector(self):
        return Vector(list(self.coords))


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

class Kite(object):
    def __init__(self, edge):
        if edge.colour == 'g':
            self.build_from_green(edge)
        else: self.build_from_red(edge)

    def build_from_green(self, edge, clockwise=False):
        white, black = edge.white_black
        # getting the other black edge
        # need only to rotate the first one through 72 degrees
        angle = math.pi*2.0/5.0
        if clockwise: angle *= -1
        new_black_vector = (white.vector).rotate_vector(black.vector, angle)
        new_black = Vertex(tuple(new_black_vector), 'b')

        white_to_black = black.vector - white.vector
        white_to_new_black = new_black_vector - white.vector
        direction = .5*(white_to_black + white_to_new_black)
        height = abs(black.vector - new_black_vector)
        additonal_distance = height/abs(direction)*math.cos(0.2*math.pi)/math.tan(0.1*math.pi)
        displacement = (1.0+additonal_distance)*direction
        new_white_vector = white.vector + displacement
        new_white = Vertex(tuple(new_white_vector), 'w')
        
        self.vertices = [white, black, new_white, new_black]
        self.edges = [  edge, 
                        Edge(black, new_white,'r'), 
                        Edge(new_white,new_black,'r'),
                        Edge(new_black, white, 'g')
                    ]

    def __rep__(self):
        return 'Kite with '+str(self.vertices)










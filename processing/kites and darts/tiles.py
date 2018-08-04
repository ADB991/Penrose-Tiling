'''
Here we have the basic geometric objects and methods

Vector is a vector class with nothing special
except for memorised rotrions for the angles used here.

A Vertex is little more than a vector with colour.

An Edge is composed of two Vertex and colour,
it has a little more geometrical awareness to deal

A Tile is a class with a list of vertices and edges,
it's a basis class for our two other classes:

Kite and Dart which differ only on how they build themselves

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

    def bisect(self, v1, v2):
        return 0.5*sum([v1-self, v2-self])
        

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

    def contains_point(self, vertex):
        a, b = self.line_coefficients()
        x, y = vertex.coords
        coords1, coords2 = self.coords
        x_coords = (coords1[0], coords2[0])
        y_coords = (coords1[1], coords2[1])
        in_rectangle =(
             (min(x_coords) <= x ) and (max(x_coords) >= x)
             and (min(y_coords) <= y ) and (max(y_coords) >= y)
            )
        if in_rectangle: return y == a*x+b
        else: return False

    def to_the_right(self, vertex, allow_crossing_horizontal=False):
        ''' Returns True if an horizontal half-line extending to
            the right would cross the edge.
            Assumes the point is *not on* the edge,
            in which case the question is ill-posed
        '''
        a, b = self.line_coefficients()
        x, y = vertex.coords
        coords1, coords2 = self.coords
        x_coords = (coords1[0], coords2[0])
        y_coords = (coords1[1], coords2[1])
        if a == 0:
            if not allow_crossing_horizontal:
                return False
            return y == coords1[1]
        #determine if it is in the corridor
        is_above = y >= max(y_coords)
        is_below = x < min(y_coords)
        is_to_the_right = x >= max(x_coords)
        if (is_above or is_below or is_to_the_right):
            return False
        #if we get here the point is in the corridor
        # to the left of the edge
        # if the line is vertical, it's a sure hit
        if a is None:
            return True
        point_below_line = y < (a*x+b)
        line_going_down = (a<0)   
    #point below    line going down     cross
    #no             no                  yes
    #no             yes                 no
    #yes            no                  no
    #yes            yes                 no
        return point_below_line == line_going_down


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

    @property
    def coords(self):
        return (v.coords for v in self.vertices)
    
    def line_coefficients(self):
        '''returns a and b in the equation
        y = ax + b of the line on which the edge lies'''
        coords1, coords2 = self.coords
        delta_x, delta_y = (coords2[i] - coords1[i] for i in range(2))
        a = delta_y / delta_x if delta_x != 0 else None
        b = coords1[1]-a*coords1[0]
        return a, b


''' Can make basic tiles, then make 'aware' tiles later'''

class Tile(object):

    def __init__(self, edge, clockwise=False):
        if edge.colour == 'g':
            vertices, edges = self.build_from_green(edge,clockwise)
        else: 
            vertices, edges = self.build_from_red(edge,clockwise)
        self.assign_definition(edge, clockwise)
        self.assign(vertices, edges)

    #these two methods be overridden for the aware tile
    def assign_definition(self, edge, clockwise):
        self.definition = (edge, clockwise)

    def assign(self, vertices, edges):
        self.vertices = tuple(vertices)
        self.edges = tuple(edges)

    def build_from_green(edge):
        raise NotImplemented

    def build_from_red(edge):
        raise NotImplemented



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

    def covers(self, vertex):
        ''' tests wether the vertex is on the edges
        or inside the area of the tile'''
        for edge in self.edges:
            if edge.contains_point(vertex): return True
        num_crossings = sum([edge.to_the_right(vertex) for edge in self.edges])
        return (num_crossings%2 == 1)



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
        return vertices, edges

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
        return vertices, edges

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
        return vertices, edges


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
        return vertices, edges


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
    '''returns a list of tiles in the shape of a sun'''
    if edge.colour != 'g':
        raise ValueError
    tile_list = []
    current_edge = edge
    for i in range(5):
        current_tile = Kite(current_edge)
        tile_list.append(current_tile)
        current_edge = current_tile.edges[-1]
    return tile_list

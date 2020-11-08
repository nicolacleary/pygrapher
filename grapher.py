"""
Simple graph plotter

Plots a graph in a tkinter window with axes, grid lines and displays
functions in the form y = f(x) using functions.py
"""

from functions import *
from tkinter import Tk, Canvas

class App:
    """A window with a Graph object that can be run to display the graph.

        Attributes:
            height (int): The height of the window.
            width (int): The width of the window.
            window (Tkinter.Tk): The window object that holds the canvas.
            graph (Graph): The canvas and lines which can be plotted to represent the graph.
            
    """
    
    def __init__(self):
        self.height = 600
        self.width = 800
        
        self.window = Tk()
        self.window.title('Graph')
        self.graph = Graph(self.window, self.height, self.width)

        #Initialise axes and gridlines so they lie underneath
        #the plotted functions
        self.graph.add_grid_lines()
        self.graph.add_axes()

    def add_function(self, function):
        """Adds a line representing a function to the list of lines.

        Parameters:
            function (Funciton): The function which should be added as a line.

        """
        
        self.graph.add_line(FunctionLine(function))

    def add_axis(self, function):
        """Adds a horizontal or vertical line to the list of lines.

        Parameters:
            function (Funciton): The function which should be added as a line.

        """
        
        if function.get_name() == 'x':
            orientation = 'horizontal'
        else:
            orientation = 'vertical'
        self.graph.add_line(Axis(orientation, function.calculate_value(0)))

    def run(self):
        """Plot the graph and open the window.

        """
        
        self.graph.plot()
        self.window.mainloop()


class Graph:
    """A canvas and group of lines that can be plotted to represent a graph.

        Attributes:
            height (int): The height of the canvas.
            width (int): The width of the canvas.
            scale (int, int): Values representing how many pixels represent 1 unit in x and y directions.
            centre (int, int): An x and y value representing the location of the centre of the canvas.
            range (int, int): The range of x and y values that the graph shows.
            lines ([Line]): The list of lines that the graph can plot.
            line_colours ([str]): The default colours that can be assigned to lines.
            axis_colour (str): The colour of the axes.
            grid_colour (str): The colour of the gridlines.
            canvas (tkinter.Canvas): The canvas object which shows the lines.
    """
    
    def __init__(self, master, height, width):
        self.height = height
        self.width = width

        #Conversion from coordinates to pixels (e.g. 1 unit = 10 pixels)
        self.scale = (20, 10) 
        self.centre = (width//2, height//2)
        self.range = (self.centre[0] // self.scale[0], self.centre[1] // self.scale[1])

        self.lines = []
        
        self.line_colours = ['red', 'green', 'blue']
        self.axis_colour = 'black'
        self.grid_colour = '#D3D3D3' #Light grey
        self.canvas = Canvas(bg='white', height=self.height, width=self.width)

    def add_line(self, line, colour=None):
        """Adds a line to the list of lines to be plotted.

        Parameters:
            line (FunctionLine or Axis): The line to be added.
            colour (str): The colour of the line (assigns colour if None).
       
        """

        #Assign a colour from a list
        if colour == None:
            colour = self.line_colours[len(self.lines) % len(self.line_colours)]
            
        line.set_colour(colour)
        self.lines.append(line)

    def add_axes(self):
        """Adds axes to the list of lines to be plotted.
       
        """
        
        x_axis = Axis('horizontal', 0)
        y_axis = Axis('vertical', 0)

        self.add_line(x_axis, self.axis_colour)
        self.add_line(y_axis, self.axis_colour)

    def add_grid_lines(self):
        """Adds grid lines to the list of lines to be plotted.
       
        """
        
        unit = 5
        for counter in range(0, self.range[0], unit):
            self.add_line(Axis('vertical', counter), self.grid_colour)
            self.add_line(Axis('vertical', -counter), self.grid_colour)

        for counter in range(0, self.range[1], unit):
            self.add_line(Axis('horizontal', counter), self.grid_colour)
            self.add_line(Axis('horizontal', -counter), self.grid_colour)
            
    def plot(self):
        """Plots each line on the canvas.
       
        """
        
        for line in self.lines:
            line.draw(self, -self.range[0], -self.range[1], self.range[0], self.range[1])
        self.canvas.pack()

    def convert_coordinate(self, coordinate):
        """Converts a coordinate into a position on the canvas.

        Parameters:
            coordinate (Coordinate): The coordinate to be converted.

        Returns:
            Coordinate: A new coordinate that refers to the canvas.        
        """
        
        #If coordinate is invalid, disregard
        if not coordinate.is_valid():
            return Coordinate(None, None)

        #Canvas coordinates start from top left corner
        #So place in centre and then adjust and scale
        new_coordinate = Coordinate(
            self.centre[0] + round(coordinate.get_x() * self.scale[0]),
            self.centre [1] - round(coordinate.get_y() * self.scale[1])
        )

        return new_coordinate

    def get_canvas(self):
        return self.canvas

class Coordinate:
    """A pair of x, y values that represent a point on the graph.

        If any value x or y is None, the coordinate is invalid.

        Attributes:
            x (int/float or None): The x value.
            y (int/float or None): The y value.
    """

    def __init__(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def set_x(self, x):
        """Changes the x coordinate.

        Parameters:
            x (int/float): The new x value.

        Raises:
            TypeError: If x is not an integer or a float.         
        """
        
        if not (isinstance(x, int) or isinstance(x, float) or x==None):
            raise TypeError('x coordinate must be a float, integer or None')
        self.x = x

    def set_y(self, y):
        """Changes the y coordinate.

        Parameters:
            y (int/float): The new y value.

        Raises:
            TypeError: If y is not an integer or a float.         
        """
        if not (isinstance(y, int) or isinstance(y, float) or y==None):
            raise TypeError('y coordinate must be a float, integer or None')
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def is_valid(self):
        """Indicates if the coordinate is valid or not.

        Returns:
            bool: If the coordinate is valid (i.e. x,y are real and not None).     
        """
        
        return self.x != None and self.y != None

    def in_range(self, x_min, y_min, x_max, y_max):
        """Indicates if the coordinate is within a given range.

        Returns:
            bool: If the coordinate is valid and within the range.     
        """
        
        if not self.is_valid():
            return False

        return (self.x >= x_min and self.x <= x_max) and (self.y >= y_min and self.y <= y_max)

    def swap(self):
        """Swaps the x and y coordinate, reflecting it in y=x.
    
        """
        temp = self.x
        self.x = self.y
        self.y = temp

    def __str__(self):
        return '({x}, {y})'.format(x=self.x, y=self.y)
    

class FunctionLine:
    """A line which can be represented by y=f(x).

        Attributes:
            function (Function): The funciton f(x) that represents the line.
            colour (str): The hexcode or name of the colour of the line (default is red).
            coordinates ([Coordinate]): The coordinates of points on the line.
            sublines ([int]): The IDs of the lines on the canvas.
            no_sublines (int): The number of lines that should be drawn to represent the funciton.
    """

    def __init__(self, function, colour='red'):
        if not isinstance(function, Function):
            raise TypeError('function must be an instance of Function')

        self.function = function
        self.colour = colour
        self.coordinates = [] 
        self.sublines = [] 
        self.no_sublines = 500

    def set_colour(self, colour):
        """Changes the colour of the line.

            Parameters:
                colour (str): The new colour (hexcode or colour name).
        """
        self.colour = colour

    def draw(self, graph, x_min, y_min, x_max, y_max):
        """Draws y=f(x) on the graph.

            Parameters:
                x_min (int/float): The minimum x value that is shown on the graph.
                x_max (int/float): The maximum x value that is shown on the graph.
                y_min (int/float): The minimum y value that is shown on the graph.
                y_max (int/float): The maximum y value that is shown on the graph.
        """
        
        self.generate_coordinates(x_min, x_max)
        self.draw_sublines(graph, x_min, y_min, x_max, y_max)

    def generate_coordinates(self, a, b):
        """Generates coordinates for y=f(x) for some a <= x <= b.

            Parameters:
                a (int/float): The start x coordinate of the range to evaluate f(x) for.
                b (int/float): The end x coordinate of the range to evaluate f(x) for.
        """
        self.coordinates = []
        step = (b-a) / self.no_sublines

        #Calculate (number of sub lines + 1) coordinates for the line
        for counter in range(self.no_sublines + 1):
            x = a + (counter * step)
            try:
                y = self.function.calculate_value(x)
                
            #If the result is a complex number, or function is undefined for
            #that x value
            except ValueError:
                y = None

            #Usually caused by an invalid x value, so say function is undefined
            #for y and provide a valid x value
            except:
                x = None
                y = None
                
            self.coordinates.append(Coordinate(x, y))

    def draw_sublines(self, graph, x_min, y_min, x_max, y_max):
        """Draws straight lines between adjacent coordinates to form the line.

            Parameters:
                x_min (int/float): The minimum x value that is shown on the graph.
                x_max (int/float): The maximum x value that is shown on the graph.
                y_min (int/float): The minimum y value that is shown on the graph.
                y_max (int/float): The maximum y value that is shown on the graph.
        """
        
        self.sublines = []
        #Accesses coordinates in pairs and draws a straight line
        #between them
        for i in range(len(self.coordinates) -1):
            c1 = self.coordinates[i]
            c2 = self.coordinates[i+1]

            #If either is invalid, do not draw the line
            if not (c1.is_valid() and c2.is_valid()):
                continue

            #If either is out of range, do not draw the line
            if not (c1.in_range(x_min, y_min, x_max, y_max) and c2.in_range(x_min, y_min, x_max, y_max)):
                continue

            #Convert the coordinates into canvas locations
            n1 = graph.convert_coordinate(c1)
            n2 = graph.convert_coordinate(c2)

            canvas = graph.get_canvas()
            
            line = canvas.create_line(n1.get_x(), n1.get_y(), n2.get_x(), n2.get_y(), fill=self.colour)
            self.sublines.append(line)

    def __str__(self):
        return 'y = {function}'.format(function=self.function)

class Axis(FunctionLine):
    """A line which is perpendicular to one of the axes.

        Attributes:
            orientation (int): Indicates if the line is parallel to the x or y axis.
    """

    orientations = {
        'vertical' : 0,
        'horizontal': 1
        }

    variable_names = {
        'vertical' : 'x',
        'horizontal' : 'y'
        }

    def __init__(self, orientation, value, colour='red'):
        if orientation not in Axis.orientations.keys():
            raise ValueError('Invalid value for orientation')
        
        self.orientation = Axis.orientations[orientation]

        try:
            f = Function([Constant(value)], Axis.variable_names[orientation])
        except TypeError:
            raise

        super().__init__(f, colour)

    def draw(self, graph, x_min, y_min, x_max, y_max):
        """Draws an axis (horizontal or vertical line) on the graph.

            Parameters:
                x_min (int/float): The minimum x value that is shown on the graph.
                x_max (int/float): The maximum x value that is shown on the graph.
                y_min (int/float): The minimum y value that is shown on the graph.
                y_max (int/float): The maximum y value that is shown on the graph.
        """
        
        if self.orientation == Axis.orientations['horizontal']:
            self.generate_coordinates(x_min, x_max)
            
        else:
            #Treat a vertical line like a horizontal one, then
            #swap x and y coordinates, essentially reflecting
            #it in y=x
            self.generate_coordinates(y_min, y_max)
            for coordinate in self.coordinates:
                coordinate.swap()
                
        self.draw_sublines(graph, x_min, y_min, x_max, y_max)

    #Generate values for f(a), ..., f(b)
    def generate_coordinates(self, a, b):
        """Generates coordinates of the start and end points of the line.

        Parameters:
            a (int/float): The start x coordinate (horizontal) or y coordinate (vertical).
            b (int/float): The end x coordinate (horizontal) or y coordinate (vertical).
        """
        
        self.coordinates = []

        try:
            #Treats the line like its horizontal (i.e. constant y value, x varies)
            #If it is a vertical line, this can be later accounted for by switching
            #x and y coordinates
            self.coordinates.append(Coordinate(a, self.function.calculate_value(a)))
            self.coordinates.append(Coordinate(b, self.function.calculate_value(b)))
        except:
            self.coordinates = [Coordinate(None, None), Coordinate(None, None)]

    def __str__(self):
        if self.orientation == Axis.orientations['horizontal']:
            return 'x = {function}'.format(function=self.function)
        return 'y = {function}'.format(function=self.function)

  
            
if __name__ == '__main__':
    app = App()

    examples = [
        Function([Power(Constant(1), Constant(1)), Constant(1)]),
        Function([Power(Constant(1), Constant(2))]),
        Function([Power(Constant(1), Constant(3))]),
        Function([Constant(5)], 'y'),
        Function([Constant(6)]),
        Function([Power(Constant(1), Constant(-1))]),
        Function([Power(Constant(1), Constant(0.5))])
        ]

    #Display menu of different functions that the user can see
    counter = 1
    for example in examples:
        print('{no}: {function}'.format(no=counter, function = str(example)))
        counter += 1
    print()

    #Get the user's selection of function to see
    response = -1
    while response < 1 or response > len(examples):
        print('Please ensure that you enter a number between 1 and {no}'.format(no=len(examples)))
        try:
            response = int(input('Please choose a function to see: '))
        except ValueError:
            print('Please enter an integer')
            response = -1
            continue

    response -= 1

    if response == 3 or response == 4:
        app.add_axis(examples[response])
    else:
        app.add_function(examples[response])

    app.run()
        









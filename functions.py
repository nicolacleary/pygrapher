"""
Simple mathemetical function implementation

Implements functions as a group of terms that can then be evaluated
for different x values. Terms can either be expressed as a constant
or a power of x with a multiplicative constant
"""

from abc import ABC, abstractmethod 

class Term(ABC):
    """Abstract class for inheritance that provides one abstract method.

    A term should have some kind of numerical value and should be able
    to calculate a value for a given x value.

    """
    
    @abstractmethod
    def calculate_value(self, x):
        pass


class Constant(Term):
    """A term in the form c that has a constant value.

        Attributes:
            value (int/float): The constant value.
    """

    def __init__(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError('Value must be a float or an integer: value={x}'.format(x=value))
        self.value = value

    def calculate_value(self, x):
        """Evaluates the constant for a specific value of x.

        Parameters:
            x (int/float): The value of x that the term should be evaluated for.

        Returns:
            float: The value of the constant term.
        """
        return self.value

    def __str__(self):
        return str(self.value)

class Power(Term):
    """A term in the form ax^b that can be evaluated for int or float values of x.

        Attributes:
            a (int/float): The multiplicative term.
            b (int/float): The power which x should be raised to.
    """

    def __init__(self, a, b):
        self.set_a(a)
        self.set_b(b)

    def set_a(self, a):
        """Sets the value of the multiplicative term.

        Parameters:
            a (Term): The term which is the new multiplicative term.

        Raises:
            TypeError: If a is not a Term obj.
        """
        
        if not isinstance(a, Term):
            raise TypeError('a must be an instance of a Term object')
        self.a = a

    def set_b(self,b):
        """Sets the value of the power term.

        Parameters:
            b (Term): The term which is the new power term.

        Raises:
            TypeError: If b is not a Term obj.
        """
        if not isinstance(b, Term):
            raise TypeError('b must be an instance of a Term object')
        self.b = b

    def calculate_value(self, x):
        """Evaluates the term for a specific value of x.

        Parameters:
            x (int/float): The value of x that the term should be evaluated for.

        Returns:
            float: The value of the term when x=x.

        Raises:
            ValueError: If the result is a complex number (negative number raised a fractional power).
        """
        
        result = self.a.calculate_value(x) * (x)**self.b.calculate_value(x)

        if isinstance(result, complex):
            raise ValueError('Result is a complex number: {result}'.format(result=result))
        return result

    def __str__(self):
        return '{a}x^({b})'.format(a=self.a, b=self.b)


class Function():
    """A list of terms that can be evaluated for int or float values of x.

        Attributes:
            terms ([Term]): The list of terms that can be evaluated, default is empty.
            name (str): The name of the variable used in the function, default is x.
    """
    
    def __init__(self, terms=[], name='x'):
        self.terms = terms
        self.name = name

    def add_term(self, term):
        """Adds a term to the function.

        Parameters:
            term (Term): The term to be added.

        Raises:
            TypeError: If the term is not a Term object.
        """
        
        if not isinstance(term, Term):
            raise TypeError('Term must be an instance of a Term object')
        self.terms.append(term)

    def remove_term(self, index):
        """Removes a term from the function.

        Parameters:
            index (int): The position of the term to be removed.

        Raises:
            TypeError: If the index is not an integer.
            IndexError: If the index is not in range.            
        """
        
        if not isinstance(index, int):
            raise TypeError('Index must be an integer')
        if index < 0 or index >= len(self.terms):
            raise IndexError('Index {i} is out of range 0 <= i < {n}'.format(i=index, n=len(self.terms)))
        self.terms.pop(index)

    def set_name(self, name):
        """Changes the variable name of the function.

        Parameters:
            name (str): The new variable name (must be one character long).

        Raises:
            TypeError: If x is not a str.
            ValueError: If the str is longer than one character.
        """
        
        if not isinstance(name, str):
            raise TypeError('Variable name must be a string')
        if len(name) != 1:
            raise ValueError('Variable name must only be one character')
        self.name = name

    def get_name(self):
        """Returns the name of the variable in the function.

        Returns:
            str: The name of the variable used in the function.
        """
        
        return self.name

    def calculate_value(self, x):
        """Evaluates the function for a specific value of x.

        Parameters:
            x (int/float): The value of x that the function should be evaluated for.

        Returns:
            float: The value of f(x).

        Raises:
            TypeError: If x is not an int or a float.
            ValueError: If the function is undefined (has no terms).
        """
        
        if not (isinstance(x, int) or isinstance(x, float)):
            raise TypeError('Value must be a float or an integer: {name}={x}'.format(name=self.name, x=x))

        if len(self.terms) == 0:
            raise ValueError('Function f({name}) is undefined'.format(name=self.name))

        result = 0

        for t in self.terms:
            try:
                result += t.calculate_value(x)
            except ValueError:
                raise 

        return result

    def __str__(self):
        if len(self.terms) == 0:
            return 'f({name}) = undefined'.format(name=self.name)
        
        return 'f({name}) = {terms}'.format(
            name=self.name, terms=' + '.join(str(term) for term in self.terms)
            )

    



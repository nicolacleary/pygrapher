#Test
import unittest
from functions import *
from grapher import *

class TestConstant(unittest.TestCase):

    def test_init(self):
        constant_term = Constant(1)
        self.assertEqual(constant_term.calculate_value(3), 1, 'Should be 1')

        with self.assertRaises(TypeError):
            constant_term=Constant('1') #String should not be accepted
            constant_term=Constant([0]) #List should not be accepted
            constant_term=Constant(2+3j) #Complex number should not be accepted
        

    def test_str(self):
        constant_term = Constant(5.35)
        self.assertEqual(str(constant_term), '5.35', 'Should be \'5.35\'')

class TestPower(unittest.TestCase):

    def test_error_a(self):
        with self.assertRaises(TypeError):
            power_term = Power(1, Constant(2)) #Multiplicative constant should inherit from Term
            power_term = Power('1', Constant(2))
            power_term = Power([1], Constant(2))
            power_term = Power(1.5, Constant(2))
            power_term = Power([Constant(1)], Constant(2))

    def test_error_b(self):
        with self.assertRaises(TypeError):
            power_term = Power(Constant(1), 2) #Power should inherit from Term
            power_term = Power(Constant(1), '2')
            power_term = Power(Constant(1), [2])
            power_term = Power(Constant(1), 2.5)
            power_term = Power(Constant(1), Constant(2))

    def test_multiplication(self):
        power_term = Power(Constant(2), Constant(1))
        self.assertEqual(power_term.calculate_value(3), 6, 'Should be 6')
        self.assertEqual(power_term.calculate_value(4), 8, 'Should be 8')
        self.assertEqual(power_term.calculate_value(5), 10, 'Should be 10')

    def test_power(self):
        power_term = Power(Constant(1), Constant(2))
        self.assertEqual(power_term.calculate_value(1), 1, 'Should be 1')
        self.assertEqual(power_term.calculate_value(2), 4, 'Should be 4')
        self.assertEqual(power_term.calculate_value(3), 9, 'Should be 9')

    #1.5 = 3/2
    def test_fractional_powers(self):
        power_term = Power(Constant(1), Constant(1.5))
        self.assertEqual(power_term.calculate_value(1), 1, 'Should be 1')
        self.assertEqual(power_term.calculate_value(4), 8, 'Should be sqrt(4) ^ 3 = 2^3 = 8')
        self.assertEqual(power_term.calculate_value(9), 27, 'Should be sqrt(9) ^ 3 = 3^3 = 27')

        with self.assertRaises(ValueError):
            power_term.calculate_value(-4) #Should produce an error since sqrt(-4) = 2i

        power_term = Power(Constant(1), Constant(-1))
        with self.assertRaises(ZeroDivisionError):
            power_term.calculate_value(0) #Should produce an error since 0^(-1) = 1/0

    #testing 3x^2
    def test_calculate_value(self):
        power_term = Power(Constant(3), Constant(2))
        self.assertEqual(power_term.calculate_value(-1), 3, 'Should be 3')
        self.assertEqual(power_term.calculate_value(1), 3, 'Should be 3')
        self.assertEqual(power_term.calculate_value(2), 12, 'Should be 12')
        self.assertEqual(power_term.calculate_value(3), 27, 'Should be 27')

    def test_str(self):
        power_term = Power(Constant(3), Constant(2))
        self.assertEqual(str(power_term), '3x^(2)', 'Should be \'3x^(2)\'')

        power_term = Power(Constant(3), Power(Constant(1), Constant(2)))
        self.assertEqual(str(power_term), '3x^(1x^(2))', 'Should be \'3x^(1x^(2))\'')



class TestNestedTerms(unittest.TestCase):

    #1x^(x^2)
    def test_two_powers(self):
        power_term = Power(Constant(1), Power(Constant(1), Constant(2)))
        self.assertEqual(power_term.calculate_value(-1), -1, 'Should be (-1)^(1) = 1')
        self.assertEqual(power_term.calculate_value(1), 1, 'Should be 1^1 = 1')
        self.assertEqual(power_term.calculate_value(2), 16, 'Should be 2^(4) = 16')
        self.assertEqual(power_term.calculate_value(3), 19683, 'Should be 3^9 = 19683')

    def test_str(self):
        power_term = Power(Constant(3), Constant(2))
        self.assertEqual(str(power_term), '3x^(2)', 'Should be \'3x^(2)\'')

        power_term.set_b(Power(Constant(1), Constant(2)))
        self.assertEqual(str(power_term), '3x^(1x^(2))', 'Should be \'3x^(1x^(2))\'')

        power_term.set_a(Power(Constant(3), Constant(1)))
        self.assertEqual(str(power_term), '3x^(1)x^(1x^(2))', 'Should be \'3x^(1)x^(1x^(2))\'')

class TestFunctions(unittest.TestCase):

    def test_variable_name(self):
        f = Function([])
        self.assertEqual(f.get_name(), 'x', 'Should be \'x\'')
        f.set_name('y')
        self.assertEqual(f.get_name(), 'y', 'Should be \'y\'')
        f.set_name('z')
        self.assertEqual(f.get_name(), 'z', 'Should be \'z\'')

    def test_add_remove_term(self):
        f = Function([])

        with self.assertRaises(TypeError):
            f.remove_term(0.5) #Float should not be accepted
            f.remove_term('0') #String should not be accepted
            f.remove_term([0]) #List should not be accepted

        with self.assertRaises(IndexError):
            f.remove_term(0) #Term list is empty

        with self.assertRaises(TypeError):
            f.add_term(0.5) #Float should not be accepted
            f.add_term('0') #String should not be accepted
            f.add_term([0]) #List should not be accepted

        with self.assertRaises(TypeError):
            f.add_term(None) #None should not be accepted

        f.add_term(Constant(1))
        f.remove_term(0)
        self.assertEqual(str(f), 'f(x) = undefined', 'No terms so should be \'f(x) = undefined\'')

        f.add_term(Constant(0))
        f.add_term(Constant(1))
        f.add_term(Constant(2))
        f.add_term(Constant(3))
        f.remove_term(3)
        self.assertEqual(str(f), 'f(x) = 0 + 1 + 2', 'Should be \'f(x) = 0 + 1 + 2\' since 3 was removed')

        f.remove_term(1)
        self.assertEqual(str(f), 'f(x) = 0 + 2', 'Should be \'f(x) = 0 + 2\' since 2 was removed')

        with self.assertRaises(IndexError):
            f.remove_term(-2) #Negative index
            f.remove_term(2) #Term list only has length 2
            f.remove_term(100) #Term list only has length 2

    def test_calculate_value(self):
        f = Function([])

        with self.assertRaises(ValueError):
            f.calculate_value(1) #Function is undefined

        f.add_term(Constant(1))

        with self.assertRaises(TypeError):
            f.calculate_value('1') #String should not be accepted
            f.calculate_value([0]) #List should not be accepted
            f.calculate_value(2+3j) #Complex number should not be accepted

        #Checking constants
        for i in range (-4, 5):
            self.assertEqual(f.calculate_value(i), 1 , 'f({x}) = 1'.format(x=i))
            d=i+0.5
            self.assertEqual(f.calculate_value(d), 1 , 'f({x}) = 1'.format(x=d))

        f.remove_term(0)
        f.add_term(Power(Constant(3), Constant(1)))

        #Checking simple multiplication
        for i in range (-4, 5):
            self.assertEqual(f.calculate_value(i), 3 * i , 'f({x}) = ({a}) * ({x})^({b})'.format(x=i, a=3, b=1))
            d=i+0.5
            self.assertEqual(f.calculate_value(d), 3 * d , 'f({x}) = ({a}) * ({x})^({b})'.format(x=d, a=3, b=1))

        f.remove_term(0)
        f.add_term(Power(Constant(1), Constant(2)))

        #Checking squaring
        for i in range (-4, 5):
            self.assertEqual(f.calculate_value(i), i * i , 'f({x}) = ({a}) * ({x})^({b})'.format(x=i, a=1, b=2))
            d=i+0.5
            self.assertEqual(f.calculate_value(d), d * d , 'f({x}) = ({a}) * ({x})^({b})'.format(x=d, a=1, b=2))

        f.remove_term(0)
        f.add_term(Power(Constant(1), Constant(0.5)))

        #Checking square roots
        squares = [0, 1, 4, 9, 16]
        for s in range(len(squares)):
            i = squares[s]
            self.assertEqual(f.calculate_value(i), s , 'f({x}) = ({a}) * ({x})^({b})'.format(x=i, a=1, b=2))

        f.remove_term(0)
        f.add_term(Power(Constant(1), Constant(1/3)))

        #Checking cube roots
        cubes = [0, 1, 8, 27, 64]
        for s in range(len(cubes)):
            i = cubes[s]
            #Test positive cube roots
            self.assertEqual(f.calculate_value(i), s , 'f({x}) = ({a}) * ({x})^({b})'.format(x=i, a=1, b=2))
            #Test negative roots
            self.assertEqual(f.calculate_value(-i), -s , 'f({x}) = ({a}) * ({x})^({b})'.format(x=-i, a=1, b=2))

        f.remove_term(0)
        f.add_term(Constant(7))
        f.add_term(Power(Constant(3), Constant(2)))

        #Testing combined terms f(x) = 7 + 3x^2
        for i in range(-5, 6):
            self.assertEqual(f.calculate_value(i), 7 + 3 * i ** 2,
                             'f({x}) = 7 + ({a}) * ({x})^({b})'.format(x=i, a=3, b=2))

    def test_undefined(self):
        f = Function([])
        f.add_term(Constant(1))
        f.add_term(Power(Constant(1), Constant(0.5)))

        self.assertEqual(f.calculate_value(1), 1+1) #f(x) is defined for x >= 0

        with self.assertRaises(ValueError):
            f.calculate_value(-4) #Since f(x) not defined for x < 0
        

    def test_str(self):
        f = Function([])

        self.assertEqual(str(f), 'f(x) = undefined', 'No terms so should be \'f(x) = undefined\'')
        
        f.add_term(Constant(1))

        self.assertEqual(str(f), 'f(x) = 1', 'Should be \'f(x) = 1\'')

        f.add_term(Power(Constant(3), Constant(7)))

        self.assertEqual(str(f), 'f(x) = 1 + 3x^(7)', 'Should be \'f(x) = 1 + 3x^(7)\'')


class TestCoordinates(unittest.TestCase):

    def test_set(self):
        c = Coordinate(1, 2)

        for v in ['1', 1+2j, [1]]:
            with self.assertRaises(TypeError):
                c.set_x(v)
            with self.assertRaises(TypeError):
                c.set_y(v)

        c.set_x(None)
        c.set_y(2)
        self.assertEqual(str(c), '(None, 2)', 'Should be \'(None, 2)\'')

    def test_validity(self):
        c = Coordinate(1, 2)
        self.assertTrue(c.is_valid())

        c = Coordinate(1, None)
        self.assertTrue(not c.is_valid())

        c = Coordinate(None, 2)
        self.assertTrue(not c.is_valid())

    def test_range(self):
        for c in [Coordinate(1, None), Coordinate(None, 2), Coordinate(None, None)]:
            self.assertTrue(not c.in_range(1, 2, 3, 4)) #Upper range
            self.assertTrue(not c.in_range(0, 1, 1, 2)) #Lower range

            #X out of range
            self.assertTrue(not c.in_range(2, 2, 4, 4)) #Too small
            self.assertTrue(not c.in_range(-3, 2, -2, 4)) #Lower range

            #Y out of range
            self.assertTrue(not c.in_range(1, 3, 2, 4)) #Too small
            self.assertTrue(not c.in_range(1, -4, 2, -3)) #Too large

            #Both out of range
            self.assertTrue(not c.in_range(2, 3, 4, 5)) #Too small
            self.assertTrue(not c.in_range(-5, -4, -3, -2)) #Too large
            
        c = Coordinate(1, 2)
        self.assertTrue(c.in_range(1, 2, 3, 4)) #Upper range
        self.assertTrue(c.in_range(0, 1, 1, 2)) #Lower range

        #X out of range
        self.assertTrue(not c.in_range(2, 2, 4, 4)) #Too small
        self.assertTrue(not c.in_range(-3, 2, -2, 4)) #Lower range

        #Y out of range
        self.assertTrue(not c.in_range(1, 3, 2, 4)) #Too small
        self.assertTrue(not c.in_range(1, -4, 2, -3)) #Too large

        #Both out of range
        self.assertTrue(not c.in_range(2, 3, 4, 5)) #Too small
        self.assertTrue(not c.in_range(-5, -4, -3, -2)) #Too large

class TestAxis(unittest.TestCase):
    def test_init(self):
        for orientation in ['vertical', 'horizontal']:
            for value in [-1, 0, 1, 2.5, -2.5]:
                line = Axis(orientation, value)
                if orientation == 'vertical':
                    self.assertEqual(str(line), 'y = f(x) = {value}'.format(value=value))
                else:
                    self.assertEqual(str(line), 'x = f(y) = {value}'.format(value=value))
                    
            for value in [[1], '1', 1+3j]:
                with self.assertRaises(TypeError):
                   line = Axis(orientation, value)

                with self.assertRaises(ValueError):
                   line = Axis('not in dictionary', value) 
        

if __name__ == '__main__':
    unittest.main()

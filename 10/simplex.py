from unittest import TestCase
import numpy as np

def volume(array, *args):
    dimension = len(array)
    if dimension < 1:
        raise ValueError("Invalid space dimension")

    for point in array:
        if len(point) > dimension-1:
            raise ValueError("Point dimension is bigger than space")
        elif len(point) < dimension-1:
            raise ValueError("Point dimension is lower than space")

    
    last_point = array[-1]

    matrix = []
    for point in array[:-1]:
        matrix.append(np.subtract(point, last_point))
    det = np.linalg.det(matrix)
    fac_dim = np.math.factorial(dimension-1)
    return det/fac_dim





class VolumeTest(TestCase):

    def vol_triangle(self, a, b):
        return 1/2 * a * b

    def vol_tetrahedron(self, a, b, c):
        return 1/3 * self.vol_triangle(a, b) * c

    def test_triangle(self):
        n_simplex = [[0, 0], [0, 1], [1, 0]]
        vol = volume(n_simplex)
        self.assertEqual(vol, self.vol_triangle(1, 1))

    def test_simple_triangle(self):
        n_simplex = [[1, 1], [4, 1], [3, 0]]
        vol = volume(n_simplex)
        a = 2
        b = 3
        self.assertEqual(vol, self.vol_triangle(a, b))


    def test_simple_tetrahedron(self):
        n_simplex = [[0, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0]] 
        vol = volume(n_simplex)
        a = 1
        b = 1
        c = 1
        self.assertEqual(vol, self.vol_tetrahedron(a, b, c))

    def test_tetrahedron(self):
        n_simplex = [[1, 1, 0], [4, 1, 0], [1, 5, 0], [0, 0, 3]] 
        vol = volume(n_simplex)
        a = 3
        b = 4
        c = 3
        self.assertEqual(vol, self.vol_tetrahedron(a, b, c))

    def test_zero(self):
        n_simplex = [[0, 0],[0, 0],[0, 0]]
        vol = volume(n_simplex)
        self.assertEqual(vol, 0)        

    def test_wrong_points_triangle(self):
        n_simplex = [[1, 1, 0], [2, 4, 1], [5, 4 ,2]]
        self.assertRaises(volume(n_simplex), ValueError())

    def test_wrong_dimension(self):
        n_simplex = [[1, 2], [1, 4], [2, 5], [3, 5]]
        self.assertRaises(volume(n_simplex), ValueError())

    def test_str_in_point(self):
        n_simplex = [['s', 3], ['y', 4]]
        self.assertRaises(volume(n_simplex), ValueError())

    def not_array_of_array(self):
        n_simplex = [1, 2, 3]
        self.assertRaises(volume(n_simplex), ValueError())



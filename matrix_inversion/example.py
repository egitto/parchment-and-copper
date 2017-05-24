from matrix_inversion import *
import numpy

m = [
[4.5, 5.0, 0.0, 0.1, 2.0],
[1.0, 0.0, 3.4, 9.9, 1.0],
[0.99,0.1, 3.4, 9.9, 1.1],
[1.0, 0.1, 3.4, 9.9, 1.1],
[1.0, 0.1, 3.4, 9.9, 1.1001]
]
m_Fract = as_Fractions(m)
m_inv = invert(m_Fract)
id_matrix = matrix_multiply(m_inv, m_Fract)

m_np = numpy.matrix(m)
m_np_inv = numpy.linalg.inv(m_np)
almost_id_matrix = m_np_inv*m_np

print("matrix_inversion finds:\n",as_floats(id_matrix))
print("numpy finds:\n",almost_id_matrix)
NumPy Notes & Practice

This repository contains my personal notes, practice code, and examples while learning NumPy — one of the most important Python libraries for numerical computing and data science.

The goal of this repo is to understand NumPy fundamentals, array operations, mathematical computations, indexing, reshaping, and data manipulation techniques used in real-world machine learning and scientific computing.

⸻

Topics Covered

1. Introduction to NumPy

* What NumPy is
* Why NumPy is important
* Installing and importing NumPy

import numpy as np

⸻

2. NumPy vs Python Lists

Learned why NumPy arrays are preferred over normal Python lists.

Advantages of NumPy

* Faster computations
* Less memory usage
* Supports vectorized operations
* Better mathematical functionality

Example:

a = np.array([1, 2, 3])
print(a * 2)

Output:

[2 4 6]

⸻

3. Applications of NumPy

NumPy is widely used in:

* Data Science
* Machine Learning
* Artificial Intelligence
* Deep Learning
* Computer Vision
* Scientific Computing

Libraries built using NumPy:

* Pandas
* TensorFlow
* PyTorch
* SciPy

⸻

NumPy Basics

Creating Arrays

1D Array

a = np.array([1, 2, 3])

2D Array

b = np.array([[1,2,3],[4,5,6]])

⸻

Important Array Attributes

a.ndim
a.shape
a.dtype
a.size
a.itemsize

Notes

* ndim → number of dimensions
* shape → rows and columns
* dtype → data type of elements
* size → total number of elements

⸻

Accessing & Modifying Elements

Access Specific Element

a[1,2]

Access Rows

a[0,:]

Access Columns

a[:,1]

Modify Elements

a[1,1] = 20

Slicing

a[0,1:4]

Notes

* Slicing is extremely useful for data manipulation.
* NumPy slicing is faster and cleaner than loops.

⸻

Initializing Arrays

Zeros Array

np.zeros((2,3))

Ones Array

np.ones((3,3))

Full Array

np.full((2,2), 99)

Random Values

np.random.rand(4,2)

Random Integers

np.random.randint(1,10,size=(3,3))

Identity Matrix

np.identity(5)

⸻

Important Practice Problem

Created patterns using:

* zeros
* ones
* indexing
* slicing
* assignment

This section helped improve array manipulation skills.

⸻

Copying Arrays Carefully

Wrong Way

b = a

Both variables point to the same array.

Correct Way

b = a.copy()

Important Note

Always use .copy() if you want an independent array.

⸻

Basic Mathematics

NumPy supports element-wise operations.

a + 2
a - 2
a * 2
a / 2

Trigonometric Functions

np.sin(a)
np.cos(a)

Notes

NumPy makes mathematical operations very efficient without using loops.

⸻

Linear Algebra

Matrix Multiplication

np.matmul(a,b)

Determinant

np.linalg.det(a)

Notes

Linear algebra is heavily used in:

* Machine Learning
* AI
* Graphics
* Data Analysis

⸻

Statistics

Useful Functions

np.min(a)
np.max(a)
np.sum(a)

Notes

Statistical functions can also be applied row-wise and column-wise.

⸻

Reorganizing Arrays

Reshape Arrays

before.reshape((2,4))

Vertical Stack

np.vstack([v1,v2])

Horizontal Stack

np.hstack((h1,h2))

Notes

Reshaping is useful while preparing datasets for ML models.

⸻

Loading Data from Files

filedata = np.genfromtxt('data.txt', delimiter=',')

Notes

Useful for handling CSV and structured numerical datasets.

⸻

Advanced Indexing & Boolean Masking

Boolean Masking

a > 50

Filter Values

a[a > 50]

Notes

Boolean masking is one of the most powerful NumPy features for filtering data efficiently.

⸻

Key Learnings

* NumPy arrays are faster than Python lists
* Vectorized operations improve performance
* Slicing and indexing are essential skills
* Reshaping arrays is important in data preprocessing
* Boolean masking simplifies filtering operations
* NumPy is foundational for Data Science and Machine Learning

⸻

Resources

* NumPy Documentation: https://numpy.org/
* Python Documentation: https://docs.python.org/3/

⸻

Author

Created while learning and practicing NumPy fundamentals.
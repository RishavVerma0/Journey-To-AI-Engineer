## I am trying to implement cosine simailarity using numpy with a simple basic example

import numpy as np

def cos_sim(A, B):

    #Converting the lists to numpy arrays
    A = np.array(A, dtype=np.float32)
    B = np.array(B, dtype=np.float32)

    #Calculating the dot product of both A and B
    dot_prod = np.dot(A, B)

    #Now Calculating the magnitude of both A and B
    mag_A = np.linalg.norm(A)
    mag_B = np.linalg.norm(B)

    # Finally we are calculating the cosine similarity using the formula
    cosine_sim = dot_prod / (mag_A * mag_B)

    return cosine_sim

def main():
    A = [11 , 22 , 33]
    B = [66, 55, 44]

    print("Cosine similarity between A and B is : " , cos_sim(A, B))

main()
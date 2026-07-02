import numpy as np

def cos_sim(A, B):
    A = np.array(A, dtype=np.float32)
    B = np.array(B, dtype=np.float32)

    dot_prod = np.dot(A, B)
    mag_A = np.linalg.norm(A)
    mag_B = np.linalg.norm(B)

    if mag_A == 0 or mag_B == 0:
        return None

    return dot_prod / (mag_A * mag_B)


def identify_relationship(A, B):
    similarity = cos_sim(A, B)

    if similarity is None:
        print("Cosine similarity is undefined (one vector is a zero vector).")
        return

    print(f"Cosine Similarity : {similarity:.6f}")

    # Check if vectors are exactly equal
    if np.array_equal(A, B):
        relationship = "Identical vectors"

    elif similarity >= 0.99:
        relationship = "Highly similar (same direction)"

    elif similarity >= 0.70:
        relationship = "Moderately similar"

    elif np.isclose(similarity, 0.0, atol=1e-6):
        relationship = "Perpendicular"

    elif similarity <= -0.99:
        relationship = "Opposite direction"

    else:
        relationship = "Different directions"

    print(f"Relationship      : {relationship}")

def main():
    A = [12, 25, 37, 49, 58, 61]
    B = [11, 24, 36, 50, 57, 63]

    print("=" * 50)
    print("Cosine Similarity Analysis")
    print("=" * 50)

    print(f"Vector A : {A}")
    print(f"Vector B : {B}\n")

    identify_relationship(A, B)

    print("=" * 50)

main()
import numpy as np

a1 = np.array([1,2,3])
a2 = np.array([4,5,6])
a3 = np.array([7,8,9])
# Save the arrays:
np.savez_compressed('some_data.npz', 0=a1,1=a2,2=a3)
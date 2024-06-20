import numpy as np
import random
import matplotlib.pyplot as plt


# Degrees of freedom
df = 10

# Number of samples
num_samples = 10000

# Generate chi-square distributed random numbers
chi_square_samples = np.random.chisquare(df, num_samples)

# Plot histogram of chi-square samples
plt.hist(chi_square_samples, bins=50, density=True, color='skyblue', edgecolor='black')
plt.title('Chi-Square Distribution (df={})'.format(df))
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.show()
exit()
data = np.random.normal(loc=0, #mean 
                        scale=1, #std
                        size=10000)

results = []
for i in range(10000):
    # Pick 5 elements randomly from the array
    sample = random.sample(list(data), k=5)
    diff_arr = np.diff(sample)
    result  = np.square(diff_arr)
    results.append(sum(result))

plt.hist(results, bins=50, density=True, color='skyblue', edgecolor='black')
plt.show()
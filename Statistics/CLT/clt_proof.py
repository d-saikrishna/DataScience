import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import random
import matplotlib.pyplot as plt

# Set the mean (mu) for the Poisson distribution
mu = 3

# Generate data points from the Poisson distribution
#data = poisson.rvs(mu, size=1000)
# Uniform Distirbution
data = np.random.uniform(1, 100, 1000)

means = []
for i in range(10000):
    # Pick 5 elements randomly from the array
    sample = random.sample(list(data), k=5)
    mean = np.array(sample).mean()
    means.append(mean)

plt.hist(means, alpha=0.7, color='blue', edgecolor='black')

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Distirbution of Sample Means')

# Show plot
plt.show()
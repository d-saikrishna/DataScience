import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm
import random
import matplotlib.pyplot as plt
import os

# Generate data points from the Poisson distribution
# Set the mean (mu) for the Poisson distribution
#mu = 3
#data = poisson.rvs(mu, size=1000)

# Generate data points Uniform Distirbution
data = np.random.uniform(0, 1, 1000)

# Generate data points from Bernoulli distribution
# Define parameters for the Bernoulli distribution
#probability_of_success = 0.5  # Probability of success (e.g., getting a "1")
#size = 100000  # Number of data points

#data = np.random.binomial(n=1, p=probability_of_success, size=size)

means = []
for i in range(10000):
    # Pick 3 elements randomly from the array
    sample = random.sample(list(data), k=30)
    mean = np.array(sample).max()
    means.append(mean)

plt.hist(means, alpha=0.7, color='blue', edgecolor='black', density=True)

# Overlay normal curve
mu, std = np.mean(means), np.std(means)
x = np.linspace(mu - 3*std, mu + 3*std, 1000)
plt.plot(x, norm.pdf(x, mu, std), 'r-', lw=2)

# Add labels and title
plt.xlabel('Value || n=30 i=10000')
plt.ylabel('Frequency')
plt.title('Histogram of Distribution of Sample Max \n Population: Uniform Distribution')

# Show plot
#plt.show()
plt.savefig(os.getcwd() + '/Statistics/CLT/german_tank_cltfail.png')
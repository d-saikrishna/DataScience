import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm
import random
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Generate data points from the Poisson distribution
# Set the mean (mu) for the Poisson distribution
#mu = 3
#data = poisson.rvs(mu, size=1000)

# Generate data points Uniform Distirbution
class1 = np.random.uniform(500000, 2400000, 1000)
class10 = np.random.uniform(50000000, 60000000, 2)

# Generate random data from a normal distribution
# class10 = np.random.normal(loc=5000.5, #mean 
#                         scale=10, #std
#                         size=100)

# Generate random data from an exponential distribution
# Define the rate parameter (lambda) for the exponential distribution
# rate = 0.01  # Adjust this parameter as needed
# class10 = np.random.exponential(scale=1/rate, size=10000)

pop = np.concatenate((class1, class10))

#sns.histplot(pop, kde=True)
#plt.show()

means = []
for i in range(100000):
    # Pick 5 elements randomly from the array
    sample = random.sample(list(pop), k=50)
    mean = np.array(sample).mean()
    means.append(mean)

plt.hist(means, density=True)

# # Overlay normal curve
mu, std = np.mean(means), np.std(means)
x = np.linspace(mu - 3*std, mu + 3*std, len(list(pop)))
plt.plot(x, norm.pdf(x, mu, std), 'r-', lw=2)

# Add labels and title
plt.xlabel('Value || n=50 i=100000')
plt.ylabel('Frequency')
plt.title('Histogram of Distirbution of Sample Means')

# Show plot
plt.savefig(os.getcwd()+'/Statistics/CLT/taleb.png')

print('Mixed Dist: Mean - {} STD - {}'.format(np.mean(pop), np.std(pop)/np.sqrt(20)))
print('Sampling Dist: Mean - {} STD - {}'.format(np.mean(means), np.std(means)))
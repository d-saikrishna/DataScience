# Probability

Language to quantify uncertainty.


| Terms  | Definition |
| ------------- | ------------- |
| `Sample space`$\Omega$  | `Set` of possible outcomes of an experiment  |
| `Events` $\omega$  | Outcomes we are interested in. It is a subset of Sample space  |
| `Partition` of $\Omega$  | Sequence of disjoint sets A1, A2 ... such that $\cup_{i=1}^\infty A_i = \Omega $  |
| `Independent Events`  | When two events (outcomes) are independent of each other. P(AB) = P(A).P(B)  <br> Independence can be `assumed` or `derived`(above formula).|

## Frequentist vs Bayesian interpretation of Probability

**Frequentist interpretation**: P(A) : If you do an experiment 100000 times, what is the frequency (proportion) of event A. 

**Bayesian interpretation**: P(A): Degree of beleif that event A is true.

This difference is key in statistical inference.

## Conditional Probability

A and B are not indepenent events (Hence conditional probability)

$ P(A|B) = P(B|A). P(A) / P(B) = P(A \cap B)/P(B)$ 

**Bayes' Theorem**

Posterior opinion = Prior opinion * Likelihood of new evidence.

Posterior = P(A|B) <br>
Prior = P(A) <br>
Likelihood of new evidence = $\frac{P(B|A)}{\sum_j P(B|A_j).P(A_j)} $

$P(B) = \sum_j P(B|A_j).P(A_j) $ -- [Law of Total Probability](https://www.youtube.com/watch?v=U3_783xznQI) - better written as sum of all intersections between B and Ai

`Monty Hall problem` is a good example to understand this.

Where people get confused:
1. `Prosecutor's fallacy` P(A|B) != P(B|A). Also called `Confusion of the Inverse` I wrote a blog on it. [Why Doctor's need Bayes](https://d-saikrishna.github.io/Blogs/Anviksiki/bayes-doctor.html)



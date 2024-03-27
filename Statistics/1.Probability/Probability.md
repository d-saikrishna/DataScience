# Probability

Language to quantify uncertainty.


| Terms  | Definition |
| ------------- | ------------- |
| `Sample space`$\Omega$  | `Set` of possible outcomes of an experiment  |
| `Events` $\omega$  | Outcomes we are interested in. It is a subset of Sample space  |
| `Partition` of $\Omega$  | Sequence of disjoint sets A1, A2 ... such that $\cup_{i=1}^\infty A_i = \Omega $  |
| `Independent Events`  | When two events (outcomes) are independent of each other. P(AB) = P(A).P(B)  |

## Frequentist vs Bayesian interpretation of Probability

**Frequentist interpretation**: P(A) : If you do an experiment 100000 times, what is the frequency (proportion) of event A. 

**Bayesian interpretation**: P(A): Degree of beleif that event A is true.

This difference is key in statistical inference.

## Conditional Probability


**Bayes' Theorem**

Posterior opinion = Prior opinion * Likelihood of new evidence.

Posterior = P(A|B)
Prior = P(A)
Likelihood of new evidence = $\frac{P(B|A)}{\sum_j P(B|A_j).P(A_j)} $

Where people get confused:
1. `Prosecutor's fallacy` P(A|B) != P(B|A). Also called `Confusion of the Inverse` I wrote a blog on it. [Why Doctor's need Bayes](https://d-saikrishna.github.io/Blogs/Anviksiki/bayes-doctor.html)



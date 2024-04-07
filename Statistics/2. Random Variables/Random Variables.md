# Random Variables

Say you toss a fair coin ten times. The sample space $\Omega$ is [T,H]. You want to calculate number of heads - such measurable entities are called `Random Variables`

You might want to measure probability that there will be 5 heads $P(X=5)$. Generally we denote this as $P(X=x)$

Every value of `x` corresponds to some outcome/event sequence $\omega$. For instance, in the above problem $P(X=0)$ corresponds to $P(\omega=[TTTTTTTTT])$ = $1/2^{10}$

You can thus calculate $P(X)$ for each x. This is nothing but the `distribution function`

Cumulative Distribution Function (CDF) => $F_X = P(X<=x)$


X can be discrete or continuous.

1. If discrete, $P(X)$ can be calculated for each discrete values of x. This is also called PMF $f_X$.  $F_X = \Sigma f_x$. There are many types of discrete distributions -- Point Mass, Uniform, Bernoulli, Binomial, Geometric, Poisson.

2. If continous, $P(X) = 0$ for each discrete x. Here, it is called PDF $f(x)$. It is calculated through integrals - $P(a<X<b) = \int_a^b f(x)$. Uniform, Gaussian, Exponential, Gamma, Beta, Chi-Square, t and Cauchy.

Note: PDF can be >1 (not PMF)

$f = F^`x $

When there are 2 random variables $(X, Y)$:
1. Joint Mass functions (or) Joint densities
2. Joint CDF
3. Marginal Mass functions (or) Marginal densities

$X, Y$ can be called independent Random Variables if:
$P(X,Y) = P(X)*P(Y)$ i.e $f_{XY} = f_X*f_Y$

$f_{X|Y} = \frac{f_{XY}}{f_Y}$

When there are 2+ Random Variables X1, X2.....
X is called Random Vector!

IID - Independent and identically distributed (same marginal distribution with CDF F)
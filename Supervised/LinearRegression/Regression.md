
## BLUE
1. Best: Estimator has minimum variance (efficient). Also consistent
2. Linear: Assumption of linearity
3. Unbiased: Expected value of residual for a given X should be 0. 
[Source](https://www.youtube.com/watch?v=vOBtEiij-fA)

OLS estimator is BLUE under the assumptions (Gauss Markov assumptions):
1. Linearity
2. Random Sampling
3. Non-collinearity
4. Zero Conditional Mean of residuals: E(e|X)=0
5. Exogeneity / Homoscedascticity. 

## Why intercept is needed?
[Nice explainer!](https://medium.com/swlh/why-do-we-need-an-intercept-in-regression-models-76485a98d03c)


## Expected value of residual for given X should be 0

Otherwise, it is a biased model.

## Why heteroscedasticity is bad?

In OLS, we calculate the estimate by minimising RSS. When there is heteroscedasticity, points where there is more variance in residuals influence RSS more. 

*Standard Errors of the coefficients are biased in case of heteroscedasticity.* As a result, we can't correctly infer the significance of the coefficients. The confidence intervals of the the coefficients and prediction intervals are thus not accurate.

When there is heteroscedasticity:
1. Transformation of variables can help.
2. Calculate Robust Standard Errors. All statistical softwares have this provision. Robust standard errors assign larger weight when variation of the residual is more. This can be used even we don't know the form of heteroscedasticity.
2. Weighted least squares (WLS) regression can be done to down-weight those observations that produce large variation in residuals. But this can be used when we know the form of Heteroscedasticity.

[Source](https://www.statisticssolutions.com/free-resources/directory-of-statistical-analyses/homoscedasticity/) | 
[Medium blog](https://medium.com/keita-starts-data-science/heteroskedasticity-in-linear-regressions-and-python-16eb57eaa09)

# Reading material
1. [Adrian Olszewski on Logsitic Regression](https://medium.com/@r.clin.res/is-logistic-regression-a-regression-46dcce4945dd)
# t-Statistics

*!! First read the Confidence Interval section before continuing this !!*

So, to do an inference using just a sample, use use t-stat instead of a z-stat. But why?

Z-Stat assumes that the sampling distribution is in normal distribution. So, when you try to calcluate confidence interval using $\mu = \overline{x} \pm z^* * \sigma_s$ - all assumptions of normal distribution exist (95% of samples within in 2 $\sigma_s$ etc)

But say your survey got you a very very small sample $n$ = 5 from you which you have to infer population. How sure can you be that the standard deviation of this sample equal to that of population. $\sigma \approx S$ - Not equal to! So, we cannot be sure that with $S$, we have a normal distribution of the samples. There would be more than 5% of samples outside the 2*$S$ - Basically you would have a fat tail! (More chance of extreme values). Hence, to avoid underestimation of the confidence interval, we use the t-Statistic (considering a t-Distribution). 

$\mu = \overline{x} \pm t^* * \frac{S}{\sqrt{n}}$

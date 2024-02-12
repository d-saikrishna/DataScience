# Confidence Interval

Consider a population. You want to calculate the mean height of this population. To do that, you need data of heights of all. You cannot do that.

So, you do a survey and collect heights of 50 people (sample size $n$ = 50). **How confident are you that the mean height of this sample is the mean height of the population?**

Since you cannot be 100% confident, you give a confidence band of mean population.

$\mu = \overline{x} \pm z^* * \sigma_s$

$\mu$ -- mean of population <br>
$\overline{x}$ -- mean of sample <br>
$\sigma_s$ -- Standard deviation of sampling distribution <br>
$z^*$ --  It is called the **Critical Value** - basically how many standard deviations above or below do you want to be confident about.

You don't know the sampling distribution too! You only did one survey and have one sample. Not a distribution of it. How will you know $\sigma_s$ now?

Don't worry. $\sigma_s$ can be approximated as $\sigma/\sqrt{n}$. Where $\sigma$ is the standard deviation of the population.

YOU DON'T KNOW THE POPULATION! THAT'S WHY YOU DID THE SURVEY!

Don't worry again. It is considered $\sigma \approx S$ where $S$ is the standard deviation of the sample. But, since you are making so many approximations, you cannot use $z^*$ any more. So, you'll use -- $t^*$! -- t-Statistics

$\mu = \overline{x} \pm t^* * \frac{S}{\sqrt{n}}$

# Bootstrapping
You can do bootsrapping to calculate Confidence Interval. Check `Bootstrapping.ipynb`




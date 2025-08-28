library("rstanarm")

setwd('C:\\Users\\dskcy\\DataScience\\Statistics\\Regression\\ROS-Examples-master\\ElectionsEconomy')
hibbs <- read.table("data\\hibbs.dat", header=TRUE)

plot(hibbs$growth, hibbs$vote,
     xlab="Average recent growth in personal income", ylab="Incumbent party's vote share")
# Bayesian Inference
M1 <- stan_glm(vote ~ growth, data=hibbs)

# Classical Inference
M2 <- lm(vote ~ growth, data=hibbs)

abline(coef(M1), col='gray')
print(M1)

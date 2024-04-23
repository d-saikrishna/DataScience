from bayesian import BayesianNetwork
import sys

conditional_prob = False
observations = []
query = []
command = sys.argv
for i in command:

        if i == "given":
                conditional_prob = True
        query.append(i)
        if conditional_prob:
                observations.append(i)

bnet = BayesianNetwork()

if query:
	numerator = bnet.nextValues(bnet.getValue(query))
	if observations:
		denominator = bnet.nextValues(bnet.getValue(observations))
	else:
		denominator = 1
	print ("The probability is : %.10f" % (numerator/denominator))
else:
	print ("Invalid query string")
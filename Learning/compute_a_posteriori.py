import pandas as pd
import sys
def get_posteriors_bags(evidence, p_c, prior):
    '''
    evidence: New evidence string;
    p_c: Tuple containing probability of finding candy in each of the bag
    prior: Given priors
    '''

    file1 = open("result.txt", "w")
    file1.seek(0)
    l1 = "Observation of sequence Q: {}\n".format(evidence)
    l2 = "Length of Q: {}\n".format(len(evidence))
    file1.writelines([l1, l2, '\n'])

    if evidence == '':
        l = 'After observation {} = {}\n'.format(0, '')
        file1.writelines([l, '\n'])
        l1 = 'P(h1 | Q) = {}\n'.format(prior['h1'])
        l2 = 'P(h2 | Q) = {}\n'.format(prior['h2'])
        l3 = 'P(h3 | Q) = {}\n'.format(prior['h3'])
        l4 = 'P(h4 | Q) = {}\n'.format(prior['h4'])
        l5 = 'P(h5 | Q) = {}\n'.format(prior['h5'])
        file1.writelines([l1, l2, l3, l4, l5, '\n'])
        l1 = 'Probability that the next candy we pick will be C, given Q: {}\n'.format((prior * p_c).sum())
        l2 = 'Probability that the next candy we pick will be L, given Q: {}\n'.format(1 - (prior * p_c).sum())
        file1.writelines([l1, l2, '\n'])
        return prior

    for i in range(len(evidence)):
        likelihoods = p_c if evidence[i] == "C" else tuple(
            [1 - i for i in p_c])  # Since infinite bag; likelihood won't change with iterations
        unnorm = prior * likelihoods
        posterior = unnorm / unnorm.sum()

        l = 'After observation {} = {}\n'.format(i + 1, evidence[i])
        file1.writelines([l, '\n'])
        l1 = 'P(h1 | Q) = {}\n'.format(posterior['h1'])
        l2 = 'P(h2 | Q) = {}\n'.format(posterior['h2'])
        l3 = 'P(h3 | Q) = {}\n'.format(posterior['h3'])
        l4 = 'P(h4 | Q) = {}\n'.format(posterior['h4'])
        l5 = 'P(h5 | Q) = {}\n'.format(posterior['h5'])
        file1.writelines([l1, l2, l3, l4, l5, '\n'])
        l1 = 'Probability that the next candy we pick will be C, given Q: {}\n'.format((posterior * p_c).sum())
        l2 = 'Probability that the next candy we pick will be L, given Q: {}\n'.format(1 - (posterior * p_c).sum())
        file1.writelines([l1, l2, '\n'])
        prior = posterior

    file1.truncate()
    file1.close()
    return posterior

if __name__ == "__main__":
    p_c_1 = 1
    p_c_2 = 0.75
    p_c_3 = 0.5
    p_c_4 = 0.25
    p_c_5 = 0
    p_c = (p_c_1, p_c_2, p_c_3, p_c_4, p_c_5)

    hypotheses = 'h1', 'h2', 'h3', 'h4', 'h5'
    priors = 0.1, 0.2, 0.4, 0.2, 0.1
    prior = pd.Series(priors, hypotheses)

    evidence = sys.argv
    evidence = evidence[1]

    get_posteriors_bags(evidence,p_c,prior)
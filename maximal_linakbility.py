import numpy

def maximal_linakbility_metric(mated_scores, nonmated_scores, n_bin=30):
    """
    Parameters:
        (array) mated_scores:    mated scores
        (array) nonmated_scores: nonmated scores
        (int)   n_bin:         the number of histogram bins 

    Return:
        (float) linkability of templates in [0,1] interval. 
                higher value indicates higher link between templates.
    """
    
    # find histogram bin edges
    min_interval_scores = min(mated_scores.min(), nonmated_scores.min())
    max_interval_scores = max(mated_scores.max(), nonmated_scores.max())
    bin_edges = min_interval_scores + numpy.arange(n_bin+1)* (max_interval_scores - min_interval_scores)/n_bin

    # calculate histograms
    y1 = numpy.histogram(mated_scores, bins = bin_edges, density = True)[0]
    y2 = numpy.histogram(nonmated_scores, bins = bin_edges, density = True)[0]

    # calclulate maximal leakage
    MaxLeakage_score = 0 
    for i in range(n_bin):
        MaxLeakage_score += max(y1[i], y2[i])
        
    return numpy.log2( MaxLeakage_score * ( bin_edges[1]-bin_edges[0] ) )



if __name__ == '__main__':

    from argparse import ArgumentParser

    # Args
    parser = ArgumentParser()

    parser.add_argument(
        '--mated_scores',
        type=str,
        required=True,
        help='Path to mated scores (npy file).')
    parser.add_argument(
        '--nonmated_scores',
        type=str,
        required=True,
        help='Path to nonmated scores (npy file).')
    parser.add_argument(
        '--nbin',
        type=int,
        default=30,
        help='Number of histogram bins.')

    args = parser.parse_args()

    mated_scores = numpy.load(args.mated_scores)
    nonmated_scores = numpy.load(args.nonmated_scores)

    maximal_linakbility = maximal_linakbility_metric(mated_scores=mated_scores, nonmated_scores=nonmated_scores, n_bin=args.nbin)

    print('----------------------')
    print('Maximal linakbility is', maximal_linakbility)
    print('----------------------')
    print('According to Lemmma 3, upper bounds for True Match Rate (TMR) of the adversary\'s hypothesis testing for different values of False Match Rates (FMRs) are as follows:')
    for fmr in [1e-2,1e-3,1e-4]:
        print(f'- {min(round((2**maximal_linakbility-1+fmr) *100, 2),100)} % for the TMR of adversary\'s hypothesis testing at FMR={round(fmr*100,4)} %')

# Evaluating Linkability of Biometric Templates
If you want to evaluate the linkability of your biometric templates using the [Maximal Linkability](https://ieeexplore.ieee.org/abstract/document/10098649), you can use the provided function in [`maximal_linakbility.py`](maximal_linakbility.py) and as follows:

```python
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
```
**NOTE:** This code only requires `numpy` package to be installed.


You can also use the following command to evaluate the linkability of biometric templates:
```sh
python maximal_linakbility.py --mated_scores <path_to_mated_scores> --nonmated_scores <path_to_nonmated_scores>
```


# Reference
If you use this metric, please cite the following paper, which is published in the IEEE Transactions on Information Forensics and Security. The [PDF version of the paper](https://ieeexplore.ieee.org/abstract/document/10098649) is available as *open access* on the IEEE-Xplore. The complete source code for reproducing all experiments in the paper is also publicly available in the [official repository](https://gitlab.idiap.ch/bob/bob.paper.tifs2023_linkability_ml).

```Bibtex
@article{linkability_maxleakage,
  title={Measuring Linkability of Protected Biometric Templates using Maximal Leakage},
  author={Otroshi Shahreza, Hatef and Shkel, Yanina Y. and Marcel, S{\'e}bastien},
  journal={IEEE Transactions on Information Forensics and Security},
  year={2023},
  publisher={IEEE}
}
```
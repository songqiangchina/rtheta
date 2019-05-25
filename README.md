# rtheta
A python implementation of a sliding window quantile estimator
The program implements this [research paper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwjBi9TnmrbiAhVEq48KHUavBdkQFjAAegQIARAC&url=https%3A%2F%2Fraw.githubusercontent.com%2Ftdunning%2Ft-digest%2Fmaster%2Fdocs%2Ft-digest-paper%2Fhisto.pdf&usg=AOvVaw048xBndi9K3iTwhwSiSt35) by Dunning to estimate the quantile values for each window as the window slides over the 1-D data, ,which has been randomly initialized.
The results for each window are displayed at the end with the coressponding index

Optimisation over standard tdigest is obtained as in the standard implementation, the original data points are lost when clustering and a tdigest has to be created again for each window, so to avoid this overhead, my implementation keeps track of data point indices and instead of creating a new digest each time, just pops the redundant points and keeps on merging new ones as the window slides over the data.

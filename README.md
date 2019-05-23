# rtheta
A sliding window quantile estimator
The program uses [tdigest](https://github.com/CamDavidsonPilon/tdigest) to estimate the quantile values for each window as the window slides over the 1-D data, ,which has been randomly initialized.
The results for each window are displayed at the end with the coressponding index
___
*Required* tdigest

````pip install tdigest````

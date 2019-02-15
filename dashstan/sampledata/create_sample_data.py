import pickle
import os
from pystan import StanModel

DATA_FILE_NAME = 'sampledata.pkl'

def main():
    schools_dat = {'J': 8,
                   'y': [28, 8, -3, 7, -1, 1, 18, 12],
                   'sigma': [15, 10, 16, 11, 9, 11, 10, 18]}
    sm = StanModel(file='model.stan')
    fit = sm.sampling(data=schools_dat, iter=1000, chains=4, seed=555)
    with open(DATA_FILE_NAME, 'wb') as f:
        pickle.dump({'model': sm, 'fit': fit}, f)

if __name__=='__main__':
    main()


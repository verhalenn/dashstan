#      DashStan a dashboard to analyse and diagnose Markov chain Monte Carlo simulations.
#      Copyright (C) 2019.  Nicholas Ver Halen
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>

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


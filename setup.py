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

from setuptools import setup, find_packages

setup(
    name='dashstan',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/verhalenn/dashstan',
    license='GPLv3',
    author='Nicholas Ver Halen',
    author_email='verhalenn@gmail.com',
    description='Dashboard for Stan MCMC simulations.',
    install_requires=[
        "dash>=0.39.0",
        "dash_core_components>=0.44.0",
        "dash_html_components>=0.14.0",
        "dash_table>=3.6.0",
        "pystan>=2.18.1.0",
        "pandas>=0.24.1",
        "plotly>=3.5.0",
    ]
)

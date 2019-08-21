# Source: https://plot.ly/ipython-notebooks/markowitz-portfolio-optimization/
# Source 2: http://ahmedas91.github.io/blog/2016/03/01/efficient-frontier-with-python/

#import required libraries
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import cufflinks as cf
import cvxopt as opt
from cvxopt import blas, solvers
import matplotlib.pyplot as plt
import io
import sys
import math

#Function to get evctor $x$ of random portfolio weighs that sums to 1:
def random_wieghts(n):
    a = np.random.rand(n)
    return a/a.sum()


def returns(dataframe):
	(dataframe - dataframe.shift(1))/dataframe.shift(1)


data = pd.read_csv("portfolio/wealthfront_funds_cut.csv")

data.Date = pd.to_datetime(data.Date, format = "%Y-%m-%d")


# Columns names of all stock tickers
columns = data.columns[1:]

# Monthly returns of all stocks
monthly_returns = (data[columns] - data[columns].shift(1) ) / data[columns].shift(1)
monthly_returns = monthly_returns[["VTI", "VTMGX","VEMAX","MUB","VIG","VDE"]]

# Add Date to monthly returns and remove first row (which will be NaN for all returns becuase there is no return for the first month)
monthly_returns.insert(0, "Date", data.Date)

monthly_returns.set_index("Date", inplace = True)


# print(monthly_returns.index)

monthly_returns = monthly_returns.drop(monthly_returns.index[0])


cov = np.matrix(monthly_returns.cov())
expected_returns = np.matrix(monthly_returns.mean())

print(monthly_returns.columns)
print((expected_returns).round(4) * 12)

print(np.sqrt(np.diag(cov)) * math.sqrt(12))

def initial_portfolio(monthly_returns):
    wieghs = np.matrix(random_wieghts(expected_returns.shape[1]))
    
    mu = wieghs.dot(expected_returns.T)
    sigma = np.sqrt(wieghs * cov.dot(wieghs.T))
    
    return mu[0,0],sigma[0,0]

#print(np.matrix(monthly_returns.cov()))

n_portfolios = 10000
means, stds = np.column_stack([
    initial_portfolio(monthly_returns) 
    for _ in range(n_portfolios)
])



def optimal_portfolio(returns):
    n = len(returns)
    returns = np.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))
    
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    opt.solvers.options['show_progress'] = False
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] 
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]

    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
   
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)
    
    return np.asarray(wt), returns, risks



w_f, mu_f, sigma_f = optimal_portfolio(monthly_returns.T)


mu_f_year = [i * 12 for i in mu_f]
sigma_f_year = [i * 12 for i in sigma_f]

plt.plot(stds*12, means*12, 'o', markersize = 1, color='black')
plt.plot(sigma_f_year, mu_f_year, 'x', markersize=5, color='red')

plt.xlabel('std')
plt.ylabel('mean')

plt.show()



# data.set_index("Date", inplace = True)

# data.plot(legend = True)

# plt.show()


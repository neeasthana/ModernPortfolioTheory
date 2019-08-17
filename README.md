# ModernPortfolioTheory
Tool to analyze a portfolio of stocks using modern portfolio theory to understand risks and returns. The theory states that holding a single asset is very risk but creating a portfolio of uncorrelated, disversified assets will generate more consistent returns and less volatility (stock prices jumping up and down) and therefore create long term wealth. 

## Procedure

1. I will indentify a list of uncorrelated and diversified assets. The assets will be diversified by company size, industry, country, volatility, expected return, etc. Assets will consist of stocks, bonds, and alternatives (REITs). 
1. Monthly stock prices will then be retreived from online for as far back as the data is available (ideally more than 15 years). I have currently been downloading the data from Yahoo Fianance (TODO)
1. For each stock, calculate expected monthly return 
1. From the stock return data, calculate expected yearly return and risk (standard deviation of returns)
1. Create different portfolios of the identified assets and calculate each portfolios expected yearly return and volatility (standard deviation).
1. Create the efficient frontier for the portfolio identified using modern portfolio theory. (TODO MATH). The efficient frontier will provide an allocation that will have the maximum possible return for a level of risk in the set of assets. One of the portfolios in the efficient frontier can then be selected as a portfolio for returns. 

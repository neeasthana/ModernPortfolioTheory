class Stock(Asset):
	def __init__(self, ticker):
		self.name = ticker
		self.ticker = ticker

	def returns_from_yahoo(self):
		# use self.ticker
		pass

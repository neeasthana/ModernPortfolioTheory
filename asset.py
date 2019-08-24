class Asset:
	def __init__(self, name):
		self.name = name
		self.quotes = []
		self._calculate_returns()
	
	def _calculate_returns(self):
		pass

	def average_return(self):
		return sum(self.returns)/len(returns)

	def average_risk(self):
		return Math.std(self.returns)

	def returns_from_csv(self, csv_file):
                pass

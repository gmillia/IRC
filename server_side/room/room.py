class Room():
	def __init__(self, name="random", owner="boss"):
		self._name = name
		self._owner = owner
		self._users = []
		self._usernames = []
		self._messages = []
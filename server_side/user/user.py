class User():
	def __init__(self, username="random", password="secure"):
		self._username = username
		self._password = password
		self._rooms = []
		self._room_names = []
		self._inbox = []

	
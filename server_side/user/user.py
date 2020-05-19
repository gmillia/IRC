class User():
	def __init__(self, username="random", password="secure"):
		self._username = username
		self._password = password
		self._last_room = None
		self._rooms = []
		self._room_names = []
		self._inbox = []

	
import socket

class _Option():
	def __init__(self, msg, func_pointer):
		self.msg = msg
		self.func_pointer = func_pointer

class Client():
	def __init__(self):
		self._client_socket = None
		self._host = '127.0.0.1'
		self._port = 4444
		self._current_user = None
		self._connected = False

	##############################################################################################
	#MENU STUFF########################################################################MENU STUFF#
	##############################################################################################

	def menu(self):
		options = [
			_Option("Connect to a server.", self.attempt_connect_to_server),
			_Option("Disconnect from a server.", self.disconnect_from_server),
			_Option("Create new user.", self.new_user_menu),
			_Option("Login to existing account.", self.login_menu),
			_Option("Create new room.", self.new_room_menu),
			_Option("List all rooms.", self.list_all_rooms_menu),
			_Option("Join new room.", self.join_new_room_menu),
			_Option("Leave room.", self.leave_room),
			_Option("Exit.", lambda: "Exit")
		]

		self._menu("Welcome.", options)

	def _menu(self, title, options):
		if len(options) == 0:
			return

		should_exit = False
		while not should_exit:
			if self._connected == False:
				msg = " ".join([str(title), "Please connect to a server first:"])
			elif self._current_user == None: 
				msg = " ".join([str(title), "Please login or create user first:"])
			else:
				msg = " ".join([str(title), self._current_user + " choose what you'd like to do:"])

			print()
			print(msg)
			print()
			print()
			for i in range(len(options)):
				print(str(i) + ": " + options[i].msg)
			print()

			option = None
			try:
				option = self._get_menu_option(0, len(options)-1)
			except EOFError:
				option = 0

			if options[option].func_pointer() == "Exit":
				self.disconnect_from_server()
				should_exit = True

	def _get_menu_option(self, min_value, max_value, cli_symbol="> "):
		should_continue = True
		while should_continue:
			try:
				option = input(cli_symbol)
				option = int(option)

				if option < min_value or option > max_value:
					print("{" + str(option) + "} is not within range [" + str(min_value) + ", " + str(max_value) + "]; try again.")
				else:
					should_continue = False

			except ValueError:
				print("Please enter an integer.")

		return option

	##############################################################################################
	#SERVER INTERACTION########################################################SERVER INTERACTION#
	##############################################################################################

	def attempt_connect_to_server(self):
		if(self._client_socket != None):
			try:
				response = self.send_request_to_server(666)
				if not response:
					self.connect_to_server()
				else:
					print("Already established connection.")
					return 
			except:
				self.connect_to_server()
		else:
			self.connect_to_server()

	def connect_to_server(self):
		self._client_socket = socket.socket()
		print("Connecting")
		try:
			self._client_socket.connect((self._host, self._port))
		except socket.error as e:
			#print(str(e))
			print("Couldn't connect to a server: start the server first!")
			return

		self._connected = True
		data = self._client_socket.recv(2048)
		response = data.decode('utf-8')
		print(response)

	def disconnect_from_server(self):
		if self._client_socket != None: 
			self._client_socket.close()
			self._client_socket = None
			self._connected = False
			self._current_user = None
			print("Disconnected from the server.")

	##############################################################################################
	#MENU HELPERS####################################################################MENU HELPERS#
	##############################################################################################

	def new_user_menu(self):
		if self._connected == False:
			print("Please connect to a server first!")
			return

		username = input("Enter new user username: ")
		password = input("Enter new user password: ")

		response = self.send_request_to_server(1, [username, password])

		if response == None: return
		else: response = int(response)

		if response == 1:
			print("Successfuly created new user " + username)
			self._current_user = username
		elif response == 0:
			print("User " + username + " already exists!")

	'''
	def list_all_users_menu(self):
		response = self.send_request_to_server(2)
		if response != None:
			if len(response) == 0:
				print("Server doesn't have any users, add users first!")
			else:
				print("#", "Username")
				for i in range(len(response)):
					print(i + 1, response(i))

	def remove_user_menu(self):
		username = input("Enter username of the user to remove: ")

		response = self.send_request_to_server(3, username)

		if response == None: return
		else: response = int(response)

		if response == 1:
			print("Successfuly removed user " + username + " from the server.")
		elif response == 0:
			print("User " + username + " doesn't exist!")
		elif response == 2:
			print("Error removing " + username + ". Try again.")
	'''

	def login_menu(self):
		if self._connected == False:
			print("Please connect to a server first!")
			return

		username = input("Enter user username: ")
		password = input("Enter user password: ")

		response = self.send_request_to_server(2, [username, password])

		if response == None: return
		else: response = int(response)

		if response == 1:
			print("Successfuly logged in to " + username)
			self._current_user = username
		elif response == 0:
			print("Username or password is invalid!")

	def new_room_menu(self):
		if self._connected == False:
			print("Please connect to a server first!")
			return

		if self._current_user == None:
			print("Please create user or login first!")
			return 

		room_name = input("Enter new room name: ")

		response = self.send_request_to_server(3, [room_name, self._current_user])

		if response == None: return
		else: response = int(response)

		if response == 1:
			print("Successfuly created new room " + room_name)
		elif response == 0:
			print("Room " + room_name + " already exists!")

	def list_all_rooms_menu(self):
		if self._connected == False:
			print("Please connect to a server first!")
			return

		if self._current_user == None:
			print("Please create user or login first!")
			return 

		response = self.send_request_to_server(4)
		if response != None:
			if len(response) == 0:
				print("Server doesn't have any rooms, add rooms first!")
			else:
				print("#", "Room name")
				for i in range(len(response)):
					print(i + 1, response[i])

	def join_new_room_menu(self):
		if self._connected == False:
			print("Please connect to a server first!")
			return

		if self._current_user == None:
			print("Please create user or login first!")
			return 

		room_name = input("Please enter name of the room to join: ")
		response = self.send_request_to_server(5, [room_name, self._current_user])

		if response == None: return
		else: response = int(response)

		if response == 0:
			print("Room " + room_name + " doesn't exist. Create first!")
		elif response == 1:
			print("You already participate in the room " + room_name + "!")
		elif response == 2:
			print("Successfuly created new room " + room_name)

	def leave_room(self):
		if self._connected == False:
			print("Please connect to a server first!")
			return

		if self._current_user == None:
			print("Please create user or login first!")
			return 

		room_name = input("Please enter name of the room to leave: ")
		response = self.send_request_to_server(6, [room_name, self._current_user])

		if response == None: return
		else: response = int(response)

		if response == 0:
			print("Room " + room_name + " doesn't exist. Create first!")
		elif response == 1:
			print("You can't leave room that you haven't joined. Join first!")
		elif response == 2:
			print("Successfuly left " + room_name)

	##############################################################################################
	#MULTI USE FUNCTIONS######################################################MULTI USE FUNCTIONS#
	##############################################################################################
	def send_request_to_server(self, request_code, request_body=None):
		"""
		Response is sent in the form of the list
		"""
		if self._client_socket == None:
			print("Unable to communicate with the server: Connect to the server first!")
			return None

		request = str([request_code, request_body])
		try:
			self._client_socket.sendall(request.encode())
		except socket.timeout:
			print("Server closed connection.")
			self.disconnect_from_server()
		except:
			print("Couldn't send request. Closing connection.")
			self.disconnect_from_server()

		data = self._client_socket.recv(2048)
		if (not data) or data == b'':
			print("Didn't receive response from the server: disconnecting.")
			self.disconnect_from_server()
			return

		response = eval(data.decode('utf-8'))
		return response
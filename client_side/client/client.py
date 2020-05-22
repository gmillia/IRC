import socket
import datetime

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
		self._current_room = None
		self._connected = False

	##############################################################################################
	#MENU STUFF########################################################################MENU STUFF#
	##############################################################################################

	def menu(self):
		options = [
			_Option("Connect to a server.", self.attempt_connect_to_server),
			_Option("Disconnect from a server.", self.disconnect_from_server),
			_Option("Create new user.", self.create_new_user),
			_Option("Login to existing account.", self.login),
			_Option("Logout", self.logout),
			_Option("Create new room.", self.create_new_room),
			_Option("List all rooms.", self.list_all_rooms),
			_Option("Join new room.", self.join_new_room),
			_Option("Leave room.", self.leave_room),
			_Option("Switch room", self.switch_room),
			_Option("Send message to room: ", self.send_room_message),
			_Option("View room messages.", self.view_room_messages),
			_Option("View room members", self.view_room_members),
			_Option("Send personal message", self.send_personal_message),
			_Option("View personal inbox", self.view_personal_inbox),
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
				msg = " ".join([str(title), "[User: " + self._current_user + " | Room: " + str(self._current_room) + "] choose what you'd like to do:"])

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
		"""
		Helper function that helps connect to a server
		"""

		#If connection was valid
		if(self._client_socket != None):
			#Check if connection still exists by sending quick request
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
		"""
		Function that actually connects to a server
		"""

		self._client_socket = socket.socket()
		print("Connecting")
		try:
			self._client_socket.connect((self._host, self._port))
		except socket.error as e:
			#print(str(e))
			print("Couldn't connect to a server: start the server first!")
			return

		#Connected
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
			self._current_room = None
			print("Disconnected from the server.")

	##############################################################################################
	#MENU HELPERS####################################################################MENU HELPERS#
	##############################################################################################

	def create_new_user(self):
		"""
		Function that creates a new user in the system.
		Server response is an array that consists of one item: 
			[0] - user already exists
			[1] - successful user creation on the systemser
		"""

		#Check that client is connected
		if self._connected == False:
			print("Please connect to a server first!")
			return

		if self._current_user != None:
			print("Please logout first.")
			return

		#Prompt user for input
		username = input("Enter new user username: ")
		password = input("Enter new user password: ")

		#Validate input
		if username == None or password == None or len(username) == 0 or len(password) == 0:
			print("Invalid input, please try again!")
			return

		#Send request to the server to create new user on the system
		response = self.send_request_to_server(1, [username, password])

		#Validate not errored response on request
		if response == None: return
		
		#Transform first item from response to integer
		response = int(response[0])

		#Check for error from server
		if response == 0:
			print("User " + username + " already exists!")
			return

		#All checks passed: user created on the system: can update local info
		print("Successfully created new user " + username)
		self._current_user = username

	def login(self):
		"""
		Function that logs user in (matches user with user on the system)
		Server response is a list:
			[0] - username doesn't exist on the system OR password doesn't match user
			[String] - successful login: return name of the last room used by user (can be None)
		"""

		#Check if connected to a server first
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check if not already logged in
		if self._current_user != None:
			print("Already logged in, logout first!")
			return

		#Prompt user to input login info
		username = input("Enter user username: ")
		password = input("Enter user password: ")

		#Validate user input
		if username == None or password == None or len(username) == 0 or len(password) == 0:
			print("Invalid input, please try again!")
			return

		#Send request to server to log user in
		response = self.send_request_to_server(2, [username, password])

		#Validate not errored response on request
		if response == None: return

		#Check errors on login
		if type(response[0]) == int and int(response[0]) == 0:
			print("Username or password is invalid!")
			return

		#All checks have passed: user logged in: can update local info
		print("Successfully logged in to " + username)
		self._current_user = username
		self._current_room = response[0]

	def logout(self):
		"""
		Function that doesn't communicate with server:
		Checks for connection and current user existence, and clears local info, thus "logging out"
		"""
		#Check if not connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check if logged in
		if self._current_user == None:
			print("Login first!")
			return

		#All checks passed: can log user out: clear local info
		self._current_user = None
		self._current_room = None

		print("Successfully logged out.")

	def create_new_room(self):
		"""
		Function that creates new room on the system
		Serer responds with a list consisting of just 1 item:
			[0] - room already exists on the system
			[1] - successful room creation
		"""

		#Check if connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check if logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Prompt user to input name of the room to create
		room_name = input("Enter new room name: ")

		#Validate user input
		if room_name == None or len(room_name) == 0:
			print("Invalid input, please try again!")
			return

		#Send request to server to create new room
		response = self.send_request_to_server(3, [room_name, self._current_user])

		#Check errored request
		if response == None: return
		
		#Transform first item on the response list to an integer
		response = int(response[0])

		#Check server error
		if response == 0:
			print("Room " + room_name + " already exists!")
			return

		#All checks passed: new room created on the system: can update local info
		print("Successfully created new room " + room_name)
		self._current_room = room_name

	def list_all_rooms(self):
		"""
		Function that lists all rooms on the system
		Server responds with a list consisting either of 1 or 2 items:
		When server returns a list with just 1 item, it means there was an error on the server side with the request 
		When server returns a list with 2 items, it means successful request:
			[0] - user doesn't exist on the system
			[last_room, room_names] - last_room = room last used by the user, room_names = list of rooms that exist on the system
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that client is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Send a request to a server to fetch all room names
		response = self.send_request_to_server(4, [self._current_user, self._current_room])

		#Check for errored request
		if response == None: return

		#Check if server returned list with 1 item: signifies some error
		if len(response) == 1:
			print("Login or create user first!")
			return

		#All checks passed: update current room
		self._current_room = response[0]

		#Check if system doesn't have any rooms
		if len(response[1]) == 0:
			print("No rooms: create first!")
			return

		#Print all rooms
		print("#", "Room name")
		for i in range(len(response[1])):
			print(i + 1, response[1][i])

	def join_new_room(self):
		"""
		Function that lets user join new room and automatically switches user current room to this newly joined room
		Server responds with a list consisting of 1 item:
			[0] - room_name (room) doesn't exist on the system
			[1] - user is already a participant of the room he wants to join
			[2] - user successfully joined room
		"""

		#Check if client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check of client is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Prompt user to enter name of the new room they want to join
		room_name = input("Please enter name of the room to join: ")

		#Validate used input
		if room_name == None or len(room_name) == 0:
			print("Invalid input, please try again!")
			return 

		#Send request to server to join new room
		response = self.send_request_to_server(5, [room_name, self._current_user])

		#Check errored request
		if response == None: return

		#Transform first item on server response to an integer
		response = int(response[0])

		#Check for server errors
		if response == 0:
			print("Room " + room_name + " doesn't exist. Create first!")
			return
		if response == 1:
			print("You already participate in the room " + room_name + "!")
			self._current_room = room_name
			return

		#All checks passed: user joined new room: can update local info
		print("Successfully joined new room " + room_name)
		self._current_room = room_name

	def leave_room(self):
		"""
		Function that lets user leave current room
		Server response consists of a list with 1 item:
			[0] - room with room_name doesn't exist on the system
			[1] - user with username doesn't exist on the system
			[2] - room doesn't have user with username as a participant 
			[3] - user doesn't have room with room_name in rooms that he participates in
			[4] - user succesfully left room
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that client is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Check that client is in the room currently (room to be left)
		if self._current_room == None:
			print("Please join or create room first.")
			return

		#Send a request to a server for user to leave current room
		response = self.send_request_to_server(6, [self._current_room, self._current_user])

		#Check errored request
		if response == None: return

		#Transform first item from server response to an integer
		response = int(response[0])

		#Check for sever errors
		if response == 0:
			print("Room " + self._current_room + " doesn't exist. Create first!")
			return

		if response == 1:
			print("User " + self._current_user + " doesn't exist. Create first!")

		if response == 2 or response == 3:
			print("You can't leave room that you haven't joined. Join first!")
			return

		#All checks passed: user Successfully left room: can update local info
		print("Successfully left " + self._current_room)
		self._current_room = None

	def switch_room(self):
		"""
		Function that lets user switch to a new room that he is a participant of
		Server response is a list that consists of one item:
			[0] - user with given username doesn't exist on the system
			[1] - room with given room_name doesn't exist on the system
			[2] - user with a givn username doesn't exist in room users records
			[3] - room with a given room_name doesn't exist in user rooms records
			[4] - successfuly switched room
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that client is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Check that client is a participant of a room
		if self._current_room == None:
			print("Please join or create room first.")
			return

		#Prompt user to input name of the room they want to switch to
		new_room = input("Please enter room to go to: ")

		#Validate user input
		if new_room == None or len(new_room) == 0:
			print("Invalid input, please try again!")
			return

		#Send request to a server to switch current room
		response = self.send_request_to_server(7, [self._current_user, new_room])

		#Check for errored request
		if response == None: return

		#Transform first item on response to be an integer
		response = int(response[0])

		#Check for server errors
		if response == 0:
			print(self._current_user + " doesn't exist. Please create user first!")
			return

		if response == 1:
			print("Room " + new_room + " doesn't exist - create first!")
			return

		if response == 2 or response == 3:
			print(self._current_user + " doesn't participate in " + self._current_room + ". Please join first!")
			return

		#All checks passed: room Successfully switched: can update local info
		print("Successfully switched room to " + new_room)
		self._current_room = new_room

	def send_room_message(self):
		"""
		Function that lets user send message to a room he is currently in
		Server response is a list that consists of one item:
			[0] - room with a given room_name doesn't exist on the system
			[1] - user with a given username doesn't exist on the system
			[2] - user with a given username doesn't exist in room users records
			[3] - room with a given room_name doesn't exist in user rooms records
			[4] - message successfuly sent
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that client is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Check that user is in a room
		if self._current_room == None:
			print("Please join or create room first.")
			return

		#Prompt user to input a message to be sent to a room
		message = input("Please enter message: ")

		#Validate user input
		if message == None or len(message) == 0:
			print("Invalid input, please try again!")
			return 

		#Send request to server to send a message to a room
		response = self.send_request_to_server(8, [self._current_user, self._current_room, message])

		#Check errored request
		if response == None: return
		
		#Transform first item on the server response list to be an integer
		response = int(response[0])

		#Check for server errors
		if response == 0:
			print("Can't send a message: " + self._current_room + " doesn't exist. Create or join first.")
			return

		if response == 1:
			print("Can't send a message: " + self._current_user + " doesn't exist. Please create user first!")
			return

		if response == 2 or response == 3:
			print(self._current_user + " doesn't participate in " + self._current_room + ". Please join first!")
			return

		#All checks passed: display message
		print("Succesfully sent message.")

	def view_room_messages(self):
		"""
		Function that gets all the messaged from current user room and displays them to a user
		Server response is a list that consists of 1 item:
			[0] - room with a given room_name doesn't exist on the system
			[1] - user with a given username doesn't exist on the system
			[2] - user with a given username doesn't exist in room users records
			[3] - room with a given room_name doesn't exist in user rooms records
			[room_messages] - list of room messages
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that user is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 
		
		#Check that user is a room participant
		if self._current_room == None:
			print("Please join or create room first.")
			return

		#Send request to server to fetch all messaged from current room
		response = self.send_request_to_server(9, [self._current_user, self._current_room])

		#Check errored request
		if response == None: return

		#Check server errors: On successful message fetch server can send empty list (no messages in the room): check for that
		if len(response) > 0:
			if type(response[0]) == str and int(response[0]) == 0:
				print("Can't view messages: " + self._current_room + " doesn't exist. Create or join first.")
				return

			if type(response[0]) == str and int(response[0]) == 1:
				print("Can't view messages: " + self._current_user + " doesn't exist. Create or login first.")

			if type(response[0]) == str and (int(response[0]) == 2 or int(response[0]) == 3):
				print("Can't send message: join the room first.")
				return

		#All checks passed: check if room doesn't have any messages
		if len(response) == 0:
			print("No messages in the room. Send first.")
			return
	
		#Print all messaged from a room
		print("**************************************************************")
		for i in range(len(response)):
			print(response[i]["At"], " | ", response[i]["From"], " | ", response[i]["Message"])

		print("**************************************************************")

	def view_room_members(self):
		"""
		Function that fetches all room users and displays it to the current user
		Calls a server and gets a response in form of a list:
			[0] - room with a given room_name doesn't exist on the system
			[1] - user with a given username doesn't exist on the system
			[2] - user with a given username doesn't exist in room users records
			[3] - room with a given room_name doesn't exist in user rooms records
			[room_members] - list of room members
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that user is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 
		
		#Check that user is a room participant
		if self._current_room == None:
			print("Please join or create room first.")
			return

		#Send request to server to fetch all messaged from current room
		response = self.send_request_to_server(10, [self._current_user, self._current_room])

		#Check errored request
		if response == None: return

		#When trying to convert to int, it will fail when response returned list with users (e.g.: can't convert John to int), and except will catch it (meaning valid response)
		try:
			#Check server errors
			if len(response) > 0:
				if int(response[0]) == 0:
					print("Can't view messages: " + self._current_room + " doesn't exist. Create or join first.")
					return

				if int(response[0]) == 1:
					print("Can't view messages: " + self._current_user + " doesn't exist. Create or login first.")

				if int(response[0]) == 2 or int(response[0]) == 3:
					print("Can't send message: join the room first.")
					return
			else:
				raise 
		except:
			#Print all members of a room
			print("**************************************************************")
			print("#", "Username")
			for i in range(len(response)):
				print(i + 1, response[i])

			print("**************************************************************")

	def send_personal_message(self):
		"""
		Function that lets user send personal message to another user
		Calls server-side function that sends back response in form of a list:
			[0] - user with given username doesn't exist on the system
			[1] - user with recipient username doesn't exist on the system
			[2] - successful message sent
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that user is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Prompt user input for recipient name
		recipient = input("Please enter username of the user you want to send message to: ")

		#Validate input
		if recipient == None or len(recipient) == 0:
			print("Invalid input, please try again.")

		#Prompt user to input personal message they want to send
		message = input("Please enter message you'd like to send to " + recipient + " : ")

		#Validate user input for message
		if message == None or len(message) == 0:
			print("Invalid input, please try again.")

		#Attempt sending message
		response = self.send_request_to_server(11, [self._current_user, recipient, message])

		if response == None: return
		response = int(response[0])

		#Check server errors
		if response == 0:
			print(self._current_user + " doesn't exist. Please create first.")
			return 
		if response == 1:
			print(recipient + " doesn't exist. Please try again.")
			return

		#All checks passed, message was sent
		print("Message to " + recipient + " was successfuly sent.")

	def view_personal_inbox(self):
		"""
		Function that fetches inbox for current user and displays it
		Calls a server function, which returns a list:
			[0] - user with given username doesn't exist on the system
			[inbox] - list of users personal messages
		"""

		#Check that client is connected to a server
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Check that user is logged in
		if self._current_user == None:
			print("Please create user or login first!")
			return 

		#Get server response
		response = self.send_request_to_server(12, [self._current_user])

		if response == None: return

		try:
			if len(response) > 0:
				if int(response) == 0:
					print("Can't view inbox: " + self._current_user + " doesn't exist on the system.")
					return
			else:
				raise
		except:
			if len(response) == 0:
				print("Inbox is empty!")
				return
			else:
				#Print all messaged from a room
				print("**************************************************************")
				for i in range(len(response)):
					print(response[i]["At"], " | ", response[i]["From"], " | ", response[i]["Message"])

				print("**************************************************************")

	##############################################################################################
	#MULTI USE FUNCTIONS######################################################MULTI USE FUNCTIONS#
	##############################################################################################
	def send_request_to_server(self, request_code, request_body=None):
		"""
		Function that actually communicates with a server and sends response back to the user
		Response is sent in the form of the list
		"""

		#Check that connection exists
		if self._client_socket == None:
			print("Unable to communicate with the server: Connect to the server first!")
			return 

		#Check for established connection
		if self._connected == False:
			print("Please connect to a server first!")
			return

		#Create request list and transform it into list
		request = str([request_code, request_body])

		#Attempt server request
		try:
			self._client_socket.sendall(request.encode())
		except socket.timeout:
			print("Server closed connection.")
			self.disconnect_from_server()
		except:
			print("Couldn't send request. Closing connection.")
			self.disconnect_from_server()

		#Receive server response
		data = self._client_socket.recv(2048)

		#Check for valid server response
		if (not data) or data == b'':
			print("Didn't receive response from the server: disconnecting.")
			self.disconnect_from_server()
			return

		#All checks passed: decode server response and transform into a list, then send back the list
		response = eval(data.decode('utf-8'))
		return response

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
			_Option("Login to an existing account.", self.login),
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
			_Option("Send message to all rooms", self.send_all_room_message),
			_Option("Send message to selected rooms", self.send_message_to_selected_rooms),
			_Option("Join selected rooms", self.join_selected_rooms),
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

			print("---------------------------------------------")
			print(msg)
			print("---------------------------------------------")
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
				self.disconnect_from_server(exit=True)
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

	def disconnect_from_server(self, exit=False):
		if self._connected == True or self._client_socket != None or exit == True: 
			if self._client_socket != None:
				self._client_socket.close()
			self._client_socket = None
			self._connected = False
			self._current_user = None
			self._current_room = None
			print("Disconnected from the server.")
		else:
			print("ERROR: connect to the server first.")

	##############################################################################################
	#MENU HELPERS####################################################################MENU HELPERS#
	##############################################################################################

	def create_new_user(self):
		"""
		Function that creates a new user in the system.
		Server response is an array that consists of one item: 
			[OK] - successful user creation on the systemser
		"""

		#Perform before check
		if self.before_check(connected=True, logged_out=True) != True: 
			return

		#Prompt user for input
		username = input("Enter new user username: ")
		#Validate user input
		if self.validate_user_input(username) != True:
			return

		password = input("Enter new user password: ")
		if self.validate_user_input(password) != True:
			return

		#Send request to the server to create new user on the system
		response = self.send_request_to_server(1, [username, password])

		if self.after_check(response) != True:
			return

		#All checks passed: user created on the system: can update local info
		print("Successfully created new user " + username)
		self._current_user = username

	def login(self):
		"""
		Function that logs user in (matches user with user on the system)
		Server response is a list:
			[String] - successful login: return name of the last room used by user (can be None)
		"""

		#Perform before check
		if self.before_check(connected=True, logged_out=True) != True: 
			return

		#Prompt user for input
		username = input("Enter username: ")
		#Validate user input
		if self.validate_user_input(username) != True:
			return

		password = input("Enter password: ")
		if self.validate_user_input(password) != True:
			return

		#Send request to server to log user in
		response = self.send_request_to_server(2, [username, password])

		if self.after_check(response) != True:
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

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#All checks passed: can log user out: clear local info
		self._current_user = None
		self._current_room = None

		print("Successfully logged out.")

	def create_new_room(self):
		"""
		Function that creates new room on the system
		Serer responds with a list consisting of just 1 item:
			[OK] - successful room creation
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user to input name of the room to create
		room_name = input("Enter new room name: ")

		if self.validate_user_input(room_name) != True:
			return

		#Send request to server to create new room
		response = self.send_request_to_server(3, [room_name, self._current_user])

		if self.after_check(response) != True:
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
			[last_room, room_names] - last_room = room last used by the user, room_names = list of rooms that exist on the system
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Send a request to a server to fetch all room names
		response = self.send_request_to_server(4, [self._current_user, self._current_room])

		#Check for errored request
		if response == None: return

		if self.after_check(response) != True:
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
			[OK] - user successfully joined room
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user to enter name of the new room they want to join
		room_name = input("Please enter name of the room to join: ")

		if self.validate_user_input(room_name) != True:
			return

		#Send request to server to join new room
		response = self.send_request_to_server(5, [room_name, self._current_user])

		if self.after_check(response) != True:
			return

		#All checks passed: user joined new room: can update local info
		print("Successfully joined new room " + room_name)
		self._current_room = room_name

	def leave_room(self):
		"""
		Function that lets user leave current room
		Server response consists of a list with 1 item:
			[OK] - user succesfully left room
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True, have_room=True) != True: 
			return

		#Send a request to a server for user to leave current room
		response = self.send_request_to_server(6, [self._current_room, self._current_user])

		if self.after_check(response) != True:
			return

		#All checks passed: user Successfully left room: can update local info
		print("Successfully left " + self._current_room)
		self._current_room = None

	def switch_room(self):
		"""
		Function that lets user switch to a new room that he is a participant of
		Server response is a list that consists of one item:
			[OK] - successfuly switched room
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user to input name of the room they want to switch to
		new_room = input("Please enter room to go to: ")

		if self.validate_user_input(new_room) != True:
			return

		#Send request to a server to switch current room
		response = self.send_request_to_server(7, [self._current_user, new_room])

		if self.after_check(response) != True:
			return

		#All checks passed: room Successfully switched: can update local info
		print("Successfully switched room to " + new_room)
		self._current_room = new_room

	def send_room_message(self):
		"""
		Function that lets user send message to a room he is currently in
		Server response is a list that consists of one item:
			[OK] - message successfuly sent
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True, have_room=True) != True: 
			return

		#Prompt user to input a message to be sent to a room
		message = input("Please enter message: ")

		if self.validate_user_input(message) != True:
			return

		#Send request to server to send a message to a room
		response = self.send_request_to_server(8, [self._current_user, self._current_room, message])

		if self.after_check(response) != True:
			return

		#All checks passed: display message
		print("Succesfully sent message.")

	def view_room_messages(self):
		"""
		Function that gets all the messaged from current user room and displays them to a user
		Server response is a list that consists of 1 item:
			[room_messages] - list of room messages
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True, have_room=True) != True: 
			return

		#Send request to server to fetch all messaged from current room
		response = self.send_request_to_server(9, [self._current_user, self._current_room])

		if self.after_check(response) != True:
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
			[room_members] - list of room members
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True, have_room=True) != True: 
			return

		#Send request to server to fetch all messaged from current room
		response = self.send_request_to_server(10, [self._current_user, self._current_room])

		if self.after_check(response) != True:
			return

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
			[OK] - successful message sent
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user input for recipient name
		recipient = input("Please enter username of the user you want to send message to: ")
		if self.validate_user_input(recipient) != True:
			return

		#Prompt user to input personal message they want to send
		message = input("Please enter message you'd like to send to " + recipient + " : ")
		if self.validate_user_input(message) != True:
			return

		#Attempt sending message
		response = self.send_request_to_server(11, [self._current_user, recipient, message])

		if self.after_check(response) != True:
			return

		#All checks passed, message was sent
		print("Message to " + recipient + " was successfuly sent.")

	def view_personal_inbox(self):
		"""
		Function that fetches inbox for current user and displays it
		Calls a server function, which returns a list:
			[inbox] - list of users personal messages
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Get server response
		response = self.send_request_to_server(12, [self._current_user])

		if self.after_check(response) != True:
			return

		if len(response) == 0:
			print("Inbox is empty!")
			return

		#Print all messaged from a room
		print("**************************************************************")
		for i in range(len(response)):
			print(response[i]["At"], " | ", response[i]["From"], " | ", response[i]["Message"])

		print("**************************************************************")

	def send_all_room_message(self):
		"""
		Function sends message to all rooms that user participates in.
		Fetches all users rooms, and sends message to each one
		"""
		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user to input message they want to send
		message = input("Please enter message you'd like to send: ")
		if self.validate_user_input(message) != True:
			return

		#Get server response
		response = self.send_request_to_server(13, [self._current_user, message])

		if self.after_check(response) != True:
			return

		print("Message was sent to: " + '[%s]' % ', '.join(map(str, response)))

	def send_message_to_selected_rooms(self):
		"""
		Function that sends messages to user selected rooms
		User types in rooms to send message to
		Calls server function that returns a list of rooms to which message was sent, and not sent
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user to input rooms they want to send message to
		room_names = input("Please enter room names (separated by comma): ")
		if self.validate_user_input(room_names) != True:
			return

		#Reformat to remove spaces between commas if any
		room_names = [x.strip() for x in room_names.split(',')]

		#Prompt user to input message they want to send
		message = input("Please enter message you'd like to send: ")
		if self.validate_user_input(message) != True:
			return

		#Get server response: No need to do after check, errors will be displayed as failed messages
		response = self.send_request_to_server(14, [self._current_user, room_names, message])

		if len(response[0]) > 0:
			print("Message was successfuly sent to: " + '[%s]' % ', '.join(map(str, response[0])))

		if len(response[1]) > 0:
			print("Message FAILED to be sent to: " + '[%s]' % ', '.join(map(str, response[1])))

	def join_selected_rooms(self):
		"""
		Function that lets user to join multiple selected rooms
		Lets user type in room names of the rooms they want to join.
		Calls server function that lets them join.
		Server function returns a list of successfuly joined rooms, and failed rooms
		"""

		#Perform before check
		if self.before_check(connected=True, logged_in=True) != True: 
			return

		#Prompt user to input rooms they want to send message to
		room_names = input("Please enter room names (separated by comma): ")
		if self.validate_user_input(room_names) != True:
			return

		#Reformat to remove spaces between commas if any
		room_names = [x.strip() for x in room_names.split(',')]

		#Get server response: No need to do after check, errors will be displayed as failed joins
		response = self.send_request_to_server(15, [self._current_user, room_names])

		if len(response[0]) > 0:
			print("Successfuly joined: " + '[%s]' % ', '.join(map(str, response[0])))
			#update current room to last joined one
			self._current_room = response[0][-1]

		if len(response[1]) > 0:
			print("FAILED to join: " + '[%s]' % ', '.join(map(str, response[1])))


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

	def before_check(self, connected=False, logged_in=False, logged_out=False, have_room=False):
		"""
		Helper function that checks required checks before server side function can be called.
		Not all functions need all checks, thus flags will specify which checks need to be performed

		Args:
			connected 		(Boolean) - specifies whether we need to check for connection (default = True)
			logged_in 	 	(Boolean) - specifies whether we need to check if user is logged in (default = True)
			logged_out 		(Boolean) - specifies whether we need to check if the user must be logged out (default = False)
			have_room 	 	(Boolean) - specifies whether we need to check if user participates in room atm (default = False)

		Returns:
			True 	- when all checks passed
			None 	- when check failed
		"""

		if connected == True and self._connected == False:
			return self.not_connected_error()

		if logged_in == True and self._current_user == None:
			return self.not_logged_in_error()

		if logged_out == True and self._current_user != None:
			return self.not_logged_out_error()

		if have_room == True and self._current_room == None:
			return self.not_in_room_error()

		return True

	def not_connected_error(self):
		"""
		Helper function that displays error message when clients hasn't connected to server
		"""

		print("ERROR: please connect to server.")
		return

	def not_logged_in_error(self):
		"""
		Helper function that displays error message when clients hasn't logged in into account
		"""

		print("ERROR: please create account or login.")
		return

	def not_logged_out_error(self):
		"""
		Helper function that displays error message when client has a logged in user, whereas he needs to log out before performing some action 
		"""

		print("ERROR: please log out.")

	def not_in_room_error(self):
		"""
		Helper function that displays error message when logged in user hasn't joined a room yet (without a room atm)
		"""

		print("ERROR: please create or join a room.")
		return

	def validate_user_input(self, user_input):
		"""
		Helper function that validates user input 

		Args:
			user_input (String) - user entered input (can be empty)

		Returns:
			True - when all checks pass
			None - when checks fail (will display message)
		"""

		if type(user_input) == None or len(user_input) == 0:
			print("ERROR: invalid input. Please try again.")
			return

		return True

	def after_check(self, response):
		"""
		Helper function that performs checks on response from the server
		
		Args:
			response (List) - list containing server response (either error codes or actual data)
		Returns:
			True - all checks pass, no errors
			None - displays error messages and returns None when errors are detected

		"""
		#None signifies some error while requesting occured
		if response == None:
			return

		#Emtpy list is only returned when operation has been performed successfuly
		if len(response) == 0:
			return True

		if response[0] == None:
				return True

		#Try some checks
		try:
			r = str(response[0])
			if r == "OK":
				return True
		except:
			pass

		#Only error dict contains code as a key, check for that:
		try:
			e = response[0]["description"]
		except TypeError:
			return True
		except:
			return True

		#Response is an error. Display it
		print(response[0]["description"])



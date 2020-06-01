import socket
import sys
import traceback
import os
from _thread import *
from threading import Thread

import datetime

from user import User 
from room import Room

class Server():
	def __init__(self):
		self._server_socket = socket.socket()
		self._host = '127.0.0.1'
		self._port = 4444

		self._max_clients = 100

		self._threads = 0
		self._users = []
		self._usernames = []

		self._rooms = []
		self._room_names = []

	def start(self):
		"""
		Main function that starts the server and listens for new connections from the user. 
		Upon new connection, starts new thread (to be able to handle multiple client connections).
		At the moment shutsdown upon user interrupt (ctrl+c)
		"""
		#Start server
		try: 
			self._server_socket.bind((self._host, self._port))
		except socket.error as e:
			print(str(e))

		print("Press Ctrl+C to shutdown.")
		print("Waiting for a connection...")

		#Accept new connections until 100 user use service simultaneously.
		self._server_socket.listen(self._max_clients)

		#Upon each new connection start new thread
		try:
			while True:
				Client, address = self._server_socket.accept()
				print("Connected to: " + address[0] + ":" + str(address[1]))
				start_new_thread(self.threaded_client, (Client, address))
				self._threads += 1
		except KeyboardInterrupt:
			print("\nShutdown on KeyboardInterrupt.\n")

		self._server_socket.close()


	def stop(self):
		self._run = False
		self._server_socket.close()

	def threaded_client(self, connection, address):
		"""
		Helper function that actually handles individual client
		"""

		#Initially send user greeting
		connection.send(str.encode("Welcome to the Server.\n"))

		#Keep communicating (receiving/sending) while connection is established with the client
		while True:
			data = connection.recv(2048)
			#Check if data is empty or client closed the connection
			if (not data) or data == b'': 
				print("Disconnected from: " + address[0] + ":" + str(address[1]))
				connection.close()
				return

			#Get user request
			request = eval(data.decode('utf-8'))

			#All helper functions return a list as a response. If lsit isn't returned - means there is an error
			response = self._request_handler(request, address)
			if type(response) != list:
				connection.close()
			else:
				response = str(response)

			#Send response to client request
			try:
				connection.sendall(response.encode())
			except OSError:
				connection.close()

		connection.close()

	def _request_handler(self, request, address):
		"""
		Helper function that handles user requests based on the code user sent.

		Args:
			request 	(List) - [0] contains request code, [1] contains request details
			address  	(List) - specifies full IP address of user who made request

		Returns:
			(List) - contains either information, OK (successful operation), or error message
		"""

		addr = address[0] + ":" + str(address[1])

		if(request[0] == "create_new_user"): 
			try:
				print(addr + " | create_new_user | " + " username: " + str(request[1][0]) + " | password: " + str(request[1][1]))
				result = self.create_new_user(request[1][0], request[1][1])
				print(addr + " | create_new_user | result | " + str(result))
				return result
			except:
				print(addr + " | create_new_user | ERROR")
				return

		if(request[0] == "login"): 
			try:
				print(addr + " | login | " + str(request[1]))
				result = self.login(request[1][0], request[1][1])
				print(addr + " | login | result | " + str(result))
				return result
			except:
				print(addr + " | login | ERROR")
				return

		if(request[0] == "create_new_room"): 
			try:
				print(addr + " | create_new_room : " + str(request[1]))
				result = self.create_new_room(request[1][0], request[1][1])
				print(addr + " | create_new_room | result | " + str(result))
				return result
			except:
				print(addr + " | create_new_room | ERROR")
				return

		if(request[0] == "list_all_rooms"): 
			try:
				print(addr + " | list_all_rooms : " + str(request[1]))
				result = self.list_all_rooms(request[1][0], request[1][1])
				print(addr + " | list_all_rooms | result | " + str(result))
				return result
			except:
				print(addr + " | list_all_rooms | ERROR")
				return

		if(request[0] == "join_new_room"): 
			try:
				print(addr + " | join_new_room : " + str(request[1]))
				result = self.join_new_room(request[1][0], request[1][1])
				print(addr + " | join_new_room | result | " + str(result))
				return result
			except:
				print(addr + " | join_new_room | ERROR")
				return

		if(request[0] == "leave_room"): 
			try:
				print(addr + " | leave_room : " + str(request[1]))
				result = self.leave_room(request[1][0], request[1][1])
				print(addr + " | leave_room | result | " + str(result))
				return result
			except:
				print(addr + " | leave_room | ERROR")
				return

		if(request[0] == "switch_room"):
			try:
				print(addr + " | switch_room : " + str(request[1]))
				result = self.switch_room(request[1][0], request[1][1])
				print(addr + " | switch_room | result | " + str(result))
				return result
			except:
				print(addr + " | switch_room | ERROR")
				return

		if(request[0] == "send_room_message"): 
			try:
				print(addr + " | send_room_message : " + str(request[1]))
				result = self.send_room_message(request[1][0], request[1][1], request[1][2])
				print(addr + " | send_room_message | result | " + str(result))
				return result
			except:
				print(addr + " | send_room_message | ERROR")
				return

		if(request[0] == "view_room_messages"): 
			try:
				print(addr + " | view_room_messages : " + str(request[1]))
				result = self.view_room_messages(request[1][0], request[1][1])
				print(addr + " | view_room_messages | result | " + str(result))
				return result
			except:
				print(addr + " | view_room_messages | ERROR")
				return

		if(request[0] == "view_room_members"): 
			try:
				print(addr + " | view_room_members : " + str(request[1]))
				result = self.view_room_members(request[1][0], request[1][1])
				print(addr + " | view_room_members | result | " + str(result))
				return result
			except:
				print(addr + " | view_room_members | ERROR")
				return

		if(request[0] == "send_personal_message"): 
			try:
				print(addr + " | _send_personal_message : " + str(request[1]))
				result = self.send_personal_message(request[1][0], request[1][1], request[1][2])
				print(addr + " | send_personal_message | result | " + str(result))
				return result
			except:
				print(addr + " | send_personal_message | ERROR")
				return

		if(request[0] == "view_personal_inbox"): 
			try:
				print(addr + " | view_personal_inbox : " + str(request[1]))
				result = self.view_personal_inbox(request[1][0])
				print(addr + " | view_personal_inbox | result | " + str(result))
				return result
			except:
				print(addr + " | view_personal_inbox | ERROR")
				return

		if(request[0] == "send_all_room_message"): 
			try:
				print(addr + " | send_all_room_message : " + str(request[1]))
				result = self.send_all_room_message(request[1][0], request[1][1])
				print(addr + " | send_all_room_message | result | " + str(result))
				return result
			except:
				print(addr + " | send_all_room_message | ERROR")
				return

		if(request[0] == "send_message_to_selected_rooms"): 
			try:
				print(addr + " | send_message_to_selected_rooms : " + str(request[1]))
				result = self.send_message_to_selected_rooms(request[1][0], request[1][1], request[1][2])
				print(addr + " | send_message_to_selected_rooms | result | " + str(result))
				return result
			except:
				print(addr + " | send_all_room_message | ERROR")
				return

		if(request[0] == "join_selected_rooms"): 
			try:
				print(addr + " | join_selected_rooms : " + str(request[1]))
				result = self.join_selected_rooms(request[1][0], request[1][1])
				print(addr + " | join_selected_rooms | result | " + str(result))
				return result
			except:
				print(addr + " | send_all_room_message | ERROR")
				return

		if(request[0] == 666): 
			return 1

	def create_new_user(self, username, password):
		"""
		Function that creates new user on the system

		Args:
			username (String) - username of the user to be created
			password (String) - password for the user to be created

		Returns (one of the following):
			[OK] - successful user creation on the system
		"""

		#Perform checks
		before_check = self.before_check(check_user_already_exists=True, username=username)

		if before_check != True:
			return before_check

		new_user = User(username=username, password=password)	#create new user
		self._users.append(new_user)							#append user to system user list
		self._usernames.append(username)						#append username to system username list
		return ["OK"]

	def login(self, username, password):
		"""
		Function that tries to log user in (match if the record exists)

		Args:
			username (String) - username of the user that tries to log in
			password (String) - password for the user that tries to log in

		Returns (one of the following):
			[String] - successful login: return name of the last room used by user (can be None)
		"""

		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		#Match user and password
		user = self._find_user(username)
		if user._password != password:
			return [{"description": "ERROR: Invalid username or password."}]

		#All checks passed: return room last used by the user
		return [user._last_room]

	def create_new_room(self, room_name, username):
		"""
		Function that creates new room on the system

		Args:
			room_name 	(String) - name of the room to be created
			owner 		(String) - username of the user that wants to create new room

		Returns (one of the following):
			[OK] - successful room creation
		"""

		before_check = self.before_check(check_username=True, check_room_already_exists=True, username=username, room_name=room_name)
		if before_check != True:
			return before_check

		new_room = Room(name=room_name, owner=username)	#create new Room object

		user = self._find_user(username)				#find user object
		user._rooms.append(new_room)					#append room to the list of user rooms
		user._room_names.append(room_name)				#appends room name to the user room names
		user._last_room = room_name 					#update last room user interacted with

		new_room._users.append(user)					#append user to list of user objects in room	
		new_room._usernames.append(username)			#append name to list of usernames in room

		self._rooms.append(new_room)					#append to list of rooms on server
		self._room_names.append(room_name)				#append to list of room names on server

		return ["OK"]

	def list_all_rooms(self, username, current_room):
		"""
		Function that returns all rooms existing on the system

		Args:
			username 		(String) - username of the user that wants to fetch all rooms
			current_room 	(String) - room currently used by the user that wants to fetch all rooms

		Returns (one of the following):
			[last_room, room_names] - last_room = room last used by the user, room_names = list of rooms that exist on the system
		"""

		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		#Find user object on the system
		user = self._find_user(username)

		#Update user last room
		if user._last_room == None and current_room != None:
			user._last_room = current_room

		return [user._last_room, self._room_names]

	def join_new_room(self, room_name, username):
		"""
		Function that lets user join new room

		Args:
			room_name 	(String) - name of the server that user wants to join
			username 	(String) - username of the user that wants to join new room

		Returns (one of the following):
			[OK] - successful join
		"""

		before_check = self.before_check(check_username=True, check_room_name=True, check_user_not_in_room=True, check_room_not_in_user=True, 
			username=username, room_name=room_name)
		if before_check != True:
			return before_check

		#Find Room object on the system
		room = self._find_room(room_name)
	
		user = self._find_user(username)		#create new User object
		room._users.append(user)				#append user to room users list
		room._usernames.append(username)		#append username to room usernames list
		user._rooms.append(room)				#append room to user rooms list
		user._room_names.append(room_name)		#append room name to user room names
		user._last_room = room_name 			#update user last room to room_name
		return ["OK"]

	def leave_room(self, room_name, username):
		"""
		Function that lets user to leave room

		Args:
			room_name 	(String) - name of the room user wants to leave
			username 	(String) - username of the user that wants to leave room

		Returns:
			[OK] - successful leaving

		"""

		before_check = self.before_check(check_username=True, check_room_name=True, check_user_in_room=True, check_room_in_user=True, 
			username=username, room_name=room_name)
		if before_check != True:
			return before_check

		#Find Room object on the system
		room = self._find_room(room_name)
		
		#Find user object in the system
		user = self._find_user(username)

		#All checks passed: can update info to leave
		room._users.remove(user)				#remove user from rooms user list			
		room._usernames.remove(username)		#remove username from rooms username list
		user._rooms.remove(room)				#remove room from user rooms list
		user._room_names.remove(room_name)		#remove room_name from user room_names list

		#Check if the room user is leaving is the last he was using: if so, change last_room to None
		if user._last_room == room_name: 
			user._last_room = None

		#Successful leaving
		return ["OK"]

	def switch_room(self, username, room_name):
		"""
		Function that lets user switch from one room to another room.
		User must be a participant of the room he wants to switch to.

		Args: 
			username 	(String) - username of the user that wants to switch rooms
			room_name 	(String) - name of the room that user wants to switch to

		Returns (one of the following): 
			[OK] - successfuly switched room
		"""

		before_check = self.before_check(check_username=True, check_room_name=True, check_user_in_room=True, check_room_in_user=True, 
			username=username, room_name=room_name)
		if before_check != True:
			return before_check

		#Find user
		user = self._find_user(username)

		#Update user info and return successful switch
		user._last_room = room_name
		return ["OK"]

	def send_room_message(self, username, room_name, message):
		"""
		Function that sends a rooms message: appends message list in room object

		Args: 
			username 	(String) - username of the user trying to send message
			room_name 	(String) - name of the room user is trying to send message to
			message 	(String) - message user is trying to send to a room

		Returns: 
			[OK] - message successfuly sent
		"""

		before_check = self.before_check(check_username=True, check_room_name=True, check_user_in_room=True, check_room_in_user=True, 
			username=username, room_name=room_name)
		if before_check != True:
			return before_check

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#Passed all checks, can actually send a message
		user._last_room = room_name
		time = datetime.datetime.now()
		final_message = {"At": time, "From": username, "Message": message}

		#Add message to room messages
		room._messages.append(final_message)
		return ["OK"]

	def view_room_messages(self, username, room_name):
		"""
		Function that returns room messages to the user who requested to view room messages

		Args: 
			username 	(String) - username of the user that wants to switch rooms
			room_name 	(String) - name of the room that user wants to switch to

		Returns (one of the following):
			[room_messages] - list of room messages
		"""

		before_check = self.before_check(check_username=True, check_room_name=True, check_user_in_room=True, check_room_in_user=True, username=username, room_name=room_name)
		if before_check != True:
			return before_check

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#All checks passed, can send back messages
		user.last_room = room_name
		return room._messages

	def view_room_members(self, username, room_name):
		"""
		Function that returns room messages to the user who requested to view room messages

		Args: 
			username 	(String) - username of the user that wants to switch rooms
			room_name 	(String) - name of the room that user wants to switch to

		Returns:
			[room_members] - list of room members
		"""

		before_check = self.before_check(check_username=True, check_room_name=True, check_user_in_room=True, check_room_in_user=True, username=username, room_name=room_name)
		if before_check != True:
			return before_check

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#All checks passed, can send back messages
		user.last_room = room_name
		return room._usernames

	def send_personal_message(self, username, recipient, message):
		"""
		Function that sends personal message from one user to another: inputs messge into message list

		Args:
			username 	(String) - username of the user that attempts to send the message
			recipient 	(String) - username of the user that will receive the message
			message 	(String) - message that is meant to be sent

		Returns (One of the following):
			[OK] - successful message sent
		"""

		#Check for sender
		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		#Check for recipient
		before_check = self.before_check(check_username=True, username=recipient)
		if before_check != True:
			return before_check

		#All checks passed, can send message
		receiver = self._find_user(recipient)

		time = datetime.datetime.now()
		final_message = {"At": time, "From": username, "Message": message}
		receiver._inbox.append(final_message)

		return ["OK"]

	def view_personal_inbox(self, username):
		"""
		Function fetches users inbox and sends it back to the user to view

		Args:
			username 	(String) - username of the user that attempts to view his inbox

		Returns:
			[inbox] - list of users personal messages
		"""

		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		#All checks passed, can send back list of messages
		user = self._find_user(username)

		return user._inbox

	def send_all_room_message(self, username, message):
		"""
		Function puts a user message into all rooms that user is a participant of

		Args: 
			username 	(String) - username of the user that wants to send the message
			message 	(String) - message user wants to send to all the rooms

		Returns:
			["OK"] - successful message sent
		"""

		sent_to = []

		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		user = self._find_user(username)

		for room_name in user._room_names:
			before_check = self.before_check(check_user_in_room=True, check_room_in_user=True, username=username, room_name=room_name)
			if before_check != True:
				return before_check

			room = self._find_room(room_name)
			time = datetime.datetime.now()
			final_message = {"At": time, "From": username, "Message": message}
			room._messages.append(final_message)
			sent_to.append(room_name)

		return sent_to

	def send_message_to_selected_rooms(self, username, room_names, message):
		"""
		Function that sends a message from a user to a list of rooms which have been specified

		Args: 
			username 	(String) - username of the user that wants to send the message
			room_names 	(List) 	 - room names to which message should be sent
			message 	(String) - message that needs to be sent to the rooms

		Retuns:
			sent_to 	(List) - names of the rooms to which message was successfuly sent
			failed 		(List) - names of the rooms to which message failed to be sent
		"""

		sent_to = []
		failed = []

		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		user = self._find_user(username)

		for room_name in room_names:
			before_check = self.before_check(check_room_name=True, check_user_in_room=True, check_room_in_user=True, username=username, room_name=room_name)
			if before_check != True:
				failed.append(room_name)
			else:
				room = self._find_room(room_name)
				time = datetime.datetime.now()
				final_message = {"At": time, "From": username, "Message": message}
				room._messages.append(final_message)
				sent_to.append(room_name)

		return [sent_to, failed]

	def join_selected_rooms(self, username, room_names):
		"""
		Function that lets user join multiple rooms

		Args:
			username 	(String) - username of the user that wants to join rooms
			room_names 	(List)   - names of the rooms user is attemptin to join

		Returns:
			joined 	(List) - names of the rooms that user successfuly joined
			failed 	(List) - names of the rooms user failed to join
		"""

		joined = []
		failed = []
		
		before_check = self.before_check(check_username=True, username=username)
		if before_check != True:
			return before_check

		user = self._find_user(username)

		for room_name in room_names:
			result = self.join_new_room(room_name, username)

			if result[0] == "OK":
				joined.append(room_name)
			else:
				failed.append(room_name)

		user._last_room = joined[-1]  # update last user room
		return [joined, failed]	

	##############################################################################################
	#HELPER FUNCTIONS############################################################HELPER FUNCTIONS#
	##############################################################################################

	def _find_user(self, username):
		"""
		Helper function that returns User object with a passed in username. Before checks make sure user exists

		Args:
			username 	(String) - username of the User object

		Returns:
			user 	(Object) - User object with a given username
		"""

		user = [x for x in self._users if x._username == username][0]
		return user

	def _find_room(self, room_name):
		"""
		Helper function that returns Room object with a passed in room_name. Before checks make sure room exists

		Args:
			room_name 	(String) - name of the Room object

		Returns:
			room 	(Object) - Room object with a given room_name
		"""
		room = [x for x in self._rooms if x._name == room_name][0]
		return room

	def before_check(self, check_username=False, check_user_already_exists=False, check_room_name=False, check_room_already_exists=False, check_user_in_room=False, 
		check_room_in_user=False, check_user_not_in_room=False, check_room_not_in_user=False, username=None, room_name=None):
		"""
		Helper function that provides a centralized error system
		Performs checks and returns either an error or True (signifies successful pass of all tests)

		Args:
			check_username 				(Boolean) 		- specifies whether to check if user with username EVEN exists on system
			check_user_already_exists 	(Boolean) 		- specifies whether to check if user with username ALREADY exists on the system (for new user registration)
			check_room_name 			(Boolean) 		- specifies whether to check if room with room_name EVEN exists on the system
			check_room_already_exists 	(Boolean) 		- specifies whether to check if room with room_name ALREADY exists on the system (for new room registration)
			check_user_in_room 			(Boolean) 		- specifies whether to check if room with room_name EVEN has a user with a given username
			check_room_in_user 			(Boolean) 		- specifies whether to check if user with username EVEN has a room with a given room_name
			check_user_not_in_room 		(Boolean) 		- specifies whether to check if room with room_name ALREADY has user with username as a participant
			check_room_not_in_user 		(Boolean) 		- specifies whether to check if user with username ALREADY participates in a room with room_name
			username 					(String/None) 	- username of the user checks will be performed for
			room_name  					(String/None) 	- room name of the room checks will be performed for
		"""

		#Check username
		if check_username and not username in self._usernames:
			#print("ERROR: " + username + " doesn't exist on the system.")
			return [{"description": "ERROR: " + username + " doesn't exist on the system."}]

		#Check alredy exists
		if check_user_already_exists and username in self._usernames:
			#print("ERROR: " + username + " already exists on the system.")
			return [{"description": "ERROR: " + username + " already exists on the system."}]

		#Check room_name
		if check_room_name and not room_name in self._room_names:
			#print("ERROR: " + room_name + " doesn't exist on the system.")
			return [{"description": "ERROR: " + room_name + " doesn't exist on the system."}]

		if check_room_already_exists and room_name in self._room_names:
			#print("ERROR: " + room_name + " already exists on the system.")
			return [{"description": "ERROR: " + room_name + " already exists on the system."}]

		#Check user in room
		if check_user_in_room:
			room = self._find_room(room_name)
			if not username in room._usernames:
				#print("ERROR: " + room_name + " doesn't have " + username + " as a participant.")
				return [{"description": "ERROR: " + room_name + " doesn't have " + username + " as a participant."}]

		#Check room in user
		if check_room_in_user:
			user = self._find_user(username)
			if not room_name in user._room_names:
				#print("ERROR: " + username + " doesn't participate in " + room_name)
				return [{"description": "ERROR: " + username + " doesn't participate in " + room_name}]

		#Check user not in room
		if check_user_not_in_room:
			room = self._find_room(room_name)
			if username in room._usernames:
				return [{"description": "ERROR: " + room_name + " already has " + username + " as a participant."}]

		#Check room not in user
		if check_room_not_in_user:
			user = self._find_user(username)
			if room_name in user._room_names:
				return [{"description": "ERROR: " + username + " already participates in " + room_name}]

		return True

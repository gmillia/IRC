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

		self._threads = 0
		self._users = []
		self._usernames = []

		self._rooms = []
		self._room_names = []

		self._run = True

		self._current_client = None

	def start(self):
		try: 
			self._server_socket.bind((self._host, self._port))
		except socket.error as e:
			print(str(e))

		print("Waiting for a connection...")
		self._server_socket.listen(5)

		while True:
			Client, address = self._server_socket.accept()
			print("Connected to: " + address[0] + ":" + str(address[1]))
			start_new_thread(self.threaded_client, (Client, address))
			self._threads += 1

		self._server_socket.close()


	def stop(self):
		self._run = False
		self._server_socket.close()

	def threaded_client(self, connection, address):
		connection.send(str.encode("Welcome to the Server.\n"))

		while True:
			data = connection.recv(2048)
			#Check if data is empty or client closed the connection
			if (not data) or data == b'': 
				print("Disconnected from: " + address[0] + ":" + str(address[1]))
				connection.close()
				return

			#Send response on user request
			request = eval(data.decode('utf-8'))
			#All helper functions return a list as a response
			response = str(self._request_handler(request, address))
			try:
				connection.sendall(response.encode())
			except OSError:
				connection.close()

		connection.close()

	def _request_handler(self, request, address):
		"""
		request is a list
		request [0] = act to be performed
		request [1] = data that is needed to perform act

		description of the act flags can be found in docs
		"""

		addr = address[0] + ":" + str(address[1])
		if(request[0] == 1): 
			print(addr + " | create_new_user | " + " username: " + str(request[1][0]) + " | password: " + str(request[1][1]))
			return self._create_new_user(request[1][0], request[1][1])
		if(request[0] == 2): 
			print(addr + " | attempt_user_login | " + str(request[1]))
			return self._attempt_user_login(request[1][0], request[1][1])
		if(request[0] == 3): 
			print(addr + " | create_new_room : " + str(request[1]))
			return self._create_new_room(request[1][0], request[1][1])
		if(request[0] == 4): 
			print(addr + " | list_all_rooms : " + str(request[1]))
			return self._list_all_rooms(request[1][0], request[1][1])
		if(request[0] == 5): 
			print(addr + " | join_room : " + str(request[1]))
			return self._join_room(request[1][0], request[1][1])
		if(request[0] == 6): 
			print(addr + " | leave_room : " + str(request[1]))
			return self._leave_room(request[1][0], request[1][1])
		if(request[0] == 7):
			print(addr + " | switch_room : " + str(request[1]))
			return self._switch_room(request[1][0], request[1][1])
		if(request[0] == 8): 
			print(addr + " | send_room_message : " + str(request[1]))
			return self._send_room_message(request[1][0], request[1][1], request[1][2])
		if(request[0] == 9): 
			print(addr + " | show_room_messages : " + str(request[1]))
			return self._show_room_messages(request[1][0], request[1][1])
		if(request[0] == 666): 
			return 1

	def _create_new_user(self, username, password):
		"""
		Function that creates new user on the system

		Args:
			username (String) - username of the user to be created
			password (String) - password for the user to be created

		Returns:
			[0] - user already exists
			[1] - successful user creation on the system
		"""

		#Check if user with passed username doesn't exist on the system
		if not (username in self._usernames):
			new_user = User(username=username, password=password)	#create new user
			self._users.append(new_user)							#append user to system user list
			self._usernames.append(username)						#append username to system username list
			return [1]
		else: 
			return [0]

	def _attempt_user_login(self, username, password):
		"""
		Function that tries to log user in (match if the record exists)

		Args:
			username (String) - username of the user that tries to log in
			password (String) - password for the user that tries to log in

		Returns:
			[0] - username doesn't exist on the system OR password doesn't match user
			[String] - successful login: return name of the last room used by user (can be None)
		"""

		#Check username existence on the system
		if not(username in self._usernames):
			return [0]

		#Match user and password
		user = self._find_user(username)
		if user._password != password:
			return [0]

		#All checks passed: return room last used by the user
		return [user._last_room]

	'''
	def _list_all_users(self):
		return self._usernames

	def _remove_user(self, username):
		#User doesn't exist
		if not (username in self._usernames):
			return 0
		else:
			try:
				del self._users[self._find_item_index(username, self._usernames)]
				self._usernames.remove(username)
				return 1
			except:
				return 2
	'''

	def _create_new_room(self, room_name, owner):
		"""
		Function that creates new room on the system

		Args:
			room_name (String) - name of the room to be created
			owner (String) - username of the user that wants to create new room

		Returns:
			[0] - room already exists on the system
			[1] - successful room creation
		"""

		#Check that room doesn't exist on the system yet
		if not (room_name in self._room_names):
			new_room = Room(name=room_name, owner=owner)	#create new Room object
			user = self._find_user(owner)					#find user object
			user._room_names.append(room_name)				#appends room name to the user room names
			new_room._users.append(user)					#append user to list of user objects in room	
			new_room._usernames.append(owner)				#append name to list of usernames in room
			self._rooms.append(new_room)					#append to list of rooms on server
			self._room_names.append(room_name)				#append to list of room names on server
			user._last_room = room_name 					#update last room user interacted with
			return [1]
		else: 
			return [0]

	def _list_all_rooms(self, username, current_room):
		"""
		Function that returns all rooms existing on the system

		Args:
			username (String) - username of the user that wants to fetch all rooms
			current_room (String) - room currently used by the user that wants to fetch all rooms

		Returns:
			[0] - user doesn't exist on the system
			[last_room, room_names] - last_room = room last used by the user, room_names = list of rooms that exist on the system
		"""

		#Check if user exists on the system
		if not (username in self._usernames):
			return [0]

		#Find user object on the system
		user = self._find_user(username)

		#Update user last room
		if user._last_room == None && current_room != None:
			user._last_room = current_room

		return [user._last_room, self._room_names]

	def _join_room(self, room_name, username):
		"""
		Function that lets user join new room

		Args:
			room_name (String) - name of the server that user wants to join
			username (String) - username of the user that wants to join new room

		Returns:
			[0] - room_name (room) doesn't exist on the system
			[1] - user is already a participant of the room he wants to join
			[2] - user successfully joined room
		"""

		#Check if room exists on the system
		if not (room_name in self._room_names):
			return [0]

		#Find Room object on the system
		room = self._find_room(room_name)

		#User already joined room
		if username in room._usernames:
			return [1]
	
		user = self._find_user(username)		#create new User object
		room._users.append(user)				#append user to room users list
		room._usernames.append(username)		#append username to room usernames list
		user._rooms.append(room)				#append room to user rooms list
		user._room_names.append(room_name)		#append room name to user room names
		user._last_room = room_name 			#update user last room to room_name
		return [2]

	def _leave_room(self, room_name, username):
		"""
		Function that lets user to leave room

		Args:
			room_name (String) - name of the room user wants to leave
			username (String) - username of the user that wants to leave room

		Returns:
			[0] - room with room_name doesn't exist on the system
			[1] - user with username doesn't exist on the system
			[2] - room doesn't have user with username as a participant 
			[3] - user doesn't have room with room_name in rooms that he participates in
			[4] - user successfully left room

		"""

		#Check if room doesn't exist on the system
		if not (room_name in self._room_names):
			return [0]

		#Check if username doesn't exist on the system
		if not (username in self._usernames):
			return [1]

		#Find Room object on the system
		room = self._find_room(room_name)

		#Check if user with username is in rooms usernames list
		if  not (username in room._usernames):
			return [2]
		
		#Find user object in the system
		user = self._find_user(username)

		#Check if user has room_name in his room_names list
		if not (room_name in user._room_names):
			return [3]

		#All checks passed: can update info to leave
		room._users.remove(user)				#remove user from rooms user list			
		room._usernames.remove(username)		#remove username from rooms username list
		user._rooms.remove(room)				#remove room from user rooms list
		user._room_names.remove(room_name)		#remove room_name from user room_names list

		#Check if the room user is leaving is the last he was using: if so, change last_room to None
		if user._last_room == room_name: 
			user._last_room = None

		#Successful removal
		return [4]

	def _switch_room(self, username, room_name):
		"""
		Function that lets user switch from one room to another room

		Args: 
			username (String) - username of the user that wants to switch rooms
			room_name (String) - name of the room that user wants to switch to

		Returns: 
			[0] - 
		"""

		#Check that user exists on the server
		if not (username in self._usernames):
			return [0]

		#Check that room exists on the server
		if not (room_name in self._room_names):
			return [1]

		#Find user
		user = self._find_user(username)

		#Check if user participates in the room he wants to switch to
		if not (room_name in user._room_names):
			return [2]

		#Update user info and return successful switch
		user._last_room = room_name
		return [3]


	def _send_room_message(self, username, room_name, message):
		#Check if such room exists
		if not (room_name in self._room_names):
			return [0]

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#Check that user is in the room in room side
		if  not (username in room._usernames):
			return [1]

		#Check that user in the room in user side
		if not (room_name in user._room_names):
			return [2]

		#Passed all checks, can actually send a message
		user._last_room = room_name
		time = datetime.datetime.now()
		final_message = {"At": time, "From": username, "Message": message}

		#Add message to room messages
		room._messages.append(final_message)
		return [3]

		#Send message to all room users
		#Probably not needed - users will fetch messages from current room

	def _show_room_messages(self, username, room_name):
		#Check if such room exists
		if not (room_name in self._room_names):
			return 0

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#Check that user is in the room in room side
		if  not (username in room._usernames):
			return [1]

		#Check that user in the room in user side
		if not (room_name in user._room_names):
			return [2]

		#All checks passed, can send back messages
		user.last_room = room_name
		return room._messages

	#Helper functions
	def _find_user(self, username):
		user = [x for x in self._users if x._username == username][0]
		return user

	def _find_room(self, room_name):
		room = [x for x in self._rooms if x._name == room_name][0]
		return room

	def _find_item_index(self, username, list):
		return list.index(username)

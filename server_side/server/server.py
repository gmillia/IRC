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
			response = str(self._request_handler(request))
			try:
				connection.sendall(response.encode())
			except OSError:
				connection.close()

		connection.close()

	def _request_handler(self, request):
		"""
		request is a list
		request [0] = act to be performed
		request [1] = data that is needed to perform act

		description of the act flags can be founds in docs
		"""
		if(request[0] == 1): return self._create_new_user(request[1][0], request[1][1])
		if(request[0] == 2): return self._attempt_user_login(request[1][0], request[1][1])
		if(request[0] == 3): return self._create_new_room(request[1][0], request[1][1])
		if(request[0] == 4): return self._list_all_rooms(request[1][0], request[1][1])
		if(request[0] == 5): return self._join_room(request[1][0], request[1][1])
		if(request[0] == 6): return self._leave_room(request[1][0], request[1][1])
		if(request[0] == 7): return self._send_room_message(request[1][0], request[1][1], request[1][2])
		if(request[0] == 8): return self._show_room_messges(request[1][0], request[1][1])
		if(request[0] == 666): return 1

	def _create_new_user(self, username, password):
		if not (username in self._usernames):
			new_user = User(username=username, password=password)
			self._users.append(new_user)
			self._usernames.append(username)
			return 1
		else: return 0

	def _attempt_user_login(self, username, password):
		if not(username in self._usernames):
			return 0
		else:
			user = self._find_user(username)
			if user._password != password:
				return "invalid"
			else:
				return user._last_room

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
		if not (room_name in self._room_names):
			new_room = Room(name=room_name, owner=owner)
			user = self._find_user(owner)	#find user object
			new_room._users.append(user)	#append user to list of user objects in room	
			new_room._usernames.append(owner)	#append name to list of usernames in room
			self._rooms.append(new_room)	#append to list of rooms on server
			self._room_names.append(room_name)	#append to lst of room names on server
			user._last_room = room_name 	#update last room user interacted with
			return 1
		else: return 0

	def _list_all_rooms(self, username, current_room):
		#Don't return rooms if username doesn't checkout
		if not (username in self._usernames):
			return [0]

		#User called and doesn't have last room
		if current_room == None:
			return [None, self._room_names]

		user = self._find_user(username)
		return [user._last_room, self._room_names]

	def _join_room(self, room_name, username):
		if not (room_name in self._room_names):
			return 0

		room = self._find_room(room_name)

		#User already joined room
		if username in room._usernames:
			return 1
		else:
			user = self._find_user(username)
			#Update room info
			room._users.append(user)
			room._usernames.append(username)
			#Update user info
			user._rooms.append(room)
			user._room_names.append(room_name)
			user._last_room = room_name
			return 2

	def _leave_room(self, room_name, username):
		if not (room_name in self._room_names):
			return 0

		room = self._find_room(room_name)

		if  not (username in room._usernames):
			return 1
		else:
			user = self._find_user(username)
			#Update room stuff
			room._users.remove(user)
			room._usernames.remove(username)
			#Update user info
			user._rooms.remove(room)
			user._room_names.remove(room_name)
			if user._last_room == room_name: 
				user._last_room = None
			return 2

	def _send_room_message(self, username, room_name, message):
		#Check if such room exists
		if not (room_name in self._room_names):
			return 0

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#Check that user is in the room in room side
		if  not (username in room._usernames):
			return 1

		#Check that user in the room in user side
		if not (room_name in user._room_names):
			return 2

		#Passed all checks, can actually send a message
		time = datetime.datetime.now()
		final_message = {"At": time, "From": username, "Message": message}

		#Add message to room messages
		room._messages.append(final_message)
		return 3

		#Send message to all room users
		#Probably not needed - users will fetch messges from current room

	def _show_room_messages(self, username, room_name):
		#Check if such room exists
		if not (room_name in self._room_names):
			return 0

		#Room exists: Find room object and User object
		room = self._find_room(room_name)
		user = self._find_user(username)

		#Check that user is in the room in room side
		if  not (username in room._usernames):
			return 1

		#Check that user in the room in user side
		if not (room_name in user._room_names):
			return 2

		#All checks passed, can send back messages
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

# IRC

Final project for CS494 - Internet Relay Chat (Socket programming done on Python)

> Simple chat that allows client to create user and interact with other users, as well as create/join room to exchange messages with multiple users.

---

## To use

1. Start server - navigate to server_side folder, and then run: `python3 main.py`
2. Start client - navigate to client_side folder, and then run: `python3 main.py`
3. Server supports multiple clients. To start new client simply open new terminal and start another client.
4. Connect to server -> Create user / Login -> Choose what happends next from user menu... 
5. User can view his username on top of the menu, along with current room he participates in.

---

## User menu

0. `Connect to a server` 				
1. `Disconnect from a server` 		
2. `Create new user` 					
3. `Login to existing account` 
4. `Logout`
5. `Create new room`
6. `List all rooms`
7. `Join new room`
8. `Leave room`
9. `Switch room`
10. `Send message to room`
11. `View room messages`
12. `View room members`
13. `Send personal message`
14. `View personal inbox`
15. `Exit`

---

## Specifics

1. Without connecting to server, all other menu choices will result in error, and menu will be displayed again.
2. Without valid user account, all other menu choices will result in error, and menu will be displayed again.
3. While logged in, user can perform user specific actions, such as: [Disconnect from a server, Logout, Create new room, List all rooms, Join new room, Switch room, Send personal message, View personal inbox]
4. While user is a participant of a room, in addition to user specific actions, user can perform room specific actions, such as: [Leave room, Send message to room, View room messages, View room members]

---

## Docs

Navigate to `client_side/` to view more information about user menu options.

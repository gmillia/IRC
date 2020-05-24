# IRC

Final project for CS494 - Internet Relay Chat (Socket programming done on Python)

> Simple chat that allows client to create user and interact with other users, as well as create/join room to exchange messages with multiple users.

---

## Start

Simply run `python3 main.py`

---

## Specs

> **NOTE**: On the client_side no actual information is stored. Client keeps track current user (user that is logged-in into the system) and users room. All information is stored on the server_side. Thus, when user wants to perform user specific actions, they must be logged-in into an existing user account. Also, when user wants to perform room specific action (e.g.: leave room or send room message), they **must** currently be a participant of that room (current room can be seen above menu).

---

## Usage

> Each function has its purpose and limitations. This document explains purpose of each function.

---

### 0. Connect to a server  	
**Purpose**: Let client connect to a server (establish connection with the server).

**Errors**:
- When client is already connected and attempts to connect again. 
---

### 1. Disconnect from a server 	
**Purpose**: Let client disconnect from a server (close connection with the server).

**Errors**:
- When client isn't connected and attempts to disconnect. 
---

### 2. Create new user 	
**Purpose**: Let client create new user account on the system.

**Errors**:
- When client isn't connected to a server.
- When client is already signed-in into some user account.
- When client inputs invalid information for either username or password.
- When user with a given username already exists on the system (server).
---

### 3. Login to existing account 
**Purpose**: Let client login to an existing user account.

**Errors**:
- When client isn't connected to a server.
- When client is already signed-in into some user account.
- When client inputs invalid information for either username or password.
- When user with a given username doesn't exist on the system (server) OR username and password don't match up.
---

### 4. Logout
**Purpose**: Let user logout of current user account.

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 5. Create new room
**Purpose**: Let user create new room.

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user inputs invalid information for a room name
- When room with a supplied room name already exists on the system (server)
---

### 6. List all rooms
**Purpose**: Let user see all existing rooms on the system (server)

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 7. Join new room
**Purpose**: Let user join new room.

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user inputs invalid information for a room they want to join.
- When room with a supplied room name doesn't exist on the system (server)
- When user already participates in the room they want to join.
---

### 8. Leave room
**Purpose**: Let user leave current room.

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user is not currently in the room.
---

### 9. Switch room
**Purpose**: Let user switch their current room.

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user inputs invalid information for a room they want to switch too.
- When room that user wants to switch to doesn't exist on the system (server).
- When user is not a participant of the room they want to switch to.
---

### 10. Send message to room
**Purpose**: Let user send a public room message.

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user isn't a participant of a room (current room = None)
- When user inputs invalid information for a message they want to send.
---

### 11. View room messages
**Purpose**: Let user view all messages in the room (users current room).

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user isn't a participant of a room (current room = None)
---

### 12. View room members
**Purpose**: Let user view all members of a room (users current room).

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user isn't a participant of a room (current room = None)
---

### 13. Send personal message
**Purpose**: Let user send a personal message to another user

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
- When user inputs invalid information for either user they want to send message to OR message.
- When recipient user with a supplied username doesn't exist on the system (server).
---

### 14. View personal inbox
**Purpose**: Let user view all the messaged other users sent him (himself included)

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 15. Exit
**Purpose**: Let client exist the program (and close connection with a server)

**NOTE**: If server instance isn't closed, and during current session client made a user account 
and performed some user/room specific actions, client will be able to login and view all the progress.

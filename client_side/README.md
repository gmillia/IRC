# IRC

Final project for CS494 - Internet Relay Chat (Socket programming done on Python)

> Simple chat that allows client to create user and interact with other users, as well as create/join room to exchange messages with multiple users.

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
**Purpose**:

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 10. Send message to room
**Purpose**:

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 11. View room messages
**Purpose**:

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 12. View room members
**Purpose**:

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 13. Send personal message
**Purpose**:

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 14. View personal inbox
**Purpose**:

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

### 15. Exit
**Purpose**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.

**Errors**:
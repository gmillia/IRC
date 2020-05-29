# IRC

Final project for CS494 - Internet Relay Chat (Socket programming done on Python)

> Simple chat that allows client to create user and interact with other users, as well as create/join room to exchange messages with multiple users.

---

## Run

Simply run: `python3 main.py`

---

## Specs

> **NOTE**: Server saves all the user and room information until it is shutdown. At the restart clients will need to create new user accounts and new rooms (all previous information will NOT be saved). Once server is started, it keeps waiting for new user connections, until user interrupt occurs (`ctrl+c`). 

---

## Functions

---

### Create new user 	
**Purpose**: Let client create new user account on the system.

**Errors**:
- When user with a given username already exists on the system
---

### Login to an existing account 
**Purpose**: Let client login to an existing user account.

**Errors**:
- When user with a given username doesn't exist on the system. 
- When password doesn't match user password.
---

### Create new room
**Purpose**: Let user create new room.

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name already exists on the system.

### List all rooms
**Purpose**: Let user see all existing rooms on the system (server)

**Errors**:
- When user with a given username doesn't exist on the system.
---

### Join new room
**Purpose**: Let user join new room.

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room already has user as a participant.
- When user already participates in a room.
---

### Leave room
**Purpose**: Let user leave current room. (Updates user last room to None)

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### Switch room
**Purpose**: Let user switch their current room (Updats user last room to the switched room)

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### Send message to room
**Purpose**: Let user send a public room message.

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### View room messages
**Purpose**: Let user view all messages in the room.

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### View room members
**Purpose**: Let user view all members of a room.

**Errors**:
- When user with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### Send personal message
**Purpose**: Let user send a personal message to another user

**Errors**:
- When sender with a given username doesn't exist on the system.
- When receiver with a given username doesn't exist on the system.
---

### View personal inbox
**Purpose**: Let user view all the messaged other users sent him (himself included)

**Errors**:
- When sender with a given username doesn't exist on the system.
---

### Send message to all rooms
**Purpose**: Let user send message to all rooms that he is a participant of

**Errors**:
- When sender with a given username doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### Send message to selected rooms
**Purpose**: Let user send message to rooms which they choose to send message to

**Errors**:
- When sender with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room doesn't have user as a participant.
- When user doesn't participate in the room.
---

### Join selected rooms
**Purpose**: Let user join selected rooms. Updates current room to the rooms joined last

**Errors**:
- When sender with a given username doesn't exist on the system.
- When room with a given room name doesn't exist on the system.
- When room already has user as a participant.
- When user already participates in the room.
---



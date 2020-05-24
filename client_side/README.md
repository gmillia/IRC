# IRC

Final project for CS494 - Internet Relay Chat (Socket programming done on Python)

> Simple chat that allows client to create user and interact with other users, as well as create/join room to exchange messages with multiple users.

---

## Specs

> **NOTE**: On the client_side no actual information is stored. Client keeps track current user (user that is logged-in into the system) and users room. All information is stored on the server_side. 

---

## Usage

> Each function has its purpose and limitations. This document explains purpose of each function.

---

### 0. Connect to a server  	
**Purpose**: Let client connect to a server (establish connection with the server).

**Errors**:
- When client is already connected and attempts to connect again. 
---

#### 1. Disconnect from a server 	
**Purpose**: Let client disconnect from a server (close connection with the server).

**Errors**:
- When client isn't connected and attempts to disconnect. 
---

## 2. Create new user 	
**Purpose**: Let client create new user account on the system.

**Errors**:
- When client isn't connected to a server.
- When client is already signed-in into some user account.
- When client inputs invalid information for either username or passowrd.
- When user with a given username already exists on the system (server).
---

## 3. Login to existing account 
**Purpose**: Let client login to an existing user account.

**Errors**:
- When client isn't connected to a server.
- When client is already signed-in into some user account.
- When user with a given username doesn't exist on the system (server) OR username and password don't match up.
---

## 4. Logout
**Purpose**: Let user logout of current user account

**Errors**:
- When client isn't connected to a server.
- When client isn't logged-in into some user account.
---

## 5. Create new room
**Purpose**: Let user 

**Errors**:
---

## 6. List all rooms
**Purpose**:

**Errors**:
---

## 7. Join new room
**Purpose**:

**Errors**:
---

## 8. Leave room
**Purpose**:

**Errors**:
---

## 9. Switch room
**Purpose**:

**Errors**:
---

## 10. Send message to room
**Purpose**:

**Errors**:
---

## 11. View room messages
**Purpose**:

**Errors**:
---

## 12. View room members
**Purpose**:

**Errors**:
---

## 13. Send personal message
**Purpose**:

**Errors**:
---

## 14. View personal inbox
**Purpose**:

**Errors**:
---

## 15. Exit
**Purpose**:

**Errors**:
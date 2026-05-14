# Password Vault

A desktop password manager built with Python. Password Vault allows users to register an account, log in securely, and store, view, and delete website credentials through a local MongoDB database. Passwords are hashed using SHA-256 before being written to the database. The interface is built with customtkinter and runs as a fixed 1080x720 desktop window.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Database Schema](#database-schema)
- [Module Reference](#module-reference)
- [Security Notes](#security-notes)
- [Author](#author)
- [License](#license)

---

## Features

- User registration with name, email, and password; duplicate email detection on signup
- Password confirmation validation at registration
- Login authenticated against a SHA-256 hashed password stored in MongoDB
- Add website credentials (app name, email, password) to a per-user stored array
- Delete a stored credential by matching app name and email
- View all saved credentials in a scrollable popup window
- Logout returns to the signup screen without restarting the application

---

## Project Structure

```
Password-Vault/
|
|-- mainProject.py    # Self-contained application: signup, login, and home window in one file
|-- home.py           # Standalone home window module (split version)
|-- login.py          # Standalone login window module (split version)
|-- signUp.py         # Standalone signup window module (split version)
|-- README.md
```

`mainProject.py` is the primary entry point and contains the complete application. The other three files are modular versions of each screen split into separate files.

---

## Tech Stack

**Language**

- Python 3.x

**GUI**

- customtkinter — styled widget layer providing the main window, frames, entries, buttons, and labels
- tkinter.messagebox — used for error and success dialogs

**Database**

- MongoDB (local instance on `mongodb://localhost:27017/`)
- pymongo — Python driver for MongoDB; used for all read and write operations

**Security**

- hashlib — SHA-256 hashing applied to passwords before storage and before login comparison

**Typography**

- Rubik — used across all font sizes in the application (loaded as a system font)

---

## Prerequisites

- Python 3.8 or above
- MongoDB Community Server running locally on the default port (`27017`)
- pip

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Atharvakumkar/Password-Vault.git
cd Password-Vault
```

Install required Python packages:

```bash
pip install customtkinter pymongo
```

Ensure MongoDB is running before starting the application:

```bash
# macOS/Linux
mongod --dbpath /your/data/path

# Windows (if installed as a service)
net start MongoDB
```

---

## Running the Application

```bash
python mainProject.py
```

The application opens to the Sign Up screen. From there, users can register a new account or navigate to the Login screen if they already have one.

---

## Database Schema

The application uses the `passwordManager` database with a single collection: `userDetails`.

### Collection: `userDetails`

Each document represents one registered user. The `apps` array grows as the user adds credentials.

```json
{
  "name": "string",
  "email": "string",
  "password": "string (SHA-256 hex digest)",
  "apps": [
    {
      "appName": "string",
      "appEmail": "string",
      "appPassword": "string (stored as plaintext)"
    }
  ]
}
```

**Write operations:**

- Registration: `insert_one()` with an empty `apps` array
- Add credential: `update_one()` with `$push` on the `apps` array, matched by user email
- Delete credential: `update_one()` with `$pull` on the `apps` array, matched by `appName` and `appEmail`
- Read credentials: `find_one()` matched by user email, returns the full document including `apps`

---

## Module Reference

### `mainProject.py`

The application entry point. Contains three window functions and a hash utility.

**`hash_password(password)`**

Encodes the input string to bytes and returns its SHA-256 hex digest. Used at both registration and login.

**`main()`**

Builds and displays the Sign Up window (1080x720). Collects name, email, password, and confirm password. Validates that all fields are filled, passwords match, and the email is not already registered. On success, calls `insert_one()` to create the user document, then transitions to `login_window()`.

**`login_window()`**

Builds and displays the Login window. Hashes the entered password and calls `find_one()` to match against the stored hash. On success, sets the `current_user` global variable to the authenticated email and transitions to `create_home_window()`.

**`create_home_window()`**

Builds and displays the main dashboard window with three panels:

- **Add Password panel** — three entry fields (app name, email, password with masking). On submit, calls `update_one()` with `$push` to append a new entry to the user's `apps` array.
- **Delete Password panel** — two entry fields (app name and email). On delete, calls `update_one()` with `$pull` to remove the matching entry from the `apps` array.
- **View Passwords panel** — a button that opens a `CTkToplevel` window containing a `CTkScrollableFrame`. Each stored credential is rendered as a labelled card showing app name, email, and password in plaintext.
- **Logout button** — destroys the home window and calls `main()` to return to the signup screen.

### `signUp.py`, `login.py`, `home.py`

Split versions of each screen as standalone modules. Functionally equivalent to their counterparts in `mainProject.py`.

---

## Security Notes

- User account passwords are hashed with SHA-256 before being written to MongoDB. The plaintext password is never stored.
- Stored application passwords (the credentials the user is managing) are written to MongoDB as plaintext. If stronger security is required, consider encrypting these with a key derived from the user's master password before storage.
- The MongoDB connection does not use authentication. For any deployment beyond local development, enable MongoDB access control and use an authenticated connection string.

---

## Author

Atharva Kumkar

---

## License

This project is released under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, and to permit persons to whom the software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

DB = {
  "jadcode": {
    "username": "jadcode",
    "password": "123456"
  }
}

def getUser(userName: str):
    user = DB.get(userName)
    return user

def checkUserName(userName : str):
    for user in DB:
        if userName == user:
            return False
    return True

def addUser(userName, password):
    newUser = {
      "username": userName,
      "password": password
    }
    DB[userName] = newUser

    
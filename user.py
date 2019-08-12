class User(object):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return "User(id='%s')" % self.id






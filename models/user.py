class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.password
        }

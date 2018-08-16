class Authorinfo:
    def __init__(self, author, birthday, home, description):
        self.author = author
        self.birthday = birthday
        self.home = home
        self.description = description

    def get_name(self):
        return self.author

    def get_birthday(self):
        return self.birthday

    def get_home(self):
        return self.home

    def get_description(self):
        return self.description
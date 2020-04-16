
class User:
    def __init__(self, user, objs):
        self.user = user
        self.players = objs
        self.preferences = []

    def add_obj(self, new_obj):
        self.players += new_obj

    def add_preferences(self, preferences):
        """Trying an ordered list of preferences"""
        self.preferences = preferences

    def __repr__(self):
        return f'User: {self.user}\nPlayers: {[p.name for p in self.players]}'

    def __str__(self):
        return self.__repr__()


class Player:
    def __init__(self, name):
        self.name = name
        self.is_available = True
        self.preference = None

    def add_preference(self, preference):
        self.preference = preference

    def __repr__(self):
        return f'"{self.name}"'

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    en_1 = User('Jon-Ross', [])
    print(en_1)

from entites import *


class Algorithm:
    def __init__(self, users):
        self.users = users

    def run_algorithm(self):
        """Requires that self has a list of users, all of whom contain
        players and a list of preferences"""
        self.run_assertions()

        # TODO: Frontend for cycle
        # I think the cycle object should be passed to the frontend
        cycles = self.get_cycles()
        player_map = combine_dicts([c.dict for c in cycles])

        for owner in self.users:
            owner.players = [player_map[p] for p in owner.players]

        return self.users

    def update_available_players(self, cycles):
        """Change the availability of players who are in a cycle"""
        players = []
        for cycle in cycles:
            players.extend(cycle.values)

        for player in players:
            player.is_available = False

    def update_player_preference(self):
        """To be run before every iteration. Will switch each player
        to point at the highest rated pick for his owner"""
        available_players = self.get_available_players()

        for owner in self.users:
            preferred_player = self.get_owners_highest_preference(owner, available_players)

            for player in owner.players:
                player.add_preference(preferred_player)

    def get_available_players(self):
        players_nested = [u.players for u in self.users]
        return set( [p for s in players_nested for p in s if p.is_available] )

    def get_owners_highest_preference(self, owner, available_players):
        for p in owner.preferences:
            if p in available_players: return p
        assert 1 == 0, "Players available not on owner's list"

    def get_cycles(self):
        cycles = []

        while len(self.get_available_players()):
            self.update_player_preference()
            cycles.extend( self.detect_cycle() )
            self.update_available_players(cycles)

        return cycles

    def detect_cycle(self):
        """Returns a list of cycles"""
        cycles = []
        players = self.get_available_players()
        players_ = players.copy()

        # Self-referencing cycles
        for p in players_:
            if p.name == p.preference.name:
                players.remove(p)
                cycles.append( Cycle([p]) )

        # Multi-Player cycles
        for p in players:
            cycles.append( Cycle(self.detect_cycle_recursive(p, p.preference)) )

        # TODO: Fix bad way of De-Duping
        new_cycles, already_seen_sets = [], []

        for cycle in cycles:
            if set(cycle.values) not in already_seen_sets:
                new_cycles.append(cycle)
                already_seen_sets.append( set(cycle.values) )

        return [c for c in new_cycles if c.values != []]

    def detect_cycle_recursive(self, origin, current, history=[]):
        # If the current is the origin, we've found a cycle
        if origin == current:
            return history + [current]

        # If we've seen the current already, we're in a loop
        if current in history:
            return []

        # Otherwise, traverse down the cycle
        return self.detect_cycle_recursive(origin, current.preference, history+[current])

    def print_player_preferences(self):
        print('Player,Preference')
        for u in self.users:
            for p in u.players:
                print(f'{p.name},{p.preference}')

    def run_assertions(self):
        empty_users = "List of users is empty"
        empty_players = "List of players is empty"
        empty_preferences = "List of preferences is empty"
        differing_pref = "List of player preferences are not equal in length"

        assert len(self.users) > 0, empty_users
        assert sum([(len(u.players) == 0) for u in self.users]) == 0, empty_players
        assert len(self.users[0].preferences) > 0, empty_preferences
        assert all_same([len(u.preferences) for u in self.users]), differing_pref


class Cycle:
    def __init__(self, values):
        """A list of values, representing a cycle (in order)
        Ex: [A, B, C] represents A->B->C->A"""
        self.values = values

        value_len = len(values)
        if not value_len:
            self.dict = {}
        elif value_len == 1:
            self.dict = {values[0]: values[0]}
        else:
            self.dict = {values[i]: values[j] for i,j in zip(range(value_len), range(1, value_len))}
            self.dict[values[-1]] = values[0]

    def __repr__(self):
        return '->'.join([str(v) for v in self.values])

    def __str__(self):
        return self.__repr__()

###########
# HELPERS #
###########

def all_same(items):
    return all(x == items[0] for x in items)


def combine_dicts(list_of_dicts):
    rtrn_dict = {}

    for d in list_of_dicts:
        rtrn_dict.update(d)

    return rtrn_dict


if __name__ == '__main__':
    brady = Player("Tom Brady")
    gronk = Player("Rob Gronkowski")
    juju = Player("JuJu Smith-Schuster")
    kiki = Player("Kiki Coutee")
    kam = Player("Alvin Kamara")
    obj = Player("Odell Beckham Jr.")

    bill = User("Bill", [brady, gronk, juju])
    jr = User("Jon-Ross", [kiki, kam])
    sam = User("Sam", [obj])

    bill.add_preferences([kam, brady, obj, juju, gronk, kiki])
    jr.add_preferences([juju, obj, kam, gronk, brady, kiki])
    sam.add_preferences([juju, gronk, kam, brady, kiki, obj])

    al = Algorithm([bill, sam, jr])
    print(al.run_algorithm())



    brady = Player("Tom Brady")
    lamar = Player("Lamar Jackson")
    juju  = Player("JuJu Smith-Schuster")
    dede  = Player("Dede Westbrook")
    kam   = Player("Alvin Kamara")
    obj   = Player("Odell Beckham Jr.")

    bill = User("Bill", [brady, lamar, juju])
    jr = User("Jon-Ross", [dede, kam])
    sam = User("Sam", [obj])

    bill.add_preferences([obj, lamar, kam, juju, brady, dede])
    sam.add_preferences([kam, obj, brady, lamar, juju, dede])
    jr.add_preferences([juju, kam, lamar, brady, dede, obj])

    al = Algorithm([bill, sam, jr])
    print(al.run_algorithm())

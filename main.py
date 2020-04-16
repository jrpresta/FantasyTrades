from entites import *


if __name__ == '__main__':
    brady = Player("Tom Brady")
    lamar = Player("Lamar Jackson")
    juju  = Player("JuJu Smith-Schuster")
    dede  = Player("Dede Westbrook")
    kam   = Player("Alvin Kamara")
    obj   = Player("Odell Beckham Jr.")

    en_1 = User("Bill", [brady, lamar, juju])
    en_2 = User("JonRoss", [dede, kam])
    en_3 = User("Sam", [obj])

    en_1.add_preferences([kam, brady, obj, juju, lamar, dede])
    en_2.add_preferences([juju, obj, kam, lamar, brady, dede])
    en_3.add_preferences([juju, lamar, kam, brady, dede, obj])

    print(en_1)
    print(en_2)
    print(en_3)

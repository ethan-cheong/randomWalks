import random

def createPreferences(n, identity):
    pref_list = [i for i in range(n)]
    random.shuffle(pref_list) # randomize the order of people's preferences
    return pref_list

class Person:
    def __init__(self, identity, n):
        # Representation of a person
        self.identity = identity
        self.preferences = createPreferences(n, identity)

    def getIdentity(self):
        return self.identity

    def getPreferences(self):
        return self.preferences

class Man(Person):
    def __init__(self, identity, n):
        # Representation of a man
        super().__init__(identity, n)
        self.remaining_preferences = self.preferences

    def getRemainingPreferences(self):
        return self.remaining_preferences

    def getRejected(self):
        # By convention, the list of preferences will in increasing order.
        # This is because popping from the back of a list is faster than popping the front.
        self.remaining_preferences.pop()

class Woman(Person):
    def __init__(self, identity, n):
        # Representation of a woman
        super().__init__(identity, n)

    def chooseMan(self, man_list):
        # Given a list of men, pick the one whos identity is the rightmost entry 
        # on your list of identities.

# We're ready to implement the algorithm!
m1 = Man(4, 8)
print(m1.getRemainingPreferences())
m1.getRejected()
print(m1.getRemainingPreferences())

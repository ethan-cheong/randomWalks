import random
import collections # For improved time complexity

def createPreferences(identity, n):
    pref_list = [i for i in range(n)]
    random.shuffle(pref_list) # randomize the order of people's preferences
    pref_deque = collections.deque(pref_list)
    return pref_deque

class Person:
    def __init__(self, identity, n):
        # Representation of a person
        self.identity = identity
        self.preferences = createPreferences(identity, n)

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
        self.remaining_preferences.popleft() # time complexity O(1)

class Woman(Person):
    def __init__(self, identity, n):
        # Representation of a woman
        super().__init__(identity, n)
        self.man_list = []

    def getManList(self):
        print(self.man_list)

    def addToList(self, man):
        self.man_list.append(man)

    def chooseMan(self):
        # Given a list of men, pick the one whos identity is the leftmost entry
        # from your list of preferences.
        for preferred_man in self.preferences:
            if preferred_man in self.man_list:
                return preferred_man

    def getRejectedMen(self, chosen_man):
        self.man_list.remove(chosen_man)
        return self.man_list

    def clearManList(self):
        self.man_list = []

def traditionalMarriage(n):
    # Initialize arrays of men and women
    men = [Man(i, n) for i in range(n)]
    women = [Woman(i, n) for i in range(n)]

    nights = 0 # counter for number of nights

    for man in men:
        favourite_woman = man.getRemainingPreferences()[0]
        women[favourite_woman].addToList(man.getIdentity()) # add the men visiting them to their man_list

    for woman in women:
        preferred_man = woman.chooseMan()
        rejected_men = woman.getRejectedMen(preferred_man)
        for rejected_man in rejected_men:
            men[rejected_man].getRejected()

    for man in men:
        print(self.remaining_preferences())

traditionalMarriage(5)

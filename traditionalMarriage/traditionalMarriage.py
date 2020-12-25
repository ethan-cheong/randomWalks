import random
import collections # For improved time complexity
import copy

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

    def setPreferences(self, input):
        # Takes a list as input, allowing us to set custom preferences
        self.preferences = collections.deque(input)

class Man(Person):
    def __init__(self, identity, n):
        # Representation of a man
        super().__init__(identity, n)
        self.remaining_preferences = copy.copy(self.preferences)

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
        return self.man_list

    def addToList(self, man):
        self.man_list.append(man)

    def clearManList(self):
        # We need to reset the list of men visiting after every iteration
        self.man_list = []

    def chooseMan(self):
        # Given a list of men, pick the one whos identity is the leftmost entry
        # from your list of preferences.
        for preferred_man in self.preferences:
            if preferred_man in self.man_list:
                return preferred_man

    def getRejectedMen(self, chosen_man):
        # Get the men that the woman didn't choose each night so they can be rejected
        rejected_men = self.man_list[:]
        rejected_men.remove(chosen_man)
        return rejected_men

def initializePeople(n):
    # Initialize arrays of men and women
    men = [Man(i, n) for i in range(n)]
    women = [Woman(i, n) for i in range(n)]
    return (men,women)

def nightIteration(men_array, women_array):
    # Function for each night that passes
    for woman in women_array:
        woman.clearManList()

    for man in men_array:
        print("Man " + str(man.getIdentity()) + " has the preferences "
        + ','.join([str(i) for i in man.getRemainingPreferences()]) + ".")
        favourite_woman = man.getRemainingPreferences()[0]
        print("Man " + str(man.getIdentity()) + " is visiting woman "
        + str(favourite_woman) + "!")
        women_array[favourite_woman].addToList(man.getIdentity()) # add the men visiting them to their man_list

    for woman in women_array:
        if woman.getManList():
            print("Woman " + str(woman.getIdentity())
            + " is being visited by man/men "
            + ','.join([str(i) for i in woman.getManList()]) + "!")
        preferred_man = woman.chooseMan()
        if preferred_man is not None:
            print("Woman " + str(woman.getIdentity()) + " chose man "
            + str(preferred_man) + "!")
            rejected_men = woman.getRejectedMen(preferred_man)
            for rejected_man in rejected_men:
                men_array[rejected_man].getRejected()

def traditionalMarriage(men, women):
    # Implementation of the algorithm
    if len(men) != len(women):
        print("We need the same number of men and women!")
    nights = 0
    # Iterate until each woman has exactly one man visiting them.
    while True:
        if all(len(woman.getManList()) == 1 for woman in women):
            print("Matching took " + str(nights) + " nights!")
            break
        else:
            nightIteration(men, women)
            nights += 1
            print(str(nights) + " nights have passed!")

# The * here expands the tuple made by initializePairs() and sets them as arguments
traditionalMarriage(*initializePeople(5))

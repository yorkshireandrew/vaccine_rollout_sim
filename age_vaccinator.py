class AgeVaccinator(object):

    def __init__(self, people):
        self.candidates = people.copy()
        
    def candidate(self):
        # candidates are ordered by age decending so return first non dead candidate
        c = None
        dead = True
        while len(self.candidates) >= 1 and dead:
            c = self.candidates[0]
            dead = c.dead
            self.candidates.remove(c)
        return c
        
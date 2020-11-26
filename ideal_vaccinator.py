class IdealVaccinator(object):

    def __init__(self, people):
        self.candidates = people.copy()
        self.candidates = sorted(self.candidates, key=lambda x: x.prob, reverse=True)
        print("vaccination order")
        print(self.candidates[0].prob)
        print(self.candidates[-1].prob)
        
    def candidate(self):
        # candidates are ordered by age decending so return first non dead candidate
        c = None
        dead = True
        while len(self.candidates) >= 1 and dead:
            c = self.candidates[0]
            dead = c.dead
            self.candidates.remove(c)
        return c
        
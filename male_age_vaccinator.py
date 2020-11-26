class MaleAgeVaccinator(object):

    def __init__(self, people):
        self.candidates = people.copy()
        self.ordered = []
        age = None
        girls = []
        boys = []
        for c in self.candidates:
            if age == None:
                age = c.age
                # process                
                if c.male:
                    boys.append(c)
                else:
                    girls.append(c)             
            else:
                if c.age == age:
                    # process                
                    if c.male:
                        boys.append(c)
                    else:
                        girls.append(c)
                else:
                    # flush
                    self.ordered.extend(boys)
                    self.ordered.extend(girls)
                    boys = []
                    girls = []
                    # process
                    if c.male:
                        boys.append(c)
                    else:
                        girls.append(c)
        # flush
        self.ordered.extend(boys)
        self.ordered.extend(girls)
        # swap
        self.candidates = self.ordered
        
    def candidate(self):
        c = None
        dead = True
        while len(self.candidates) >= 1 and dead:
            c = self.candidates[0]
            dead = c.dead
            self.candidates.remove(c)
        return c
        
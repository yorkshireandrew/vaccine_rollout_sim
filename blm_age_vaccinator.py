class BLMAgeVaccinator(object):

    def __init__(self, people):
        self.candidates = people.copy()
        self.ordered = []
        age = None
        not_bame = []
        bame = []
        for c in self.candidates:
            if age == None:
                age = c.age
                # process                
                if c.bame:
                    bame.append(c)
                else:
                    not_bame.append(c)             
            else:
                if c.age == age:
                    # process                
                    if c.bame:
                        bame.append(c)
                    else:
                        not_bame.append(c)
                else:
                    # flush
                    self.ordered.extend(bame)
                    self.ordered.extend(not_bame)
                    bame = []
                    not_bame = []
                    # process
                    if c.bame:
                        bame.append(c)
                    else:
                        not_bame.append(c)
        # flush
        self.ordered.extend(bame)
        self.ordered.extend(not_bame)
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
        
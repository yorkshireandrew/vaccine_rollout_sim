class Person(object):

    def __init__(self):
        self.dead = False
        self.infection_phase = 0
        self.infected = False
        self.vaccinated = False
        self.vaccine_effective = False
        self.immune = False
        self.age = 0
        self.male = False
        self.adhd = False
        self.bipolar = False
        self.depressed = False
        self.schiz = False
        self.bame = False
        self.obese = False
        self.prob = 0 # Probability of dying - populated later
        
    def factor(self):
        f = 0.01 * pow(10, 4 * (self.age - 20)/80)
        if self.male:
            f = f * 1.59
        if self.adhd:
            f = f * 5.82
        if self.bipolar:
            f = f * 5.72
        if self.depressed:
            f = f * 7.64
        if self.schiz:
            f = f * 7.34
        if self.bame:
            f = f * 1.75 # middle of 1.62–1.88
        if self.obese:
            f = f * 1.92
        return f
         
        
if __name__ == '__main__':
    p = Person()
    p.age = 5
    print(str(p.factor()))
    p.age = 100
    print(str(p.factor()))   
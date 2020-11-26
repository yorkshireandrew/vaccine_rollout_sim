import random
from person import Person

class PopulationCreator(object):

    def __init__(self):
        #self.age_dist=[7431000, 7667000, 8604000, 8320000, 9269000, 7709000, 6824000, 4469000, 2414000, 476000] # population in decade groups
        self.age_dist=[3914000,3517000,3670000, \
        3997000,4297000,4307000,4126000,4194000, \
        4626000,4643000,4095000,3614000,3807000, \
        3017000,2463000,2006000,1496000,918000,476000] # population in 5 year groups
        
        self.male_prob = 0.5
        self.adhd_prob = 0.02
        self.depressed_prob = 0.03 # mind severe depression
        self.schiz_prob = 0.0145
        self.male_obese_prob = 0.02
        self.female_obese_prob = 0.04
        self.ifr = 0.01 # IFR - Infection Fatality Ratio (overall)
        
        
    def create_population(self, size):
        pop = sum(self.age_dist)
        people = []
        
        for x in range(18,-1,-1):
            age_seg = int(self.age_dist[x] * size / pop)
            for dood in range(0, age_seg):
                person = Person()
                person.age = x * 5 + 2 # could be more random here
                if random.random() < self.male_prob:
                    person.male = True
                if random.random() < self.adhd_prob:
                    person.adhd = True
                if random.random() < self.depressed_prob:
                    person.depressed = True
                if random.random() < self.schiz_prob:
                    person.schiz = True
                if person.male:
                    if random.random() < self.male_obese_prob:
                        person.obese = True
                else:
                    if random.random() < self.female_obese_prob:
                        person.obese = True
                people.append(person)
        return people

    def set_probability(self, people):
        tot = sum([person.factor() for person in people])
        av = tot / len(people)
        factor = self.ifr / av
        for person in people:
            person.prob = factor * person.factor()
        
    def contaminate(self, people, number):
        size = len(people) - 1
        day_number = int(number / 4)
        # Spread infection_phase
        for x in range(0, day_number):
            # pick healthy victim
            infected = True
            index = 0
            while infected:
                index = random.randint(0, size)
                infected = people[index].infected
            people[index].infected = True
            people[index].infection_phase = 0
            
        for x in range(0, day_number):
            # pick healthy victim
            infected = True
            index = 0
            while infected:
                index = random.randint(0, size)
                infected = people[index].infected
            people[index].infected = True
            people[index].infection_phase = 1            

        for x in range(0, day_number):
            # pick healthy victim
            infected = True
            index = 0
            while infected:
                index = random.randint(0, size)
                infected = people[index].infected
            people[index].infected = True
            people[index].infection_phase = 2
            
        for x in range(0, day_number):
            # pick healthy victim
            infected = True
            index = 0
            while infected:
                index = random.randint(0, size)
                infected = people[index].infected
            people[index].infected = True
            people[index].infection_phase = 3
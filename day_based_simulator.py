from age_vaccinator import AgeVaccinator
from male_age_vaccinator import MaleAgeVaccinator
from ideal_vaccinator import IdealVaccinator
from blm_age_vaccinator import BLMAgeVaccinator

from population_creator import PopulationCreator

import random

class Simulator(object):

    def __init__(self, vaccinator_type):
        self.r_natural                                  = 3.5
        self.r_partial_lockdown                         = 1.3
        self.r_lockdown                                 = 0.9
        
        self.vaccine_effectiveness                      = 0.9
        self.population_size                            = 60000000
        self.cycle_time_days                            = 5.6
        self.vaccination_rollout_days                   = 120
        self.into_lockdown_new_cases_per_day            = 20000
        self.outof_lockdown_new_cases_per_day           = 10000
#        self.into_lockdown_new_cases_per_day            = 14000 # If you want a full lockdown at 20000 positive tests per day
#        self.outof_lockdown_new_cases_per_day           = 7000
        self.into_partial_lockdown_new_cases_per_day    = 500
        self.outof_partial_lockdown_new_cases_per_day   = 100 # needs to be a small fraction of: into_partial_lockdown_new_cases_per_day 
        self.asymptomatic_factor                        = 0.4 # proportion that dont contribute to figures
        self.initial_infections                         = 65000 #65000 gives around 20000 cases per day after 3 cycles

        if vaccinator_type == 'AgeVaccinator':
            self.vaccinator = AgeVaccinator
        if vaccinator_type == 'MaleAgeVaccinator':
            self.vaccinator = MaleAgeVaccinator
        if vaccinator_type == 'IdealVaccinator':
            self.vaccinator = IdealVaccinator
        if vaccinator_type == 'BLMAgeVaccinator':
            self.vaccinator = BLMAgeVaccinator
        

        # Initialise
        self.lockdown = False
        self.partial_lockdown = True
        self.day = 0
        self.simulation_size = 100000
        self._people = None
        
        # Derive values    
        self.ratio = self.population_size / self.simulation_size

        asymtomatic_compensation = 1.0 + self.asymptomatic_factor
          
        self.initial = int(self.initial_infections / self.ratio)

        self.into_lockdown_threshold = self.into_lockdown_new_cases_per_day * asymtomatic_compensation # Work out true cases added per day
        self.into_lockdown_threshold = self.into_lockdown_threshold / self.r_partial_lockdown # Work out how many cases in a partial lockdown are needed to cause that many new cases per day
        self.into_lockdown_threshold = self.into_lockdown_threshold / self.ratio
        
        self.outof_lockdown_threshold = self.outof_lockdown_new_cases_per_day * asymtomatic_compensation
        self.outof_lockdown_threshold = self.outof_lockdown_threshold / self.r_lockdown
        self.outof_lockdown_threshold = self.outof_lockdown_threshold / self.ratio

        self.into_partial_lockdown_threshold = self.into_partial_lockdown_new_cases_per_day * asymtomatic_compensation
        self.into_partial_lockdown_threshold = self.into_partial_lockdown_threshold / self.r_natural # Work out how many cases with no measures are needed to cause that many cases per cycle
        self.into_partial_lockdown_threshold = self.into_partial_lockdown_threshold / self.ratio
        
        self.outof_partial_lockdown_threshold = self.outof_partial_lockdown_new_cases_per_day * asymtomatic_compensation
        self.outof_partial_lockdown_threshold = self.outof_partial_lockdown_threshold / self.r_partial_lockdown
        self.outof_partial_lockdown_threshold = self.outof_partial_lockdown_threshold / self.ratio

        vaccination_rollout_in_cycles = self.vaccination_rollout_days        
        self.vaccinations_per_day = int(self.simulation_size / vaccination_rollout_in_cycles)
        
    def carry_on(self, people):
        for p in people:
            if p.infected and not p.immune:
                return True
        return False
          
    def number_of_spreaders(self, people):
        case_list = [1 for p in people if p.infected and p.infection_phase >= 4 and p.infection_phase <= 8] # 5 days centered around 6 day point
        return len(case_list)
        
    def number_vaccinated(self, people):
        case_list = [1 for p in people if p.vaccinated]
        return len(case_list)
    
    def number_infected(self, people):
        case_list = [1 for p in people if p.infected]
        return len(case_list)
    
    def number_dead(self, people):
        case_list = [1 for p in people if p.dead]
        return len(case_list)

    def number_bame(self):
        case_list = [1 for p in self._people if p.bame]
        return len(case_list)

    def number_bame_dead(self):
        case_list = [1 for p in self._people if p.dead and p.bame]
        return len(case_list)  
        
    def get_people_to_infect(self, people):
        return [p for p in people if not p.dead and (p.infection_phase < 9 or p.infection_phase > 11)] # sick people dont go out
        
    def not_vaccinated(self, people):
        return [p for p in people if not p.vaccinated]
        
    def age_active_cases(self, people):
        case_list = [p for p in people if p.infected and not p.immune]
        for case in case_list:
            case.infection_phase += 1
            if case.infection_phase == 15:
                case.immune = True
                # The horrid bit
                if random.random() < case.prob:
                    case.dead = True
                
    def infect(self, people_to_infect, new_cases):
        # This doesn't mean they will get infected - but its likely if not vaccinated or heard immunity.
        size = len(people_to_infect) - 1
        for x in range(0, new_cases):
            index = random.randint(0, size)
            p = people_to_infect[index]
            if not p.immune and not p.infected and not p.vaccine_effective:
                p.infected = True
     
    def get_r(self):
        if self.lockdown:
            return self.r_lockdown
        if self.partial_lockdown:
            return self.r_partial_lockdown
        return self.r_natural

    def get_status(self):
        if self.lockdown:
            return '####'
        if self.partial_lockdown:
            return '##--'
        return '----'
        
    def boris(self, nac):
        if nac > self.into_lockdown_threshold:
            self.lockdown = True
            self.partial_lockdown = False
            
        if nac < self.outof_lockdown_threshold and nac >= self.into_partial_lockdown_threshold:
            self.lockdown = False
            self.partial_lockdown = True
            
        if nac < self.outof_partial_lockdown_threshold:
            self.lockdown = False
            self.partial_lockdown = False     
     
    def run(self):
        pc = PopulationCreator()
        people = pc.create_population(self.simulation_size)
        self._people = people
        print('created people')
        pc.set_probability(people)
        print('set probabilities')
        vaccinator = self.vaccinator(people)
        print('created vacinator')        
        pc.contaminate(people, self.initial)
        print('contaminated population')              
        while self.carry_on(people):
            # Time passes
            self.age_active_cases(people)
            self.day += 1
            
            # People get infected
            spreaders = self.number_of_spreaders(people)
            r = self.get_r()
            number_to_infect = int(spreaders * r * 0.2) # spreaders have 5 days to infect - this is just one of those days so divide by 5
            people_to_infect = self.get_people_to_infect(people)
            daily_cases = int(number_to_infect * self.ratio)
            self.infect(people_to_infect, number_to_infect)
            
            # People get vaccinated
            for x in range(0, self.vaccinations_per_day):
                candidate = vaccinator.candidate()
                if candidate:
                    candidate.vaccinated = True
                    if random.random() < self.vaccine_effectiveness:
                        candidate.vaccine_effective = True
             
            # The government reacts
            self.boris(spreaders * 0.2) # Todays Spreaders dictate todays number of new cases
            
            # We watch
            day_str = '{:{width}.{prec}f}'.format(self.day, width=6, prec=1)
            cases_str = '{:{width}.{prec}f}'.format(daily_cases, width=6, prec=0)
            infected_percentage =   '{:{width}.{prec}f}'.format(100.0 * self.number_infected(people) / self.simulation_size, width=6, prec=2)
            dead_percentage = '{:{width}.{prec}f}'.format(100.0 * self.number_dead(people) / self.simulation_size, width=8, prec=3)
            vaccinated_percentage = '{:{width}.{prec}f}'.format(100.0 * self.number_vaccinated(people) / self.simulation_size, width=6, prec=2)
            state = self.get_status()
            print(day_str + ' ' + state + ' ' + cases_str + ' ' + infected_percentage + ' ' + dead_percentage + ' ' + vaccinated_percentage)

        print('===========================================')
        print('===========================================')
        print('===========================================')
        print(str(self.ratio * self.number_dead(people)))
        print('===========================================')
        print('===========================================')
        print('===========================================')
        return self.ratio * self.number_dead(people)
            
if __name__ == '__main__':

    bame_numbers=[]
    bame_dead=[]
    improved_bame_numbers=[]
    improved_bame_dead=[]

    for x in range(0,28):      
        s = Simulator('AgeVaccinator')
        s.run()
        bame_numbers.append(s.number_bame())
        bame_dead.append(s.number_bame_dead())
        
        s = Simulator('BLMAgeVaccinator')
        s.run()
        improved_bame_numbers.append(s.number_bame())
        improved_bame_dead.append(s.number_bame_dead())

        print('--------------')
        print('bame_numbers')
        print(bame_numbers)
        print('bame_dead')
        print(bame_dead)
        print('improved_bame_numbers')
        print(improved_bame_numbers)
        print('improved_bame_dead')
        print(improved_bame_dead)
        print('--------------')
        print('sum bame_numbers')
        print(sum(bame_numbers))
        print('sum bame_dead')
        print(sum(bame_dead))
        print('sum improved_bame_numbers')
        print(sum(improved_bame_numbers))
        print('sum improved_bame_dead')
        print(sum(improved_bame_dead))
               
            
            
            
            
        
        
        
        
        
            
        
        

from random import randint

# global vars
poaching_amount = 0
yearly_population = list()
rhino_populations = list()
natural_death_population = 0
poaching_death_population = 0
predator_death_population = 0
age_death_population = 0
new_born_population = 0
population = 0

class Rhino:
    def __init__(self, gender, age):
        self.is_alive = True
        self.gender = gender
        self.age = age
        self.max_age = randint(35, 50)  # random between 35 to 50 years
        self.is_mature = True
        if gender == "Female":
            self.maturity_age = randint(3, 6)
        else:
            self.maturity_age = randint(6, 12)
        if self.age > self.maturity_age:
            self.is_mature = True  # used for determine if a female rhino can reproduce
        else:
            self.is_mature = False
        self.birth_counter = 0 # used for female reprduction cycle.  No use for male rhinos

    def annual_update(self):  # run through all every year
        global population, natural_death_population, age_death_population, \
            predator_death_population, new_born_population, rhino_populations
        if self.is_alive:
            if self.age < 1:  # Chance to die from predators
                random_number_one = randint(1, 100)
                random_number_two = randint(10, 20)
                if random_number_one < random_number_two:
                    natural_death_population += 1
                    predator_death_population += 1
                    population -= 1
                    self.is_alive = False
                    return
            self.age += 1
            if self.age >= self.maturity_age:
                self.is_mature = True
            else:
                self.is_mature = False
            if self.age >= self.max_age:  # If the rhino dies from old age
                natural_death_population += 1
                age_death_population += 1
                population -= 1
                self.is_alive = False
                return
            if self.age < 1:  # Chance to die from predators
                random_number_one = randint(1, 100)
                random_number_two = randint(10, 20)
                if random_number_one < random_number_two:
                    natural_death_population += 1
                    predator_death_population += 1
                    population -= 1
                    self.is_alive = False
                    return
                else:
                    pass
            if self.gender == "Female":  # Reproduction cycle
                if self.is_mature:
                    if self.birth_counter >= 0:
                        self.birth_counter += 1
                    if self.birth_counter >= randint(4, 5):
                        random_number_one = randint(1, 2)
                        if random_number_one == 1:
                            population += 1
                            rhino_populations.append(Rhino("Female", 0))
                        if random_number_one == 2:
                            population += 1
                            rhino_populations.append(Rhino("Male", 0))
                        self.birth_counter = 0
                        new_born_population += 1
        else:
            return




def simulation(poaching_amount, simulation_length, max_population, simulation_amount, start_population):
    global population, rhino_populations

    simulations_results = list()
    for t in range(0, simulation_amount):  # MULTIPLE RUN LOOP
        # RESET VARIABLES
        yearly_population = list()
        rhino_populations = list()
        natural_death_population = 0
        poaching_death_population = 0
        predator_death_population = 0
        age_death_population = 0
        new_born_population = 0
        population = 0

        for i in range(0, start_population):  # SET UP INITIAL POPULATION

            random_number = randint(1, 2)
            if random_number == 1:
                rh = Rhino("Female", randint(0, 45))
                if rh.is_mature:
                    rh.birth_counter = randint(0, 5)
                rhino_populations.append(rh)
            if random_number == 2:
                rhino_populations.append(Rhino("Male", randint(0, 45)))

        population = start_population

        yearly_population.append(population)

        # SIMULATION BEGINS HERE
        breakAll = False
        for yrs in range(0, simulation_length - 1):
            if breakAll:
                break

            # POACHING
            selected = 0
            kills = poaching_amount  # TEST POACHING LIST DURING VALIDATION
            if kills >= population:
                poaching_death_population += population
                population = 0
                yearly_population.append(population)
                print("Species has become extinct after", yrs, "years")
                breakAll = True
                break

            while selected < kills:
                index = randint(0, len(rhino_populations) - 1)
                if rhino_populations[index].is_alive:
                    rhino_populations[index].is_alive = False
                    population -= 1
                    poaching_death_population += 1
                    selected += 1

            for rh in rhino_populations:
                rh.annual_update()
                
            yearly_population.append(population)

            if population <= 0:
                population = 0
                print("Species has become extinct after", yrs + 1, "years.")
                breakAll = True
                break
            if population >= max_population:
                print("Species has reached max population of the simulation after", yrs + 1, "years.")
                breakAll = True
                break
        print("Sim", t + 1, yearly_population)

        simulations_results.append(yearly_population)


    # SORT DATA AND AVERAGE SIMULATIONS
    avg_population = list()
    s_list = list()
    e_list = list()
    s_averages = list()
    e_averages = list()
    for r in simulations_results: # SORT EXTINCT OR NOT EXTINCT
        if r[-1] == 0:
            r.remove(0)
            e_list.append(r)
        else:
            s_list.append(r)
        
    for yrs in range(0, simulation_length):

        total_population = 0
        count_1 = 0
        if len(s_list) > 0:
            for iter in range(0, len(s_list)):  # AVERAGE SURVIVING LISTS
                if yrs <= len(s_list[iter]) - 1:
                    count_1 += 1
                    total_population += s_list[iter][yrs]

            if count_1 > 0:
                s_averages.append(int(total_population / count_1 + 0.5))
        else:
            s_averages.append(-1)

        total_population = 0
        count_1 = 0
        if len(e_list) > 0:
            for iter in range(0, len(e_list)):  # AVERAGE EXTINCT LISTS
                if yrs <= len(e_list[iter]) - 1:
                    count_1 += 1
                    total_population += e_list[iter][yrs]

            if count_1 > 0:
                e_averages.append(int(total_population / count_1 + 0.5))
        else:
            e_averages.append(-1)


    print("Avg S:", s_averages)
    print("Avg E:", e_averages)
    print("\n")
    avg_population.append(e_averages)
    avg_population.append(s_averages)
    return(avg_population)


# Main Simulation Program
#    Run program: python ScienceFair_RhinoSim.py
#    Output to terminal and save the result to Science_Fair_Averages.csv

# Simulation setup values
simulation_length = 100  # number of years in a simulation
max_population = 100000  # simulation stop when reach this number, no longer endangered
start_population = 30000

# Number of run of the same simulation setup - variation from random
simulation_amount = 100  # number of simularion runs for each setting

#Write data to csv file
filename = "./Science_Fair_Averages.csv"
sims = list()
experiment_poaching_list = [0, 500, 1000, 1500, 1550, 1565, 1570, 1575, 1600, 2000, 2500]
with open (filename, 'a') as file_object:
    for p_amount in experiment_poaching_list:
        sims_res = simulation(p_amount, simulation_length, max_population, simulation_amount, start_population)
        file_object.write("poach amount (e)," + str(p_amount) + "," + str(sims_res[0]) + "\n")
        file_object.write("poach amount (s)," + str(p_amount) + "," + str(sims_res[1]) + "\n")

#END PROGRAM

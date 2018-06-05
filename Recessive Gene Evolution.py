# Recessisve Gene Evolution Simulation by Danny Pham
# A simple simulation on evolution. 
# Simulates generations of new species until the species goes extinct or
# the species completely evolves to have the recessive trait.
# Shows recessive traits are not necessarily less common than dominant traits.

import random

class Species:
    def __init__(self, species_name, starting_population, maximum_population, dominant_advantage):
        # species_name is the name of the tested species

        # starting_population is the population that the species starts with in the simulation
        
        # population is the current population of the species. 
        # In the constructor, it will simply be equal to starting_population

        # maximum_population is the highest number of animals the environment can sustain

        # dominant_advantage is a boolean that returns whether or not the dominant 
        # trait has an survival advantage in the environment

        self.starting_population = starting_population
        self.species_name = species_name
        self.maximum_population = maximum_population
        self.dominant_advantage = dominant_advantage
        
        # create a list of the starting population
        self.population = []
        for animal in range(0,starting_population): # use loop to add newly generated animals 1 by 1
            # give each animal its starting characteristics
            if random.randint(0,1) == 0:
                new_animal_allele_1 = True
            else:
                new_animal_allele_1 = False
            if random.randint(0,1) == 0:
                new_animal_allele_2 = True
            else:
                new_animal_allele_2 = False

            # add the newly created animal to the population 
            self.population.append(Animal(random.randint(0,1), new_animal_allele_1, new_animal_allele_2))

    def breed_new_generation(self):
        # breeds a new generation and adds them to the population
        males = []
        females = []

        # shuffle the population to ensure unique children are created each time
        random.shuffle(self.population)

        # start with loop to sort out males and females into 2 lists
        for animal in self.population:
            if animal.sex == 0:
                males.append(animal)
            else:
                females.append(animal)
            
        # cut extra animals if there are more of one gender than the other
        if len(males) > len(females):
            while len(males) > len(females):
                # keep deleting males until they are equal to females
                del males[0]
        if len(females) > len(males):
            while len(females) > len(males):
                # keep deleting females until they are equal to males
                del females[0]
            
        # breed the animals
        for couple_number in range(len(males)):
            new_baby = breed(males[couple_number], females[couple_number])
            self.population.append(new_baby)
    
    def cull_past_maximum(self):
        # kills animals randomly until population is under maximum_population

        random.shuffle(self.population)
        while len(self.population) > maximum_population:
            del self.population[0]

    def predator_attack(self, survival_percent, trait_advantage):
        # survival_percent is the base chance that any given animal will die from a predator attack
        # trait_advantage is how much a certain trait will increase the chance of survival

        new_population = []
        if self.dominant_advantage:
            # if the dominant phenotype has a survival advantage
            for animal in self.population:
                if animal.get_phenotype(): # if the animal has the dominant phenotype
                    if random.randint(1,100) < (survival_percent + trait_advantage):
                        # if the animal survives, add it to the new list
                        new_population.append(animal)
                else:
                    # if the animal has the recessive phenotype
                    if random.randint(1,100) < survival_percent:
                        # if the animal survives, add it to the new list
                        new_population.append(animal)
        else:
            # if the recessive phenotype has a survival advantage
            for animal in self.population:
                if animal.get_phenotype() == False: # if the animal has the recessive phenotype
                    if random.randint(1,100) < (survival_percent + trait_advantage):
                        # if the animal survives, add it to the new list
                        new_population.append(animal)
                else:
                    # if the animal has the dominant phenotype
                    if random.randint(1,100) < survival_percent:
                        # if the animal survives, add it to the new list
                        new_population.append(animal)
        
        # replace the old population list with the new one
        self.population = new_population

        # shuffle population to maintain randomness
        random.shuffle(self.population)
      
class Animal:
    def __init__(self, sex, allele_1, allele_2):
        # sex is an integer, 0 is male, 1 is female

        # allele_1 and allele_2 are booleans that return if the allele is dominant

        self.sex = sex
        self.allele_1 = allele_1
        self.allele_2 = allele_2

    def get_phenotype(self):
        # returns True if the phenotype is dominant, otherwise returns False
        return self.allele_1 or self.allele_2

    def meiosis(self):
        if random.randint(0,1):
            return self.allele_1
        else:
            return self.allele_2

def breed(male, female):
    # method that breeds two animals together, returns new baby animal
    # male is the first animal object and has a sex property of 0
    # female is the second animal object and has a sex property of 1

    # verify that this is a valid couple (male and female)
    if male.sex == 0 and female.sex == 1:
        # determine all of the baby's parameters
        new_baby_allele_1 = male.meiosis()
        new_baby_allele_2 = female.meiosis()
        baby_sex = random.randint(0,1)

        # return a new baby
        return Animal(baby_sex, new_baby_allele_1, new_baby_allele_2)
    else:
        # if not a valid couple, return null
        return None

# main program
instructions = '''
RECESSIVE GENE EVOLUTION SIMULATION by Danny Pham
Instructions: Enter the requested data.
Species Name: The name of the species being tested.
Initial Population: The population that the tested species starts with.
Maximum Population: The highest population that the environment can sustain.
Survival Chance: The chance that any given animal survives until the next generation (number from 1-100).
Trait bonus: How much more likely a holder of the tested recessive gene is to survive until the next generation than a holder of the dominant gene (number from 1-100).
'''
print(instructions)
species_name = input("Enter species name: ")
initial_population = int(input("Enter initial population: "))
maximum_population = int(input("Enter maximum population: "))
survival_chance = int(input("Enter predator survival chance: "))
trait_bonus = int(input("Enter trait bonus: "))

tested_species = Species(species_name, initial_population, maximum_population, False)

generation = 0
while True:
    # display generation number
    print("GENERATION " + str(generation))
    
    # check if species has gone extinct
    if len(tested_species.population) == 0:
        print ("The " + species_name + " have gone extinct.")
        break
    
    # calculate the amount of animals with the recessive phenotype
    homozygous_recessive_animals = 0
    for animal in tested_species.population:
        if animal.get_phenotype() == False:
            homozygous_recessive_animals = homozygous_recessive_animals + 1
    
    # calculate the % of animals with the recessive phenotype
    homozygous_recessive_animals_percent = homozygous_recessive_animals / len(tested_species.population)

    if homozygous_recessive_animals_percent == 1 and len(tested_species.population) > initial_population:
        print("The entire population has evolved to have the recessive phenotype.")
        break
    
    # print the info about the generation
    print ("There are " + str(len(tested_species.population)) + " total.") 
    print (str(homozygous_recessive_animals_percent*100) + " percent of " + species_name + " have the recessive trait.")

    # modify the population before going through another iteration
    tested_species.breed_new_generation()
    tested_species.predator_attack(survival_chance, trait_bonus)
    tested_species.cull_past_maximum()

    # iterate
    generation += 1

input()
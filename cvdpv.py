#! /usr/bin/env python3

import numpy as np
import random
from scipy.stats import poisson

class Individual:
    def __init__(self):
        self.state = 'S'  # Initial state is Susceptible
        self.days_infected = 0  # Track the number of days since the individual was exposed
        self.strain = None  # None, 'V' (vaccine), or 'W' (wild/virulent)
        self.transmissions = 0  # Track the number of transmissions by this individual

    def infect(self, strain):
        if self.state == 'S':
            self.state = 'E'
            self.strain = strain

    def step(self):
        if self.state == 'E':
            self.days_infected += 1
            if self.days_infected >= incubation_period:
                self.state = 'I'
        elif self.state == 'I':
            self.days_infected += 1
            if self.days_infected >= infectious_period + incubation_period:
                self.state = 'R'
                self.strain = None

# Parameters
population_size = 1000
beta = 0.3  # Transmission rate
incubation_period = 5  # Days from exposed to infectious
infectious_period = 10  # Days infectious
reversion_threshold = poisson.rvs(mu=3, size=population_size)  # Poisson-distributed reversion thresholds

# Create population
population = [Individual() for i in range(population_size)]

# Initial infection with vaccine strain
patient_zero = random.choice(population)
patient_zero.infect('V')

# Simulation loop
days = 160
for day in range(days):
    # Randomly pair individuals to interact, and possibly transmit the infection
    for individual in population:
        if individual.state == 'I':
            other = random.choice(population)
            if random.random() < beta:
                individual.transmissions += 1
                if individual.strain == 'V' and individual.transmissions >= reversion_threshold[population.index(individual)]:
                    individual.strain = 'W'  # Revert to virulent strain
                other.infect(individual.strain)

    # Update state of each individual
    for individual in population:
        individual.step()

    # (Optional) Collect and store data for analysis, visualization, etc.

# Now you can analyze the results, e.g., by counting the number of S, E, I, R individuals each day, and the prevalence of vaccine vs. virulent strains.

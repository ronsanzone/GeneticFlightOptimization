import math
import random


class GeneticFlightPath(object):
    def __init__(self, domain, costf):
        self.domain = domain
        self.costf = costf
        self.popsize = 200
        self.step = 1
        self.mutprob = 0.2
        self.elite = 0.5
        self.maxiter = 100

    # Mutation operation

    def mutate(self, vec):
        i = random.randint(0, len(self.domain) - 1)
        if random.random() < 0.5 and vec[i] > self.domain[i][0]:
            return vec[0:i] + [vec[i] - self.step] + vec[i + 1:]
        elif vec[i] < self.domain[i][1]:
            return vec[0:i] + [vec[i] + self.step] + vec[i + 1:]
        else:
            return vec

            # crossover operation

    def crossover(self, r1, r2):
        i = random.randint(1, len(self.domain) - 2)
        return r1[0:i] + r2[i:]

    def build_intial_pop(self):
        pop = []
        for i in range(self.popsize):
            vec = [random.randint(self.domain[i][0], self.domain[i][1])
                   for i in range(len(self.domain))]
            pop.append(vec)
        return pop

    def genetic_optimize(self):
        # Build the initial population
        pop = self.build_intial_pop()
        # How many winners from each generation
        topelite = int(self.elite * self.popsize)

        # main loop
        for j in range(self.maxiter):
            scores = [(self.costf(v), v) for v in pop]
            scores.sort()
            if j == self.maxiter - 1: pass
            ranked = [v for (s, v) in scores]

            pop = []

            # add mutated and bread forms of the winners
            while len(pop) < self.popsize:
                # introduce competitor
                if random.random() < self.mutprob:
                    c = [random.randint(self.domain[j][0], self.domain[j][1])
                         for j in range(len(self.domain))]
                    pop.append(c)
                # breed parents
                else:
                    p1 = random.randint(0, topelite)
                    p2 = random.randint(0, topelite)

                    c1 = self.crossover(ranked[p1], ranked[p2])
                    c2 = self.crossover(ranked[p2], ranked[p1])

                    if len(pop) == self.popsize - 1:
                        if random.random() < self.mutprob:
                            pop.append(self.mutate(c1))
                        else:
                            pop.append(c1)
                    else:
                        if random.random() < self.mutprob:
                            pop.append(self.mutate(c1))
                            pop.append(self.mutate(c2))
                        else:
                            pop.append(c1)
                            pop.append(c2)

            print "Best Cost:" + str(scores[0][0])
            print "Top winners in current population:"
            for x in range(5):
                print scores[x][1]
            print '---------------------------------------------'
        return scores[0][1]

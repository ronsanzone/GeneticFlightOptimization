import time
import random
import math


class FlightPathOptimization():
  def __init__(self, people, destination, filename):
    self.people = people
    self.destination = destination
    self.filename = filename
    self.flights = {}
    self.initializeOptimization()

  def initializeOptimization(self):
    for line in file(self.filename):
      origin,dest,depart,arrive,price=line.strip().split(',')
      self.flights.setdefault((origin,dest),[])

      #Add details to the possible self.flights
      self.flights[(origin,dest)].append((depart,arrive,int(price)))

  def getminutes(self, t):
    x=time.strptime(t, '%H%M')
    return x[3]*60+x[4]

  def printschedule(self, r):
    for d in range(len(r)/2):
      name=self.people[d][0]
      origin=self.people[d][1]
      out=self.flights[(origin, self.destination)][r[d*2]]
      ret=self.flights[(self.destination, origin)][r[d*2+1]]
      print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                    out[0],out[1],out[2],
                                                    ret[0],ret[1],ret[2])

  def schedulecost(self, sol):
    totalprice=0
    latestarrival=0
    earliestdep=24*60

    for d in range(len(sol)/2):
      #Get inbound and outbound self.flights
      origin=self.people[d][1]
      outbound=self.flights[(origin,self.destination)][int(sol[d*2])]
      returnf=self.flights[(self.destination, origin)][int(sol[d*2+1])]

      #Check for optimal depart times
      if (int(outbound[1]) > 1200 and int(outbound[1]) < 500):
        totalprice -= 50

      #prioritize cheaper tickets
      if outbound[2] < 100:
        totalprice+=outbound[2]-20
      else:
        totalprice+=outbound[2]

      if returnf[2] < 100:
        totalprice+=returnf[2]-20
      else:
        totalprice+=returnf[2]

      #Track the latest arrival and earliest departure
      if latestarrival<self.getminutes(outbound[1]): latestarrival=self.getminutes(outbound[1])
      if earliestdep>self.getminutes(returnf[0]): earliestdep=self.getminutes(returnf[0])


    #Every person must wait at the airport until the latest person arrives
    #They also must arrive at the same time and wait for their self.flights
    totalwait=0
    for d in range(len(sol)/2):
      origin=self.people[d][1]
      outbound=self.flights[(origin, self.destination)][int(sol[d*2])]
      returnf=self.flights[(self.destination, origin)][int(sol[d*2+1])]
      totalwait+=latestarrival-self.getminutes(outbound[1])
      totalwait+=self.getminutes(returnf[0])-earliestdep

    if latestarrival > earliestdep: totalprice+=50

    return totalprice+totalwait


class GeneticFlightPath():
  def __init__(self, domain, costf):
    self.domain = domain
    self.costf = costf
    self.popsize = 200
    self.step = 1
    self.mutprob = 0.2
    self.elite = 0.5
    self.maxiter = 100

    #Mutation operation
  def mutate(self, vec):
    i=random.randint(0,len(self.domain)-1)
    if random.random()<0.5 and vec[i]>self.domain[i][0]:
      return vec[0:i]+[vec[i]-self.step]+vec[i+1:]
    elif vec[i]<self.domain[i][1]:
      return vec[0:i]+[vec[i]+self.step]+vec[i+1:]
    else:
      return vec

    #crossover operation
  def crossover(self, r1,r2):
    i=random.randint(1,len(self.domain)-2)
    return r1[0:i]+r2[i:]

  def buildIntialPop(self):
    pop=[]
    for i in range(self.popsize):
      vec=[random.randint(self.domain[i][0],self.domain[i][1])
            for i in range(len(self.domain))]
      pop.append(vec)
    return pop

  def geneticoptimize(self):
    #Build the initial population
    pop = self.buildIntialPop()
    # How many winners from each generation
    topelite=int(self.elite*self.popsize)

    #main loop
    for j in range(self.maxiter):
      scores=[(self.costf(v), v) for v in pop]
      scores.sort()
      if j == self.maxiter-1: pass
      ranked=[v for (s,v) in scores]

      pop = []

      #add mutated and bread forms of the winners
      while len(pop)<self.popsize:
        #introduce competitor
        if random.random()<self.mutprob:
          c=[random.randint(self.domain[j][0],self.domain[j][1])
              for j in range(len(self.domain))]
          pop.append(c)
        #breed parents
        else:
          p1=random.randint(0,topelite)
          p2=random.randint(0,topelite)

          c1=self.crossover(ranked[p1],ranked[p2])
          c2=self.crossover(ranked[p2],ranked[p1])

          if len(pop) == self.popsize-1:
            if random.random()<self.mutprob:
              pop.append(self.mutate(c1))
            else:
              pop.append(c1)
          else:
            if random.random()<self.mutprob:
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

def main():
  people = [('Seymour','BOS'),
            ('Franny','RIC'),
            ('Zooey','CAK'),
            ('Walt','MIA'),
            ('Buddy','ORD'),
            ('Les','TYS')]

  #Destination New York
  destination = 'LGA'

  domain = [(0,8)]*(len(people)*2)

  flightPathOptimization  = FlightPathOptimization(people, destination, 'realflight.txt')
  geneticFlightPath = GeneticFlightPath(domain, flightPathOptimization.schedulecost)
  s = geneticFlightPath.geneticoptimize()

  print "\n\nBest Schedule Found Through Optimization"
  flightPathOptimization.printschedule(s)

if __name__ == '__main__':
  main()
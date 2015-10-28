import FlightPathOptimization
import GeneticFlightPath

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
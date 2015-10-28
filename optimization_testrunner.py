from FlightPathOptimization import FlightPathOptimization
from GeneticFlightPath import GeneticFlightPath


def main():
    people = [('Seymour', 'BOS'),
              ('Franny', 'RIC'),
              ('Zooey', 'CAK'),
              ('Walt', 'MIA'),
              ('Buddy', 'ORD'),
              ('Les', 'TYS')]

    # Destination New York
    destination = 'LGA'

    domain = [(0, 8)] * (len(people) * 2)

    flight_path_optimization = FlightPathOptimization(people, destination, 'realflight.txt')
    genetic_flight_path = GeneticFlightPath(domain, flight_path_optimization.schedule_cost)
    s = genetic_flight_path.genetic_optimize()

    print "\n\nBest Schedule Found Through Optimization"
    flight_path_optimization.print_schedule(s)


if __name__ == '__main__':
    main()

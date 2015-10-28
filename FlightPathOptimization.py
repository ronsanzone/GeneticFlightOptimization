import time


class FlightPathOptimization(object):
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


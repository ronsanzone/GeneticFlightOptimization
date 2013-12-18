##Script that can generate random flight data. Data conforms to the required format for
#the genetic algorithm

import time
import random

def generateRandomSchedules(filename, flightsPerAirport, locations, destination):
  paths = []
  for loc in locations:
    paths.append((loc, destination))
    paths.append((destination, loc))

  f = open(filename, 'w')
  for item in paths:
    for i in range(flightsPerAirport):
      f.write(generateRandomFlightInfo(item)+'\n')
  f.close()

def generateRandomFlightInfo(flightPath):
  departTime = generateRandomDepartTime()
  arrivalTime = generateRandomArrivalTime(departTime)
  return flightPath[0]+','+flightPath[1]+','+departTime+','+arrivalTime+','+generateRandomCost()

def generateRandomDepartTime():
  return str(convertHourFormat(random.randint(1,23)))+':'+str(convertMinuteFormat(random.randint(1,59)))

def convertHourFormat(hour):
  if hour > 23:
    hour = hour - 23
  if hour < 10:
    return '0'+str(hour)
  else:
    return hour

def convertMinuteFormat(minute):
  if minute < 10:
    return '0'+str(minute)
  else:
    return minute

def generateRandomArrivalTime(departTime):
  if departTime[0] == '0':
    departTimeHour = departTime[1]
  else:
    departTimeHour = departTime[:2]
  arivalTimeHour = convertHourFormat(random.randint(int(departTimeHour)+2,int(departTimeHour)+10))
  return str(arivalTimeHour)+':'+str(convertMinuteFormat(random.randint(0,59)))

def generateRandomCost():
  return str(random.randint(80,400))

def main():
  locations = ['BOS','RIC','CAK','MIA','ORD','TYS']
  generateRandomSchedules('randomflights.txt', 5, locations, 'LGA')

if __name__ == '__main__':
  main()
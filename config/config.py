from random import randint
class Config(object):
    price_range = [0, 10]  # say for a uniform distribution
    quantity_range = [100, 1500]  # again uniform?
    run_length = 250
    random_agent_creation = .05
    number_of_subregions = 9
    subregionx = 100
    subregiony = 100
    region = [] #Where there are 9 subregions, numbering from 0 to 8
    hubs = []
    for i in range(int(number_of_subregions/3)):
        for j in range(int(number_of_subregions/3)):
            region.append([[j*subregionx, (j+1)*subregionx],[(i)*subregiony, (i+1)*subregiony]])
            hubs.append([(j+1)*subregionx - .5*subregionx, (i+1)*subregiony - .5*subregiony])

 

    print(randint(*region[4][0])) #Test-run for x-coordinates in subregion i=4, such that region[i][0]
    print(randint(*region[4][1])) #Test-run for y-coordinates in subregion i=4, such that region[i][1]
    print([randint(*region[4][0]), randint(*region[4][1])]) #Test-run for location in subregion i = 4



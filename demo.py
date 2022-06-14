#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options



#def generate_routefile():
#    with open("demo2.rou.xml", "w") as routes:
#        print("""<routes>
#        <vType id="car" vClass="passenger" length="2" accel="3.5" decel="2.2" sigma="1.0" maxSpeed="10" color="1,0,0"/>
#        <vType id="car1" 
#        vClass="passenger" length="2" accel="3.5" decel="2.2" 
#        sigma="1.0" maxSpeed="10" color="0,255,255"/>
#            
#        <vType id="car2" 
#        vClass="passenger" length="2" accel="3.5" decel="2.2" 
#        sigma="1.0" maxSpeed="10" color="1,0,0"/>
#
#            <vType id="car3" 
#        vClass="passenger" length="2" accel="3.5" decel="2.2" 
#        sigma="1.0" maxSpeed="10" color="0,255,0"/>
#
#        <route id="route_0" edges="E0 E1 E2 E3 E4 -E0" />
#
#        <vehicle id="0" type="car" route="route_0" depart="0"/>
#        <vehicle id="1" type="car3" route="route_0" depart="3"/>
#        <vehicle id="2" type="car1" route="route_0" depart="6"/>
#        <vehicle id="3" type="car2" route="route_0" depart="9"/>
#        <vehicle id="4" type="car3" route="route_0" depart="12"/>        
#        </routes>""", file=routes)


#def generate_routefile():
#    N = 20
#    with open("demo2.rou.xml", "w") as routes:
#        print("""<routes>
#        
#        <vType id="car" vClass="passenger" length="2" accel="3.5" decel="2.2" sigma="1.0" maxSpeed="10" color="1,0,0"/>
#        
#        <route id="route_0" edges="E0 E1 E2 E3 E4 -E0" />
#        <vehicle id="0" type="car" route="route_0" depart="0"/>""", file=routes)
#
#        for i in range(N):
#            print('    <vehicle id="car_%i" type="car" route="route_0" depart="%i" />' file=routes)
#        print("</routes>", file=routes)

    

def run():
    step = 0 

    while step < 200:
        traci.simulationStep() 
        print(step)

        if step == 100:
            traci.vehicle.changeTarget("0", "-E0")
        step += 1

    traci.close()
    sys.stdout.flush()




# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    
    # first, generate the route file for this simulation
    generate_routefile()

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "demo.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    print("Starting SUMO - UTN project")
    run()

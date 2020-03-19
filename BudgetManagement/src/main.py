from scenario import Scenario
from simulation import Simulation, Budget, TransmissionModel

# Budget:
#   - 50 packets per day
#   - Each packet is 12 bytes
#   - A message takes up 6 bytes
#   - Messages are considered especially significant if they represent a change
#     of 300 or more
#   - Always send messages that exceed 300 by a factor of 2
#   - Sample three times per hour, or once every 20 minutes
scenario = Scenario('../scenarios/real1.csv')
budget = Budget(50, 1440, 12, 6)
model = TransmissionModel(300, 2)
simulation = Simulation(20, budget, model, scenario)
simulation.run()

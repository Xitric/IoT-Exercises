from scenario import Scenario
file = open('reception.csv', 'w')
stack = [(0.0, (0.0, 0.0)), (0.0, (0.0, 0.0))]


def transmit(time: float, value: float):
    file.write('{},{}\n'.format(time, value))


def push_to_stack(change: float, value: (float, float)):
    for i, v in enumerate(stack):
        if change > v[0]:
            if i == 0:
                stack[1] = stack[0]
            stack[i] = (change, value)
            return


# Budget
#   Sample every minute
#   Transmit a message every 30 minutes
#   We can batch two samples in every message (2 bytes for time,
#   4 bytes for value, 12 bytes per message)
simulation_time = 0
simulation_end = 1440
simulation_step = 1
transmit_delay = 10
transmit_countdown = transmit_delay
scenario = Scenario('scenarios/synth3.csv')
previous_value = 0

while simulation_time <= simulation_end:
    sample = scenario.sample(simulation_time)
    difference = sample - previous_value
    push_to_stack(difference, (simulation_time, sample))
    previous_value = sample

    simulation_time += simulation_step
    transmit_countdown -= simulation_step

    if transmit_countdown <= 0:
        if stack[0][0] != 0:
            transmit(stack[0][1][0], stack[0][1][1])
        if stack[1][0] != 0:
            transmit(stack[1][1][0], stack[1][1][1])
        transmit_countdown = transmit_delay
        stack = [(0.0, (0.0, 0.0)), (0.0, (0.0, 0.0))]

file.close()

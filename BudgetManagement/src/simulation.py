from typing import TextIO

from scenario import Scenario
from message_buffer import MessageBuffer
import subprocess


# To keep track of remaining transmission budget
class Budget:

    def __init__(self, daily_transmits: int, replenish_delay: int, packet_size: int, message_size: int):
        self.remaining_transmits = daily_transmits
        self.period_length = replenish_delay
        self.packet_capacity = packet_size // message_size  # Floor division
        self.recommended_transmit_interval = replenish_delay // daily_transmits

    def use_transmit(self):
        if self.remaining_transmits == 0:
            raise RuntimeError('no remaining transmits')
        self.remaining_transmits -= 1

    def has_exceeded_transmit_interval(self, simulation_time: float):
        if self.remaining_transmits == 0:
            return False

        remaining_time = self.period_length - simulation_time
        return remaining_time // self.remaining_transmits < self.recommended_transmit_interval


# To evaluate if it is worth sending a message
class TransmissionModel:

    def __init__(self, significant_delta: float, early_transmit_factor: float):
        self.significant_delta = significant_delta
        self.early_transmit_factor = early_transmit_factor

    def should_transmit(self, simulation_time: float, buffer: MessageBuffer, budget: Budget) -> bool:
        # Never transmit an empty buffer
        if len(buffer.stack) == 0:
            return False

        if len(buffer.stack) == buffer.size:
            if budget.has_exceeded_transmit_interval(simulation_time):
                # Transmit if we have filled the buffer and it is time to transmit
                return True
            else:
                # Transmit early only if all messages are significant
                return buffer.stack[buffer.size - 1].delta > self.significant_delta
        else:
            # Transmit a partial buffer only if the message is very significant
            return buffer.stack[0].delta > self.significant_delta * self.early_transmit_factor


# A simulation using adaptive sampling and batch transmissions
class Simulation:

    def __init__(self, step: int, budget: Budget, transmission_model: TransmissionModel, scenario: Scenario):
        self.simulation_time = 0
        self.previous_value = 0
        self.simulation_end = budget.period_length
        self.simulation_step = step
        self.budget = budget
        self.model = transmission_model
        self.scenario = scenario
        self.buffer = MessageBuffer(budget.packet_capacity)

    # Outer run method with house-keeping
    def run(self):
        with self.__init_output() as output:
            self.__run(output)
            self.__render()

    # Main simulation loop
    def __run(self, output: TextIO):
        while self.simulation_time <= self.simulation_end:
            self.__sample()
            self.__progress()
            if self.model.should_transmit(self.simulation_time, self.buffer, self.budget):
                self.__transmit(output)

    # Sample value and save in buffer
    def __sample(self):
        sample = self.scenario.sample(self.simulation_time)
        delta = abs(sample - self.previous_value)
        self.buffer.push_message(self.simulation_time, sample, delta)
        self.previous_value = sample

    def __progress(self):
        self.simulation_time += self.simulation_step

    def __transmit(self, output: TextIO):
        self.budget.use_transmit()
        for message in self.buffer.extract_messages():
            output.write('{},{}\n'.format(message.time, message.value))
        output.flush()

    @staticmethod
    def __init_output():
        output = open('../scenarios/reception.csv', 'w')
        output.write('# time, value\n')
        return output

    def __render(self):
        subprocess.call('gnuplot reception.gp', cwd='../scenarios')
        print('Completed with {} remaining transmits in budget'.format(self.budget.remaining_transmits))
        print('Used buffer size {}'.format(self.buffer.size))

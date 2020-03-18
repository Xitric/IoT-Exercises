class Scenario:

    def __init__(self, scenario_file: str):
        self.scenario = []

        with open(scenario_file, 'r') as file:
            file.readline()  # Skip the first line
            for line in file:
                elements = line.split(',')
                time = int(elements[0])
                value = float(elements[1])
                self.scenario.append((time, value))
                self.maxTime = time

    def __to_scenario_time(self, simulation_time: float):
        return simulation_time / 1440 * self.maxTime

    def __find_time_index(self, scenario_time: float):
        # Perform a binary search
        left = mid = 0
        right = len(self.scenario) - 1
        while left <= right:
            mid = (left + right) // 2  # Floor division
            if self.scenario[mid][0] == scenario_time:
                break
            elif self.scenario[mid][0] < scenario_time:
                left = mid + 1
            else:
                right = mid - 1

        # Where the element should have been
        return mid

    def sample(self, simulation_time: float):
        scenario_time = self.__to_scenario_time(simulation_time)
        index = self.__find_time_index(scenario_time)
        if self.scenario[index][0] == scenario_time:
            return self.scenario[index][1]
        elif index == 0:
            return self.scenario[index][1] * scenario_time / scenario_time
        else:
            val_diff = self.scenario[index][1] - self.scenario[index - 1][1]
            time_diff = self.scenario[index][0] - self.scenario[index - 1][0]
            time_offset = scenario_time - self.scenario[index - 1][0]
            return val_diff * time_offset / time_diff + self.scenario[index - 1][1]

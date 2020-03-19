from unittest import TestCase
from scenario import Scenario


class TestScenarioZeroOrigin(TestCase):
    def setUp(self):
        self.scenario = Scenario('testScenarioZeroOrigin.csv')

    def test_zero(self):  # 0
        self.assertAlmostEqual(self.scenario.sample(0), 2)

    def test_one_half(self):  # 0
        self.assertAlmostEqual(self.scenario.sample(72), 2.5)

    def test_one(self):  # 144
        self.assertAlmostEqual(self.scenario.sample(144), 3)

    def test_two(self):  # 288
        self.assertAlmostEqual(self.scenario.sample(288), 4)

    def test_three(self):  # 432
        self.assertAlmostEqual(self.scenario.sample(432), 5)

    def test_five(self):  # 720
        self.assertAlmostEqual(self.scenario.sample(720), 7)

    def test_eight(self):  # 1152
        self.assertAlmostEqual(self.scenario.sample(1152), 9)

    def test_nine(self):  # 1296
        self.assertAlmostEqual(self.scenario.sample(1296), 9.5)

    def test_ten(self):  # 1440
        self.assertAlmostEqual(self.scenario.sample(1440), 10)


class TestSampleNonzeroOrigin(TestCase):
    def setUp(self):
        self.scenario = Scenario('testScenarioNonzeroOrigin.csv')

    def test_zero(self):  # 0
        self.assertAlmostEqual(self.scenario.sample(0), 0)

    def test_one(self):  # 360
        self.assertAlmostEqual(self.scenario.sample(360), 5)

    def test_two(self):  # 720
        self.assertAlmostEqual(self.scenario.sample(720), 10)

    def test_three(self):  # 1080
        self.assertAlmostEqual(self.scenario.sample(1080), 12)

    def test_four(self):  # 1440
        self.assertAlmostEqual(self.scenario.sample(1440), 14)


class TestSampleRoundingErrors(TestCase):
    def setUp(self):
        self.scenario = Scenario('testScenarioRoundingErrors.csv')

    def test_zero(self):
        self.assertAlmostEqual(self.scenario.sample(0), 0.501526, places=3)

    def test_one_half(self):
        self.assertAlmostEqual(self.scenario.sample(0.5), 0.6885285, places=3)

    def test_one(self):
        self.assertAlmostEqual(self.scenario.sample(1), 0.875531, places=3)

    def test_end(self):
        self.assertAlmostEqual(self.scenario.sample(1440), 0.766185, places=3)

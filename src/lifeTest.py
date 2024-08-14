import unittest
from life import next_state

class TestNextStateMethod(unittest.TestCase):

    # Rule 1: Any live cell with 0 or 1 live neighbors becomes dead
    def test_rule1(self):
        initState1 = [
            [0,0,0],
            [0,1,0],
            [0,0,0]
        ]

        initState2 = [
            [0,1,0],
            [0,1,0],
            [0,0,0]
        ]

        expectedNextState = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]

        self.assertListEqual(next_state(initState1), expectedNextState)
        self.assertListEqual(next_state(initState2), expectedNextState)

    # Rule 2: Any live cell with 2 or 3 live neighbors stays alive
    def test_rule2(self):
        initState1 = [
            [0,0,0],
            [1,1,1],
            [0,0,0]
        ]

        expectedNextState = [
            [0,1,0],
            [0,1,0],
            [0,1,0]
        ]

        self.assertListEqual(next_state(initState1), expectedNextState)

    # Rule 3: Any live cell with more than 3 live neighbors becomes dead
    def test_rule3(self):
        initState1 = [
            [0,1,0],
            [1,1,1],
            [0,1,0]
        ]

        expectedNextState = [
            [1,1,1],
            [1,0,1],
            [1,1,1]
        ]

        self.assertListEqual(next_state(initState1), expectedNextState)

    # Rule 4: Any dead cell with exactly 3 live neighbors becomes alive
    def test_rule4(self):
        initState1 = [
            [0,1,0],
            [1,0,1],
            [0,0,0]
        ]

        expectedNextState = [
            [0,1,0],
            [0,1,0],
            [0,0,0]
        ]

        self.assertListEqual(next_state(initState1), expectedNextState)

    # Tests cases where live cells are on the edges
    def test_edges(self):
        initState1 = [
            [1,0,0],
            [0,0,0],
            [0,0,0]
        ]

        initState2 = [
            [1,1,0],
            [0,0,0],
            [0,0,0]
        ]

        initState3 = [
            [1,1,1],
            [0,0,0],
            [0,0,0]
        ]

        initState4 = [
            [1,1,1],
            [1,0,0],
            [0,0,0]
        ]

        initState5 = [
            [1,1,1],
            [1,1,0],
            [0,0,0]
        ]

        initState6 = [
            [1,1,1],
            [1,1,1],
            [0,0,0]
        ]

        expectedNextState1 = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]

        expectedNextState2 = [
            [0,1,0],
            [0,1,0],
            [0,0,0]
        ]

        expectedNextState3 = [
            [1,1,0],
            [1,0,0],
            [0,0,0]
        ]

        expectedNextState4 = [
            [1,0,1],
            [1,0,1],
            [0,0,0]
        ]

        expectedNextState5 = [
            [1,0,1],
            [1,0,1],
            [0,1,0]
        ]

        self.assertListEqual(next_state(initState1), expectedNextState1)
        self.assertListEqual(next_state(initState2), expectedNextState1)
        self.assertListEqual(next_state(initState3), expectedNextState2)
        self.assertListEqual(next_state(initState4), expectedNextState3)
        self.assertListEqual(next_state(initState5), expectedNextState4)
        self.assertListEqual(next_state(initState6), expectedNextState5)

if __name__ == '__main__':
    unittest.main()

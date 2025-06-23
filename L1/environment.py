import random


class Environment:

    def __init__(self):
        self.qT = self.create_qT()
    
    def create_qT(self):
        qT = {}
        for row in range(0,5):
            for col in range(0,5):
                key = (row, col)
                qT[key] = [random.randint(2000, 4000) for _ in range(4)]
        
                if row == 0 and col == 0:
                    qT[key][2] = 0
                    qT[key][3] = 0
                elif row == 0 and col == 4:
                    qT[key][0] = 0
                    qT[key][3] = 0
                elif row == 4 and col == 0:
                    qT[key][1] = 0
                    qT[key][2] = 0
                elif row == 4 and col == 4:
                    qT[key][0] = 0
                    qT[key][1] = 0
                    qT[key][2] = 100
                    qT[key][3] = 100
                elif row == 0:
                    qT[key][3] = 0
                elif row == 4:
                    qT[key][1] = 0
                elif col == 0:
                    qT[key][2] = 0
                elif col == 4:
                    qT[key][0] = 0

        return qT

# DSA for Biology - Assignment 2 
# Template for question  - Conway's Game of Life

class Simulate_Conways_Game_of_Life():
    def __init__(self, MyMatrix):
        self.matrix = MyMatrix
        """ Add your code here """
        self.neighbors = [[0 for i in range(100)] for j in range(100)]

    """ Add your functions here """
    
    def neighborcount(self, grid, row, col):
        count = 0
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if i == 0 and j == 0:
                        continue
                    elif grid[row + i][col + j] == 1:
                        count += 1
                except: continue
        return count
    
    def updatematrix(self, grid, row, col):
        curr = grid[row][col]
        count = self.neighbors[row][col]
        
        if curr == 1:
            if (count == 2 or count == 3):
                return 1
            else:
                return 0
        else:
            if count == 3:
                return 1
            else:
                return curr

    def simulate_one_step(self):
        """ Add your code """
        grid = self.matrix.copy()
        # First calculate the neighbor count for each cell
        for i in range(100):
            for j in range(100):
                self.neighbors[i][j] = self.neighborcount(grid, i, j)
        
        # Then we update the value of each cell
        for i in range(100):
            for j in range(100):
                grid[i][j] = self.updatematrix(grid, i, j)
        
        self.matrix = grid

    def final_output(self):
        """
        Return the output of the 39th step 
        """
        for i in range(39):
            self.simulate_one_step()

        return self.matrix


Glider = [[0 for i in range(100)] for j in range(100)]
Glider[1][2] = 1
Glider[2][3] = 1
Glider[3][1:4] = [1,1,1]

# 0 - Dead cell, 1 - Live cell
Game1 = Simulate_Conways_Game_of_Life(Glider)
Step_39 = Game1.final_output()

from matplotlib.pyplot import matshow

matshow(Step_39)
import random
import copy
import glob
import time
import numpy as np
from math import sqrt
from functools import reduce
from memory_profiler import profile

class ShikakuPuzzle():
  def __init__(self, array):
    self.__matrix__ = copy.deepcopy(array)
    self.__locationData__ = []
    self.__locationDataFactor__ = []
    length_array = len(array)
    self.__partitions__ = []
    self.__population__ = []
    self.__puzzle__ = [length_array * [""] for i in range(length_array)]
    for n_row, row in enumerate(array):
      for n_col, cell in enumerate(row):
        if cell == 0:
          self.__puzzle__[n_row][n_col] = -1
        else:
          self.__locationData__.append((n_row, n_col, cell))
          self.__partitions__.append("")
          self.__puzzle__[n_row][n_col] = len(self.__locationData__) - 1
    self.__backup__ = copy.deepcopy(self.__puzzle__)
    print("__puzzle__ Before Preprocess")
    for row in self.__puzzle__:
      print(row)
    self.__factors()
    self.__generate_partitions()
    self.__preprocess()
    self.__gen_population()

  
  def showInfo(self):
    print("__locationData__", self.__locationData__)
    print("__locationDataFactor__", self.__locationDataFactor__)
    print("__puzzle__ after Preprocess")
    for row in self.__puzzle__:
      print(row)
    print("__partitions__", self.__partitions__)
    print("fitness", self.fitness)

  def __factors(self):
    for data in self.__locationData__:
      value = data[2]
      current = []
      bound = round(sqrt(value))+1
      for i in range(1, int(bound)):
        if value % i == 0:
          if i == value//i:
            current.insert(0, i)
          else:
            current.insert(0, i)
            current.insert(0, value//i)
      self.__locationDataFactor__.append(current)


  def __generate_partitions(self):
    for n_row, row in enumerate(self.__puzzle__):
      for n_col, cell in enumerate(row):
        if cell == -1: continue
    row = col = len(self.__puzzle__) - 1
    for idx, (r_idx, c_idx, value) in enumerate(self.__locationData__):
      list_rect = []
      for width in self.__locationDataFactor__[idx]:
        # Get valued squared and its factor
        height = value // width
        for i in range(r_idx-width+1, r_idx+1):
          if i < 0 or i+width-1 > col: continue
          for j in range(c_idx-height+1,c_idx+1):
            if j < 0 or j+height-1 > row: continue
            is_valid = True
            for x in range(i,i+width):
              for y in range(j,j+height):
                if self.__puzzle__[x][y] != -1 and self.__backup__[x][y] != idx:
                  is_valid = False
            if is_valid:
              list_rect.append((i,j,width,height,idx))
      self.__partitions__[idx] = list_rect

  def __draw_partition(self, partition):
    (row,col,width,height,idx) = partition
    for i in range(row, row+width):
      for j in range(col, col+height):
        self.__puzzle__[i][j] = idx

  def __preprocess(self):
    while True:
      for idx, part in enumerate(self.__partitions__):
        if len(part) == 1:
          self.__draw_partition(part[0])
          self.__partitions__[idx] = []

      self.__generate_partitions()
      should_break = True
      for part in self.__partitions__:
        if len(part) == 1: should_break = False
      if should_break: break

  @property
  def fitness(self):
    n = len(self.__puzzle__)
    sum = 0
    for row in self.__puzzle__:
      for cell in row:
        if cell != -1: sum += 1
    return sum / n**2

  def fitness_of(self, puzzle):
    n = len(puzzle)
    sum = 0
    for row in puzzle:
      for cell in row:
        if cell != -1: sum += 1
    return sum / n**2

  def __gen_population(self):
    n_pop = 20
    for i in range(n_pop):
      chromos = []
      for part in self.__partitions__:
        if len(part) > 0:
          chromos.append(str(random.randrange(0,len(part))))
        else: chromos.append("-")
      self.__population__.append(("".join(chromos),0))
  
  def __run(self, chromos):
    puzzle = copy.deepcopy(self.__puzzle__)
    for idx, x in enumerate(chromos[0]):
      if x == "-": continue
      part = self.__partitions__[idx][int(x)]
      (row,col,width,height,idx) = part
      for i in range(row, row+width):
        for j in range(col, col+height):
          puzzle[i][j] = idx
    fn = self.fitness_of(puzzle)
    if fn == 1.0:
      print("Answer:", chromos[0])
      for row in puzzle:
        print(row)
      raise ValueError(chromos[0])
    return [chromos[0], fn]
      

  def __tournament_selection(self):
    sum = 0
    for pop in self.__population__:
      sum += pop[1]
    new_pop = []
    for _ in range(len(self.__population__)):
      point = random.uniform(0, sum)
      cum_sum = 0
      for part in self.__population__:
        cum_sum += part[1]
        if cum_sum > point:
          new_pop.append(part)
          break
    self.__population__ = new_pop

  def __crossover(self):
    if random.randrange(10) > 6:
      new_pop = []
      random.shuffle(self.__population__)
      for i in range(len(self.__population__)//2):
        crossover_point = random.randrange(len(self.__population__[i]))
        crossover_with = random.randrange(len(self.__population__))
        c1 = self.__population__[i][0][:crossover_point] + self.__population__[crossover_with][0][crossover_point:]
        c2 = self.__population__[crossover_with][0][:crossover_point] + self.__population__[i][0][crossover_point:]
        c1, c2 = (self.__run([c1, 0]), self.__run([c2, 0]))
        if c1[1] >= self.__population__[i][1] and c2[1] >= self.__population__[crossover_with][1]:
          self.__population__[i] = c1
          self.__population__[crossover_with] = c2
    # print("After CROSSOVER", self.__population__)

  def __mutation(self):
    for i in range(len(self.__population__)):
      if random.randrange(10) > 2: 
        mutation_point = random.randrange(len(self.__population__[i][0]))
        if self.__population__[i][0][mutation_point] == "-": continue
        new_muta = random.randrange(len(self.__partitions__[mutation_point]))
        c = self.__population__[i][0][:mutation_point] + str(new_muta) + self.__population__[i][0][mutation_point+1:]
        c = self.__run([c, 0])
        if c[1] >= self.__population__[i][1]:
          self.__population__[i] = c
    # print("After MUTATION ", self.__population__)

  def __check_solve_puzzle(self):
    for p in self.__population__:
      if p[1] == 1.0:
        return p
    return False

  def execute(self):
    try:
      for idx, chromos in enumerate(self.__population__):
        rt = self.__run(chromos)
        self.__population__[idx] = rt
      if self.__check_solve_puzzle(): return self.__check_solve_puzzle()
      while True:
        self.__tournament_selection()
        self.__crossover()
        if self.__check_solve_puzzle(): return self.__check_solve_puzzle()
        self.__mutation()
        if self.__check_solve_puzzle(): return self.__check_solve_puzzle()
        # print(self.__population__)
    except Exception:
      pass

# @profile
def solve():
    

  startTime = time.time()

  # shikaku = ShikakuPuzzle([
  #   [0,6,0,0,0,3,0],
  #   [0,0,0,0,0,2,0],
  #   [0,2,0,3,0,2,0],
  #   [2,0,0,0,5,0,0],
  #   [0,0,6,0,0,0,4],
  #   [0,0,0,0,0,0,7],
  #   [0,3,0,0,4,0,0]
  # ])


  shikaku = ShikakuPuzzle([
    [0,0,0,4,2,2,2],
    [0,2,2,0,0,0,0],
    [0,0,7,0,0,0,0],
    [0,4,0,0,0,2,0],
    [2,0,0,0,3,0,0],
    [0,4,4,0,0,0,0],
    [0,0,0,2,0,3,4]
  ])

  # shikaku = ShikakuPuzzle([
  #   [2,0,3,0,0],
  #   [3,0,0,0,0],
  #   [0,0,4,4,0],
  #   [0,0,2,2,0],
  #   [0,3,0,2,0]
  # ])

  shikaku.showInfo()
  shikaku.execute()
  endTime = time.time()
  print(f"Solution Found in {endTime - startTime} seconds")

solve()
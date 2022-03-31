import random
import copy
import time
from memory_profiler import profile

class SudokuPuzzles():
  def __init__(self, array):
    self.__matrix__ = copy.deepcopy(array)
    self.__backup__ = copy.deepcopy(array)
    print("Before Preprocess:")
    for row in self.__matrix__ :
      print(row)
    self.preprocess()
    print("After Preprocess:")
    for row in self.__matrix__:
      print(row)

  def preprocess(self):
    process = 'abcdef'
    while True:
      prev_fitness = self.fitness()
      for i in process:
        exec(f"self.{i}()")
      new_fitness = self.fitness()
      if new_fitness == prev_fitness:
        break
    self.__backup__ = copy.deepcopy(self.__matrix__)
  
  def reset(self):
    self.__matrix__ = copy.deepcopy(self.__backup__)

  @property
  def matrix(self):
    return self.__matrix__

  def _row(self, n):
    return self.__matrix__[n]

  def _col(self, n):
    for i in range(9):
      yield self.__matrix__[i][n]

  def _block(self, m, n):
    _m, _n = m, n
    while (_m % 3 != 0): _m -= 1
    while (_n % 3 != 0): _n -= 1
    for i in range(_m, _m+3):
      for j in range(_n, _n+3):
        yield self.__matrix__[i][j]

  def _idx_block(self, n):
    _m = n // 3
    _n = n % 3
    for i in range(_n*3, _n*3+3):
      for j in range(_m*3, _m*3+3):
        yield (i,j)

  def _val_block(self, n):
    _m = n // 3
    _n = n % 3
    for i in range(_n*3, _n*3+3):
      for j in range(_m*3, _m*3+3):
        yield self.__matrix__[i][j]
  
  # def row_move(self):
  def a(self):
    for n in range(9):
      for nums in range(1,10):
        fin = False
        cell = None
        if nums in self._row(n): continue
        for idx, cells in enumerate(self._row(n)):
          if cells == 0 and not fin:
            if nums not in self._col(idx) and nums not in self._block(n, idx):
              if cell is None:
                cell = idx
              else:
                fin = True

        if not fin and cell is not None: self.__matrix__[n][cell] = nums

  # def col_move(self):
  def b(self):
    for n in range(9):
      for nums in range(1,10):
        fin = False
        cell = None
        if nums in self._col(n): continue
        for idx, cells in enumerate(self._col(n)):
          if cells == 0 and not fin:
            if nums not in self._row(idx) and nums not in self._block(idx, n):
              if cell is None:
                cell = idx
              else:
                fin = True
        if not fin and cell is not None: self.__matrix__[cell][n] = nums


  # def block_move(self):
  def c(self):
    for n in range(9):
      for nums in range(1,10):
        fin = False
        row, col = None, None
        if nums in self._val_block(n): continue
        for r,c in self._idx_block(n):
          if self.__matrix__[r][c] == 0 and not fin:
            if nums not in self._row(r) and nums not in self._col(c):
              if row is None:
                row, col = r, c
              else:
                fin = True

        if not fin and row is not None: self.__matrix__[row][col] = nums

  # def row_move_3(self):
  def d(self):
    for r in range(9):
      list_nums = []
      for nums in range(1, 10):
        if nums not in self._row(r): list_nums.append(nums)

      if len(list_nums) != 3: continue

      empty_cells = {}
      for idx, cells in enumerate(self._row(r)):
        if cells == 0: empty_cells[idx] = []

      for c in empty_cells.keys():
        for nums in list_nums:
          if nums in self._block(r,c) or nums in self._col(c):
            empty_cells[c] = empty_cells.get(c) + [nums]

      for k, val in empty_cells.items():
        if len(val) == 2:
          _x = None
          for x in list_nums:
            if x not in val:
              _x = x
          self.__matrix__[r][k] = _x

  # def col_move_3(self):
  def e(self):
    for c in range(9):
      list_nums = []
      for nums in range(1, 10):
        if nums not in self._col(c): list_nums.append(nums)

      if len(list_nums) != 3: continue

      empty_cells = {}
      for idx, cells in enumerate(self._col(c)):
        if cells == 0: empty_cells[idx] = []

      for r in empty_cells.keys():
        for nums in list_nums:
          if nums in self._block(r,c) or nums in self._row(r):
            empty_cells[r] = empty_cells.get(r) + [nums]

      for k, val in empty_cells.items():
        if len(val) == 2:
          _x = None
          for x in list_nums:
            if x not in val:
              _x = x
          self.__matrix__[k][c] = _x

  # def block_move_3(self):
  def f(self):
    for b in range(5,6):
      list_nums = []
      for nums in range(1, 10):
        if nums not in self._val_block(b): list_nums.append(nums)

      if len(list_nums) != 3: continue

      empty_cells = {}
      for idx, cells in enumerate(self._idx_block(b)):
        if self.__matrix__[cells[0]][cells[1]] == 0: empty_cells[cells] = []

      for ib in empty_cells.keys():
        for nums in list_nums:
          if nums in self._col(ib[1]) or nums in self._row(ib[0]):
            empty_cells[ib] = empty_cells.get(ib) + [nums]

      for k, val in empty_cells.items():
        if len(val) == 2:
          _x = None
          for x in list_nums:
            if x not in val:
              _x = x
          self.__matrix__[k[0]][k[1]] = _x

  # def try_row_move(self):
  def g(self):
    for r in range(9):
      dict_cell = {}
      for num in range(1,10):
        list_cell = []
        if num not in self._row(r):
          for c, cells in enumerate(self._row(r)):
            if cells == 0 and num not in self._block(r,c) and num not in self._col(c):
              list_cell.append(c)
        dict_cell[num] = list_cell
      for key, val in dict_cell.items():
        if len(val) == 2:
          _c = val[random.randrange(2)]
          self.__matrix__[r][_c] = key
          break

  # def try_col_move(self):
  def h(self):
    for c in range(9):
      dict_cell = {}
      for num in range(1,10):
        list_cell = []
        if num not in self._col(c):
          for r, cells in enumerate(self._col(c)):
            if cells == 0 and num not in self._block(r,c) and num not in self._row(r):
              list_cell.append(r)
        dict_cell[num] = list_cell

      for key, val in dict_cell.items():
        if len(val) == 2:
          _r = val[random.randrange(2)]
          self.__matrix__[_r][c] = key
          break

  # def try_block_move(self):
  def i(self):
    for b in range(0,1):
      dict_cell = {}
      for num in range(1,10):
        list_cell = []
        if num not in self._val_block(b):
          for r, c in self._idx_block(b):
            if self.__matrix__[r][c] == 0 and num not in self._row(r) and num not in self._col(c):
              list_cell.append((r,c))
        dict_cell[num] = list_cell

      for key, val in dict_cell.items():
        if len(val) == 2:
          b = val[random.randrange(2)]
          self.__matrix__[b[0]][b[1]] = key
          break

  def fitness(self):
    sum = 0
    for i in range(9):
      for j in range(9):
        if self.__matrix__[i][j] == 0:
          sum += 1
    return sum

def display(arr):
  # for i in range(len(arr.matrix)):
  #   if i == 3 or i == 6: print(" ------+-------+------")
  #   row = arr.matrix[i]
  #   for j in range(len(row)):
  #     if j == 3 or j == 6: print(" |",end="")
  #     print(" ", row[j], sep="", end="")
  #   print()
  for row in arr.matrix:
    print(row)

def run_and_fit(obj, cmds):
  for i in cmds:
    exec(f"obj.{i}()")
  fit = obj.fitness()
  if fit == 0:
    print(cmds)
    raise ValueError(cmds)
  obj.reset()
  return 9*9 - fit

def tournament_selection(list_fitness):
  sum = 0
  for pop in list_fitness:
    sum += pop[1]
  length = len(list_fitness)
  lst = []
  for i in range(length):
    ran = random.randrange(1,sum+1)
    acc_sum = 0
    for pop in list_fitness:
      acc_sum += pop[1]
      if acc_sum >= ran:
        lst.append(pop)
        break
  lst = sorted(lst, key=lambda x: x[1], reverse=True)
  return lst

def crossover(list_fitness):
  if random.randrange(10) > 6:
    for i in range(0, len(list_fitness)):
      prev_fit = list_fitness[i][1]
      count = 0
      while count < 100:
        count += 1
        crossover_point = random.randrange(len(list_fitness[i]))
        crossover_with = random.randrange(len(list_fitness))
        crossover_point1 = random.randrange(len(list_fitness[crossover_with]))
        list_fitness[i][0] = list_fitness[i][0][:crossover_point] + list_fitness[crossover_with][0][crossover_point1:]
        new_fit = run_and_fit(puzzle, list_fitness[i][0])
        if new_fit >= prev_fit:
          list_fitness[i][1] = new_fit
          break
  print("After CROSSOVER ", list_fitness)
  return list_fitness

def mutation(list_fitness):
  if random.randrange(10) > 3:
    for i in range(0, len(list_fitness)):
      prev_fit = list_fitness[i][1]
      count = 0
      while count < 100:
        count += 1
        mutation_point = random.randrange(len(list_fitness[i][0]))
        chosen_move = chr(random.randrange(97, 106))
        list_fitness[i][0] = list_fitness[i][0][:mutation_point] + chosen_move + list_fitness[i][0][mutation_point+1:]
        new_fit = run_and_fit(puzzle, list_fitness[i][0])
        if new_fit >= prev_fit:
          list_fitness[i][1] = new_fit
          break
  print("After MUTATION  ", list_fitness)
  return list_fitness

def check_solve_puzzle(list_fitness):
  for e in list_fitness:
    if e[1] == 9*9:
      return e
  return False

# @profile
def solve(puzzle):
  try:
    initial_population = ["".join([chr(random.randrange(97, 106)) for i in range(1,50)]) for i in range(10)]
    list_fitness = []
    for gen in initial_population:
      list_fitness.append([gen, run_and_fit(puzzle, gen)])
    list_fitness = sorted(list_fitness, key=lambda x: x[1], reverse=True)
    while True:
      list_fitness = tournament_selection(list_fitness)
      list_fitness = crossover(list_fitness)
      if check_solve_puzzle(list_fitness): break
      list_fitness = mutation(list_fitness)
      if check_solve_puzzle(list_fitness): break
    print(check_solve_puzzle(list_fitness))
    print()
  except Exception:
    print(Exception)
    display(puzzle)
  
  

startTime = time.time()
# puzzle = SudokuPuzzles([
#   [0,0,7,2,8,0,0,0,0],
#   [0,0,0,0,0,0,5,0,6],
#   [4,1,3,0,0,6,0,8,0],
#   [7,2,0,3,9,0,0,0,0],
#   [3,4,0,0,0,0,8,1,0],
#   [6,8,0,1,0,7,0,0,2],
#   [0,0,0,6,7,4,0,2,3],
#   [0,0,0,0,0,5,7,0,0],
#   [1,0,6,0,2,3,0,4,0]
# ])

# puzzle = SudokuPuzzles([
#   [9,7,4,2,3,6,1,5,8],
#   [6,3,8,5,9,1,7,4,2],
#   [1,2,5,4,8,7,9,3,6],
#   [3,1,6,7,5,4,2,8,9],
#   [7,4,2,9,1,8,5,6,3],
#   [5,8,9,3,6,2,4,1,7],
#   [8,6,7,1,2,5,3,9,4],
#   [2,5,3,6,4,9,8,7,1],
#   [4,9,1,8,7,3,6,2,5]
# ])

# puzzle = SudokuPuzzles([
#   [0,0,0,0,5,0,9,7,6],
#   [8,0,5,1,9,0,0,3,0],
#   [3,7,0,0,4,0,0,8,0],
#   [0,8,0,0,0,0,0,0,9],
#   [0,2,0,0,0,0,4,0,7],
#   [0,9,0,0,2,6,0,1,5],
#   [0,0,0,0,8,1,6,0,0],
#   [9,0,0,3,0,0,0,0,0],
#   [2,0,0,4,0,9,0,0,0]
# ])

# puzzle = SudokuPuzzles([
#   [0,3,9,0,0,0,1,2,0],
#   [0,0,0,9,0,7,0,0,0],
#   [8,0,0,4,0,1,0,0,6],
#   [0,4,2,0,0,0,7,9,0],
#   [0,0,0,0,0,0,0,0,0],
#   [0,9,1,0,0,0,5,4,0],
#   [5,0,0,1,0,9,0,0,3],
#   [0,0,0,8,0,5,0,0,0],
#   [0,1,4,0,0,0,8,7,0]
# ])

# puzzle = SudokuPuzzles([
#   [0,3,0,0,0,1,5,0,0],
#   [0,0,0,5,0,0,0,8,4],
#   [0,0,5,0,0,7,0,6,0],
#   [0,0,0,0,0,0,0,0,0],
#   [0,8,0,2,0,0,0,7,0],
#   [0,0,0,8,5,0,0,0,9],
#   [0,0,3,0,9,4,0,0,7],
#   [0,0,4,0,0,0,0,0,8],
#   [5,0,6,0,1,0,0,0,0]
# ])

puzzle = SudokuPuzzles([
  [4, 0, 0, 0, 7, 8, 0, 0, 3],
  [0, 0, 0, 2, 0, 0, 0, 0, 0],
  [0, 0, 9, 0, 0, 0, 0, 1, 0],
  [0, 1, 0, 0, 6, 2, 0, 3, 0],
  [0, 0, 0, 4, 0, 0, 0, 0, 2],
  [6, 0, 0, 5, 0, 0, 0, 0, 0],
  [0, 4, 0, 0, 0, 0, 7, 0, 0],
  [7, 0, 0, 0, 3, 6, 0, 0, 8],
  [0, 0, 0, 0, 5, 0, 0, 0, 0],
])
# print(" After Preprocess")
# display(puzzle)
solve(puzzle)
print()
endTime = time.time()
print(f"Solution Found in {endTime - startTime} seconds")
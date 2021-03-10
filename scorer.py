from os import sys

class Problem:

  # pizza is a 2D binary array. True means ham, False mushrooms
  def __init__(self, min_ham, max_size, pizza):
    self.min_ham = min_ham
    self.max_size = max_size
    self.pizza = pizza

  def is_valid_slice(self, row, col, height, width):
    if row < 0 or row >= len(self.pizza) or row+height < 0 or row+height > len(self.pizza) or col<0 or col >= len(self.pizza[0]) or col+width < 0 or col+width > len(self.pizza[0]):
        print(f"slice {row} {col} out of bounds", file=sys.stderr)
        return False

    if width * height > self.max_size:
      print(f"slice too large (coordinates {row} {col})", file=sys.stderr)
      return False

    nb_H = 0

    for r in range(row, row+height):
      for c in range(col, col+width):
        if self.pizza[r][c]:
          nb_H += 1

    if nb_H < self.min_ham:
      print(f"Too few ham on slice starting at {row} {col}", file=sys.stderr)
      return False

    return True


def parse_problem(filename):
  with open(filename) as file:
    rows, cols, hams, size = map(int, file.readline().strip().split(" "))
    pizza = [[] for r in range(rows)]

    for r in range(rows):
      line = file.readline().strip()

      for letter in line:
        pizza[r].append(letter == "H")

    return Problem(hams, size, pizza)

def parse_sol(problem, filename):
  score = 0

  occupied = [[False for c in range(len(problem.pizza[0]))] for r in range(len(problem.pizza))]

  with open(filename) as file:
    nb_slices = int(file.readline().strip())

    for s in range(nb_slices):
      line = file.readline().strip()
      values = line.split(" ")

      if len(values) != 4:
        print(f"Wrong format on line {s+1}", file=sys.stderr)
        return 0

      row, col, r2, c2 = map(int, values)
      height = r2 - row + 1
      width = c2 - col + 1

      if problem.is_valid_slice(row, col, height, width):
        for r in range(row, row+height):
          for c in range(col, col+width):
            if occupied[r][c]:
              print(f"Slice collision on coordinate {r} {c}", file=sys.stderr)
              return 0
            else:
              occupied[r][c] = True

        score += height*width
      else:
        return 0

  return score



if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage:", file=sys.stderr)
    print("python3 scorer.py problem_file.txt solution_file.txt", file=sys.stderr)
    exit(0)
  pb = parse_problem(sys.argv[1])
  score = parse_sol(pb, sys.argv[2])
  print(score)

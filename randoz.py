import random

for xy in range(16):
  x = random.randrange(0, 38400) / 10
  y = random.randrange(0, 38400) / 10
  print(x, '|', y)
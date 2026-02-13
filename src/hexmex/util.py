import sys

def get_first_pos_arg():  
  """
  Retrieves the first positional argument from the command line.
  """
  if len(sys.argv) > 1:
    return sys.argv[1]
  else:
    # print("Error: No name provided.")
    return None


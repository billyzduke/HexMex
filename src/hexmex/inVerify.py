from notSoRandoz import inhumanOrder

# VERIFY the list is 78 items long and contains numbers 1-78
# VERIFY the numbers within each lane (of 2's and 4's) are sequential

it = 78
slo = 26
fst = it - slo
error = ''
inhumanItems = len(inhumanOrder)

if not inhumanItems == it:
  error = 'List contains only ' + str(inhumanItems) + ' items. List should contain ' + str(it) + ' items.'
else:
  print('VERIFIED: List contains', it, 'items.')
  inhumanSorted = sorted(inhumanOrder)
  for n, g in enumerate(inhumanSorted):
    if not g == n + 1:
      error = 'Incremental issue at list item ' + str(n) + '. Item value is ' + str(g) + ', but should be ' + str(n + 1) + '.'
      break
  if len(error) == 0:
    print('VERIFIED: List contains numbers 1 -', it)
    
    inhumanLana = inhumanOrder.copy()
    laner = range(6)
    slowLane = []
    fastLane = []

    for n, g in enumerate(inhumanOrder):
      if n % 6 == 0 or (n - 1) % 6 == 0:
        slowLane.append(g)
      else:
        fastLane.append(g)
    
    slowLen = len(slowLane)
    if not slowLen == slo:
      error = 'Slow Lane contains ' + str(slowLen) + ' items. Lane should contain exactly ' + str(slo) + ' items.'
      
    if len(error) == 0:
      fastLen = len(fastLane)
      if not fastLen == fst:
        error = 'Fast Lane contains ' + str(fastLen) + ' items. Lane should contain exactly ' + str(fst) + ' items.'
        
      if len(error) == 0:
        print('VERIFIED: List successfully split into Slow Lane with ' + str(slowLen) + ' items and Fast Lane with ' + str(fastLen) + ' items.')
        
        slowCheck = all(slowLane[i] < slowLane[i + 1] for i in range(slowLen - 1))
        slowDoubleCheck = slowLane == sorted(slowLane)
        
        if not slowCheck and slowDoubleCheck:
          error = 'Ascending order issue in Slow Lane.'
          
          if len(error) == 0:
            print('VERIFIED: Slow Lane is in ascending order.')
            
            fastCheck = all(fastLane[i] < fastLane[i + 1] for i in range(fastLen - 1))
            fastDoubleCheck = fastLane == sorted(fastLane)
        
            if not fastCheck and fastDoubleCheck:
              error = 'Ascending order issue in Fast Lane.'
              
            if len(error) == 0:
              print('VERIFIED: Fast Lane is in ascending order.')

if len(error) > 0:
  print('ERROR:', error)
else:
  print('ALL TESTS PASSED. Good to go, mate.')
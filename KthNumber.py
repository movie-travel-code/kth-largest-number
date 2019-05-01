import time

import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.plotly as py

array = np.random.randint(-10000, 10000, size=1000)
K = np.random.randint(1, 1000, size=1)[0]
x = range(1000)
trace = go.Scatter(x=x, y=array, mode='markers', marker = dict(size = 8), name='array')
data = [trace]

Guesses = []
GuessesContext = []

def getKth(array, K, Max, Min, size) :
  if K == 1:
    return Max
  k = K
  G = (Max - (Max - Min) * (k - 1.0) / (size - 1))
  Guesses.append(G)
  GuessesContext.append((Max, Min, k, G))
  print('Max:' + str(Max) + " Min:" + str(Min) + " size: " + str(size) + " G:" + str(G) + " K:" + str(k))

  GUB = Max
  GLB = Min
  Count = 0
  for ele in array:
    if ele > Max or ele < Min:
      continue
    
    if ele > G and ((ele - G) < (GUB - G)):
      GUB = ele
    
    if ele < G and ((G - ele) < (G - GLB)):
      GLB = ele
    
    if ele >= G:
      k = k - 1
    
    if ele < G:
      Count = Count + 1
  print(k)
  if k <= 0:
    return getKth(array, K, Max, GUB, size - Count)
  if k > 0:
    return getKth(array, k, GLB, Min, size - (K - k))

result = getKth(array, K, np.max(array), np.min(array), 1000)
inter = 1000 / len(Guesses)
guessPointsy = Guesses
guessPointsx = range(0, 1000, inter)

guessPointsy.append(result)

guessPoints = go.Scatter(
  x = guessPointsx,
  y = guessPointsy,
  mode='lines+markers',
  name='guess process',
  marker = dict(
    color='red',
    size=12
  )
)

contextX = 0
for context in GuessesContext:
  trace = go.Scatter(
    y = [context[0], context[1]],
    x = [contextX, contextX],
    name = 'Max:' + str(context[0]) + ', Min:' + str(context[1]) + ', K:' + str(context[2]) + ', G:' + str(context[3]),
    marker = dict(
    color='blue',
    size=12
    )
  )
  data.append(trace)
  contextX = contextX + inter

data.append(guessPoints)

layout = go.Layout(
  title = dict (
    text = 'N=1000, K = ' + str(K) + ' result= ' + str(result),
    xref = 'paper',
    x = 0
  ),
  xaxis = dict (
    range = [-1, 1100]
  ),
  yaxis = dict(
    range= [-10100, 10100]
  )
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='The Kth number.html')

# Edward Kuanshi Lu
# Calculations for neural network homework

# learning rate
l = 10
# outputs 1 to 6. val 0 is a placeholder to align indices.
outputs = [0, 1, 2, 0.7311, 0.0179, 0.9933, 0.8387]
# errors 1 to 6. Again, val at 0 is a placeholder.
errors = [0]*7
# 2d struct. weights[a][b] is weight from node a to b
weights = {}
weights[1] = {3: -3, 4: 2, 5: 4}
weights[2] = {3: 2, 4: -3, 5: 0.5}
weights[3] = {6: 0.2}
weights[4] = {6: 0.7}
weights[5] = {6: 1.5}

### Calculations

# error of output layer is a special case
errors[6] = outputs[6]*(1-outputs[6])*(0-outputs[6])

# fill out errors 3 to 5. Errors 1-2 are left as 0.
for i in range(3,6):
    errors[i] = outputs[i]*(1-outputs[i])*(errors[6]*weights[i][6])

# adjust weights
for source, dests in weights.iteritems():
    for dest, value in dests.iteritems():
        weights[source][dest] += l*errors[dest]*outputs[source]

# write & print answers
f = open("nn-train.txt", 'w')

for i in range(1,7):
    w = "err_%s = %s" % (i, errors[i])
    print w
    f.write(w + '\n')

for source, dests in weights.iteritems():
    for dest, value in dests.iteritems():
        w = "w_%s%s = %s" % (source, dest, value)
        print w
        f.write(w + '\n')
f.close()

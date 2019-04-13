lel = "one two tree four"

index = 0
lel = lel.split(' ')
omg = []
for x in range(3, len(lel), 3):
    omg += lel[index:3] + ['\n']
    index = x
else:
    omg += lel[index:]


print(omg)

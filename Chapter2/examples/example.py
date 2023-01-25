import fileinput

ans = ""
for line in fileinput.input():
    value = len(line.split(","))
    print(value)


from collections import Counter
import sys
sys.stdin = open("input.txt", "r")
a = []
for i in range(67900):
    a.append(input())

print(Counter(a))
n = int(input())

p = [0] + list(map(int, input().split()))

pi = [0] * (n + 1)


for i in range(1, n + 1):
    pi[p[i]] = i


for i in range(1, n + 1):
    print(pi[i], end=" ")

print()
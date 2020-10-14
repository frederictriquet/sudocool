def orange(c,d,u):
    return c != 2 and c!= 4 and \
        d != 2 and d != 4 and d!=3 and \
        u != 2 and u != 4

def jaune(c,d,u):
    return d == 2

def vert(c,d,u):
    return c!=2 and c!=3 and \
        d != 2 and d != 4 and d!=3 and \
        u != 2 and u!=3

for i in range(11,33):
    n = i*i
    u = n % 10
    d = ((n-u)/10)%10
    c = ((n-d*10-u)/100)%10
    if vert(c,d,u) and u != d and u!= c and c != d and n < 1000:
        print(f'{i} -> {n}')



# # ORANGE
# 13 -> 169 *
# 14 -> 196 *
# 19 -> 361     +
# 24 -> 576 *
# 31 -> 961 *


# # JAUNE
# 18 -> 324
# 23 -> 529     +
# 25 -> 625
# 27 -> 729


# # VERT
# 13 -> 169
# 14 -> 196
# 24 -> 576
# 28 -> 784     +
# 31 -> 961


orange  jaune   vert
361     529     784

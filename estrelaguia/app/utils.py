def n_last_path(s, n):
    end = len(s)
    while n >= 0:
        for i in reversed(range(end)):
            if s[i] == '/':
                break
        if i == 0:
            return "/"
        end = i-1
        n -= 1
    return s[:end+1]

def bread(s):
    bread = []
    i = 0
    while s != "/":
        s = n_last_path(s, 0)
        bread.append(s)
        i += 1
    bread.reverse()
    return bread

import json
import random

CATALOG_PATH = 'catalog/set_everything.json'

E = [0,0,0,0,0]
dump = ''
while len(E) > 4 or dump.count("Writing-Intensive Course") < 2 or dump.count("Research and Information Literacy") < 2:
    G = json.load(open(CATALOG_PATH))
    G = [{'n': e['n'], 'u': list(filter( \
            lambda s : not s == 'Philosophical Inquiry and Life\'s Meanings' \
        , e['u']))} for e in G]

    random.shuffle(G)

    # print(G[0])

    F = [set(v['u']) for v in G]

    print(F[0])

    # exit()
    from collections import defaultdict

    # First prepare a list of all sets where each element appears
    D = defaultdict(list)
    for y,S in enumerate(F):
        for a in S:
            D[a].append(y)

    L=defaultdict(set)
    # Now place sets into an array that tells us which sets have each size
    for x,S in enumerate(F):
        L[len(S)].add(x)

    E=[] # Keep track of selected sets
    # Now loop over each set size
    for sz in range(max(len(S) for S in F),0,-1):
        if sz in L:
            P = L[sz] # set of all sets with size = sz
            while len(P):
                x = P.pop()
                E.append(x)
                for a in F[x]:
                    for y in D[a]:
                        if y!=x:
                            S2 = F[y]
                            L[len(S2)].remove(y)
                            S2.remove(a)
                            L[len(S2)].add(y)

    print(len(E))

    catalog = json.load(open(CATALOG_PATH))

    def lookup(num):
        # print(num)
        return next(filter(lambda e : e['n'] == num, catalog))

    dump = json.dumps([
        G[e] for e in E
    ], indent=2, sort_keys=True)

    print(len(E), dump.count("Writing-Intensive Course"), dump.count("Research and Information Literacy"))

dump = json.dumps([
lookup(G[e]['n']) for e in E
], indent=2, sort_keys=True)
print(dump)

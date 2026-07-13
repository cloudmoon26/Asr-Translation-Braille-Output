from math import inf

def dtw(seq1, seq2):
    n, m = len(seq1), len(seq2)
    dtw = [[inf]*(m+1) for _ in range(n+1)]
    dtw[0][0] = 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            dist = abs(seq1[i-1] - seq2[j-1])
            dtw[i][j] = dist + min(dtw[i-1][j], dtw[i][j-1], dtw[i-1][j-1])

    path = []
    i, j = n, m
    while i > 0 and j > 0:
        path.append((i-1, j-1))
        step = min(
            (dtw[i-1][j], i-1, j),
            (dtw[i][j-1], i, j-1),
            (dtw[i-1][j-1], i-1, j-1)
        )
        i, j = step[1], step[2]

    return path[::-1]

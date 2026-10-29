# 3841. Palindromic Path Queries in a Tree
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given an undirected tree with n nodes labeled 0 to n - 1. This is represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi] indicates an undirected edge between nodes ui and vi.

# You are also given a string s of length n consisting of lowercase English letters, where s[i] represents the character assigned to node i.

# You are also given a string array queries, where each queries[i] is either:

# "update ui c": Change the character at node ui to c. Formally, update s[ui] = c.
# "query ui vi": Determine whether the string formed by the characters on the unique path from ui to vi (inclusive) can be rearranged into a palindrome.
# Return a boolean array answer, where answer[j] is true if the jth query of type "query ui vi"​​​​​​​ can be rearranged into a palindrome, and false otherwise.

 

# Example 1:

# Input: n = 3, edges = [[0,1],[1,2]], s = "aac", queries = ["query 0 2","update 1 b","query 0 2"]

# Output: [true,false]

# Explanation:

# "query 0 2": Path 0 → 1 → 2 gives "aac", which can be rearranged to form "aca", a palindrome. Thus, answer[0] = true.
# "update 1 b": Update node 1 to 'b', now s = "abc".
# "query 0 2": Path characters are "abc", which cannot be rearranged to form a palindrome. Thus, answer[1] = false.
# Thus, answer = [true, false].

# Example 2:

# Input: n = 4, edges = [[0,1],[0,2],[0,3]], s = "abca", queries = ["query 1 2","update 0 b","query 2 3","update 3 a","query 1 3"]

# Output: [false,false,true]

# Explanation:

# "query 1 2": Path 1 → 0 → 2 gives "bac", which cannot be rearranged to form a palindrome. Thus, answer[0] = false.
# "update 0 b": Update node 0 to 'b', now s = "bbca".
# "query 2 3": Path 2 → 0 → 3 gives "cba", which cannot be rearranged to form a palindrome. Thus, answer[1] = false.
# "update 3 a": Update node 3 to 'a', s = "bbca".
# "query 1 3": Path 1 → 0 → 3 gives "bba", which can be rearranged to form "bab", a palindrome. Thus, answer[2] = true.
# Thus, answer = [false, false, true].

 

# Constraints:

# 1 <= n == s.length <= 5 * 104
# edges.length == n - 1
# edges[i] = [ui, vi]
# 0 <= ui, vi <= n - 1
# s consists of lowercase English letters.
# The input is generated such that edges represents a valid tree.
# 1 <= queries.length <= 5 * 104​​​​​​​
# queries[i] = "update ui c" or
# queries[i] = "query ui vi"
# 0 <= ui, vi <= n - 1
# c is a lowercase English letter.

class Solution:
    def palindromePath(self, n, edges, s, queries):
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        LOG = max(1, (n - 1).bit_length())
        parent = [0] * n
        depth = [0] * n
        tin = [0] * n
        tout = [0] * n
        it = [0] * n
        stack = [0]
        timer = 1
        tin[0] = 1
        while stack:
            u = stack[-1]
            if it[u] < len(g[u]):
                v = g[u][it[u]]
                it[u] += 1
                if v == parent[u]:
                    continue
                parent[v] = u
                depth[v] = depth[u] + 1
                timer += 1
                tin[v] = timer
                stack.append(v)
            else:
                tout[u] = timer
                stack.pop()

        up = [parent]
        for j in range(1, LOG):
            prev = up[j - 1]
            up.append([prev[prev[v]] for v in range(n)])

        bit = [0] * (n + 2)

        def add(i, x):
            while i <= n + 1:
                bit[i] ^= x
                i += i & -i

        def get(i):
            r = 0
            while i > 0:
                r ^= bit[i]
                i -= i & -i
            return r

        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u
            d = depth[u] - depth[v]
            for j in range(LOG):
                if (d >> j) & 1:
                    u = up[j][u]
            if u == v:
                return u
            for j in range(LOG - 1, -1, -1):
                if up[j][u] != up[j][v]:
                    u = up[j][u]
                    v = up[j][v]
            return up[0][u]

        cs = [ord(c) - 97 for c in s]
        for u in range(n):
            x = 1 << cs[u]
            add(tin[u], x)
            add(tout[u] + 1, x)

        res = []
        for q in queries:
            p = q.split()
            if p[0] == "update":
                u = int(p[1])
                c = ord(p[2]) - 97
                if cs[u] != c:
                    x = (1 << cs[u]) ^ (1 << c)
                    add(tin[u], x)
                    add(tout[u] + 1, x)
                    cs[u] = c
            else:
                u = int(p[1])
                v = int(p[2])
                l = lca(u, v)
                m = get(tin[u]) ^ get(tin[v]) ^ (1 << cs[l])
                res.append((m & (m - 1)) == 0)
        return res
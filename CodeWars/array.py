def array_diff(a, b):
    if len(a + b) > len(set(a + b)):
        for i in sorted(b):
            while i in a:
                a.remove(i)
        return a
    return a


#an alternative implementation with O(n) time complexity:
def array_diff(a, b):
    hash_table = set(b)
    return [x for x in a if x not in hash_table]

def fissbuzz(i):
    if isinstance(i, (int, float)) and i > 0:
        i = int(i)
        if i % 15 == 0:
            return 'fissbuzz'
        if i % 5 == 0:
            return 'buzz'
        if i % 3 == 0:
            return 'fiss'
        return i
    else:
        if isinstance(i, (int, float)):
            return 0
        return None

# bez refaktoringu
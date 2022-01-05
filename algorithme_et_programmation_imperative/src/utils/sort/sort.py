# fusion_rec_decreasing ---> O(n.log(n))
def fusion_sort_decreasing(tab: list) -> list:
    n = len(tab)
    if n <= 1:
        return tab
    else:
        middle = n // 2
        return __fusion_decreasing__(fusion_sort_decreasing(tab[:middle]), fusion_sort_decreasing(tab[middle:]))


# O(size_tab1 + size_tab2)
def __fusion_decreasing__(tab1: list, tab2: list) -> list:
    ind1, ind2            = 0, 0
    size_tab1, size_tab2  = len(tab1), len(tab2)
    t                     = []

    while ind1 < size_tab1 and ind2 < size_tab2:
        if tab1[ind1] > tab2[ind2]:
            t.append(tab1[ind1])
            ind1 += 1
        else:
            t.append(tab2[ind2])
            ind2 += 1

    if ind1 == size_tab1:
        t.extend(tab2[ind2:])
    else:
        t.extend(tab1[ind1:])

    return t


# fusion_sort_growing---> O(n.log(n))
def fusion_sort_growing(tab: list) -> list:
    n = len(tab)
    if n <= 1:
        return tab
    else:
        middle = n // 2
        return __fusion_growing__(fusion_sort_growing(tab[:middle]), fusion_sort_growing(tab[middle:]))


# O(size_tab1 + size_tab2)
def __fusion_growing__(tab1: list, tab2: list) -> list:
    ind1, ind2            = 0, 0
    size_tab1, size_tab2  = len(tab1), len(tab2)
    t                     = []

    while ind1 < size_tab1 and ind2 < size_tab2:
        if tab1[ind1] < tab2[ind2]:
            t.append(tab1[ind1])
            ind1 += 1
        else:
            t.append(tab2[ind2])
            ind2 += 1

    if ind1 == size_tab1:
        t.extend(tab2[ind2:])
    else:
        t.extend(tab1[ind1:])

    return t

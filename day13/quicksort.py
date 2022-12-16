
def partition(A:list, lo:int, hi:int, compare):

    pivot = A[ (lo + hi) // 2] #Floor division used to ensure that last element is never picked

    i = lo - 1
    k = hi + 1

    while True:

        #Move low idx (i) to the right:
        i += 1
        
        while compare(A[i], pivot) < 0:
            i += 1

        k -= 1
        while compare(A[k], pivot) > 0:
            k -= 1
        
        if i >= k:
            return k

        holder = A[i]
        A[i] = A[k]
        A[k] = holder

def quicksort(A:list, lo:int, hi:int, compare):
    if lo >= 0  and hi >= 0 and lo < hi:
        p = partition(A, lo, hi, compare)
        quicksort(A, lo, p, compare)
        quicksort(A, p + 1, hi, compare)

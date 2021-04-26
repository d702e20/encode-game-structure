import queue
import threading
import time
import timeit
from pip._vendor.msgpack.fallback import xrange

batch_size = 7
test_batch_size = 500
arr_len = 298937
total_threads = 5

to_test = {}
res_total = {}


class TimerBoi(threading.Thread):
    def __init__(self, thread_id, queue_hue: queue.Queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue_hue = queue_hue

    def run(self) -> None:
        while True:
            queue_lock.acquire()
            if self.queue_hue.empty():
                queue_lock.release()
                break
            q = self.queue_hue.get()
            queue_lock.release()
            try:
                res = timeit.timeit(q[1], number=test_batch_size)
                res_total[q[0]] = res
                print(f"{self.thread_id} -> {q[0]}: {res}")
            except Exception as e:
                print(f"{q[0]} error {str(e)}")
            time.sleep(1)


def wrapper(func, *args, **kwargs):
    def wrapped():
        func(*args, **kwargs)

    return wrapped


# ---------slice-------------
def slice(arr, n):
    while True:
        if not arr:
            break
        tmp = arr[0:n]
        arr = arr[n:-1]


# Wayyyy too slow
#to_test['slice'] = wrapper(slice, [i for i in range(0, arr_len)], batch_size)


# -----------index-----------
def index(arr, n):
    for i in range(0, round(len(arr) / n + 1)):
        tmp = arr[n * i: n * (i + 1)]


to_test['index'] = wrapper(index, [i for i in range(0, arr_len)], batch_size)


# ----------batches 1------------
def batch_help(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def batch(arr, n):
    for x in batch_help(arr, n):
        tmp = x


to_test['batch1'] = wrapper(batch, [i for i in range(0, arr_len)], batch_size)


# ---------chunks-------------
def chunks_help(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def chunks(arr, n):
    for x in chunks_help(arr, n):
        tmp = x


to_test['chunks'] = wrapper(chunks, [i for i in range(0, arr_len)], batch_size)


# -----------chunks simple---------
def chunks_simple(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


to_test['chunks_simple'] = wrapper(chunks_simple, [i for i in range(0, arr_len)], batch_size)

# -----------numpy split----------
import numpy as np


def numpy_split(arr, n):
    for x in np.array_split(arr, size=n):
        tmp = x


to_test['numpy'] = wrapper(numpy_split, [i for i in range(0, arr_len)], batch_size)

# -----------itertools-----------
from itertools import islice


def iter_tools(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


to_test['numpy'] = wrapper(iter_tools, [i for i in range(0, arr_len)], batch_size)


# -----------recursive---------
def recursive(li, n):
    if li == []:
        return
    yield li[:n]
    yield from recursive(li[n:], n)


to_test['recursive'] = wrapper(recursive, [i for i in range(0, arr_len)], batch_size)


# -----------dec recursive-----
def dec(gen):
    def new_gen(li, n):
        for e in gen(li, n):
            if e == []:
                return
            yield e

    return new_gen


@dec
def recursive_dec(li, n):
    yield li[:n]
    for e in recursive_dec(li[n:], n):
        yield e


to_test['recursive_dec'] = wrapper(recursive_dec, [i for i in range(0, arr_len)], batch_size)


# -----------"explicit version"-
def chunkList(initialList, chunkSize):
    """
    This function chunks a list into sub lists
    that have a length equals to chunkSize.

    Example:
    lst = [3, 4, 9, 7, 1, 1, 2, 3]
    print(chunkList(lst, 3))
    returns
    [[3, 4, 9], [7, 1, 1], [2, 3]]
    """
    finalList = []
    for i in range(0, len(initialList), chunkSize):
        finalList.append(initialList[i:i + chunkSize])
    return finalList


to_test['chunkList'] = wrapper(chunkList, [i for i in range(0, arr_len)], batch_size)

# -----------oneliner----------

chunk = lambda ulist, step: map(lambda i: ulist[i:i + step], xrange(0, len(ulist), step))

to_test['oneliner'] = wrapper(recursive_dec, [i for i in range(0, arr_len)], batch_size)

# -----------grouper-----------
from itertools import zip_longest  # for Python 3.x


def grouper_help(iterable, n, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def grouper(arr, n):
    for x in grouper_help(arr, n):
        tmp = x


to_test['grouper'] = wrapper(grouper, [i for i in range(0, arr_len)], batch_size)

print('Running timeit test suit, with the following settings:')
print(f"""
    - {total_threads} threads
    - All times is an average of {test_batch_size} runs.
    - array length {arr_len}
    - batch size {batch_size}

""")
q = queue.Queue()
all_threads = []
queue_lock = threading.Lock()

for key in to_test.keys():
    q.put((key, to_test[key]))

for index in range(total_threads):
    thread = TimerBoi(index, q)
    thread.start()
    all_threads.append(thread)

while not q.empty():
    pass

for t in all_threads:
    t.join()

print('\n\rSorted by best value')
for i, key in enumerate(sorted(res_total, key=res_total.__getitem__)):
    print(f'{i + 1}. {key} : {res_total[key]}')


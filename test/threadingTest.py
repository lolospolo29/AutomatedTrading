import time
import threading

from numpy.random import uniform

# region Start / Run / Join / isalive
def func():
    time.sleep(uniform(5, 10))

def main():
    from threading import Thread, Event, Lock

    threads:list[Thread] = []
    for i in range(100):
        t = Thread(target=func)
        t.name =  str(i)
        t.start() # startet den thread und führt das programm weiter aus nebenläufig
        #t.run() # führt den thread aus und wartet bis dieser zuende ist
        print(str(t.is_alive())+ str(t.name))

        threads.append(t)

    for t in threads:
        t.join(timeout=uniform(0.1,1)) # für die überwachung
        if t.is_alive():
            print("not finished"+t.name)
        if not t.is_alive():
            print("finished"+t.name)
#main()
# endregion

# region Lock / Acquire / Release / islocked
l = threading.Lock()

def bye():
        with l:
            print("bye")
            time.sleep(5)
            print("bye")

def hello_there():
        with l:
            print("hello there")
            time.sleep(5)
            print("hello there")

def main2():
    from threading import Thread, Event, Lock
    hello = Thread(target=hello_there)
    hello.start() # start
    l.acquire() # setze lock solange bis er l.released() wird mit oder timeout released ihn
    time.sleep(2)
    if l.locked():
        print("not finished")
    while hello.is_alive():
        time.sleep(1)
    time.sleep(5)
    l.release()
    print("released")
    goodbye = Thread(target=bye)
    goodbye.start()

#main2()
# endregion

# region Condition notify / wait
cv = threading.Condition()
items = []

class item:
    def __init__(self):
        self.count = 0

def an_item_is_available()->bool:
        if len(items) == 0:
            return False
        return True
def get_an_available_item():
    print("get_an_available_item")

def make_an_item_available():
    items.append(an_item_is_available())


def consume():
    # Consume one item
    with cv:
        cv.wait_for(an_item_is_available) # waits for specific condiition to be true / timeout can be set
        #while not an_item_is_available():
        #   cv.wait() # also works with timeout
        get_an_available_item()
def produce():
    with cv:
        #cv.notify_all() # notify all waiters
        cv.notify() # notify one waiter n1
        make_an_item_available()

def main3():
    t = threading.Thread(target=consume)
    t.start()
    t2 = threading.Thread(target=consume)
    t2.start()
    p = threading.Thread(target=produce)
    p.start()
#main3()
# endregion

# region Semaphore with Max Pool Acquire
from threading import BoundedSemaphore

maxconnections = 5
# ...
pool_sema = BoundedSemaphore(value=maxconnections)

def connectdb():
    # Simulate a database connection
    return True
def connect():
    # Acquire a semaphore to use a connection
    pool_sema.acquire()
    try:
        conn = connectdb()
        try:
            # Use the connection (simulated work)
            time.sleep(10)
        finally:
            # Close the connection
            print()
            print("Closing connection")
            print()
            # Simulate connection close
    finally:
        # Release the semaphore
        pool_sema.release()

def main4():
    threads = [threading.Thread(target=connect) for _ in range(10)]

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All workers finished.")
#main4()
# endregion

# region Event Clear / Set / Wait waiters wait for set
e = threading.Event()

e.clear()

def workerA():
    e.wait()
    print("worker A done")
def workerB():
    time.sleep(uniform(5, 10))
    e.set()
    print("worker B done")

def main5():
    for i in range(100):
        if i % 2 == 0:
            threading.Thread(target=workerA).start()
        if i == 1:
            threading.Thread(target=workerB).start()
# endregion

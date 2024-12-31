# region Start
import asyncio
import time
from random import uniform
from threading import Event

from joblib.externals.loky.backend.synchronize import Condition


async def test():
    time.sleep(1)

async def main():
    print('Hello ...')
    await test()
    print('... World!')

#asyncio.run(main())
     # Run the `main` coroutine
# endregion

# region Await Async Task = create
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main2():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello') # wait for completion
    await say_after(2, 'world') # wait for completion

    print(f"finished at {time.strftime('%X')}")

async def main3():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

#asyncio.run(main3())
# endregion

# region Create Tasks Callback and Set
background_tasks = set()

async def some_coro(param):
    print(param)
    await asyncio.sleep(param)


async def main4():
    for i in range(10):
        task = asyncio.create_task(some_coro(param=i))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    # Optionally, wait for all tasks to complete before exiting main
    print(f"started at {time.strftime('%X')}")

# Run the program
#asyncio.run(main4())
# endregion

# region Schedule Calls Gather
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main5():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)

#asyncio.run(main5())
# endregion

# region Eager Task Factory
import asyncio
from typing import Set, Callable, Awaitable

class EagerTaskFactory:
    def __init__(self):
        self._tasks: Set[asyncio.Task] = set()  # Track running tasks

    def create_task(self, coro: Callable[[], Awaitable], *, name: str = None) -> asyncio.Task:
        """
        Create and track an eager asyncio task.

        :param coro: The coroutine function to be wrapped in a task.
        :param name: Optional name for the task (used for debugging).
        :return: The created task.
        """
        task = asyncio.create_task(coro(), name=name)  # Start the task eagerly
        self._tasks.add(task)  # Track the task

        # Automatically remove the task from the set once it is done
        task.add_done_callback(self._tasks.discard)

        return task

    async def wait_all(self):
        """Wait for all tasks to complete."""
        await asyncio.gather(*self._tasks, return_exceptions=True)

    def get_running_tasks(self) -> Set[asyncio.Task]:
        """Retrieve currently running tasks."""
        return {task for task in self._tasks if not task.done()}

import random
import asyncio

# Example coroutine
async def example_task(task_id: int):
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate work
    print(f"Task {task_id} completed")

# Main function
async def main6():
    factory = EagerTaskFactory()

    # Create several tasks
    for i in range(10):
        factory.create_task(lambda i=i: example_task(i), name=f"Task-{i}")

    # Wait for all tasks to complete
    await factory.wait_all()
    print("All tasks completed.")

# Run the program
#asyncio.run(main6())
#
# Key Features of the Eager Task Factory
# Eager Task Creation:
#
# Tasks are started immediately using asyncio.create_task.
# Automatic Cleanup:
#
# Tasks are automatically removed from the internal tracking set (_tasks) when they finish, using add_done_callback.
# Centralized Management:
#
# The factory keeps track of all tasks, allowing you to:
# Check currently running tasks with get_running_tasks.
# Wait for all tasks to finish with wait_all.
# Error Handling:
#
# In wait_all, exceptions are returned as part of the results. You can process or log them if needed.
# endregion

# region Wait For
async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')
async def main8():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=5.0)
    except TimeoutError:
        print('timeout!')

#asyncio.run(main8())
# endregion

# region Lock Acquire Release
lock = asyncio.Lock()

async def main8():
    async with lock:
        await asyncio.sleep(1)
        print(f"started main at {time.strftime('%X')}")
        lock = asyncio.Lock()

        # ... later
        await lock.acquire()
        try:
            if lock.locked():
                print("lock was acquired")
        finally:
            lock.release()
#asyncio.run(main8())
# endregion

# region Await Event Task Create Task
async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # Create an Event object.
    event = asyncio.Event()
    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))
    await asyncio.sleep(1)

    event.set()
    # Wait until the waiter task is finished.
    await waiter_task

#asyncio.run(main())
# endregion

# region Cancel Task
async def cancel_me():
    print('cancel_me(): before sleep')

    try:
        # Wait for 1 hour
        await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print('cancel_me(): cancel sleep')
        raise
    finally:
        print('cancel_me(): after sleep')

async def main():
    # Create a "cancel_me" Task
    task = asyncio.create_task(cancel_me())

    # Wait for 1 second
    await asyncio.sleep(1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("main(): cancel_me is cancelled now")

#asyncio.run(main())
# endregion

# region Semaphore
import asyncio

# Semaphore to limit concurrency to 10
sem = asyncio.Semaphore(10)

async def worker(task_id):
    async with sem:  # Acquire semaphore using `async with`
        print(f"Task {task_id} is working...")
        await asyncio.sleep(10)
        print(f"Task {task_id} is done.")

async def main12():
    # Create 20 worker tasks
    tasks = [asyncio.create_task(worker(i)) for i in range(20)]
    await asyncio.gather(*tasks)

asyncio.run(main12())
# Run the program

# endregion

# region Queue Gather Task Cancell,Get Item from Queue
import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


#asyncio.run(main())
# endregion

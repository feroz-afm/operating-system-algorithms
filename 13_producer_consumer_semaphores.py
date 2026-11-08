"""Producer-Consumer Problem using Semaphores (Bounded-Buffer Problem).

Description:
    The Producer-Consumer problem is a foundational synchronization paradigm.
    One or more producer threads generate data and place it into a fixed-capacity
    buffer, while one or more consumer threads retrieve data from the buffer.

Synchronization Invariants:
    1. Mutual Exclusion: At most one thread can manipulate the buffer at any instant.
    2. Buffer Overflow Prevention: A producer must block when the buffer is full.
    3. Buffer Underflow Prevention: A consumer must block when the buffer is empty.

Classic Semaphore Solution (Dijkstra):
    - mutex (Binary Semaphore initialized to 1): Provides critical section mutual exclusion.
    - empty (Counting Semaphore initialized to CAPACITY): Tracks available buffer slots.
    - full  (Counting Semaphore initialized to 0): Tracks populated buffer slots.

Producer Algorithm:
    item = produce_item()
    empty.acquire()       # Wait if buffer is full
    mutex.acquire()       # Lock buffer access
    buffer.append(item)
    mutex.release()       # Unlock buffer
    full.release()        # Signal available item to consumers

Consumer Algorithm:
    full.acquire()        # Wait if buffer is empty
    mutex.acquire()       # Lock buffer access
    item = buffer.pop(0)
    mutex.release()       # Unlock buffer
    empty.release()       # Signal freed slot to producers
    consume_item(item)

Complexity:
    - Time Complexity: O(1) per produce/consume operation.
    - Space Complexity: O(CAPACITY) bounded by buffer size.

Practical Use:
    OS pipe buffers (IPC), print spoolers, audio streaming ring buffers, and
    asynchronous messaging queues.
"""

import time
import random
import threading
from typing import List


BUFFER_CAPACITY = 4
TOTAL_ITEMS_TO_PRODUCE = 8

# Synchronization primitives
buffer: List[int] = []
mutex = threading.Semaphore(1)
empty = threading.Semaphore(BUFFER_CAPACITY)
full = threading.Semaphore(0)

# Logging lock for clean console output
print_lock = threading.Lock()


def safe_log(msg: str) -> None:
    """Thread-safe logging utility."""
    with print_lock:
        print(msg)


def producer(producer_id: int, num_items: int) -> None:
    """Producer thread routine."""
    for i in range(1, num_items + 1):
        item = producer_id * 100 + i
        time.sleep(random.uniform(0.02, 0.05))  # Simulate production time

        empty.acquire()  # Wait for an empty slot
        mutex.acquire()  # Protect buffer manipulation

        buffer.append(item)
        safe_log(
            f"[Producer {producer_id}] Produced item {item:>3} | "
            f"Buffer: {buffer} ({len(buffer)}/{BUFFER_CAPACITY})"
        )

        mutex.release()  # Release lock
        full.release()   # Increment filled count


def consumer(consumer_id: int, num_items: int) -> None:
    """Consumer thread routine."""
    for _ in range(num_items):
        full.acquire()   # Wait for an available item
        mutex.acquire()  # Protect buffer manipulation

        item = buffer.pop(0)
        safe_log(
            f"  [Consumer {consumer_id}] Consumed item {item:>3} | "
            f"Buffer: {buffer} ({len(buffer)}/{BUFFER_CAPACITY})"
        )

        mutex.release()  # Release lock
        empty.release()  # Increment empty count

        time.sleep(random.uniform(0.03, 0.06))  # Simulate processing time


if __name__ == "__main__":
    print("=" * 65)
    print("Producer-Consumer Simulation using Semaphores")
    print(f"Buffer Capacity: {BUFFER_CAPACITY} | Total Items: {TOTAL_ITEMS_TO_PRODUCE}")
    print("=" * 65)

    # 2 Producers producing 4 items each, 2 Consumers consuming 4 items each
    producers = [
        threading.Thread(target=producer, args=(1, 4), name="Producer-1"),
        threading.Thread(target=producer, args=(2, 4), name="Producer-2"),
    ]

    consumers = [
        threading.Thread(target=consumer, args=(1, 4), name="Consumer-1"),
        threading.Thread(target=consumer, args=(2, 4), name="Consumer-2"),
    ]

    for c in consumers:
        c.start()
    for p in producers:
        p.start()

    for p in producers:
        p.join()
    for c in consumers:
        c.join()

    print("=" * 65)
    print("Simulation completed successfully. Buffer is safely empty.")
    print(f"Final Buffer State: {buffer}")
    print("=" * 65)

"""Readers-Writers Problem (Shared & Exclusive Synchronization).

Description:
    The Readers-Writers problem models access to a shared resource (such as a database
    record or file) by multiple concurrent processes:
    - Readers: Only read data; multiple readers may access the resource simultaneously.
    - Writers: Modify data; only one writer may access the resource at any given time,
      and no reader may read while a write is underway.

Classic Solution (First Readers-Writers / Readers-Preference):
    - read_count: Integer tracking active readers currently reading.
    - mutex: Binary semaphore/lock protecting access to read_count.
    - rw_mutex: Binary semaphore/lock ensuring mutual exclusion between writers and
      exclusive access over readers.

Reader Routine:
    1. Acquire `mutex`.
    2. Increment `read_count`. If this is the FIRST reader (read_count == 1), acquire `rw_mutex`
       to lock out any writers.
    3. Release `mutex`.
    4. [CRITICAL SECTION] Read shared resource concurrently with other readers.
    5. Acquire `mutex`.
    6. Decrement `read_count`. If this is the LAST reader (read_count == 0), release `rw_mutex`
       so waiting writers can proceed.
    7. Release `mutex`.

Writer Routine:
    1. Acquire `rw_mutex` (waits if readers are reading or another writer is writing).
    2. [CRITICAL SECTION] Write/modify shared resource exclusively.
    3. Release `rw_mutex`.

Complexity:
    - Time Complexity: O(1) for lock acquisition and release checks.
    - Space Complexity: O(1) auxiliary state variables.

Trade-offs & Variants:
    - Readers Preference: High reader throughput, but writers can suffer from starvation
      if a continuous stream of readers keeps read_count > 0.
    - Fair / Writers-Preference Variant: Prevents writer starvation by having waiting writers
      block incoming new readers.
    - Practical Use: Database read-replicas, file system read/write locks (POSIX pthread_rwlock).
"""

import time
import random
import threading
from typing import List


# Shared data resource
shared_resource = {"version": 0, "content": "Initial Data"}

# Synchronization primitives
read_count = 0
mutex = threading.Lock()     # Protects read_count
rw_mutex = threading.Lock()  # Protects shared_resource access
print_lock = threading.Lock()


def safe_log(msg: str) -> None:
    """Thread-safe logging utility."""
    with print_lock:
        print(msg)


def reader(reader_id: int, total_reads: int) -> None:
    """Reader thread routine."""
    global read_count

    for _ in range(total_reads):
        time.sleep(random.uniform(0.01, 0.03))

        # Reader entry protocol
        with mutex:
            read_count += 1
            if read_count == 1:
                rw_mutex.acquire()  # First reader blocks writers

        # Reading Critical Section
        safe_log(
            f"  [Reader {reader_id}] READ resource: {shared_resource['content']!r} "
            f"(v{shared_resource['version']}) | Active Readers: {read_count}"
        )
        time.sleep(random.uniform(0.01, 0.03))  # Simulate reading

        # Reader exit protocol
        with mutex:
            read_count -= 1
            if read_count == 0:
                rw_mutex.release()  # Last reader releases lock for writers

        time.sleep(random.uniform(0.01, 0.02))


def writer(writer_id: int, total_writes: int) -> None:
    """Writer thread routine."""
    for i in range(1, total_writes + 1):
        time.sleep(random.uniform(0.02, 0.04))

        # Writer entry protocol (exclusive lock)
        rw_mutex.acquire()
        try:
            # Writing Critical Section
            shared_resource["version"] += 1
            new_value = f"Data-Update-by-W{writer_id}-({i})"
            shared_resource["content"] = new_value
            safe_log(
                f"[Writer {writer_id}] *** WROTE *** -> {new_value!r} "
                f"(v{shared_resource['version']}) [Exclusive Lock Active]"
            )
            time.sleep(random.uniform(0.02, 0.04))  # Simulate write latency
        finally:
            rw_mutex.release()


if __name__ == "__main__":
    print("=" * 70)
    print("Readers-Writers Problem Simulation (First Readers-Writers)")
    print("Invariants: Multiple Readers concurrent; Writers strictly exclusive")
    print("=" * 70)

    # Launch 4 Readers and 2 Writers
    readers = [
        threading.Thread(target=reader, args=(i, 2), name=f"Reader-{i}")
        for i in range(1, 5)
    ]
    writers = [
        threading.Thread(target=writer, args=(i, 2), name=f"Writer-{i}")
        for i in range(1, 3)
    ]

    for t in readers + writers:
        t.start()

    for t in readers + writers:
        t.join()

    print("=" * 70)
    print("Simulation finished. Final shared resource state:")
    print(shared_resource)
    print("=" * 70)

"""Peterson's Algorithm for Mutual Exclusion.

Description:
    Peterson's Algorithm (1981) is a classic software-based solution to the mutual
    exclusion problem for two concurrent processes. It guarantees that two processes
    can share a single-use resource without conflicts, using only shared memory variables.

Shared Variables:
    - flag: An array of two booleans [flag[0], flag[1]]. flag[i] = True indicates
      that Process i wishes to enter its Critical Section.
    - turn: An integer (0 or 1) indicating whose turn it is to enter if both processes
      compete simultaneously.

Protocol for Process i (where j = 1 - i is the peer process):
    Entry Section:
        flag[i] = True         # Declare intent to enter
        turn = j               # Yield priority to peer
        while flag[j] and turn == j:
            pass               # Busy-wait (spin) while peer wants to enter and it's peer's turn

    Critical Section:
        # Exclusive access guaranteed here!

    Exit Section:
        flag[i] = False        # Relinquish desire to remain in critical section

Formal Correctness Proof:
    1. Mutual Exclusion: For both P0 and P1 to be in the critical section simultaneously,
       both flag[0] and flag[1] must be True, and turn must equal both 0 and 1 simultaneously,
       which is impossible.
    2. Progress Requirement: A process waiting outside cannot prevent the other from entering.
    3. Bounded Waiting: Once Pi sets turn = j, Pj can enter at most once before Pi gets its turn.

Architectural Note:
    Peterson's algorithm assumes sequential memory consistency. On modern out-of-order
    hardware (x86/ARM), memory barriers (fences) are required to prevent instruction
    reordering across the flag and turn assignments.

Complexity:
    - Time Complexity: O(1) entry/exit overhead (subject to busy-waiting under contention).
    - Space Complexity: O(1) auxiliary shared variables.
"""

import time
import threading
from typing import List


# Shared state for Peterson's Algorithm
flag = [False, False]
turn = 0

# Shared resource protected by Peterson's algorithm
shared_counter = 0
ITERATIONS_PER_THREAD = 1000

# Concurrency tracking
violations = 0
in_critical_section = [False, False]


def process(proc_id: int, iterations: int) -> None:
    """Simulates Process 0 or Process 1 using Peterson's Algorithm."""
    global turn, shared_counter, violations
    peer_id = 1 - proc_id

    for _ in range(iterations):
        # --- Entry Section ---
        flag[proc_id] = True
        turn = peer_id
        while flag[peer_id] and turn == peer_id:
            # Busy-wait / yield CPU slice
            time.sleep(0)

        # --- Critical Section ---
        in_critical_section[proc_id] = True
        if in_critical_section[peer_id]:
            violations += 1  # Mutual exclusion violated!

        # Modify shared state
        current = shared_counter
        # Small delay to expose potential race conditions if lock fails
        time.sleep(0.00001)
        shared_counter = current + 1

        in_critical_section[proc_id] = False
        # --- Exit Section ---
        flag[proc_id] = False

        # Remainder section
        time.sleep(0.00001)


if __name__ == "__main__":
    print("=" * 65)
    print("Peterson's Algorithm Mutual Exclusion Simulation")
    print(f"Two threads incrementing shared_counter {ITERATIONS_PER_THREAD} times each.")
    print("Expected final count without race conditions: 2000")
    print("=" * 65)

    t0 = threading.Thread(target=process, args=(0, ITERATIONS_PER_THREAD), name="Process-0")
    t1 = threading.Thread(target=process, args=(1, ITERATIONS_PER_THREAD), name="Process-1")

    t0.start()
    t1.start()

    t0.join()
    t1.join()

    print(f"Final Shared Counter Value : {shared_counter}")
    print(f"Mutual Exclusion Violations: {violations}")

    if shared_counter == 2 * ITERATIONS_PER_THREAD and violations == 0:
        print("[SUCCESS] Mutual exclusion strictly preserved! No race conditions.")
    else:
        print("[FAILURE] Race conditions or mutual exclusion violations detected!")
    print("=" * 65)

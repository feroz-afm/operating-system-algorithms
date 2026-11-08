"""Dining Philosophers Problem (Concurrency & Deadlock Prevention).

Description:
    The Dining Philosophers problem, originally formulated by Edsger Dijkstra, is a classic
    synchronization challenge illustrating allocation of shared resources among concurrent
    processes without deadlock or starvation.

The Problem:
    Five philosophers spend their lives thinking and eating. They sit around a circular table
    with five bowls of rice and five chopsticks (one chopstick between each adjacent pair).
    A philosopher requires BOTH the left and right chopsticks to eat.

The Deadlock Threat:
    If all five philosophers get hungry simultaneously and pick up their left chopstick first,
    every chopstick is held, and all philosophers block indefinitely waiting for their right
    chopstick -> Circular Wait Deadlock!

Deadlock Prevention Strategy (Asymmetric Resource Hierarchy):
    To break the Circular Wait condition:
    - Philosophers with an even ID pick up their LEFT chopstick first, then their RIGHT.
    - Philosophers with an odd ID pick up their RIGHT chopstick first, then their LEFT.
    Because adjacent philosophers compete for the same chopstick in reversed priority,
    at least one philosopher is always guaranteed to acquire both chopsticks, eliminating deadlock.

Complexity:
    - Time Complexity: O(1) per chopstick acquire/release attempt.
    - Space Complexity: O(N) where N is the number of philosophers and chopsticks.

Practical Use:
    Managing shared non-preemptible hardware channels, distributed database locks, and
    preventing circular waits in multi-resource kernels.
"""

import time
import random
import threading
from typing import List


NUM_PHILOSOPHERS = 5
MEALS_PER_PHILOSOPHER = 2

# One lock per chopstick
chopsticks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
print_lock = threading.Lock()


def safe_log(msg: str) -> None:
    """Thread-safe logging utility."""
    with print_lock:
        print(msg)


def philosopher(phil_id: int, total_meals: int) -> None:
    """Simulates a philosopher thinking, picking up chopsticks, eating, and releasing them."""
    left_fork = phil_id
    right_fork = (phil_id + 1) % NUM_PHILOSOPHERS

    # Enforce Asymmetric Resource Ordering to break circular wait
    if phil_id % 2 == 0:
        first_fork, second_fork = left_fork, right_fork
    else:
        first_fork, second_fork = right_fork, left_fork

    meals_eaten = 0

    while meals_eaten < total_meals:
        # 1. Thinking
        safe_log(f"Philosopher {phil_id} is THINKING.")
        time.sleep(random.uniform(0.01, 0.03))

        # 2. Hungry - Attempt to acquire chopsticks
        safe_log(f"Philosopher {phil_id} is HUNGRY (waiting for forks).")
        with chopsticks[first_fork]:
            with chopsticks[second_fork]:
                # 3. Eating
                meals_eaten += 1
                safe_log(
                    f"--> Philosopher {phil_id} is EATING (Meal {meals_eaten}/{total_meals}) "
                    f"using forks {first_fork} and {second_fork}."
                )
                time.sleep(random.uniform(0.02, 0.04))

        safe_log(f"Philosopher {phil_id} finished meal {meals_eaten} and put down forks.")

    safe_log(f"=== Philosopher {phil_id} is satisfied and leaving the table. ===")


if __name__ == "__main__":
    print("=" * 65)
    print("Dining Philosophers Problem Simulation (Asymmetric Deadlock Prevention)")
    print(f"Philosophers: {NUM_PHILOSOPHERS} | Meals each: {MEALS_PER_PHILOSOPHER}")
    print("=" * 65)

    threads: List[threading.Thread] = []
    for i in range(NUM_PHILOSOPHERS):
        t = threading.Thread(target=philosopher, args=(i, MEALS_PER_PHILOSOPHER), name=f"Phil-{i}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("=" * 65)
    print("All philosophers ate successfully without deadlock or starvation!")
    print("=" * 65)

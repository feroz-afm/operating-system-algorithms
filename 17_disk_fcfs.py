"""First-Come, First-Served (FCFS) Disk Scheduling Algorithm.

Description:
    FCFS is the simplest secondary storage disk scheduling algorithm. The disk controller
    services I/O track requests strictly in the order of their arrival in the queue,
    regardless of the head's current position.

How It Works:
    1. Start at the initial disk head position.
    2. Read the next cylinder request from the FIFO queue.
    3. Calculate the absolute seek distance: |target_cylinder - current_cylinder|.
    4. Move the head to the target cylinder and accumulate total head movement.
    5. Repeat until all requests are serviced.

Complexity:
    - Time Complexity: O(N) where N is the number of disk track requests.
    - Space Complexity: O(1) auxiliary space beyond the request list.

Characteristics & Trade-offs:
    - Pros: Completely fair; zero risk of starvation since every request is eventually reached.
    - Cons: Highly inefficient; does not optimize head movement, often causing the arm
      to swing wildly back and forth across the platter surface, resulting in large seek times.
"""

from typing import List, Tuple


def disk_fcfs(
    requests: List[int], initial_head: int
) -> Tuple[List[int], List[int], int]:
    """Computes head movement using First-Come, First-Served disk scheduling.

    Args:
        requests: List of cylinder/track request integers.
        initial_head: Starting track position of the disk head.

    Returns:
        Tuple containing:
            - Full head trajectory path (including initial head).
            - List of individual seek step distances.
            - Total seek distance (total head movement).
    """
    path = [initial_head]
    seek_steps: List[int] = []
    current_head = initial_head

    for track in requests:
        distance = abs(track - current_head)
        seek_steps.append(distance)
        current_head = track
        path.append(current_head)

    total_seek = sum(seek_steps)
    return path, seek_steps, total_seek


def print_disk_results(path: List[int], seek_steps: List[int], total_seek: int) -> None:
    """Prints a formatted step-by-step table of disk head movements."""
    header = f"{'Step':<6} {'From Track':<12} {'To Track':<12} {'Seek Distance':<14}"
    print("\n" + "=" * len(header))
    print("FCFS Disk Scheduling Execution")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for i in range(len(seek_steps)):
        print(f"{i + 1:<6} {path[i]:<12} {path[i + 1]:<12} {seek_steps[i]:<14}")

    print("-" * len(header))
    print(f"Total Head Movement (Seek Time): {total_seek} cylinders")
    print(f"Average Seek Distance         : {total_seek / len(seek_steps):.2f} cylinders")
    print("=" * len(header))
    print(f"Head Trajectory: {' -> '.join(map(str, path))}")


if __name__ == "__main__":
    sample_requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head_start = 53

    print(f"Initial Head Position: {head_start}")
    print(f"Disk Request Queue   : {sample_requests}")

    trajectory, steps, total = disk_fcfs(sample_requests, head_start)
    print_disk_results(trajectory, steps, total)

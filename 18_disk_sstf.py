"""Shortest Seek Time First (SSTF) Disk Scheduling Algorithm.

Description:
    SSTF disk scheduling selects the pending request with the minimum seek time
    from the current head position. It is the disk-scheduling counterpart of the
    Shortest Job First (SJF) CPU scheduling algorithm.

How It Works:
    1. Maintain a list of unserviced cylinder requests.
    2. At each step, search the unserviced list for the cylinder with the smallest
       distance to the current head position: min(|track - current_head|).
    3. Tie-breaker: prefer lowest cylinder index or first encountered.
    4. Move the head to the selected cylinder, record the seek distance, and remove
       the cylinder from the pending list.
    5. Repeat until all requests are serviced.

Complexity:
    - Time Complexity: O(N^2) where N is the number of requests using simple scanning,
      or O(N log N) using a balanced binary search tree / dual heaps.
    - Space Complexity: O(N) to maintain the pending request set and trajectory path.

Characteristics & Trade-offs:
    - Pros: Substantially improves throughput and reduces average seek time compared to FCFS.
    - Cons: Prone to starvation for requests located far from the current head if new
      requests cluster around the current arm position.
"""

from typing import List, Tuple


def disk_sstf(
    requests: List[int], initial_head: int
) -> Tuple[List[int], List[int], int]:
    """Computes head movement using Shortest Seek Time First disk scheduling.

    Args:
        requests: List of cylinder/track request integers.
        initial_head: Starting track position of the disk head.

    Returns:
        Tuple containing:
            - Full head trajectory path (including initial head).
            - List of individual seek step distances.
            - Total seek distance.
    """
    pending = requests.copy()
    path = [initial_head]
    seek_steps: List[int] = []
    current_head = initial_head

    while pending:
        # Find pending request with minimum distance to current_head
        closest_track = min(pending, key=lambda t: (abs(t - current_head), t))
        distance = abs(closest_track - current_head)

        seek_steps.append(distance)
        current_head = closest_track
        path.append(current_head)
        pending.remove(closest_track)

    total_seek = sum(seek_steps)
    return path, seek_steps, total_seek


def print_disk_results(path: List[int], seek_steps: List[int], total_seek: int) -> None:
    """Prints a formatted step-by-step table of disk head movements."""
    header = f"{'Step':<6} {'From Track':<12} {'To Track':<12} {'Seek Distance':<14}"
    print("\n" + "=" * len(header))
    print("SSTF Disk Scheduling Execution")
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

    trajectory, steps, total = disk_sstf(sample_requests, head_start)
    print_disk_results(trajectory, steps, total)

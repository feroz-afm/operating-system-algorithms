"""SCAN (Elevator) Disk Scheduling Algorithm.

Description:
    The SCAN algorithm (commonly referred to as the Elevator Algorithm) moves the disk arm
    in a single direction across the platter surface, servicing pending requests as it
    encounters them. When the arm reaches the boundary of the disk (either track 0 or the
    maximum cylinder), it reverses direction and services requests while traveling back.

How It Works:
    1. Divide requests into two partitions relative to the initial head:
       - left: cylinders smaller than initial head
       - right: cylinders greater than initial head
    2. Sort both partitions.
    3. If direction is "HIGH" (towards higher track numbers):
       a. Service right partition in ascending order.
       b. Travel to the end cylinder (disk_max).
       c. Reverse direction and service left partition in descending order.
    4. If direction is "LOW" (towards lower track numbers):
       a. Service left partition in descending order.
       b. Travel to the beginning cylinder (disk_min, usually 0).
       c. Reverse direction and service right partition in ascending order.
    5. Calculate cumulative seek distances along the trajectory.

Complexity:
    - Time Complexity: O(N log N) dominated by sorting the request lists.
    - Space Complexity: O(N) to store partitions and path coordinates.

Characteristics & Trade-offs:
    - Pros: Prevents starvation; provides far more uniform wait times than SSTF.
    - Cons: Requests at the opposite extreme of the reversal point may wait longer
      if newly arrived requests concentrate at the center.
"""

from typing import List, Tuple


def disk_scan(
    requests: List[int],
    initial_head: int,
    direction: str = "HIGH",
    disk_min: int = 0,
    disk_max: int = 199,
) -> Tuple[List[int], List[int], int]:
    """Computes head trajectory using the SCAN (Elevator) algorithm.

    Args:
        requests: List of cylinder requests.
        initial_head: Starting head position.
        direction: Direction of arm movement ('HIGH' for upwards, 'LOW' for downwards).
        disk_min: Minimum cylinder boundary (default 0).
        disk_max: Maximum cylinder boundary (default 199).

    Returns:
        Tuple containing:
            - Full head trajectory path.
            - Seek step distances.
            - Total seek distance.
    """
    left = sorted([r for r in requests if r < initial_head])
    right = sorted([r for r in requests if r >= initial_head])

    path = [initial_head]
    current_head = initial_head

    if direction.upper() == "HIGH":
        # Service upward requests, hit upper boundary, reverse and service downward
        for track in right:
            path.append(track)
        if disk_max not in path and left:
            path.append(disk_max)
        for track in reversed(left):
            path.append(track)
    else:
        # Service downward requests, hit lower boundary, reverse and service upward
        for track in reversed(left):
            path.append(track)
        if disk_min not in path and right:
            path.append(disk_min)
        for track in right:
            path.append(track)

    seek_steps: List[int] = []
    for i in range(len(path) - 1):
        seek_steps.append(abs(path[i + 1] - path[i]))

    total_seek = sum(seek_steps)
    return path, seek_steps, total_seek


def print_disk_results(
    path: List[int], seek_steps: List[int], total_seek: int, direction: str
) -> None:
    """Prints a formatted step-by-step table of disk head movements."""
    header = f"{'Step':<6} {'From Track':<12} {'To Track':<12} {'Seek Distance':<14}"
    print("\n" + "=" * len(header))
    print(f"SCAN (Elevator) Disk Scheduling Execution (Direction: {direction})")
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
    arm_direction = "HIGH"

    print(f"Initial Head Position: {head_start}")
    print(f"Disk Request Queue   : {sample_requests}")
    print(f"Arm Movement Direction: {arm_direction} (Disk range: 0 to 199)")

    trajectory, steps, total = disk_scan(
        sample_requests, head_start, direction=arm_direction, disk_min=0, disk_max=199
    )
    print_disk_results(trajectory, steps, total, arm_direction)

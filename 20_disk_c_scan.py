"""Circular SCAN (C-SCAN) Disk Scheduling Algorithm.

Description:
    Circular SCAN (C-SCAN) is a variant of SCAN designed to provide a more uniform
    waiting time for disk requests. Like SCAN, the disk arm moves in a single direction
    servicing requests until it reaches the disk boundary.

    Unlike SCAN, however, upon reaching the boundary, the arm immediately jumps back to
    the beginning of the disk without servicing any requests on the return trip.
    Once back at the start, it resumes servicing requests in the forward direction.
    This treats the cylinders as a circular list wrapping around from the final cylinder
    to the first.

How It Works:
    1. Divide requests into two partitions relative to initial head:
       - right: cylinders >= initial head
       - left: cylinders < initial head
    2. Sort both partitions in ascending order.
    3. If direction is "HIGH":
       a. Service right partition in ascending order.
       b. Travel to upper boundary (disk_max).
       c. Fast-return to lower boundary (disk_min, 0) without servicing.
       d. Service left partition in ascending order.
    4. Calculate seek distances for each move, including the reset return trip.

Complexity:
    - Time Complexity: O(N log N) due to sorting request partitions.
    - Space Complexity: O(N) to store partitions and trajectory coordinates.

Characteristics & Trade-offs:
    - Pros: More uniform wait times compared to standard SCAN; prevents bias toward
      cylinders near the reversal endpoints.
    - Cons: The return jump adds extra head travel distance, though modern disk drives
      can perform rapid seeks without active read head stabilization.
"""

from typing import List, Tuple


def disk_c_scan(
    requests: List[int],
    initial_head: int,
    direction: str = "HIGH",
    disk_min: int = 0,
    disk_max: int = 199,
) -> Tuple[List[int], List[int], int]:
    """Computes head trajectory using the Circular SCAN (C-SCAN) algorithm.

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

    if direction.upper() == "HIGH":
        # Service upward requests to boundary, jump to 0, service remaining upward
        for track in right:
            path.append(track)
        if disk_max not in path and left:
            path.append(disk_max)

        if left:
            path.append(disk_min)
            for track in left:
                path.append(track)
    else:
        # Service downward requests to 0, jump to max, service remaining downward
        for track in reversed(left):
            path.append(track)
        if disk_min not in path and right:
            path.append(disk_min)

        if right:
            path.append(disk_max)
            for track in reversed(right):
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
    header = f"{'Step':<6} {'From Track':<12} {'To Track':<12} {'Seek Distance':<14} {'Note':<16}"
    print("\n" + "=" * len(header))
    print(f"C-SCAN (Circular SCAN) Disk Scheduling (Direction: {direction})")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for i in range(len(seek_steps)):
        from_t = path[i]
        to_t = path[i + 1]
        dist = seek_steps[i]
        note = "Return Jump" if abs(from_t - to_t) > 150 else "Servicing"
        print(f"{i + 1:<6} {from_t:<12} {to_t:<12} {dist:<14} {note:<16}")

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

    trajectory, steps, total = disk_c_scan(
        sample_requests, head_start, direction=arm_direction, disk_min=0, disk_max=199
    )
    print_disk_results(trajectory, steps, total, arm_direction)

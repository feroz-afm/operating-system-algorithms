"""First-In, First-Out (FIFO) Page Replacement Algorithm.

Description:
    FIFO is the simplest page replacement algorithm. The operating system keeps track
    of all pages in memory in a queue. When a page needs to be replaced, the page at
    the head of the queue (the oldest page brought into memory) is selected as the victim.

How It Works:
    1. Allocate a fixed capacity of memory frames.
    2. For each page in the reference string:
       a. If the page is already present in frames -> PAGE HIT.
       b. If the page is missing -> PAGE FAULT:
          - If empty frame slots exist, append the page to frames.
          - If frames are full, evict the oldest page (FIFO order) and insert the new page.
    3. Track total faults, hits, and frame states at each reference step.

Belady's Anomaly:
    FIFO is susceptible to Belady's Anomaly, a counter-intuitive phenomenon where
    increasing the number of physical page frames results in MORE page faults for
    certain reference strings (e.g., [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]).

Complexity:
    - Time Complexity: O(N) where N is reference string length, using O(1) set lookup
      and deque pop/push.
    - Space Complexity: O(F) where F is the number of memory frames.

Practical Use:
    Simple embedded systems or buffer caches where low computational overhead is prioritized
    over hit ratio.
"""

from collections import deque
from typing import List, Tuple, Dict, Any


def fifo_page_replacement(
    pages: List[int], capacity: int
) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Simulates FIFO page replacement.

    Args:
        pages: List of memory page references.
        capacity: Number of available page frames in physical memory.

    Returns:
        Tuple containing:
            - Total page faults count.
            - Total page hits count.
            - Step-by-step history log list.
    """
    frames: deque = deque()
    frame_set = set()
    page_faults = 0
    page_hits = 0
    history: List[Dict[str, Any]] = []

    for step, page in enumerate(pages, start=1):
        if page in frame_set:
            status = "HIT"
            page_hits += 1
            evicted = None
        else:
            status = "FAULT"
            page_faults += 1
            if len(frames) < capacity:
                frames.append(page)
                frame_set.add(page)
                evicted = None
            else:
                evicted = frames.popleft()
                frame_set.remove(evicted)
                frames.append(page)
                frame_set.add(page)

        history.append({
            "step": step,
            "page": page,
            "status": status,
            "frames": list(frames),
            "evicted": evicted,
        })

    return page_faults, page_hits, history


def print_simulation_table(history: List[Dict[str, Any]], capacity: int) -> None:
    """Prints the step-by-step frame state table."""
    frame_headers = [f"F{i}" for i in range(capacity)]
    header = f"{'Step':<6} {'Page':<6} {'Status':<8} " + " ".join(f"{h:<6}" for h in frame_headers)
    print("\n" + "=" * len(header))
    print("FIFO Page Replacement - Step-by-Step Execution")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for entry in history:
        frame_cells = []
        for i in range(capacity):
            if i < len(entry["frames"]):
                frame_cells.append(f"{entry['frames'][i]:<6}")
            else:
                frame_cells.append(f"{'-':<6}")

        frame_str = " ".join(frame_cells)
        print(f"{entry['step']:<6} {entry['page']:<6} {entry['status']:<8} {frame_str}")

    print("-" * len(header))


def demonstrate_beladys_anomaly() -> None:
    """Demonstrates Belady's Anomaly using the classic reference string."""
    anomaly_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    print("\n" + "=" * 60)
    print("Demonstration of Belady's Anomaly in FIFO")
    print(f"Reference String: {anomaly_string}")
    print("=" * 60)

    for frames_count in [3, 4]:
        faults, hits, _ = fifo_page_replacement(anomaly_string, frames_count)
        print(f"Frames: {frames_count} -> Faults: {faults}, Hits: {hits}")

    print("Notice: Increasing frames from 3 to 4 increased faults from 9 to 10!")
    print("=" * 60)


if __name__ == "__main__":
    sample_pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    num_frames = 3

    print(f"Running FIFO Page Replacement Simulation (Frames: {num_frames})...")
    faults, hits, hist = fifo_page_replacement(sample_pages, num_frames)
    print_simulation_table(hist, num_frames)

    total_refs = len(sample_pages)
    print(f"\nTotal References: {total_refs}")
    print(f"Total Page Faults: {faults} (Fault Ratio: {(faults / total_refs) * 100:.2f}%)")
    print(f"Total Page Hits  : {hits} (Hit Ratio  : {(hits / total_refs) * 100:.2f}%)")

    # Run Belady's anomaly demonstration
    demonstrate_beladys_anomaly()

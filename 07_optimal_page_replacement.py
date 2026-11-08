"""Optimal (OPT / MIN / Belady's Algorithm) Page Replacement Algorithm.

Description:
    The Optimal Page Replacement algorithm (also known as OPT, MIN, or clairvoyant algorithm)
    replaces the page that will not be used for the longest period of time in the future.
    It provides the theoretical lowest possible page fault rate for a given reference string
    and frame capacity.

How It Works:
    1. Initialize an empty set of page frames with given capacity.
    2. For each page in the reference string:
       a. If the page is already in a frame -> PAGE HIT.
       b. If the page is not in a frame -> PAGE FAULT:
          - If empty frame slots are available, allocate one.
          - If all frames are occupied, inspect all currently loaded pages and find when
            each page will next be referenced in the future.
          - Select the page whose next reference occurs furthest in the future (or never).
          - Evict that page and place the new page in its frame.
    3. Track total faults, hits, and frame transitions.

Complexity:
    - Time Complexity: O(N * F * N) in naive scanning or O(N * F) where N is reference string
      length and F is the number of frames.
    - Space Complexity: O(F) for frames and O(N) for future occurrence lookup tables.

Characteristics & Trade-offs:
    - Optimality: Provably optimal; impossible to produce more page faults than FIFO or LRU.
    - Belady's Anomaly Free: OPT is a stack algorithm and does not suffer from Belady's anomaly.
    - Real-world Limitation: Impossible to implement in general-purpose operating systems because
      the kernel cannot predict future page accesses. It is primarily used as an offline
      benchmark to measure how closely practical algorithms (like LRU) approach optimality.
"""

from typing import Any, Dict, List, Optional, Tuple


def optimal_page_replacement(
    pages: List[int], capacity: int
) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Simulates the Optimal (Belady's MIN) page replacement algorithm.

    Args:
        pages: List of integer page numbers referenced sequentially.
        capacity: Number of available page frames in physical memory.

    Returns:
        Tuple containing:
            - Total page faults.
            - Total page hits.
            - Step-by-step history log list.
    """
    frames: List[int] = []
    page_faults = 0
    page_hits = 0
    history: List[Dict[str, Any]] = []

    n = len(pages)

    for i, page in enumerate(pages):
        evicted: Optional[int] = None

        if page in frames:
            status = "HIT"
            page_hits += 1
        else:
            status = "FAULT"
            page_faults += 1

            if len(frames) < capacity:
                frames.append(page)
            else:
                # Find the victim page whose next reference is furthest in the future
                furthest_next_use = -1
                victim_idx = -1

                for f_idx, loaded_page in enumerate(frames):
                    # Search future occurrences
                    try:
                        next_use = pages[i + 1 :].index(loaded_page)
                    except ValueError:
                        # Page is never used again in the future; best possible victim
                        next_use = float("inf")

                    if next_use > furthest_next_use:
                        furthest_next_use = next_use
                        victim_idx = f_idx

                evicted = frames[victim_idx]
                frames[victim_idx] = page

        history.append({
            "step": i + 1,
            "page": page,
            "status": status,
            "frames": list(frames),
            "evicted": evicted,
        })

    return page_faults, page_hits, history


def print_simulation_table(history: List[Dict[str, Any]], capacity: int) -> None:
    """Displays a formatted table of execution history."""
    frame_headers = [f"F{i}" for i in range(capacity)]
    header = (
        f"{'Step':<6} {'Page':<6} {'Status':<8} "
        + " ".join(f"{h:<6}" for h in frame_headers)
        + f" {'Evicted':<8}"
    )
    print("\n" + "=" * len(header))
    print("Optimal (OPT) Page Replacement - Step-by-Step Execution")
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
        evicted_str = str(entry["evicted"]) if entry["evicted"] is not None else "-"
        print(f"{entry['step']:<6} {entry['page']:<6} {entry['status']:<8} {frame_str} {evicted_str:<8}")

    print("-" * len(header))


if __name__ == "__main__":
    sample_pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    num_frames = 3

    print(f"Running Optimal Page Replacement Simulation (Frames: {num_frames})...")
    faults, hits, hist = optimal_page_replacement(sample_pages, num_frames)
    print_simulation_table(hist, num_frames)

    total_refs = len(sample_pages)
    print(f"\nTotal References: {total_refs}")
    print(f"Total Page Faults: {faults} (Fault Ratio: {(faults / total_refs) * 100:.2f}%)")
    print(f"Total Page Hits  : {hits} (Hit Ratio  : {(hits / total_refs) * 100:.2f}%)")
    print("\nNotice how Optimal Page Replacement yields fewer faults than FIFO on the same reference string!")

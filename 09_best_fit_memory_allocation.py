"""Best-Fit Contiguous Memory Allocation Algorithm.

Description:
    Best-Fit is a contiguous memory allocation strategy that allocates the smallest
    free partition/hole that is big enough to satisfy the requested process size.
    It minimizes the leftover fragment size created in the chosen block.

How It Works:
    1. Given a list of available memory blocks and a sequence of process requests.
    2. For each incoming process:
       a. Search all free memory blocks where block_size >= process_size.
       b. Among valid candidates, select the block with the minimum (block_size - process_size).
       c. If found:
          - Allocate the process to this block.
          - Reduce the block's size by process_size.
       d. If no block can fit the process, mark it as "Not Allocated".
    3. Output the allocation mapping, internal fragments, and remaining memory layout.

Complexity:
    - Time Complexity: O(N * M) where N is the number of processes and M is the number
      of memory blocks, because every block must be examined to find the absolute minimum fit
      (unless blocks are organized in an ordered tree/heap: O(N log M)).
    - Space Complexity: O(M + N) to maintain partition sizes and allocation status.

Characteristics & Trade-offs:
    - Pros: Minimizes wasted space in the chosen block; leaves large blocks available
      for larger processes.
    - Cons: Tends to create many tiny, unusable fragment holes scattered throughout memory
      (severe external fragmentation), and requires a full scan of all blocks.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class AllocationResult:
    process_id: int
    process_size: int
    block_id: Optional[int]
    initial_block_size: Optional[int]
    remaining_block_size: Optional[int]


def best_fit_allocation(
    block_sizes: List[int], process_sizes: List[int]
) -> Tuple[List[AllocationResult], List[int]]:
    """Allocates memory blocks to processes using the Best-Fit algorithm.

    Args:
        block_sizes: List of available memory block sizes.
        process_sizes: List of memory sizes requested by processes.

    Returns:
        Tuple containing:
            - List of AllocationResult objects.
            - Final state of memory blocks after allocations.
    """
    remaining_blocks = block_sizes.copy()
    results: List[AllocationResult] = []

    for p_id, p_size in enumerate(process_sizes, start=1):
        best_block_idx = -1
        min_waste = float("inf")

        # Scan all blocks to find the smallest valid hole
        for b_idx, b_size in enumerate(remaining_blocks):
            if b_size >= p_size:
                waste = b_size - p_size
                if waste < min_waste:
                    min_waste = waste
                    best_block_idx = b_idx

        if best_block_idx != -1:
            init_size = remaining_blocks[best_block_idx]
            remaining_blocks[best_block_idx] -= p_size
            results.append(
                AllocationResult(
                    process_id=p_id,
                    process_size=p_size,
                    block_id=best_block_idx + 1,
                    initial_block_size=init_size,
                    remaining_block_size=remaining_blocks[best_block_idx],
                )
            )
        else:
            results.append(
                AllocationResult(
                    process_id=p_id,
                    process_size=p_size,
                    block_id=None,
                    initial_block_size=None,
                    remaining_block_size=None,
                )
            )

    return results, remaining_blocks


def print_allocation_table(results: List[AllocationResult], initial_blocks: List[int]) -> None:
    """Prints a structured table showing the memory allocation results."""
    header = f"{'Process No.':<14} {'Process Size':<14} {'Block Allocated':<18} {'Remaining Space':<16}"
    print("\n" + "=" * len(header))
    print("Memory Allocation Results: Best-Fit")
    print("=" * len(header))
    print(f"Initial Memory Blocks: {initial_blocks}")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    allocated_count = 0
    for r in results:
        b_str = f"Block {r.block_id}" if r.block_id is not None else "Not Allocated"
        rem_str = f"{r.remaining_block_size} KB" if r.remaining_block_size is not None else "N/A"
        if r.block_id is not None:
            allocated_count += 1
        print(f"P{r.process_id:<13} {r.process_size:<14} {b_str:<18} {rem_str:<16}")

    print("-" * len(header))
    print(f"Total Processes: {len(results)} | Successfully Allocated: {allocated_count} | Unallocated: {len(results) - allocated_count}")
    print("=" * len(header))


if __name__ == "__main__":
    sample_blocks = [100, 500, 200, 300, 600]
    sample_processes = [212, 417, 112, 426]

    print("Running Best-Fit Memory Allocation Simulation...")
    allocation_res, final_blocks = best_fit_allocation(sample_blocks, sample_processes)
    print_allocation_table(allocation_res, sample_blocks)
    print(f"\nFinal State of Memory Blocks: {final_blocks}")

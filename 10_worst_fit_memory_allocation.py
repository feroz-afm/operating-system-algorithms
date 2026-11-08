"""Worst-Fit Contiguous Memory Allocation Algorithm.

Description:
    Worst-Fit is a contiguous memory allocation strategy that allocates the largest
    available memory partition/hole to the incoming process.

How It Works:
    1. Given a list of available memory blocks and a sequence of process requests.
    2. For each incoming process:
       a. Search all free memory blocks to find the largest block where block_size >= process_size.
       b. If found:
          - Allocate the process to this maximum-capacity block.
          - Decrement the block size by process_size.
          - The remaining leftover hole is maximized, with the goal that the leftover
            portion remains large enough to house future processes.
       c. If the largest available block cannot accommodate the process, mark it as "Not Allocated".
    3. Output the allocation status and final memory layout.

Complexity:
    - Time Complexity: O(N * M) where N is the number of processes and M is the number
      of memory blocks, because every block must be searched to find the absolute maximum size
      (or O(N log M) with a max-heap).
    - Space Complexity: O(M + N) to maintain partition sizes and allocation status.

Characteristics & Trade-offs:
    - Pros: Prevents the creation of many tiny, unusable sliver fragments (which occurs in Best-Fit).
    - Cons: Rapidly fragments and exhausts large contiguous blocks of memory, often causing
      large subsequent processes to be rejected even when total free memory is substantial.
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


def worst_fit_allocation(
    block_sizes: List[int], process_sizes: List[int]
) -> Tuple[List[AllocationResult], List[int]]:
    """Allocates memory blocks to processes using the Worst-Fit algorithm.

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
        worst_block_idx = -1
        max_size = -1

        # Scan all blocks to find the largest valid hole
        for b_idx, b_size in enumerate(remaining_blocks):
            if b_size >= p_size and b_size > max_size:
                max_size = b_size
                worst_block_idx = b_idx

        if worst_block_idx != -1:
            init_size = remaining_blocks[worst_block_idx]
            remaining_blocks[worst_block_idx] -= p_size
            results.append(
                AllocationResult(
                    process_id=p_id,
                    process_size=p_size,
                    block_id=worst_block_idx + 1,
                    initial_block_size=init_size,
                    remaining_block_size=remaining_blocks[worst_block_idx],
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
    print("Memory Allocation Results: Worst-Fit")
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

    print("Running Worst-Fit Memory Allocation Simulation...")
    allocation_res, final_blocks = worst_fit_allocation(sample_blocks, sample_processes)
    print_allocation_table(allocation_res, sample_blocks)
    print(f"\nFinal State of Memory Blocks: {final_blocks}")

"""First-Fit Contiguous Memory Allocation Algorithm.

Description:
    First-Fit is a dynamic memory allocation strategy used by operating systems
    to place processes into variable-sized memory partitions. It scans available
    memory blocks from the beginning and allocates the first hole that is large
    enough to accommodate the incoming process.

How It Works:
    1. Given a list of free memory blocks and a list of process requests.
    2. For each process request:
       a. Iterate through memory blocks from index 0 to M - 1.
       b. Find the first block where block_size >= process_size.
       c. If found:
          - Assign the process to this block.
          - Decrement the available size of the block by process_size (remaining space
            forms an updated free hole, minimizing fragmentation delay).
       d. If no block is large enough, mark the process as "Not Allocated" (waiting).
    3. Output the allocation status and remaining block fragmentations.

Complexity:
    - Time Complexity: O(N * M) worst-case, where N is the number of processes and M
      is the number of memory blocks. In practice, it terminates as soon as the first
      fit is encountered, making it faster than Best-Fit.
    - Space Complexity: O(M + N) to maintain partition sizes and allocation mapping.

Characteristics & Trade-offs:
    - Pros: Fast execution speed since it does not require exhaustive scanning of all blocks.
    - Cons: Tends to concentrate small unusable holes at the beginning of the memory space
      (external fragmentation), forcing subsequent allocations to scan further.
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


def first_fit_allocation(
    block_sizes: List[int], process_sizes: List[int]
) -> Tuple[List[AllocationResult], List[int]]:
    """Allocates memory blocks to processes using the First-Fit algorithm.

    Args:
        block_sizes: List of available memory block sizes.
        process_sizes: List of memory sizes requested by processes.

    Returns:
        Tuple containing:
            - List of AllocationResult objects.
            - Final state of memory blocks after allocations.
    """
    remaining_blocks = block_sizes.copy()
    initial_blocks = block_sizes.copy()
    results: List[AllocationResult] = []

    for p_id, p_size in enumerate(process_sizes, start=1):
        allocated_block_id = None
        init_size = None
        rem_size = None

        for b_id, b_size in enumerate(remaining_blocks, start=1):
            if b_size >= p_size:
                allocated_block_id = b_id
                init_size = remaining_blocks[b_id - 1]
                remaining_blocks[b_id - 1] -= p_size
                rem_size = remaining_blocks[b_id - 1]
                break

        results.append(
            AllocationResult(
                process_id=p_id,
                process_size=p_size,
                block_id=allocated_block_id,
                initial_block_size=init_size,
                remaining_block_size=rem_size,
            )
        )

    return results, remaining_blocks


def print_allocation_table(results: List[AllocationResult], initial_blocks: List[int]) -> None:
    """Prints a structured table showing the memory allocation results."""
    header = f"{'Process No.':<14} {'Process Size':<14} {'Block Allocated':<18} {'Remaining Space':<16}"
    print("\n" + "=" * len(header))
    print("Memory Allocation Results: First-Fit")
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

    print("Running First-Fit Memory Allocation Simulation...")
    allocation_res, final_blocks = first_fit_allocation(sample_blocks, sample_processes)
    print_allocation_table(allocation_res, sample_blocks)
    print(f"\nFinal State of Memory Blocks: {final_blocks}")

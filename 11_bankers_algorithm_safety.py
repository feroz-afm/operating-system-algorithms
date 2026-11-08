"""Banker's Algorithm for Deadlock Avoidance (Safety & Resource-Request).

Description:
    The Banker's Algorithm, developed by Edsger Dijkstra, is a classic deadlock
    avoidance algorithm. When a process requests resources, the system simulates
    the allocation and determines whether granting the request leaves the system
    in a "Safe State". If safe, resources are allocated; otherwise, the process waits.

Core Data Structures:
    - Available[j]: Number of instances of resource type Rj currently free.
    - Max[i][j]: Maximum instances of Rj that process Pi may claim.
    - Allocation[i][j]: Instances of Rj currently allocated to process Pi.
    - Need[i][j]: Remaining instances of Rj needed by Pi (Need = Max - Allocation).

Safety Algorithm:
    1. Initialize Work = Available.copy() and Finish = [False] * N.
    2. Find an index i such that:
       Finish[i] == False and Need[i] <= Work
    3. If found:
       Work += Allocation[i]
       Finish[i] = True
       Append Pi to safe sequence.
       Repeat Step 2.
    4. If Finish[i] == True for all i, system is SAFE. Otherwise, UNSAFE.

Resource-Request Algorithm:
    If process Pi requests vector Request_i:
    1. If Request_i <= Need[i], continue; else throw error (exceeded max claim).
    2. If Request_i <= Available, continue; else process must wait.
    3. Tentatively allocate:
       Available -= Request_i
       Allocation[i] += Request_i
       Need[i] -= Request_i
    4. Run Safety Algorithm.
       - If Safe -> Grant request permanently.
       - If Unsafe -> Rollback state and Pi waits.

Complexity:
    - Time Complexity: O(M * N^2) for the safety check, where N is number of processes
      and M is number of resource types.
    - Space Complexity: O(N * M) for resource tracking matrices.
"""

from typing import List, Optional, Tuple


class BankersAlgorithm:
    """Encapsulates the Banker's Algorithm state and algorithms."""

    def __init__(
        self,
        process_ids: List[str],
        available: List[int],
        max_matrix: List[List[int]],
        allocation_matrix: List[List[int]],
    ):
        self.pids = process_ids
        self.num_processes = len(process_ids)
        self.num_resources = len(available)

        self.available = available.copy()
        self.max_matrix = [row.copy() for row in max_matrix]
        self.allocation = [row.copy() for row in allocation_matrix]

        # Calculate Need = Max - Allocation
        self.need = [
            [self.max_matrix[i][j] - self.allocation[i][j] for j in range(self.num_resources)]
            for i in range(self.num_processes)
        ]

    def is_safe_state(self) -> Tuple[bool, List[str]]:
        """Executes the safety algorithm to find a safe sequence.

        Returns:
            Tuple of (is_safe: bool, safe_sequence: List[str]).
        """
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence: List[str] = []

        while len(safe_sequence) < self.num_processes:
            found_candidate = False

            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if Need[i] <= Work
                    if all(self.need[i][j] <= work[j] for j in range(self.num_resources)):
                        # Process can complete; reclaim its resources
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(self.pids[i])
                        found_candidate = True
                        break

            if not found_candidate:
                # No process could proceed -> system is in an unsafe state
                return False, []

        return True, safe_sequence

    def request_resources(
        self, process_idx: int, request: List[int]
    ) -> Tuple[bool, str, Optional[List[str]]]:
        """Evaluates whether a resource request from process_idx can be safely granted.

        Returns:
            Tuple of (granted: bool, explanation: str, safe_sequence: Optional[List[str]]).
        """
        pid = self.pids[process_idx]

        # Condition 1: Request <= Need
        if any(request[j] > self.need[process_idx][j] for j in range(self.num_resources)):
            return False, f"Error: {pid} requested more resources than its stated maximum need.", None

        # Condition 2: Request <= Available
        if any(request[j] > self.available[j] for j in range(self.num_resources)):
            return False, f"{pid} must wait: requested resources not currently available.", None

        # Tentative allocation
        for j in range(self.num_resources):
            self.available[j] -= request[j]
            self.allocation[process_idx][j] += request[j]
            self.need[process_idx][j] -= request[j]

        # Check safety of tentative state
        is_safe, safe_seq = self.is_safe_state()

        if is_safe:
            return True, f"Request granted! System remains in a SAFE state.", safe_seq
        else:
            # Rollback allocation
            for j in range(self.num_resources):
                self.available[j] += request[j]
                self.allocation[process_idx][j] -= request[j]
                self.need[process_idx][j] += request[j]
            return False, f"Request denied! Granting request leads to an UNSAFE state.", None

    def display_state(self) -> None:
        """Displays formatted Allocation, Max, Need, and Available matrices."""
        res_names = " ".join([f"R{j}" for j in range(self.num_resources)])
        print("\n" + "=" * 62)
        print("Banker's Algorithm System State")
        print("=" * 62)
        print(f"Available Resources: {self.available}")
        print("-" * 62)
        print(f"{'PID':<6} | {'Allocation':<14} | {'Max Claim':<14} | {'Need':<14}")
        print(f"{'':<6} | {res_names:<14} | {res_names:<14} | {res_names:<14}")
        print("-" * 62)

        for i in range(self.num_processes):
            alloc_str = " ".join(f"{x:2d}" for x in self.allocation[i])
            max_str = " ".join(f"{x:2d}" for x in self.max_matrix[i])
            need_str = " ".join(f"{x:2d}" for x in self.need[i])
            print(f"{self.pids[i]:<6} | {alloc_str:<14} | {max_str:<14} | {need_str:<14}")

        print("=" * 62)


if __name__ == "__main__":
    processes = ["P0", "P1", "P2", "P3", "P4"]
    # 3 resource types: A, B, C
    available_res = [3, 3, 2]

    max_req = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3],  # P4
    ]

    current_alloc = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2],  # P4
    ]

    banker = BankersAlgorithm(processes, available_res, max_req, current_alloc)
    banker.display_state()

    print("\n[Step 1] Checking Initial System Safety:")
    safe, sequence = banker.is_safe_state()
    if safe:
        print(f"-> System is SAFE! Safe Sequence: {' -> '.join(sequence)}")
    else:
        print("-> System is in an UNSAFE state (Deadlock possible).")

    print("\n[Step 2] Simulating Resource Request:")
    test_proc_idx = 1  # P1
    test_request = [1, 0, 2]
    print(f"Process {processes[test_proc_idx]} requests: {test_request}")

    granted, msg, seq = banker.request_resources(test_proc_idx, test_request)
    print(f"Result: {msg}")
    if granted and seq:
        print(f"New Safe Sequence: {' -> '.join(seq)}")
        banker.display_state()

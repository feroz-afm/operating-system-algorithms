"""Resource Allocation Graph (RAG) and Wait-For Graph (WFG) Deadlock Detection.

Description:
    In an operating system, resource allocations and requests can be modeled as a directed
    graph called the Resource Allocation Graph (RAG):
    - Process Nodes (P) and Resource Nodes (R).
    - Request Edge: Pi -> Rj (process Pi is requesting resource Rj and is blocked).
    - Assignment Edge: Rj -> Pi (resource Rj is currently held by process Pi).

    For single-unit resource systems, a cycle in the Resource Allocation Graph is both
    a necessary AND sufficient condition for deadlock.

    The RAG can be reduced to a Wait-For Graph (WFG) containing only process nodes:
    An edge Pi -> Pj exists if Pi is waiting for a resource currently held by Pj.
    Cycle detection on the WFG directly identifies all deadlocked processes.

How It Works:
    1. Construct graph adjacency list representing Wait-For dependencies between processes.
    2. Perform Depth-First Search (DFS) using 3-color marking:
       - WHITE (0): Unvisited node.
       - GRAY (1): Node currently on recursion stack (ancestor in active DFS branch).
       - BLACK (2): Completely visited node.
    3. If an edge reaches a GRAY node, a cycle (back-edge) is detected -> DEADLOCK!
    4. Reconstruct the cycle path to report the exact loop of waiting processes.

Complexity:
    - Time Complexity: O(V + E) where V is the number of processes and E is the number
      of wait-for edges.
    - Space Complexity: O(V + E) for adjacency list, color tracking, and parent pointers.

Practical Use:
    Kernel deadlock detection threads (e.g., in databases or OS transaction engines)
    periodically construct wait-for graphs and abort or roll back victim processes to
    break cycles.
"""

from typing import Dict, List, Optional, Set, Tuple


class WaitForGraph:
    """Represents a Wait-For Graph for deadlock detection among processes."""

    def __init__(self, processes: List[str]):
        self.processes = processes
        self.adj: Dict[str, List[str]] = {p: [] for p in processes}

    def add_wait_edge(self, p_from: str, p_to: str) -> None:
        """Adds a directed edge: p_from is waiting for p_to to release a resource."""
        if p_from not in self.adj:
            self.adj[p_from] = []
        if p_to not in self.adj:
            self.adj[p_to] = []
        self.adj[p_from].append(p_to)

    def detect_deadlock(self) -> Tuple[bool, List[str]]:
        """Detects if a deadlock exists and returns the cycle path if present.

        Returns:
            Tuple of (has_deadlock: bool, cycle_path: List[str]).
        """
        # Node states: 0 = unvisited (white), 1 = visiting (gray), 2 = visited (black)
        state: Dict[str, int] = {p: 0 for p in self.adj}
        parent: Dict[str, Optional[str]] = {p: None for p in self.adj}
        cycle: List[str] = []

        def dfs(node: str) -> bool:
            nonlocal cycle
            state[node] = 1  # Mark gray (in stack)

            for neighbor in self.adj.get(node, []):
                if state[neighbor] == 1:
                    # Back-edge found -> cycle detected!
                    # Reconstruct cycle from node back to neighbor
                    cycle_path = [neighbor, node]
                    curr = node
                    while curr != neighbor and parent[curr] is not None:
                        curr = parent[curr]
                        cycle_path.append(curr)
                    cycle_path.reverse()
                    cycle = cycle_path
                    return True
                elif state[neighbor] == 0:
                    parent[neighbor] = node
                    if dfs(neighbor):
                        return True

            state[node] = 2  # Mark black (visited)
            return False

        for p in self.adj:
            if state[p] == 0:
                if dfs(p):
                    return True, cycle

        return False, []

    def display_graph(self) -> None:
        """Prints an ASCII representation of Wait-For dependencies."""
        print("Wait-For Dependencies (Pi -> Pj means Pi waits for Pj):")
        for p, neighbors in self.adj.items():
            if neighbors:
                targets = ", ".join(neighbors)
                print(f"  {p} -> [{targets}]")
            else:
                print(f"  {p} -> (None)")


def build_wfg_from_rag(
    allocations: Dict[str, str], requests: Dict[str, str]
) -> WaitForGraph:
    """Builds a Wait-For Graph from RAG assignment and request mappings.

    Args:
        allocations: Map of resource -> holding_process (e.g. {'R1': 'P1'}).
        requests: Map of process -> requested_resource (e.g. {'P2': 'R1'}).

    Returns:
        A populated WaitForGraph.
    """
    all_processes = list(set(list(allocations.values()) + list(requests.keys())))
    wfg = WaitForGraph(all_processes)

    for requesting_proc, res in requests.items():
        if res in allocations:
            holding_proc = allocations[res]
            wfg.add_wait_edge(requesting_proc, holding_proc)

    return wfg


if __name__ == "__main__":
    print("=" * 60)
    print("Scenario 1: Resource Allocation Graph with DEADLOCK")
    print("=" * 60)
    # Resources: R1, R2, R3
    # P1 holds R1, requests R2
    # P2 holds R2, requests R3
    # P3 holds R3, requests R1
    allocations_1 = {"R1": "P1", "R2": "P2", "R3": "P3"}
    requests_1 = {"P1": "R2", "P2": "R3", "P3": "R1"}

    wfg1 = build_wfg_from_rag(allocations_1, requests_1)
    wfg1.display_graph()

    deadlock_found, deadlocked_cycle = wfg1.detect_deadlock()
    if deadlock_found:
        print(f"\n[ALERT] Deadlock Detected!")
        print(f"Cycle in Wait-For Graph: {' -> '.join(deadlocked_cycle)}")
    else:
        print("\nNo deadlock detected. System can proceed safely.")

    print("\n" + "=" * 60)
    print("Scenario 2: Resource Allocation Graph WITHOUT Deadlock")
    print("=" * 60)
    # P1 holds R1, requests R2
    # P2 holds R2, requests None (can finish and release R2)
    # P3 requests R1
    allocations_2 = {"R1": "P1", "R2": "P2"}
    requests_2 = {"P1": "R2", "P3": "R1"}

    wfg2 = build_wfg_from_rag(allocations_2, requests_2)
    wfg2.display_graph()

    deadlock_found_2, _ = wfg2.detect_deadlock()
    if deadlock_found_2:
        print("\n[ALERT] Deadlock Detected!")
    else:
        print("\nNo deadlock detected. P2 can complete, releasing R2 so P1 and P3 can finish.")

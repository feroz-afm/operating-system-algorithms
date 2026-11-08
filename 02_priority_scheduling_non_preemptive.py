"""Non-Preemptive Priority CPU Scheduling Algorithm.

Description:
    In Non-Preemptive Priority Scheduling, each process is assigned an integer priority.
    The CPU is allocated to the process with the highest priority (by standard convention,
    a lower numerical value indicates a higher priority). Once the CPU has been allocated
    to a process, it cannot be preempted until it voluntarily relinquishes the CPU upon completion.

How It Works:
    1. Maintain a list of arrived, unfinished processes.
    2. At current_time, select the ready process with the highest priority (lowest priority integer).
    3. If multiple processes share the highest priority, break ties using First-Come, First-Served (arrival time).
    4. If no process is ready, advance system time to the arrival time of the next incoming process (CPU idle).
    5. Execute the chosen process non-preemptively for its entire burst time.
    6. Compute metrics: Completion Time (CT), Turnaround Time (TAT = CT - AT), Waiting Time (WT = TAT - BT).
    7. Repeat until all processes are terminated.

Complexity:
    - Time Complexity: O(N^2) using iterative selection over N processes, or O(N log N) with a priority queue.
    - Space Complexity: O(N) to store process state, results, and execution timeline.

Characteristics & Trade-offs:
    - Starvation / Indefinite Blocking: A major drawback where low-priority processes may never execute
      if high-priority processes continually enter the ready queue.
    - Solution: Aging (gradually increasing the priority of processes that wait in the system for extended periods).
    - Practical Use: Real-time systems and batch kernels where critical tasks must take precedence over background tasks.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int
    start_time: int = 0
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0


def priority_non_preemptive_schedule(
    processes: List[Process],
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """Schedules processes using non-preemptive priority discipline.

    Args:
        processes: List of Process instances (lower priority value = higher priority).

    Returns:
        Tuple containing:
            - List of Process objects with metrics calculated.
            - Gantt chart representation as (pid_or_idle, start_time, end_time).
    """
    # Clone processes to avoid mutating external references
    proc_list = [
        Process(
            pid=p.pid,
            arrival_time=p.arrival_time,
            burst_time=p.burst_time,
            priority=p.priority,
        )
        for p in processes
    ]

    current_time = 0
    completed_count = 0
    total_processes = len(proc_list)
    gantt_chart: List[Tuple[str, int, int]] = []
    finished_processes: List[Process] = []

    remaining = proc_list.copy()

    while completed_count < total_processes:
        # Find all ready processes at current_time
        ready_queue = [p for p in remaining if p.arrival_time <= current_time]

        if not ready_queue:
            # CPU is idle until next process arrives
            next_arrival = min(p.arrival_time for p in remaining)
            gantt_chart.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Select process with highest priority (lowest integer value); tie-breaker: arrival_time, then pid
        chosen_process = min(
            ready_queue, key=lambda p: (p.priority, p.arrival_time, p.pid)
        )

        chosen_process.start_time = current_time
        chosen_process.response_time = chosen_process.start_time - chosen_process.arrival_time
        chosen_process.completion_time = current_time + chosen_process.burst_time
        chosen_process.turnaround_time = chosen_process.completion_time - chosen_process.arrival_time
        chosen_process.waiting_time = chosen_process.turnaround_time - chosen_process.burst_time

        gantt_chart.append((chosen_process.pid, chosen_process.start_time, chosen_process.completion_time))
        current_time = chosen_process.completion_time

        finished_processes.append(chosen_process)
        remaining.remove(chosen_process)
        completed_count += 1

    return finished_processes, gantt_chart


def print_gantt_chart(gantt_chart: List[Tuple[str, int, int]]) -> None:
    """Displays an ASCII representation of the Gantt chart."""
    if not gantt_chart:
        return

    print("\n--- Gantt Chart ---")
    top_bar = "+"
    label_bar = "|"
    time_bar = str(gantt_chart[0][1])

    for pid, start, end in gantt_chart:
        segment_len = max(6, len(pid) + 2)
        top_bar += "-" * segment_len + "+"
        label_bar += f"{pid:^{segment_len}}|"
        time_bar += f"{end:>{segment_len + 1}}"

    print(top_bar)
    print(label_bar)
    print(top_bar)
    print(time_bar)


def print_metrics_table(processes: List[Process]) -> None:
    """Prints a formatted table of scheduling metrics for each process."""
    header = (
        f"{'PID':<6} {'Arrival':<8} {'Burst':<8} {'Priority':<10} "
        f"{'Completion':<12} {'Turnaround':<12} {'Waiting':<10} {'Response':<10}"
    )
    print("\n" + "=" * len(header))
    print("Process Scheduling Results (Non-Preemptive Priority)")
    print("Note: Lower priority number = Higher priority")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    total_tat = 0
    total_wt = 0
    total_rt = 0

    # Sort by PID for clear reporting
    for p in sorted(processes, key=lambda x: x.pid):
        total_tat += p.turnaround_time
        total_wt += p.waiting_time
        total_rt += p.response_time
        print(
            f"{p.pid:<6} {p.arrival_time:<8} {p.burst_time:<8} {p.priority:<10} "
            f"{p.completion_time:<12} {p.turnaround_time:<12} {p.waiting_time:<10} {p.response_time:<10}"
        )

    print("-" * len(header))
    n = len(processes)
    print(f"Average Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Waiting Time   : {total_wt / n:.2f}")
    print(f"Average Response Time  : {total_rt / n:.2f}")
    print("=" * len(header))


if __name__ == "__main__":
    sample_processes = [
        Process(pid="P1", arrival_time=0, burst_time=4, priority=2),
        Process(pid="P2", arrival_time=1, burst_time=3, priority=1),
        Process(pid="P3", arrival_time=2, burst_time=1, priority=4),
        Process(pid="P4", arrival_time=3, burst_time=5, priority=3),
        Process(pid="P5", arrival_time=4, burst_time=2, priority=2),
    ]

    print("Running Non-Preemptive Priority Scheduling Simulation...")
    scheduled_proc, chart = priority_non_preemptive_schedule(sample_processes)
    print_gantt_chart(chart)
    print_metrics_table(scheduled_proc)

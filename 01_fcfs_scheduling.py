"""First-Come, First-Served (FCFS) CPU Scheduling Algorithm.

Description:
    FCFS is the simplest CPU scheduling algorithm. In this non-preemptive scheme,
    the process that requests the CPU first is allocated the CPU first, strictly
    in order of arrival. Processes are held in a FIFO queue.

How It Works:
    1. Sort incoming processes by their arrival time.
    2. Dispatch the head process to the CPU.
    3. If the CPU is idle when a process arrives, advance system time to arrival time.
    4. Run the process to completion (Burst Time).
    5. Calculate Completion Time (CT), Turnaround Time (TAT = CT - AT),
       Waiting Time (WT = TAT - BT), and Response Time (RT = Start Time - AT).
    6. Repeat until all processes are serviced.

Complexity:
    - Time Complexity: O(N log N) if processes need sorting by arrival time,
      or O(N) if already sorted, where N is the number of processes.
    - Space Complexity: O(N) to store process state, schedules, and Gantt records.

Characteristics & Trade-offs:
    - Pros: Simple, easy to understand, starvation-free (every process eventually runs).
    - Cons: Convoy Effect (short processes stuck waiting behind long CPU-burst jobs),
      yielding poor average waiting time and turnaround time compared to SJF/RR.
    - Practical Use: Batch systems where execution sequence is predetermined,
      or as the underlying discipline inside individual queues of complex schedulers.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    start_time: int = 0
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0


def fcfs_schedule(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """Schedules processes using First-Come, First-Served (FCFS).

    Args:
        processes: List of Process objects with arrival_time and burst_time.

    Returns:
        A tuple of:
            - List of scheduled Process objects with calculated metrics.
            - Gantt chart timeline as a list of (pid_or_idle, start_time, end_time).
    """
    sorted_processes = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
    current_time = 0
    gantt_chart: List[Tuple[str, int, int]] = []

    for process in sorted_processes:
        if current_time < process.arrival_time:
            # CPU is idle until the process arrives
            gantt_chart.append(("IDLE", current_time, process.arrival_time))
            current_time = process.arrival_time

        process.start_time = current_time
        process.response_time = process.start_time - process.arrival_time
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        gantt_chart.append((process.pid, process.start_time, process.completion_time))
        current_time = process.completion_time

    return sorted_processes, gantt_chart


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
        f"{'PID':<6} {'Arrival':<8} {'Burst':<8} "
        f"{'Completion':<12} {'Turnaround':<12} {'Waiting':<10} {'Response':<10}"
    )
    print("\n" + "=" * len(header))
    print("Process Scheduling Results (FCFS)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for p in processes:
        total_tat += p.turnaround_time
        total_wt += p.waiting_time
        total_rt += p.response_time
        print(
            f"{p.pid:<6} {p.arrival_time:<8} {p.burst_time:<8} "
            f"{p.completion_time:<12} {p.turnaround_time:<12} {p.waiting_time:<10} {p.response_time:<10}"
        )

    print("-" * len(header))
    n = len(processes)
    print(f"Average Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Waiting Time   : {total_wt / n:.2f}")
    print(f"Average Response Time  : {total_rt / n:.2f}")
    print("=" * len(header))


if __name__ == "__main__":
    # Self-contained dummy test input
    sample_processes = [
        Process(pid="P1", arrival_time=0, burst_time=4),
        Process(pid="P2", arrival_time=1, burst_time=6),
        Process(pid="P3", arrival_time=2, burst_time=8),
        Process(pid="P4", arrival_time=3, burst_time=2),
        Process(pid="P5", arrival_time=6, burst_time=4),
    ]

    print("Running First-Come, First-Served (FCFS) Scheduling Simulation...")
    scheduled_proc, chart = fcfs_schedule(sample_processes)
    print_gantt_chart(chart)
    print_metrics_table(scheduled_proc)

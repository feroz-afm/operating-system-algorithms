"""Shortest Remaining Time First (SRTF) CPU Scheduling Algorithm.

Description:
    Shortest Remaining Time First (SRTF) is the preemptive variant of Shortest Job First (SJF).
    At any given time, the CPU is allocated to the process that has the smallest amount of
    remaining burst time. If a newly arrived process requires less execution time than the
    current process has remaining, the running process is preempted.

How It Works:
    1. Maintain remaining burst times for all arrived processes.
    2. At each time tick, pick the ready process with min(remaining_burst_time).
       Tie-breaker: earliest arrival time, then PID.
    3. If no process has arrived yet, CPU is IDLE.
    4. Execute the chosen process for 1 time unit and decrement its remaining burst time.
    5. When a process finishes (remaining_burst_time == 0), record:
       - Completion Time (CT)
       - Turnaround Time (TAT = CT - Arrival Time)
       - Waiting Time (WT = TAT - Initial Burst Time)
       - Response Time (RT = First Start Time - Arrival Time)
    6. Continue until all processes have finished.
    7. Merge contiguous intervals into an ASCII Gantt chart.

Complexity:
    - Time Complexity: O(Total_Burst_Time * N) for step-wise simulation, or O((N + P) log N)
      using an event-driven min-heap, where P is the number of preemptions.
    - Space Complexity: O(N) for process metrics and execution timeline storage.

Characteristics & Trade-offs:
    - Pros: Provably optimal in terms of minimizing average waiting time for a given set of processes.
    - Cons: High context-switching overhead; risk of starvation for long processes when short
      jobs continuously arrive; requires knowing or estimating future burst times (e.g., via
      exponential smoothing).
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    remaining_time: int = 0
    start_time: Optional[int] = None
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0


def srtf_schedule(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """Schedules processes using Shortest Remaining Time First (SRTF).

    Args:
        processes: List of Process instances with pid, arrival_time, and burst_time.

    Returns:
        Tuple containing:
            - List of Process objects with metrics calculated.
            - Gantt chart timeline as (pid_or_idle, start_time, end_time).
    """
    proc_list = [
        Process(
            pid=p.pid,
            arrival_time=p.arrival_time,
            burst_time=p.burst_time,
            remaining_time=p.burst_time,
        )
        for p in processes
    ]

    total_processes = len(proc_list)
    completed_count = 0
    current_time = 0
    raw_timeline: List[str] = []

    while completed_count < total_processes:
        ready = [p for p in proc_list if p.arrival_time <= current_time and p.remaining_time > 0]

        if not ready:
            raw_timeline.append("IDLE")
            current_time += 1
            continue

        # Choose the process with the shortest remaining burst time
        # Tie-breaker: earliest arrival time, then pid
        chosen = min(ready, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))

        if chosen.start_time is None:
            chosen.start_time = current_time
            chosen.response_time = chosen.start_time - chosen.arrival_time

        raw_timeline.append(chosen.pid)
        chosen.remaining_time -= 1
        current_time += 1

        if chosen.remaining_time == 0:
            chosen.completion_time = current_time
            chosen.turnaround_time = chosen.completion_time - chosen.arrival_time
            chosen.waiting_time = chosen.turnaround_time - chosen.burst_time
            completed_count += 1

    # Compress unit ticks into Gantt segments
    gantt_chart: List[Tuple[str, int, int]] = []
    if raw_timeline:
        seg_label = raw_timeline[0]
        seg_start = 0
        for t, label in enumerate(raw_timeline):
            if label != seg_label:
                gantt_chart.append((seg_label, seg_start, t))
                seg_label = label
                seg_start = t
        gantt_chart.append((seg_label, seg_start, len(raw_timeline)))

    return proc_list, gantt_chart


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
    print("Process Scheduling Results (Shortest Remaining Time First - SRTF)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for p in sorted(processes, key=lambda x: x.pid):
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
    sample_processes = [
        Process(pid="P1", arrival_time=0, burst_time=8),
        Process(pid="P2", arrival_time=1, burst_time=4),
        Process(pid="P3", arrival_time=2, burst_time=9),
        Process(pid="P4", arrival_time=3, burst_time=5),
    ]

    print("Running Shortest Remaining Time First (SRTF) Scheduling Simulation...")
    scheduled_proc, chart = srtf_schedule(sample_processes)
    print_gantt_chart(chart)
    print_metrics_table(scheduled_proc)

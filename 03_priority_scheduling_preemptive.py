"""Preemptive Priority CPU Scheduling Algorithm.

Description:
    Preemptive Priority Scheduling dynamically interrupts the currently running process
    if a newly arrived process possesses a strictly higher priority (lower priority number).
    The interrupted process is moved back to the ready queue with its remaining burst time
    preserved.

How It Works:
    1. Track remaining burst time for each arrived process.
    2. At each discrete time unit (or event point), evaluate all ready processes.
    3. Choose the ready process with the highest priority (smallest integer).
       Ties are broken using arrival time, then PID.
    4. If no process is ready, mark the CPU as IDLE.
    5. Decrement the remaining burst time of the active process by 1.
    6. If the active process reaches 0 remaining time, record its completion time and metrics:
       - Turnaround Time (TAT) = Completion Time - Arrival Time
       - Waiting Time (WT) = Turnaround Time - Burst Time
       - Response Time (RT) = First Start Time - Arrival Time
    7. Merge contiguous execution intervals into a clean Gantt chart timeline.

Complexity:
    - Time Complexity: O(Total_Burst_Time * N) for unit-step simulation or O((N + E) log N)
      using an event-driven priority heap, where E is the number of preemption events.
    - Space Complexity: O(N) to maintain process descriptors, state, and timeline records.

Characteristics & Trade-offs:
    - Pros: Highly responsive for mission-critical and urgent tasks.
    - Cons: Context switching overhead increases with frequent preemptions; potential starvation
      for lower-priority jobs.
    - Mitigation: Aging techniques that progressively boost waiting jobs.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int
    remaining_time: int = 0
    start_time: Optional[int] = None
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0


def priority_preemptive_schedule(
    processes: List[Process],
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """Simulates preemptive priority scheduling.

    Args:
        processes: List of Process instances (lower priority value = higher priority).

    Returns:
        Tuple containing:
            - List of completed Process objects with metrics calculated.
            - Gantt chart representation as (pid_or_idle, start_time, end_time).
    """
    proc_list = [
        Process(
            pid=p.pid,
            arrival_time=p.arrival_time,
            burst_time=p.burst_time,
            priority=p.priority,
            remaining_time=p.burst_time,
        )
        for p in processes
    ]

    total_processes = len(proc_list)
    completed_count = 0
    current_time = 0

    # Raw timeline tracking per time unit
    raw_timeline: List[str] = []

    while completed_count < total_processes:
        # Arrived and unfinished
        ready = [p for p in proc_list if p.arrival_time <= current_time and p.remaining_time > 0]

        if not ready:
            raw_timeline.append("IDLE")
            current_time += 1
            continue

        # Choose highest priority (lowest integer value); tie-breaker: arrival_time, pid
        chosen = min(ready, key=lambda p: (p.priority, p.arrival_time, p.pid))

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

    # Compress raw time unit slices into Gantt segments
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
        f"{'PID':<6} {'Arrival':<8} {'Burst':<8} {'Priority':<10} "
        f"{'Completion':<12} {'Turnaround':<12} {'Waiting':<10} {'Response':<10}"
    )
    print("\n" + "=" * len(header))
    print("Process Scheduling Results (Preemptive Priority)")
    print("Note: Lower priority number = Higher priority")
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
        Process(pid="P1", arrival_time=0, burst_time=4, priority=3),
        Process(pid="P2", arrival_time=1, burst_time=3, priority=1),
        Process(pid="P3", arrival_time=2, burst_time=5, priority=4),
        Process(pid="P4", arrival_time=3, burst_time=1, priority=2),
        Process(pid="P5", arrival_time=4, burst_time=2, priority=2),
    ]

    print("Running Preemptive Priority Scheduling Simulation...")
    scheduled_proc, chart = priority_preemptive_schedule(sample_processes)
    print_gantt_chart(chart)
    print_metrics_table(scheduled_proc)

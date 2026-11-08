"""Multilevel Queue (MLQ) CPU Scheduling Algorithm.

Description:
    Multilevel Queue Scheduling partitions the ready queue into several separate queues,
    each characterized by its own scheduling algorithm and priority level. Processes are
    permanently assigned to a queue based on properties like memory size, process priority,
    or process type (e.g., system/interactive vs. batch).

How It Works:
    1. Queues are organized hierarchically:
       - Queue 0 (Top Priority): Foreground / Interactive processes scheduled with Round Robin (quantum = 2).
       - Queue 1 (Bottom Priority): Background / Batch processes scheduled with First-Come, First-Served (FCFS).
    2. Fixed-Priority Preemptive Scheduling is enforced between queues:
       No process in Queue 1 can run unless Queue 0 is completely empty.
       If a process arrives in Queue 0 while a Queue 1 process is running, the Queue 1 process is preempted.
    3. Within each queue:
       - Queue 0 executes jobs up to the specified time quantum.
       - Queue 1 executes jobs non-preemptively unless preempted by an arrival in Queue 0.
    4. Compute CT, TAT, WT, and RT across all queues.

Complexity:
    - Time Complexity: O(Total_Burst_Time * N) for step-wise multi-queue simulation.
    - Space Complexity: O(N) to store queues, process metadata, and Gantt records.

Characteristics & Trade-offs:
    - Pros: Low scheduling overhead for distinct job classes; tailors algorithms to process needs.
    - Cons: High risk of starvation for processes in lower queues if high-priority queues are saturated.
    - Difference from MLFQ: In standard Multilevel Queue, processes are static and cannot migrate between
      queues; in Multilevel Feedback Queue (MLFQ), aging and dynamic demotion allow cross-queue movement.
"""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Process:
    pid: str
    queue_id: int  # 0: Highest priority (Round Robin), 1: Lowest priority (FCFS)
    arrival_time: int
    burst_time: int
    remaining_time: int = 0
    start_time: Optional[int] = None
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0


def multilevel_queue_schedule(
    processes: List[Process], rr_quantum: int = 2
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """Simulates Multilevel Queue scheduling with Queue 0 (RR) and Queue 1 (FCFS).

    Args:
        processes: List of Process objects with queue_id (0 or 1).
        rr_quantum: Time quantum for the highest priority queue (Queue 0).

    Returns:
        Tuple containing:
            - List of completed processes with performance metrics.
            - Gantt chart timeline list: (pid_or_idle, start_time, end_time).
    """
    proc_list = [
        Process(
            pid=p.pid,
            queue_id=p.queue_id,
            arrival_time=p.arrival_time,
            burst_time=p.burst_time,
            remaining_time=p.burst_time,
        )
        for p in processes
    ]

    total_procs = len(proc_list)
    completed_count = 0
    current_time = 0

    # Queues:
    # Q0: deque of active Process objects for Round Robin
    # Q1: deque of active Process objects for FCFS
    q0: deque = deque()
    q1: deque = deque()

    # Track arrival flags
    arrived_indices = set()
    raw_timeline: List[str] = []

    def check_arrivals(time_point: int) -> None:
        # Sort by arrival time, then pid for deterministic queuing
        for idx, p in enumerate(proc_list):
            if idx not in arrived_indices and p.arrival_time <= time_point:
                arrived_indices.add(idx)
                if p.queue_id == 0:
                    q0.append(p)
                else:
                    q1.append(p)

    check_arrivals(current_time)

    # State tracking for RR slice in Q0
    q0_current_job: Optional[Process] = None
    q0_slice_left = 0

    while completed_count < total_procs:
        check_arrivals(current_time)

        # Service Queue 0 (Interactive - Round Robin) first
        if q0 or q0_current_job:
            if q0_current_job is None:
                q0_current_job = q0.popleft()
                q0_slice_left = rr_quantum

            if q0_current_job.start_time is None:
                q0_current_job.start_time = current_time
                q0_current_job.response_time = q0_current_job.start_time - q0_current_job.arrival_time

            raw_timeline.append(f"{q0_current_job.pid}(Q0)")
            q0_current_job.remaining_time -= 1
            q0_slice_left -= 1
            current_time += 1

            # Check new arrivals before deciding on queue transitions
            check_arrivals(current_time)

            if q0_current_job.remaining_time == 0:
                q0_current_job.completion_time = current_time
                q0_current_job.turnaround_time = q0_current_job.completion_time - q0_current_job.arrival_time
                q0_current_job.waiting_time = q0_current_job.turnaround_time - q0_current_job.burst_time
                completed_count += 1
                q0_current_job = None
            elif q0_slice_left == 0:
                # Time quantum expired: return to end of Q0
                q0.append(q0_current_job)
                q0_current_job = None

        # Service Queue 1 (Batch - FCFS) only if Queue 0 is completely empty
        elif q1:
            q1_job = q1[0]
            if q1_job.start_time is None:
                q1_job.start_time = current_time
                q1_job.response_time = q1_job.start_time - q1_job.arrival_time

            raw_timeline.append(f"{q1_job.pid}(Q1)")
            q1_job.remaining_time -= 1
            current_time += 1

            check_arrivals(current_time)

            if q1_job.remaining_time == 0:
                q1_job.completion_time = current_time
                q1_job.turnaround_time = q1_job.completion_time - q1_job.arrival_time
                q1_job.waiting_time = q1_job.turnaround_time - q1_job.burst_time
                completed_count += 1
                q1.popleft()
            # If a process arrived in Q0, Q1 process is preempted naturally next loop!

        else:
            # CPU is IDLE
            raw_timeline.append("IDLE")
            current_time += 1

    # Compress raw units into Gantt segments
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
        segment_len = max(8, len(pid) + 2)
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
        f"{'PID':<6} {'Queue':<8} {'Arrival':<8} {'Burst':<8} "
        f"{'Completion':<12} {'Turnaround':<12} {'Waiting':<10} {'Response':<10}"
    )
    print("\n" + "=" * len(header))
    print("Process Scheduling Results (Multilevel Queue Scheduling)")
    print("Hierarchy: Q0 (Interactive: Round Robin q=2) > Q1 (Batch: FCFS)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for p in sorted(processes, key=lambda x: (x.queue_id, x.pid)):
        queue_name = f"Q{p.queue_id} (RR)" if p.queue_id == 0 else f"Q{p.queue_id} (FCFS)"
        total_tat += p.turnaround_time
        total_wt += p.waiting_time
        total_rt += p.response_time
        print(
            f"{p.pid:<6} {queue_name:<8} {p.arrival_time:<8} {p.burst_time:<8} "
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
        Process(pid="P1", queue_id=0, arrival_time=0, burst_time=4),  # Interactive (Q0)
        Process(pid="P2", queue_id=0, arrival_time=1, burst_time=3),  # Interactive (Q0)
        Process(pid="P3", queue_id=1, arrival_time=2, burst_time=6),  # Batch (Q1)
        Process(pid="P4", queue_id=0, arrival_time=4, burst_time=2),  # Interactive (Q0)
        Process(pid="P5", queue_id=1, arrival_time=5, burst_time=3),  # Batch (Q1)
    ]

    print("Running Multilevel Queue Scheduling Simulation...")
    scheduled_proc, chart = multilevel_queue_schedule(sample_processes, rr_quantum=2)
    print_gantt_chart(chart)
    print_metrics_table(scheduled_proc)

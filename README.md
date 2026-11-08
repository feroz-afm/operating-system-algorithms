# Operating System Algorithms

A curated collection of essential Operating System (OS) algorithms implemented in clean, well-documented, standalone Python. Designed for computer science students, academic study, university coursework, and core systems programming practice.

---

## Repository Overview

All implementations are self-contained, PEP-8 compliant, and require zero external third-party dependencies (using only Python's standard library modules such as `sys`, `collections`, `threading`, and `dataclasses`). Each script includes:
- Meaningful docstrings detailing the conceptual mechanism, time/space complexity, and practical systems engineering trade-offs.
- Self-contained dummy test inputs demonstrating step-by-step executions, Gantt charts, memory layout tables, or thread-safe synchronization logs.
- Interactive and modular execution via `if __name__ == "__main__":` entry points.

---

## Index of Algorithms

### 1. CPU Scheduling Algorithms

| # | File | Description | Quick Run |
|---|---|---|---|
| **01** | [`01_fcfs_scheduling.py`](01_fcfs_scheduling.py) | Non-preemptive scheduling where the process arriving first gets allocated the CPU first. | `python 01_fcfs_scheduling.py` |
| **02** | [`02_priority_scheduling_non_preemptive.py`](02_priority_scheduling_non_preemptive.py) | Allocates CPU to highest priority process without preemption (lower integer = higher priority). | `python 02_priority_scheduling_non_preemptive.py` |
| **03** | [`03_priority_scheduling_preemptive.py`](03_priority_scheduling_preemptive.py) | Preempts running process if a newly arrived process possesses a higher priority level. | `python 03_priority_scheduling_preemptive.py` |
| **04** | [`04_srtf_scheduling.py`](04_srtf_scheduling.py) | Preemptive variant of SJF that schedules the job with the shortest remaining execution time. | `python 04_srtf_scheduling.py` |
| **05** | [`05_multilevel_queue_scheduling.py`](05_multilevel_queue_scheduling.py) | Multi-tier queue hierarchy (Round Robin for interactive jobs and FCFS for batch jobs). | `python 05_multilevel_queue_scheduling.py` |
| **-** | [`Round_Robin.py`](Round_Robin.py) | Classic interactive round-robin scheduling algorithm with configurable quantum slice. | `python Round_Robin.py` |
| **-** | [`Shortest_Job_First.py`](Shortest_Job_First.py) | Non-preemptive Shortest Job First scheduling implementation. | `python Shortest_Job_First.py` |

---

### 2. Page Replacement & Memory Management

| # | File | Description | Quick Run |
|---|---|---|---|
| **06** | [`06_fifo_page_replacement.py`](06_fifo_page_replacement.py) | Replaces the oldest page in memory; includes demonstration of Belady's Anomaly. | `python 06_fifo_page_replacement.py` |
| **07** | [`07_optimal_page_replacement.py`](07_optimal_page_replacement.py) | Belady's MIN algorithm that evicts the page not needed for the longest future duration. | `python 07_optimal_page_replacement.py` |
| **08** | [`08_first_fit_memory_allocation.py`](08_first_fit_memory_allocation.py) | Allocates the first free memory partition from the beginning that is large enough. | `python 08_first_fit_memory_allocation.py` |
| **09** | [`09_best_fit_memory_allocation.py`](09_best_fit_memory_allocation.py) | Allocates the smallest free memory block that can accommodate the requested process. | `python 09_best_fit_memory_allocation.py` |
| **10** | [`10_worst_fit_memory_allocation.py`](10_worst_fit_memory_allocation.py) | Allocates the largest available memory partition to maximize leftover hole size. | `python 10_worst_fit_memory_allocation.py` |
| **-** | [`Least_Recently_Used.py`](Least_Recently_Used.py) | Evicts the page in memory that has not been referenced for the longest period of time. | `python Least_Recently_Used.py` |

---

### 3. Deadlock Detection & Avoidance

| # | File | Description | Quick Run |
|---|---|---|---|
| **11** | [`11_bankers_algorithm_safety.py`](11_bankers_algorithm_safety.py) | Dijkstra's Banker's algorithm for system safety state verification and resource requests. | `python 11_bankers_algorithm_safety.py` |
| **12** | [`12_resource_allocation_graph_deadlock.py`](12_resource_allocation_graph_deadlock.py) | Cycle detection on Wait-For Graphs (WFG) using DFS to detect deadlock in multi-process systems. | `python 12_resource_allocation_graph_deadlock.py` |

---

### 4. Process Synchronization & Concurrency

| # | File | Description | Quick Run |
|---|---|---|---|
| **13** | [`13_producer_consumer_semaphores.py`](13_producer_consumer_semaphores.py) | Thread synchronization for bounded buffer using `mutex`, `empty`, and `full` semaphores. | `python 13_producer_consumer_semaphores.py` |
| **14** | [`14_dining_philosophers_problem.py`](14_dining_philosophers_problem.py) | Asymmetric resource hierarchy solution that prevents circular wait and deadlock. | `python 14_dining_philosophers_problem.py` |
| **15** | [`15_readers_writers_problem.py`](15_readers_writers_problem.py) | Reader-writer mutual exclusion permitting concurrent readers and exclusive writer access. | `python 15_readers_writers_problem.py` |
| **16** | [`16_petersons_algorithm.py`](16_petersons_algorithm.py) | Pure software two-process mutual exclusion algorithm guaranteeing progress and bounded waiting. | `python 16_petersons_algorithm.py` |

---

### 5. Disk Scheduling Algorithms

| # | File | Description | Quick Run |
|---|---|---|---|
| **17** | [`17_disk_fcfs.py`](17_disk_fcfs.py) | Services disk cylinder requests strictly in arrival order without head trajectory optimization. | `python 17_disk_fcfs.py` |
| **18** | [`18_disk_sstf.py`](18_disk_sstf.py) | Greedily services the pending cylinder closest to the current head position. | `python 18_disk_sstf.py` |
| **19** | [`19_disk_scan.py`](19_disk_scan.py) | Elevator algorithm moving the disk arm across cylinders to the boundary before reversing. | `python 19_disk_scan.py` |
| **20** | [`20_disk_c_scan.py`](20_disk_c_scan.py) | Circular SCAN algorithm providing uniform wait times by resetting directly to track 0. | `python 20_disk_c_scan.py` |

---

## Getting Started

### Prerequisites
- Python 3.8+ (tested on Python 3.12)
- No third-party packages required (`pip install` is not needed).

### Cloning and Execution
```bash
# Clone the repository
git clone https://github.com/feroz-afm/operating-system-algorithms.git
cd operating-system-algorithms

# Run any algorithm directly
python 01_fcfs_scheduling.py
python 06_fifo_page_replacement.py
python 11_bankers_algorithm_safety.py
python 13_producer_consumer_semaphores.py
python 18_disk_sstf.py
```

---

## License
This project is licensed under the terms of the [LICENSE](LICENSE) file included in the repository.

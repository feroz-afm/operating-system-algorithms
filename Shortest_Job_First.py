n = int(input("Enter number of processes: "))

processes = []

for i in range(n):
    bt = int(input(f"Enter Burst Time for P{i+1}: "))
    processes.append([i+1, bt])

processes.sort(key=lambda x: x[1])

time = 0
total_wt = 0
total_tat = 0

print("\nProcess\tBT\tWT\tTAT")

for p, bt in processes:
    wt = time
    tat = wt + bt

    print(f"P{p}\t{bt}\t{wt}\t{tat}")

    total_wt += wt
    total_tat += tat
    time += bt

print("\nAverage Waiting Time =", total_wt / n)
print("Average Turnaround Time =", total_tat / n)
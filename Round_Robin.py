n = int(input("Enter number of processes: "))

bt = []

for i in range(n):
    bt.append(int(input(f"Enter Burst Time for P{i+1}: ")))

q = int(input("Enter Time Quantum: "))

remaining = bt.copy()
wt = [0] * n
time = 0

while True:
    done = True

    for i in range(n):
        if remaining[i] > 0:
            done = False

            if remaining[i] > q:
                time += q
                remaining[i] -= q
            else:
                time += remaining[i]
                wt[i] = time - bt[i]
                remaining[i] = 0

    if done:
        break

tat = [wt[i] + bt[i] for i in range(n)]

print("\nProcess\tBT\tWT\tTAT")

for i in range(n):
    print(f"P{i+1}\t{bt[i]}\t{wt[i]}\t{tat[i]}")

print("\nAverage Waiting Time =", sum(wt) / n)
print("Average Turnaround Time =", sum(tat) / n)
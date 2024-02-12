'''
COP4600 PA#1 Group 31
Evelyn Adams
Andrew Brink
Alicia Hassan
Jonah Henriksson
'''
import sys
from collections import deque

class Process:
    def __init__(self, process_name, arrival_time, burst_time):
        self.process_name = process_name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.end_time = -1
        self.response_time = -1

class ProcessQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, process):
        self.queue.append(process)

    def dequeue(self):
        return self.queue.popleft() if self.queue else None

    def is_empty(self):
        return not bool(self.queue)

def calculate_metrics(processes):
    for process in processes:
        process['turnaround'] = process['finish'] - process['arrival']
        process['wait'] = process['turnaround'] - process['burst']
        process['response'] = process['wait']

def fcfs(processes):
    time = 0
    print(f"{len(processes)} processes")
    print("Using First Come First Serve")

    for process in processes:
        if time < process['arrival']:
            time = process['arrival']
        print(f"Time {time:3d} : {process['name']} arrived")
        process['wait'] = max(0, time - process['arrival'])
        process['has_run'] = True
        time += process['burst']
        process['finish'] = time
        print(f"Time {time:3d} : {process['name']} finished")

    # Calculate metrics after all processes have finished
    calculate_metrics(processes)

def sjf(processes):
    process_queue = ProcessQueue()
    current_time = 0
    total_turnaround_time = 0
    total_wait_time = 0

    while processes or not process_queue.is_empty():
        # Handle process arrivals
        while processes and processes[0].arrival_time == current_time:
            process_queue.enqueue(processes.pop(0))
            print(f"Time {current_time:3d} : {process_queue.queue[-1].process_name} arrived")

        if not process_queue.is_empty():
            shortest_process = min(process_queue.queue, key=lambda x: x.remaining_time)

            if shortest_process.start_time == -1:
                shortest_process.start_time = current_time
                shortest_process.response_time = current_time - shortest_process.arrival_time

            current_time += 1
            shortest_process.remaining_time -= 1

            if shortest_process.remaining_time == 0:
                shortest_process.end_time = current_time
                total_turnaround_time += shortest_process.end_time - shortest_process.arrival_time
                total_wait_time += shortest_process.start_time - shortest_process.arrival_time

                process_queue.dequeue()
        else:
            current_time += 1

    n = len(processes) + len(process_queue.queue)
    average_turnaround_time = total_turnaround_time / n
    average_wait_time = total_wait_time / n
    
    print("Average Turnaround Time:", average_turnaround_time)
    print("Average Wait Time:", average_wait_time)

def round_robin(processes, runfor, quantum):
    print("Using Round-Robin")
    print("Quantum", quantum)
    print()

    active_process = None
    current_q = 0
    queue = deque()
    finished_processes = []

    for i in range(runfor):
        if active_process:
            active_process["burst"] -= 1
            current_q -= 1
            active_process["wait"] += 1

        while processes and processes[0]["arrival"] == i:
            process = processes.pop(0)
            queue.append(process)
            print(f"Time {i:3} : {process['name']} arrived")

        if active_process and active_process["burst"] == 0:
            active_process["turnaround"] = i - active_process["arrival"]
            finished_processes.append(active_process)
            print(f"Time {i:3} : {active_process['name']} finished")
            active_process = None

        if queue and not active_process:
            active_process = queue.popleft()
            current_q = quantum
            if not active_process["has_run"]:
                active_process["response"] = i - active_process["arrival"]
                active_process["has_run"] = True
            print(f"Time {i:3} : {active_process['name']} selected (burst {active_process['burst']})")

        if not active_process:
            print(f"Time {i:3} : Idle")
            continue

        if current_q == 0:
            queue.append(active_process)
            active_process = queue.popleft()
            current_q = quantum
            if not active_process["has_run"]:
                active_process["response"] = i - active_process["arrival"]
                active_process["has_run"] = True
            print(f"Time {i:3} : {active_process['name']} selected (burst {active_process['burst']})")

    print("Finished at time", runfor)
    return finished_processes

def main():
    if len(sys.argv) != 2:
        print("Usage: python scheduler.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename) as file:
        lines = file.readlines()

    directives = {}
    processes = []

    for line in lines:
        if "#" in line:
            line = line.split("#")[0].strip()
        if not line:
            continue
        parts = line.split()
        directive = parts[0].lower()
        if directive == "end":
            break
        if directive == "process":
            process = {"name": parts[2], "arrival": int(parts[4]), "burst": int(parts[6]), "has_run": False,
                       "wait": 0, "turnaround": 0, "response": 0}
            processes.append(process)
        else:
            directives[directive] = parts[1]

    required_directives = ["processcount", "runfor", "use"]
    for directive in required_directives:
        if directive not in directives:
            print(f"Error: Missing parameter {directive}")
            sys.exit(1)

    process_count = int(directives["processcount"])
    if len(processes) != process_count:
        print("Error: Number of 'process' directives doesn't match 'processcount'")
        sys.exit(1)

    use_algorithm = directives["use"].lower()
    if use_algorithm == "rr" and "quantum" not in directives:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    print(f"{process_count} processes")

    for process in processes:
        process["has_run"] = False

    processes.sort(key=lambda x: x["arrival"])

    if use_algorithm == "fcfs":
        fcfs(processes, int(directives["runfor"]))
    elif use_algorithm == "sjf":
        sjf(processes, int(directives["runfor"]))
    elif use_algorithm == "rr":
        quantum = int(directives["quantum"])
        result_processes = round_robin(processes, int(directives["runfor"]), quantum)

        result_processes.sort(key=lambda x: x["name"])
        for process in result_processes:
            print(f"{process['name']} wait {process['wait']} turnaround {process['turnaround']} response {process['response']}")

if __name__ == "__main__":
    main()

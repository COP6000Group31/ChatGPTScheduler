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

def round_robin(processes, quantum):
    print("Using Round-Robin")
    active_process = None
    current_q = 0
    finished_processes = []
    queue = deque()

    for i in range(runfor):
        # Handle process arrivals
        while processes and processes[0]['arrival'] == i:
            queue.append(processes.pop(0))
            print(f"Time {i:3d} : {queue[-1]['name']} arrived")

        if queue and not active_process:
            active_process = queue.popleft()
            current_q = quantum
            active_process['has_run'] = True
            print(f"Time {i:3d} : {active_process['name']} selected (burst {active_process['burst']})")

        if not active_process:
            print(f"Time {i:3d} : Idle")
            continue

        active_process['burst'] -= 1
        current_q -= 1

        for process in queue:
            process['wait'] += 1
            if not process['has_run']:
                process['response'] += 1

        if active_process['burst'] == 0:
            turnaround_time = i - active_process['arrival']
            active_process['turnaround'] = turnaround_time
            finished_processes.append(active_process)
            print(f"Time {i:3d} : {active_process['name']} finished")
            active_process = None
        elif current_q == 0:
            queue.append(active_process)
            active_process = None

    print(f"Finished at time {runfor}\n")
    return finished_processes

def print_results(processes):
    for process in processes:
        print(f"{process['name']} wait {process['wait']} turnaround {process['turnaround']} response {process['response']}")

# Read file name from command line argument
if len(sys.argv) != 2:
    print("Error: Please provide the input file name.")
    sys.exit(1)

file_name = sys.argv[1]

# Read and parse input file
with open(file_name, 'r') as file:
    directives = {}
    processes = []

    for line in file:
        line = line.split('#')[0].strip()  # Ignore comments
        if line:
            parts = line.split()
            directive = parts[0]
            if directive == 'end':
                break

            if directive == 'process':
                processes.append({'name': parts[2], 'arrival': int(parts[4]), 'burst': int(parts[6]),
                                  'wait': 0, 'turnaround': 0, 'response': 0, 'has_run': False})
            else:
                directives[directive] = parts[1]

# Check for missing parameters
required_directives = ['processcount', 'runfor', 'use']
if any(directive not in directives for directive in required_directives):
    print("Error: Missing parameter(s)")
    sys.exit(1)

process_count = int(directives['processcount'])
runfor = int(directives['runfor'])
use_algorithm = directives['use']

if use_algorithm == 'rr':
    if 'quantum' not in directives:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)
    quantum = int(directives['quantum'])

print(f"processes: {process_count}")

# Sort processes by arrival time
processes.sort(key=lambda x: x['arrival'])

# Execute scheduling algorithm
if use_algorithm == 'fcfs':
    fcfs(processes)
elif use_algorithm == 'sjf':
    sjf(processes)
elif use_algorithm == 'rr':
    results = round_robin(processes, quantum)
    print_results(results)
else:
    print("Error: Invalid scheduling algorithm")
    sys.exit(1)

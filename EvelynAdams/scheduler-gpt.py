import sys
from collections import deque

def fcfs(processes, runfor):
    print("Using First-Come First-Served")

    active_process = None
    finished_processes = []
    queue = deque()

    for i in range(runfor):
        # If there's an active process, execute it
        if active_process:
            active_process["burst"] -= 1
            active_process["wait"] += 1

        # Check for arriving processes
        while processes and processes[0]["arrival"] == i:
            process = processes.pop(0)
            print(f"Time {i:3} : {process['name']} arrived")

            if queue and not active_process:
                active_process = process
                print(f"Time {i:3} : {active_process['name']} selected (burst {active_process['burst']})")

        # Check if the active process is finished
        if active_process and active_process["burst"] == 0:
            active_process["turnaround"] = i - active_process["arrival"]
            finished_processes.append(active_process)
            print(f"Time {i:3} : {active_process['name']} finished")
            active_process = None

        # If no active process, print idle
        if not active_process and not process:
            print(f"Time {i:3} : Idle")

    print("Finished at time", runfor)
    return finished_processes

def sjf(processes, runfor):
    # Implement Shortest Job First scheduling algorithm (stub)
    print("Using Shortest Job First")
    # Your SJF implementation here

def round_robin(processes, runfor, quantum):
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

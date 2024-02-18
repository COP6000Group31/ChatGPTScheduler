import sys

file_out = ""

def write_out(string):
    global file_out
    file_out += string + '\n'

def fcfs(processes, runfor):
    pass  # Placeholder for First Come First Serve

def sjf(processes, runfor):
    pass  # Placeholder for Shortest Job First

def round_robin(processes, runfor, quantum):
    write_out("Using Round-Robin")
    write_out("Quantum " + str(quantum))
    write_out("")  # Blank line

    active_process = None
    current_q = 0
    queue = []
    finished_processes = []

    for i in range(runfor):
        if active_process:
            active_process['burst'] -= 1
            current_q -= 1

        for process in queue:
            process['wait'] += 1

        arrivals = [process for process in processes if process['arrival'] == i]
        for arrival in arrivals:
            queue.append(arrival)
            write_out(f"Time {i} : {arrival['name']} arrived")

        if active_process and active_process['burst'] == 0:
            active_process['turnaround'] = i - active_process['arrival']
            finished_processes.append(active_process)
            write_out(f"Time {i} : {active_process['name']} finished")
            active_process = None

        if not active_process and queue:
            active_process = queue.pop(0)
            current_q = quantum
            if not active_process['has_run']:
                active_process['response'] = i - active_process['arrival']
            active_process['has_run'] = True
            write_out(f"Time {i} : {active_process['name']} selected (burst {active_process['burst']})")

        if not active_process:
            write_out(f"Time {i} : Idle")
            continue

        if current_q == 0:
            queue.append(active_process)
            active_process = queue.pop(0)
            current_q = quantum
            if not active_process['has_run']:
                active_process['response'] = i - active_process['arrival']
            active_process['has_run'] = True
            write_out(f"Time {i} : {active_process['name']} selected (burst {active_process['burst']})")

    write_out(f"Finished at time {runfor}")

    return finished_processes

def main():
    global file_out
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        lines = f.readlines()

    directives = {}
    processes = []

    for line in lines:
        line = line.split('#')[0].strip()
        if not line:
            continue
        parts = line.split()
        directive = parts[0]
        if directive == 'end':
            break
        if directive == 'process':
            processes.append({
                'name': parts[2],
                'arrival': int(parts[4]),
                'burst': int(parts[6]),
                'wait': 0,
                'turnaround': 0,
                'response': 0,
                'has_run': False
            })
        else:
            directives[directive] = ' '.join(parts[1:])

    if 'processcount' not in directives:
        write_out("Error: Missing parameter processcount")
        return
    if len(processes) != int(directives['processcount']):
        write_out("Error: Missing process directives")
        return
    if 'runfor' not in directives:
        write_out("Error: Missing parameter runfor")
        return

    write_out(f"{directives['processcount']} processes")

    processes.sort(key=lambda x: x['arrival'])

    if directives['use'] == 'fcfs':
        fcfs(processes, int(directives['runfor']))
    elif directives['use'] == 'sjf':
        sjf(processes, int(directives['runfor']))
    elif directives['use'] == 'rr':
        if 'quantum' not in directives:
            write_out("Error: Missing quantum parameter when use is 'rr'")
            return
        finished_processes = round_robin(processes, int(directives['runfor']), int(directives['quantum']))
        finished_processes.sort(key=lambda x: x['name'])
        for process in finished_processes:
            write_out(f"{process['name']} wait {process['wait']} turnaround {process['turnaround']} response {process['response']}")
    else:
        write_out("Error: Invalid scheduling algorithm")

    with open(filename.replace('.in', '.out'), 'w') as f:
        f.write(file_out)

    file_out = ""

if __name__ == "__main__":
    main()

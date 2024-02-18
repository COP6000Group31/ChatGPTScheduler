'''
COP4600 PA#1 Group 31
Evelyn Adams
Andrew Brink
Alicia Hassan
Jonah Henriksson

AI Generated Code
Lines:    ALL
Source:   ChatGPT
Prompts:   detailed in conversation document 
'''
import sys
from collections import deque

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = None  # Initialize response time to None
        self.first_execution_time = None  # Initialize first execution time to None

def read_input_file(file_path):
        processes = []
        run_time = 0

        with open(file_path, 'r') as file:
            for line in file:
                tokens = line.strip().split()
                if tokens[0] == 'process':
                    name = tokens[2]
                    arrival_time = int(tokens[4])
                    burst_time = int(tokens[6])
                    processes.append(Process(name, arrival_time, burst_time))
                elif tokens[0] == 'runfor':
                    run_time = int(tokens[1])

        return processes, run_time

file_out = ""

def write_out(string):
    global file_out
    file_out += string + '\n'

def calculate_metrics(processes):
    for process in processes:
        process['turnaround'] = process['finish'] - process['arrival']
        process['wait'] = process['first_exe_time'] - process['arrival']
        process['response'] = process['first_exe_time'] - process['arrival']
        
def fcfs(processes, runfor, input_file_path):
    output_file_path = input_file_path[:-3] + ".out"  # Change the file extension to .out
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"{len(processes)} processes\n")
        output_file.write("Using First-Come First-Served\n")

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
                queue.append(process)
                output_file.write(f"Time {i:3} : {process['name']} arrived\n")

            # Check if the active process is finished
            if active_process and active_process["burst"] == 0:
                active_process["finish"] = i
                finished_processes.append(active_process)
                output_file.write(f"Time {i:3} : {active_process['name']} finished\n")
                active_process = None

            if queue and not active_process:
                active_process = queue.popleft()
                active_process["first_exe_time"] = i
                output_file.write(f"Time {i:3} : {active_process['name']} selected (burst   {active_process['burst']})\n")
                
            # If no active process, print idle
            if not active_process:
                output_file.write(f"Time {i:3} : Idle\n")

        output_file.write(f"Finished at time  {runfor}\n")
        calculate_metrics(finished_processes)

        unfinished_processes = [process['name'] for process in processes]
        if unfinished_processes:
            output_file.write("process did not finish:\n") 
            for name in unfinished_processes:
                output_file.write(f"{name} did not finish\n")   

        output_file.write("\n")   
        for process in sorted(finished_processes, key=lambda x: x['name']):
            output_file.write(f"{process['name']} wait {process['wait']} turnaround {process['turnaround']} response {process['response']}\n")

    print(f"Output written to {output_file_path}")
    
def sjf(input_file_path):
    
    input_file_path = input_file_path
    processes, run_time = read_input_file(input_file_path)

    output_file_path = input_file_path[:-3] + ".out"  # Change the file extension to .out
    with open(output_file_path, 'w') as output_file:
        # Count the number of processes
        num_processes = len(processes)
        output_file.write(f"{num_processes} processes\n")

        # Write the preemptive algorithm type
        output_file.write("Using preemptive Shortest Job First\n")

        time_chart = []
        current_time = 0
        prev_selected_process = None
        printed_arrivals = set()

        while current_time < run_time or any(p.remaining_time > 0 for p in processes):
            eligible_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

            if not eligible_processes:
                # No eligible processes, idle time
                time_chart.append((f"Time {current_time:3d} : Idle", 1))
                current_time += 1
                prev_selected_process = None  # Reset the previous selected process
                printed_arrivals.clear()  # Clear the set for the next time unit
            else:
                # Check for arrivals
                for process in eligible_processes:
                    if process.remaining_time == process.burst_time and process not in printed_arrivals:
                        if process.response_time is None:
                            process.response_time = current_time - process.arrival_time
                        time_chart.append((f"Time {current_time:3d} : {process.name} arrived", 0))
                        printed_arrivals.add(process)

                # Select the process with the shortest remaining time
                selected_process = min(eligible_processes, key=lambda p: p.remaining_time)

                # Check for first execution time
                if selected_process.first_execution_time is None:
                    selected_process.first_execution_time = current_time

                # Execute the process for 1 time unit
                if selected_process != prev_selected_process:
                    if selected_process.remaining_time > 0:
                        time_chart.append((f"Time {current_time:3d} : {selected_process.name} selected (burst {selected_process.remaining_time})", 1))
                    else:
                        time_chart.append((f"Time {current_time:3d} : {selected_process.name} finished", 0))
                    prev_selected_process = selected_process

                # Update wait time for all other processes
                for process in processes:
                    if process != selected_process and process.remaining_time > 0:
                        process.wait_time += 1

                selected_process.remaining_time -= 1

                # Check if the selected process has finished
                if selected_process.remaining_time == 0:
                    selected_process.turnaround_time = current_time + 1 - selected_process.arrival_time
                    time_chart.append((f"Time {current_time + 1:3d} : {selected_process.name} finished", 0))

                current_time += 1

        # Check if any processes did not finish
        unfinished_processes = [process.name for process in processes if process.remaining_time > 0]
        if unfinished_processes:
            output_file.write("\nProcesses did not finish:\n")
            for process_name in unfinished_processes:
                output_file.write(f"{process_name} did not finish\n")

        time_chart.append((f"Finished at time  {current_time}\n", 0))

        # Write the time chart to the file (left-aligned)
        for entry in time_chart:
            output_file.write(f"{entry[0]:<30}\n")

        # Write the summary to the file (right-justified)
        for process in processes:
            output_file.write(f"{process.name} wait {max(process.wait_time - process.arrival_time, 0):>3d} turnaround {process.turnaround_time:>3d} response {process.first_execution_time - process.arrival_time if process.first_execution_time is not None else 0:>3d}\n")

    print(f"Output written to {output_file_path}")

def ljf(input_file_path):
    input_file_path = input_file_path
    processes, run_time = read_input_file(input_file_path)

    output_file_path = input_file_path[:-3] + ".out"  # Change the file extension to .out
    with open(output_file_path, 'w') as output_file:
        # Count the number of processes
        num_processes = len(processes)
        output_file.write(f"{num_processes} processes\n")

        # Write the preemptive algorithm type
        output_file.write("Using preemptive Longest Job First\n")

        time_chart = []
        current_time = 0
        prev_selected_process = None
        printed_arrivals = set()

        while current_time < run_time or any(p.remaining_time > 0 for p in processes):
            eligible_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

            if not eligible_processes:
                # No eligible processes, idle time
                time_chart.append((f"Time {current_time:3d} : Idle", 1))
                current_time += 1
                prev_selected_process = None  # Reset the previous selected process
                printed_arrivals.clear()  # Clear the set for the next time unit
            else:
                # Check for arrivals
                for process in eligible_processes:
                    if process.remaining_time == process.burst_time and process not in printed_arrivals:
                        if process.response_time is None:
                            process.response_time = current_time - process.arrival_time
                        time_chart.append((f"Time {current_time:3d} : {process.name} arrived", 0))
                        printed_arrivals.add(process)

                # Select the process with the longest remaining time
                selected_process = max(eligible_processes, key=lambda p: p.remaining_time)

                # Check for first execution time
                if selected_process.first_execution_time is None:
                    selected_process.first_execution_time = current_time

                # Execute the process for 1 time unit
                if selected_process != prev_selected_process:
                    if selected_process.remaining_time > 0:
                        time_chart.append((f"Time {current_time:3d} : {selected_process.name} selected (burst {selected_process.remaining_time})", 1))
                    else:
                        time_chart.append((f"Time {current_time:3d} : {selected_process.name} finished", 0))
                    prev_selected_process = selected_process

                # Update wait time for all other processes
                for process in processes:
                    if process != selected_process and process.remaining_time > 0:
                        process.wait_time += 1

                selected_process.remaining_time -= 1

                # Check if the selected process has finished
                if selected_process.remaining_time == 0:
                    selected_process.turnaround_time = current_time + 1 - selected_process.arrival_time
                    time_chart.append((f"Time {current_time + 1:3d} : {selected_process.name} finished", 0))

                current_time += 1

        # Check if any processes did not finish
        unfinished_processes = [process.name for process in processes if process.remaining_time > 0]
        if unfinished_processes:
            output_file.write("\nProcesses did not finish:\n")
            for process_name in unfinished_processes:
                output_file.write(f"{process_name} did not finish\n")

        time_chart.append((f"Finished at time  {current_time}\n", 0))

        # Write the time chart to the file (left-aligned)
        for entry in time_chart:
            output_file.write(f"{entry[0]:<30}\n")

        # Write the summary to the file (right-justified)
        for process in processes:
            output_file.write(f"{process.name} wait {max(process.wait_time - process.arrival_time, 0):>3d} turnaround {process.turnaround_time:>3d} response {process.first_execution_time - process.arrival_time if process.first_execution_time is not None else 0:>3d}\n")

    print(f"Output written to {output_file_path}")

def round_robin(processes, runfor, quantum):
    write_out(f"{len(processes)} processes")
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

    if len(sys.argv) != 2:
        print("Usage: python scheduler.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename) as file:
        lines = file.readlines()

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

    processes.sort(key=lambda x: x['arrival'])

    if directives['use'] == "fcfs":
        fcfs(processes, int(directives["runfor"]), filename)
    elif directives['use'] == "sjf":
        sjf(filename)
    elif directives['use'] == "ljf":
        ljf(filename)
    elif directives['use'] == "rr":
        if 'quantum' not in directives:
            write_out("Error: Missing quantum parameter when use is 'rr'")
            return
        finished_processes = round_robin(processes, int(directives['runfor']), int(directives['quantum']))
        finished_processes.sort(key=lambda x: x['name'])
        write_out("")
        for process in finished_processes:
            write_out(f"{process['name']} wait {process['wait']} turnaround {process['turnaround']} response {process['response']}")
        # the following was moved/inserted to be consistent with the other methods
        with open(filename.replace('.in', '.out'), 'w') as f:
            f.write(file_out)
        print(f"Output written to {filename.replace('.in', '.out')}")

if __name__ == "__main__":
    main()
import sys

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # Initialize response time to -1

def sjf_scheduler(processes, run_time, output_file):
    time_chart = []

    current_time = 0
    prev_selected_process = None
    printed_arrivals = set()

    while current_time < run_time:
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
                    if process.response_time == -1:
                        process.response_time = current_time - process.arrival_time
                    time_chart.append((f"Time {current_time:3d} : {process.name} arrived", 0))
                    printed_arrivals.add(process)

            # Select the process with the shortest remaining time
            selected_process = min(eligible_processes, key=lambda p: p.remaining_time)

            # Execute the process for 1 time unit
            if selected_process != prev_selected_process:
                if selected_process.remaining_time > 0:
                    time_chart.append((f"Time {current_time:3d} : {selected_process.name} selected (burst {selected_process.remaining_time})", 1))
                else:
                    time_chart.append((f"Time {current_time:3d} : {selected_process.name} finished", 0))

            selected_process.remaining_time -= 1
            current_time += 1

            if selected_process.remaining_time == 0:
                selected_process.turnaround_time = current_time - selected_process.arrival_time
                selected_process.wait_time = selected_process.turnaround_time - selected_process.burst_time
                time_chart.append((f"Time {current_time:3d} : {selected_process.name} finished", 0))

            prev_selected_process = selected_process

    # Check if any processes did not finish
    unfinished_processes = [process.name for process in processes if process.remaining_time > 0]
    if unfinished_processes:
        output_file.write("\nProcesses did not finish:\n")
        for process_name in unfinished_processes:
            output_file.write(f"{process_name} did not finish\n")

    time_chart.append((f"Finished at time {current_time}", 0))

    return time_chart



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

def print_summary(processes):
    print("\nSummary:")
    for process in processes:
        print(f"{process.name} wait {process.wait_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time:3d}")


def print_process_info(processes):
    print("Processes:")
    for process in processes:
        print(f"Name: {process.name}, Arrival Time: {process.arrival_time}, Burst Time: {process.burst_time}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.in")
        sys.exit(1)

    input_file_path = sys.argv[1]
    processes, run_time = read_input_file(input_file_path)

    output_file_path = input_file_path[:-3] + ".out"  # Change the file extension to .out
    with open(output_file_path, 'w') as output_file:
        time_chart = sjf_scheduler(processes, run_time, output_file)

        # Write the formatted output to the file
        for entry in time_chart:
            output_file.write(entry[0] + '\n')

        # Write the summary to the file
        output_file.write("\nSummary:\n")
        for process in processes:
            output_file.write(f"{process.name} wait {process.wait_time} turnaround {process.turnaround_time} response {process.response_time}\n")

    print(f"Output written to {output_file_path}")


if __name__ == "__main__":
    main()

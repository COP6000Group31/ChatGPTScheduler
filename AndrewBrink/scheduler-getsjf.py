import sys

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

def sjf(input_file_path):
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.in")
        sys.exit(1)

    input_file_path = sys.argv[1]
    sjf(input_file_path)

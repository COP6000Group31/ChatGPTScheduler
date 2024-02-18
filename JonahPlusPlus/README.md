# Prompt

Write a Python script that demonstrates a scheduling algorithm by doing the following:
Open up a file passed to it from the terminal.

Here is an example of the file contents (called "<name>.in"):
```
processcount 3  # Read 3 processes
runfor 20   	# Run for 20 time units
use sjf
process name A arrival 0 burst 5
process name B arrival 1 burst 4
process name C arrival 4 burst 2
end
```
And the corresponding output (called "<name>.out"):
```
3 processes
Using preemptive Shortest Job First
Time   0 : A arrived
Time   0 : A selected (burst   5)
Time   1 : B arrived
Time   4 : C arrived
Time   5 : A finished
Time   5 : C selected (burst   2)
Time   7 : C finished
Time   7 : B selected (burst   4)
Time  11 : B finished
Time  11 : Idle
Time  12 : Idle
Time  13 : Idle
Time  14 : Idle
Time  15 : Idle
Time  16 : Idle
Time  17 : Idle
Time  18 : Idle
Time  19 : Idle
Finished at time  20

A wait   0 turnaround   5  response 0
B wait   6 turnaround  10  response 6
C wait   1 turnaround   3 response 1
```
Store "<name>.out" to a global variable named "file_out", where <name> is from the input file "<name>.in".
Clear the contents of the file "file_out".

Create a function called "write_out", that appends a string to the file in "file_out".

Read each line in the file, ignoring any content that comes after a "#".
Each line has a single directive, which will be parsed and the rest of the line (which can be an integer, a string or nothing) stored into a map under keys of the same name (except for the processes, which use a special format and will be stored in an array). The directives are and appear in this order:
"processcount": an integer; required
"runfor": an integer representing the number of time units; required
"use": a string; one of "fcfs", "sjf", or "rr" (First Come First Serve, Pre-emptive Shortest Job First, and Round Robin respectively); required
"quantum": an integer; not required
"process": has the parameters "name" (a string that is the name of the process), "arrival" (a number that is the time at which the process arrives), "burst" (a number that is the duration of the process), which appear at indices 2, 4, and 6 of the line when split by spaces respectively.
"end": nothing; stop reading the file
If one of the required directives weren't given, or if the number of "process" directives didn't match the value of the "processcount" directive, call "write_out" with an error in the form "Error: Missing parameter <parameter>" and exit.
If "use" is "rr" and "quantum" is not set, pass to "write_out": "Error: Missing quantum parameter when use is 'rr'" and exit.
Then, pass to "write_out":  "  " + variable "processcount" + " processes".
Next, for each process, assign properties for wait time ("wait"), turnaround time ("turnaround") and response time ("response"), as well as "has_run", which should be false.
Finally, sort all processes by the arrival time, before calling the scheduling algorithm with the processes and "runfor" (as well as any other things the algorithm may need).

Leave implementations for "fcfs" and "sjf" as stubs.

If "use" is "rr", demonstrate Round Robin scheduling.
Pass to "write_out": "Using Round-Robin".
Pass to "write_out": "Quantum " + variable "quantum".
Pass to "write_out": a blank line.
Set "active_process" and "current_q" to null and 0 respectively and create an empty queue.
Create an empty array called "finished_processes".
Start a loop over "i" from 0 to "runfor" (exclusive).
In this loop:
If there is an active process, decrement the "burst" of the active process, decrement "current_q".
Then, increment the wait time of each of the processes in the queue.
Next, when "i" is equal to the arrival time of the first of the processes, pop it and push it onto the queue, and call "write_out" with that the process has arrived. Do this until a process has an arrival time not equal to "i".
Next, if there is an active process and it's "burst" is 0, set the turnaround time as "i" - arrival time, add the process to "finished_processes", call "write_out" with that it completed and set the active process to None.
When there is a process in the queue and no current active process, pop it and set it as the active process and set the "current_q" to "quantum"; if "has_run" is False, then set "response" to i - "arrival"; next, set the process "has_run" to true; call "write_out" with that the process has been selected.
After, if there is no active process, call "write_out" with that the scheduler is "Idle" and continue.
Next, if "current_q" is 0, move the active process to the back of the queue and pick the next one;  if "has_run" is False, then set "response" to i - "arrival"; next, set the process "has_run" to true; call "write_out" with that "<name>.out" was selected.
Once the loop is finished, call "write_out" with that it is completed and "runfor".
Return "finished_processes".

Order the returned processes by name.
Finally, call "write_out" for each process the wait time, the turnaround time and the response time.

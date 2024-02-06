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

Read each line in the file, ignoring any content that comes after a "#".
Each line has a single directive, which will be parsed and stored into variables of the same name. The directives are and appear in this order:
"processcount": a number; required
"runfor": a number representing the number of time units; required
"use": one of "fcfs", "sjf", or "rr" (First Come First Serve, Pre-emptive Shortest Job First, and Round Robin respectively); required
"quantum": a number; not required
"process": has the parameters "name" (a string that is the name of the process), "arrival" (a number that is the time at which the process arrives), "burst" (a number that is the duration of the process)
"end": stop reading the file
If one of the required directives weren't given, or if the number of "process" directives didn't match the value of the "processcount" directive, print an error in the form "Error: Missing parameter <parameter>" and exit.
If "use" is "rr" and "quantum" is not set, print "Error: Missing quantum parameter when use is 'rr'" and exit.
Then, print "processes: " + "processcount".
Next, for each process, give it properties for wait time, turnaround time and response time, as well as "has_run", which should be false.
Finally, sort all processes by the arrival time, before calling the scheduling algorithm.

Leave implementations for "fcfs" and "sjf" as stubs.

If "use" is "rr", demonstrate Round Robin scheduling.
Print "Using Round-Robin"
Set "active_process" and "current_q" to null and 0 respectively.
Create an empty array called "finished_processes".
Start a loop over "i" from 0 to "runfor" (exclusive).
In this loop:
When "i" is equal to the arrival time of the first of the processes, pop it and push it onto the queue, and print that the process has arrived. Do this until a process has an arrival time not equal to "i".
When there is a process in the queue and no current active process, pop it and set it as the active process and set the "current_q" to "quantum" and set the process "has_run" to true; print that the process has been selected.
After, if there is no active process, print that the scheduler is "Idle" and continue.
Decrement the "burst" of the active process, decrement "current_q" and increment the wait time and (if "has_run" is false) the response time of each process in the queue.
If "burst" is 0, remove the process, set the turnaround time as "i" - arrival time, add the process to "finished_processes", and print that it completed.
If "current_q" is 0, move the active process to the back of the queue and pick the next one.
Once the loop is finished, print that it is completed and "runfor".
Return "finished_processes".

Finally, print for each process the wait time, the turnaround time and the response time.

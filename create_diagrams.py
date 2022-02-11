import argparse

"""When the program terminates, the timer will send a report
of the following form to std:cerr
```
Timer(expensive): <t> = 8.867us, std = 3.463us, 4.263us <= t <= 57.62us (n=731)
```
which shows the average time spent within expensiveFunction(),
its standard deviation, the upper and lower bounds,
and the total number of calls."""

"""TeamConstProcesses
Timer(TeamConstProcesses<10>[SameNumber | 2]): <t> = 23.9962ms, std = 0ms, 23.9962ms <= t <= 23.9962ms (n=1)

TeamAsync
Timer(CalcCollatzSoloTimer): <t> = 29.5266us, std = 17.1526us, 15.379us <= t <= 456.005us (n=2998)
Timer(TeamAsync<1>[SameNumber | 2]): <t> = 73.4576ms, std = 0ms, 73.4576ms <= t <= 73.4576ms (n=1)"""

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of the file to process")
    parser.add_argument("save", help="Name of the file to save")
    args = parser.parse_args()

    return args.name, args.save

def open_file_return_list_of_lines(path):
    with open(path) as op:
        list_lines = op.readlines()
        res = [i.rstrip() for i in list_lines if i != '' and i != '\n']

        return res

def print_lines(lines):
    for line in lines:
        print(line)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path, name = command_line_args()
    lines = open_file_return_list_of_lines(path)
    print_lines(lines)
    print(lines)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

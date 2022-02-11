import argparse
import re

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

def extract_doubles(line):
    #return [float(i) for i in re.findall('\d+\.\d+', line)]
    return [float(i) for i in re.findall('\d+\.*\d*', line)]

def extract_outer_data(outer_stat):
    halves = outer_stat.split(':')
    res = [int(i) for i in re.findall('\d+', halves[0])]
    find_contest = halves[0].split('|')[0].split('[')[1].rstrip(' ')
    #print(find_contest)
    #print(res)
    res.append(find_contest)
    return res + extract_doubles(halves[1])


def prepare_stats(lines):
    range_lines = len(lines)
    index = 0

    while index < range_lines - 1:
        current_team = lines[index]
        print(current_team)

        if current_team != "TeamNewProcesses" and current_team != "TeamConstProcesses":
            inner_stats = lines[index + 1]
            outer_stats = lines[index + 2]
            #extracted_inner = extract_inner_timer(inner_stats)
            extracted_inner = extract_doubles(inner_stats)
            extracted_inner[-1] = int(extracted_inner[-1])
            print(extracted_inner)
            extracted_outer = extract_outer_data(outer_stats)
            extracted_outer[-1] = int(extracted_outer[-1])
            print(extracted_outer)
            index += 3

        else:
            outer_stats = lines[index + 1]
            extracted_outer = extract_outer_data(outer_stats)
            extracted_outer[-1] = int(extracted_outer[-1])
            print(extracted_outer)
            index += 2

    print("Total")
    total = extract_doubles(lines[-1])
    total[-1] = int(total[-1])
    print(total)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path, name = command_line_args()
    lines = open_file_return_list_of_lines(path)
  #  print_lines(lines)
 #   print(lines)
    prepare_stats(lines)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

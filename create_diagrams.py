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
    parser.add_argument("my1", help="Name of the file to process")
    parser.add_argument("my2", help="Name of the file to process")
    parser.add_argument("my3", help="Name of the file to process")

    parser.add_argument("s1", help="Name of the file to process")
    parser.add_argument("s2", help="Name of the file to process")
    parser.add_argument("s3", help="Name of the file to process")

    #parser.add_argument("save", help="Name of the file to save")
    args = parser.parse_args()

    return args.my1, args.my2, args.my3, args.s1, args.s2, args.s3

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

    final = {}

    while index < range_lines - 1:
        current_team = lines[index]
        print(current_team)

        if current_team not in final.keys():
            final[current_team] = {}

        if current_team != "TeamNewProcesses" and current_team != "TeamConstProcesses":
            inner_stats = lines[index + 1]
            outer_stats = lines[index + 2]
            print(outer_stats)
            #extracted_inner = extract_inner_timer(inner_stats)
            extracted_inner = extract_doubles(inner_stats)
            extracted_inner[-1] = int(extracted_inner[-1])
            print(extracted_inner)
            extracted_outer = extract_outer_data(outer_stats)
            extracted_outer[-1] = int(extracted_outer[-1])

            stats = {}
            stats['solo'] = extracted_inner
            stats['total'] = extracted_outer[3:]
            comp_name = extracted_outer[2]

            if comp_name not in final[current_team].keys():
                final[current_team][comp_name] = {}

            current_comp = final[current_team][comp_name]
            current_comp['num_workers'] = extracted_outer[0]
            current_comp['seed'] = extracted_outer[1]
            current_comp['stats'] = stats
            print(extracted_outer)
            index += 3

        else:
            outer_stats = lines[index + 1]
            extracted_outer = extract_outer_data(outer_stats)
            extracted_outer[-1] = int(extracted_outer[-1])

            stats = {}
            stats['solo'] = None
            stats['total'] = extracted_outer[3:]
            comp_name = extracted_outer[2]

            if comp_name not in final[current_team].keys():
                final[current_team][comp_name] = {}

            current_comp = final[current_team][comp_name]
            current_comp['num_workers'] = extracted_outer[0]
            current_comp['seed'] = extracted_outer[1]
            current_comp['stats'] = stats

            print(extracted_outer)
            index += 2

    print("Total")
    total = extract_doubles(lines[-1])
    total[-1] = int(total[-1])
    final['Total'] = {}
    final['Total']['stats'] = total

    print(total)

    return final
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    m1, m2, m3, s1, s2, s3 = command_line_args()

    m1_res = open_file_return_list_of_lines(m1)
    m2_res = open_file_return_list_of_lines(m2)
    m3_res = open_file_return_list_of_lines(m3)

    s1_res = open_file_return_list_of_lines(s1)
    s2_res = open_file_return_list_of_lines(s2)
    s3_res = open_file_return_list_of_lines(s3)
  #  print_lines(lines)
 #   print(lines)
    m1_stats = prepare_stats(m1_res)
    m2_stats = prepare_stats(m2_res)
    m3_stats = prepare_stats(m3_res)

    s1_stats = prepare_stats(s1_res)
    s2_stats = prepare_stats(s2_res)
    s3_stats = prepare_stats(s3_res)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import argparse
import re
import matplotlib.pyplot as plt
import numpy as np
import statistics

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
                final[current_team][comp_name] = []

            current_comp = final[current_team][comp_name]
            # current_comp['num_workers'] = extracted_outer[0]
            # current_comp['seed'] = extracted_outer[1]
            # current_comp['stats'] = stats
            #current_comp[extracted_outer[0]] = [extracted_outer[1], stats]
            unitNum = outer_stats.split(',')[1].split()[2]
            unit = re.findall('\D+', unitNum)

            current_comp.append([extracted_outer[0], extracted_outer[1], stats, unit[0]])
            print(extracted_outer)
            index += 3

        else:
            outer_stats = lines[index + 1]
            extracted_outer = extract_outer_data(outer_stats)
            extracted_outer[-1] = int(extracted_outer[-1])

            unitNum = outer_stats.split(',')[1].split()[2]
            unit = re.findall('\D+', unitNum)
            stats = {}
            stats['solo'] = None
            stats['total'] = extracted_outer[3:]
            comp_name = extracted_outer[2]

            if comp_name not in final[current_team].keys():
                final[current_team][comp_name] = []

            current_comp = final[current_team][comp_name]
            # current_comp['num_workers'] = extracted_outer[0]
            # current_comp['seed'] = extracted_outer[1]
            # current_comp['stats'] = stats
            #current_comp[extracted_outer[0]] = [extracted_outer[1], stats]
            current_comp.append([extracted_outer[0], extracted_outer[1], stats, unit[0]]) #num threads, seed, {solo, total}

            print(extracted_outer)
            index += 2

    print("Total")
    total = extract_doubles(lines[-1])
    #total[-1] = int(total[-1])
    #total = total[:-1]
    total = total[0]
    #final['Total'] = {}
    #final['Total']['stats'] = total
    final['Total'] = total

    print(total)

    return final
# Press the green button in the gutter to run the script.

def create_total_diagram(m1, m2, m3, s1, s2, s3):
    plt.figure()
    names = ['Pierwsza_proba', 'Druga_proba', 'Trzecia_proba']
    m_val = [m1['Total'], m2['Total'], m3['Total']]
    print(m_val)
    s_val = [s1['Total'], s2['Total'], s3['Total']]
    plt.plot(names, m_val, 'ro', label='laptop')
    plt.plot(names, s_val, 'bo', label='students')
    plt.title('Całkowity czas obliczeń na dwóch środowiskach')
    plt.ylabel('Czas [min]')
    plt.yticks(np.arange(min(min(m_val), min(s_val)) - 0.5, max(max(m_val), max(s_val)) + 1.0, 0.25))
    ax = plt.gca()
    temp = ax.yaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::4]))
    for label in temp:
        label.set_visible(False)
    plt.legend(loc='center right')
    plt.show()

def solo_stats(team_contest):
    # x_axis = []
    # stddev = []
    # minT = []
    # maxT = []
    # avr = []

    res = {}
    for workers in team_contest:
        num_workers = workers[0]
        if num_workers not in res.keys():
            res[num_workers] = [[],[],[],[],[]] #x_axis, std, min, max, avr
        # x_axis = []
        # stddev = []
        # minT = []
        # maxT = []
        # avr = []
 #       for contest in team_contest:
        print(workers)
        cur_work = res[num_workers]
        work_stats = workers[2]
        solo_work = work_stats['solo']
        # x_axis.append(str(workers[1]) + '\n[' + str(solo_work[-1]) + ']')
        # minT.append(solo_work[2])
        # maxT.append(solo_work[3])
        # avr.append(solo_work[0])
        # stddev.append(solo_work[1])
        cur_work[0].append(str(workers[1]) + '\n[' + str(solo_work[-1]) + ']')
        cur_work[2].append(solo_work[2])
        cur_work[3].append(solo_work[3])
        cur_work[4].append(solo_work[0])
        cur_work[1].append(solo_work[1])


    #return x_axis, stddev, minT, maxT, avr
    return res

def plot_contest_for_team(contest, team, stats, where):
    plt.figure()
    team_stats = stats[team]
    team_contest = team_stats[contest]

    #x_axis, stddev, minT, maxT, avr = solo_stats(team_contest)
    for_num_workers = solo_stats(team_contest)

    x_axis, stddev, minT, maxT, avr = for_num_workers[1]
    plt.figure()
    plt.xlabel('Rozmiar ziarna\n[Liczba danych]')
    plt.ylabel('Czas [us]')
    plt.title(contest + ' dla ' + team + ' na ' + where)

    colours = ['r', 'b', 'c', 'g', 'y', 'k']
    for ind, num_worker in enumerate(for_num_workers.keys()):
        print(ind)
        x_axis, stddev, minT, maxT, avr = for_num_workers[num_worker]

        plt.plot(x_axis, minT, colours[ind] + 'o', label='Min czas, liczba wątków: ' + str(num_worker))
        plt.plot(x_axis, maxT, colours[ind] + '^', label='Max czas, liczba wątków: ' + str(num_worker))
        plt.plot(x_axis, avr, colours[ind], label='Średni czas, liczba wątków: ' + str(num_worker))

    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.legend(loc='upper left')
    # plt.plot(x_axis, minT, 'ro')
    # plt.plot(x_axis, maxT, 'r^')
    # plt.plot(x_axis, avr, 'r')

    plt.show()

def convert_to_ms(val, unit):
    if unit == 's':
        return val*1000.0
    if unit == 'us':
        return val/1000.0
    else:
        return val

def compare_mean_contests(stats, contest_name):
    contest_res_per_team = {}

    for team in stats.keys():
        #print(team)
        if team != 'Total':
            contest_res_per_team[team] = stats[team][contest_name]

    for key, val in contest_res_per_team.items():
        print(key, val)

    setSeeds = set()
    for elem in contest_res_per_team['TeamSolo']:
        setSeeds.add(elem[1])

    print(setSeeds)

    meansTeams = {}
    for team in contest_res_per_team.keys():
        cur_team = contest_res_per_team[team]

        for seed in setSeeds:
            to_mean = []
            for record in cur_team:
                if record[1] == seed:
                    #print('hete', record)
                    to_mean.append(convert_to_ms(record[2]['total'][0], record[-1]))
  #          print(to_mean)
            if team not in meansTeams.keys():
                meansTeams[team] = []
            meansTeams[team].append([seed, round(statistics.mean(to_mean), 4)])

    for key, val in meansTeams.items():
        print(key, val)

    colours = ['r', 'b', 'c', 'g', 'k', 'y', 'm']
    plt.title(contest_name + " - średni czas dla wszystkich zespołów")
    plt.xlabel("Dane inicjujące")
    plt.ylabel("Czas [ms]")

    x_list = [str(i) for i in setSeeds]
    means_all = []
    for ind, team in enumerate(meansTeams.keys()):
        to_plot = []
        team_means = meansTeams[team]
        for rec in team_means:
            to_plot.append(rec[1])
            means_all.append(rec[1])
        print(ind, team)
        plt.plot(x_list, to_plot, colours[ind] + '-*', label = team)

    plt.legend(loc='upper left')

    plt.tick_params(labelright=True)
    plt.show()

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

   # create_total_diagram(m1_stats, m2_stats, m3_stats, s1_stats, s2_stats, s3_stats)
    #plot_contest_for_team('LongNumber', 'TeamPool', s1_stats, 'studentsie')
    compare_mean_contests(m1_stats, "LongNumber")
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

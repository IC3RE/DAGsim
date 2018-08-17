import sys
import csv
import configparser
import ast
import numpy as np

def update_progress(progress, transaction):
    bar_length = 50 #Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "Error: Progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "| Simulation completed...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent:  [{0}] {1}% | Number:  {2} {3}".\
        format( "#"*block + "-"*(bar_length-block), np.round((progress*100),1), transaction, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def create_distance_matrix(self, distance):
    m = [[distance] * self.no_of_agents for i in range(self.no_of_agents)]
    for i in range(self.no_of_agents):
        m[i][i] = 0
    return m


def common_elements(a, b):
    a_set = set(a)
    b_set = set(b)

    if len(a_set.intersection(b_set)) > 0:
        return list((a_set.intersection(b_set)))
    else:
        return []


def load_file(filename):

    try:

        config = configparser.ConfigParser()
        config.read(filename)

        data = []

        simulation_config_parameters = config['PARAMETERS']

        _no_of_transactions = int(simulation_config_parameters['no_of_transactions'])
        _lambda = float(simulation_config_parameters['lambda'])
        _no_of_agents = int(simulation_config_parameters['no_of_agents'])
        _alpha = float(simulation_config_parameters['alpha'])
        _latency = int(simulation_config_parameters['latency'])
        _distance = float(simulation_config_parameters['distance'])
        _tip_selection_algo = simulation_config_parameters['tip_selection_algo']
        _agent_choice = simulation_config_parameters['agent_choice']
        if (_agent_choice == 'None'):
            _agent_choice = list(np.ones(_no_of_agents) / _no_of_agents)
        else:
            _agent_choice = ast.literal_eval(_agent_choice)
        _printing = config.getboolean('PARAMETERS','printing')

        data.append((_no_of_transactions, _lambda, _no_of_agents, \
        _alpha, _latency, _distance, _tip_selection_algo, _agent_choice, _printing))

        for key in config:
            if(key != 'PARAMETERS' and key != 'DEFAULT'):
                print(key)

                event_change_parameters = config[key]
                step = int(event_change_parameters['step'])

                if 'distance' not in event_change_parameters:
                    _distance = None
                else:
                    _distance = float(event_change_parameters['distance'])

                if 'agent_choice' not in event_change_parameters:
                    _agent_choice = None
                else:
                    _agent_choice = ast.literal_eval(event_change_parameters['agent_choice'])
                data.append((step, _distance, _agent_choice))

        print(data)
    except Exception as e:
        print(e)

    return data

    # f = open(filename, 'r')
    # lines = []
    # first_line = f.readline()
    #
    # _no_of_transactions, _lambda, _no_of_agents, \
    # _alpha, _latency, _distance, _tip_selection_algo, \
    # _printing = first_line.strip().split(",")
    #
    # lines.append((int(_no_of_transactions), float(_lambda), int(_no_of_agents), \
    # float(_alpha), int(_latency), float(_distance), _tip_selection_algo, bool(_printing)))
    #
    # for line in f:
    #     ts_string, _, rest = line.strip().partition(",")
    #     dist_string, _, ac_string = rest.partition(",")
    #
    #     if ts_string=="" or dist_string=="" or ac_string=="":
    #         print("Badly formed line: {}".format(line))
    #         sys.exit(1)
    #
    #     transaction = int(ts_string)
    #
    #     if dist_string=="null":
    #         distance = None
    #     else:
    #         distance = float(dist_string)
    #
    #     if ac_string=="null":
    #         agent_choice = None
    #     else:
    #         agent_choice = [float(x) for x in eval(ac_string)]
    #
    #     if agent_choice != None and sum(agent_choice) != 1.0:
    #         print("Agent choice not summing to 1.0: {}".format(sum(agent_choice)))
    #         sys.exit(1)
    #     lines.append((transaction, distance, agent_choice))
    #
    # return lines


def csv_export(self):

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        #Write genesis
        writer.writerow([0,[]])
        for transaction in self.DG.nodes:
            #Write all other transaction
            if(transaction.arrival_time != 0):
                line = []
                line.append(transaction)
                line.append(list(self.DG.successors(transaction)))
                # line.append(transaction.arrival_time)
                # line.append(transaction.agent)
                writer.writerow(line)

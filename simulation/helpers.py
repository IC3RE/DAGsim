import sys
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


def common_elements(a, b):
    a_set = set(a)
    b_set = set(b)

    if len(a_set.intersection(b_set)) > 0:
        return list((a_set.intersection(b_set)))
    else:
        return []


def csv_export(self):

    with open('some.csv', 'w', newline='') as file:
        writer = csv.writer(file, dialect='excel')

        for transaction in self.DG.nodes:
            line = []
            line.append(transaction)
            line.append(list(self.DG.successors(transaction)))
            line.append(transaction.arrival_time)
            line.append(transaction.agent)
            writer.writerow(line)

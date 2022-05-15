import main
from common import Task, STOP, GNN_TYPE
from attrdict import AttrDict
from experiment import Experiment
import torch
from torch_geometric.utils import to_networkx, from_networkx
import rewiring
import networkx as nx
import numpy as np
from numpy import random
import torch.multiprocessing as mp

override_params = {
    2: {'batch_size': 64, 'eval_every': 1000},
    3: {'batch_size': 64},
    4: {'batch_size': 1024},
    5: {'batch_size': 1024},
    6: {'batch_size': 1024},
    7: {'batch_size': 2048},
    8: {'batch_size': 1024, 'accum_grad': 2},  # effective batch size of 2048, with less GPU memory
}


class Results:
    def __init__(self, train_acc, test_acc, epoch):
        self.train_acc = train_acc
        self.test_acc = test_acc
        self.epoch = epoch

def run(name):
    task = Task.DEFAULT
    gnn_type = GNN_TYPE.GCN

    hyperparams = {
    "cornell": AttrDict({"skip_connection": 0.1, "dropout": 0.2411, "num_layers": 1, "dim": 128, "learning_rate": 0.0172, "weight_decay": 0.0125, "max_iterations": 135, "temperature": 130, "C_plus": 0.25}),
    "texas": AttrDict({"skip_connection": 0.1, "dropout": 0.5954, "num_layers": 1, "dim": 128, "learning_rate": 0.0278, "weight_decay": 0.0623, "max_iterations": 47, "temperature": 172, "C_plus": 2.25}),
    "wisconsin": AttrDict({"skip_connection": 0.1, "dropout": 0.6033, "num_layers": 1, "dim": 128, "learning_rate": 0.0295, "weight_decay": 0.1920, "max_iterations": 27, "temperature": 32, "C_plus": 0.5}),
    "chameleon": AttrDict({"skip_connection": 0.1, "dropout": 0.7265, "num_layers": 2, "dim": 128, "learning_rate": 0.0180, "weight_decay": 0.2101, "max_iterations": 400, "temperature": 77, "C_plus": 3.35}),
    "squirrel": AttrDict({"skip_connection": 0.1, "dropout": 0.7401, "num_layers": 2, "dim": 16, "learning_rate": 0.0189, "weight_decay": 0.2255, "max_iterations": 6157, "temperature": 178, "C_plus": 0.5}),
    "actor": AttrDict({"skip_connection": 0.1, "dropout": 0.6866, "num_layers": 1, "dim": 128, "learning_rate": 0.0095, "weight_decay": 0.0727, "max_iterations": 1010, "temperature": 69, "C_plus": 1.22}),
    "cora": AttrDict({"skip_connection": 0.1, "dropout": 0.3396, "num_layers": 1, "dim": 128, "learning_rate": 0.0244, "weight_decay": 0.1076, "max_iterations": 100, "temperature": 163, "C_plus": 0.95}),
    "citeseer": AttrDict({"skip_connection": 0.1, "dropout": 0.4103, "num_layers": 1, "dim": 64, "learning_rate": 0.0199, "weight_decay": 0.4551, "max_iterations": 84, "temperature": 180, "C_plus": 0.22}),
    "pubmed": AttrDict({"skip_connection": 0.1, "dropout": 0.3749, "num_layers": 3, "dim": 128, "learning_rate": 0.0112, "weight_decay": 0.0138, "max_iterations": 166, "temperature": 115, "C_plus": 14.43}),
    }
    max_iterations = 5000 * random.random()
    num_layers = random.choice([1,2,3,4,5,6,7])
    hyperparams[name] += AttrDict({"max_iterations": max_iterations, "num_layers": num_layers})
    stopping_criterion = STOP.VALIDATION
    num_trials=20
    accuracies = []
    
    for trial in range(num_trials):
        dataset = task.get_dataset()
        dataset.generate_data(name)
        args = main.get_fake_args(task=task, num_layers=hyperparams[name].num_layers, loader_workers=7, type=gnn_type, stop=stopping_criterion, dataset=dataset, last_layer_fully_adjacent=False)
        G = to_networkx(dataset.graph, to_undirected=True)
        for i in range(int(hyperparams[name].max_iterations)):
                    rewiring.rlef(G)
        dataset.graph.edge_index = from_networkx(G).edge_index
        train_acc, validation_acc, test_acc, epoch = Experiment(args).run()
        args += hyperparams[name]
        accuracies.append(test_acc)
        #print((str(subprocess.check_output('nvidia-smi').decode('unicode_escape'))))
    print("MAX ITERATIONS: ", max_iterations)
    print("NUM LAYERS: ", num_layers)
    print("average acc: ", np.average(accuracies))
    print("plus/minus: ", 2 * np.std(accuracies)/(num_trials ** 0.5))
    print("\n")
    return np.average(accuracies), max_iterations





if __name__ == '__main__':
    #print(run('cornell'))
    names = ['chameleon', 'squirrel', 'actor']
    mp.set_start_method('spawn')
    for name in names:
        print("-----------------TESTING: ", name, "-----------------")
        with mp.Pool(5) as p:
            p.map(run, [name] * 100)

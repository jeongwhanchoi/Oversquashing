import argparse
import ast
from attrdict import AttrDict

def get_args_from_input():
	parser = argparse.ArgumentParser(description='modify network parameters', argument_default=argparse.SUPPRESS)

	parser.add_argument('--learning_rate', metavar='', type=float, help='learning rate')
	parser.add_argument('--max_epochs', metavar='', type=int, help='maximum number of epochs for training')
	parser.add_argument('--layer_type', metavar='', help='type of layer in GNN (GCN, GIN, GAT, etc.)')
	parser.add_argument('--display', metavar='', type=bool, help='toggle display messages showing training progress')
	parser.add_argument('--device', metavar='', type=str, help='name of device to use for training')
	parser.add_argument('--eval_every', metavar='X', type=int, help='calculate validation/test accuracy every X epochs')
	parser.add_argument('--stopping_criterion', metavar='', type=str, help='model stops training when this criterion stops improving (can be train, validation, or test)')
	parser.add_argument('--stopping_threshold', metavar='T', type=float, help="model perceives no improvement when it does worse than (best loss) * T")
	parser.add_argument('--patience', metavar='P', type=int, help='model stops training after P epochs with no improvement')
	parser.add_argument('--dropout', metavar='', type=float, help='layer dropout probability')
	parser.add_argument('--hidden_dim', metavar='', type=int, help='width of hidden layer')
	parser.add_argument('--hidden_layers', metavar='', type=ast.literal_eval, help='list containing dimensions of all hidden layers')
	parser.add_argument('--num_layers', metavar='', type=int, help='number of hidden layers')
	parser.add_argument('--batch_size', metavar='', type=int, help='number of samples in each training batch')
	parser.add_argument('--num_trials', metavar='', type=int, help='number of times the network is trained'),
	parser.add_argument('--rewiring', metavar='', type=str, help='type of rewiring to be performed'),
	parser.add_argument('--num_iterations', metavar='', type=int, help='number of iterations of rewiring'),
	parser.add_argument('--num_graphs', metavar='', type=int, help='number of graphs in dataset for neighborsmatch task')
	arg_values = parser.parse_args()
	return AttrDict(vars(arg_values))
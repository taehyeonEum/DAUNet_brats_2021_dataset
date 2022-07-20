import sys
from required_classes.config import parse_args_
from required_classes.train import Train_DBC
from visualization.visualization_2d import visualize_2d
from visualization.visualization_3d import visualize_3d

def main_():
    args = parse_args_(sys.argv[1:])
    if args['model_name'] == None:
        model_name = Train_DBC(args)() #you can put model name manualy if you already have trained model
    else:
        model_name = args['model_name']

    if args['visualization'] == 'none':
        return
    elif args['visualization'] == '2d':
        visualize_2d(args['device'], str(model_name))
        return
    elif args['visualization'] == '3d':
        visualize_3d(args['device'], str(model_name))
        return
    elif args['visualization'] == 'both':
        visualize_2d(args['device'], str(model_name))
        visualize_3d(args['device'], str(model_name))
        return

if __name__ == '__main__':
    main_()
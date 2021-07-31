import configparser
import numpy
import os.path
import matplotlib.pyplot as plt
import neuralNetwork
from gui import *
import tkinter as tk

from config import size


def save_effective(file_name, label, effective):
    with open(file_name, 'a') as file:
        file.write(label + " " + effective + '\n')

def make_gui(nn):
    root = tk.Tk()
    main_window = MainWindow(nn=nn, root=root)
    root.geometry('{}x{}'.format(size[0], size[1]))
    root.mainloop()

def main():
    input_nodes = 784
    output_nodes = 10
    hidden_nodes = 1000
    lr = 0.15
    nn = neuralNetwork.neuralNetwork(input_nodes, hidden_nodes, output_nodes, lr)
    print('line 1')
    nn.train_with_mnist("mnist_dataset/mnist_train.csv", epoches=4, log_progess=True)
    nn.save_weights(str(input_nodes) + "who", str(input_nodes) + "wih")
    ef = nn.test_with_mnist("mnist_dataset/mnist_test.csv")
    print(ef)
    make_gui(nn)


if __name__ == "__main__":
    main()

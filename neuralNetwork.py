import numpy
import scipy.special
from progress.bar import IncrementalBar


class neuralNetwork:

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inputnodes = inputnodes
        self.hiddennodes = hiddennodes
        self.outputnodes = outputnodes
        self.learningrate = learningrate
        self.wih = numpy.random.normal(loc=0.0, scale=pow(self.hiddennodes, -0.5),
                                       size=(self.hiddennodes, self.inputnodes))
        self.who = numpy.random.normal(loc=0.0, scale=pow(self.outputnodes, -0.5),
                                       size=(self.outputnodes, self.hiddennodes))
        self.activation_function = lambda x: scipy.special.expit(x)
        self.activation_function_reverse = lambda x: scipy.special.logit(x)

    def train(self, inputs_list, targets_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        self.who += self.learningrate * numpy.dot((output_errors * final_outputs * (1-final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.learningrate * numpy.dot((hidden_errors*hidden_outputs*(1-hidden_outputs)), numpy.transpose(inputs))

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

    def query_reverse(self, targets_list):
        final_outputs = numpy.array(targets_list, ndmin=2).T

        # calculate the signal into the final output layer
        final_inputs = self.activation_function_reverse(final_outputs)

        # calculate the signal out of the hidden layer
        hidden_outputs = numpy.dot(self.who.T, final_inputs)
        # scale them back to 0.01 to .99
        hidden_outputs -= numpy.min(hidden_outputs)
        hidden_outputs /= numpy.max(hidden_outputs)
        hidden_outputs *= 0.98
        hidden_outputs += 0.01

        # calculate the signal into the hidden layer
        hidden_inputs = self.activation_function_reverse(hidden_outputs)

        # calculate the signal out of the input layer
        inputs = numpy.dot(self.wih.T, hidden_inputs)
        # scale them back to 0.01 to .99
        inputs -= numpy.min(inputs)
        inputs /= numpy.max(inputs)
        inputs *= 0.98
        inputs += 0.01

        return inputs


    def save_weights(self, who_file_name, wih_file_name):
        numpy.save(who_file_name, self.who)
        numpy.save(wih_file_name, self.wih)

    def load_weights(self, who_file_name, wih_file_name):
        self.who = numpy.load(who_file_name)
        self.wih = numpy.load(wih_file_name)

    def train_with_mnist(self, dataset_file_name, epoches=1, log_progess=False):
        training_data_file = open(dataset_file_name, "r")
        training_data_list = training_data_file.readlines()
        training_data_file.close()
        if log_progess:
            bar = IncrementalBar('Training with mnist in ' + str(epoches) + ' epoches', max=len(training_data_list) * epoches)
            print("line 2")
            for epoch in range(epoches):
                for record in training_data_list:
                    all_values = record.split(",")
                    inputs = (numpy.asfarray(all_values[1:]) / 255 * 0.99) + 0.01
                    targets = numpy.zeros(self.outputnodes) + 0.01
                    targets[int(all_values[0])] = 0.99
                    self.train(inputs, targets)
                    bar.next()
                print("line 3")
            print("line 4")
            bar.finish()
        else:                                                                       #two almost same whiles for not check log_progress for-each iteration
            for epoch in range(epoches):
                for record in training_data_list:
                    all_values = record.split(",")
                    inputs = (numpy.asfarray(all_values[1:]) / 255 * 0.99) + 0.01
                    targets = numpy.zeros(self.outputnodes) + 0.01
                    targets[int(all_values[0])] = 0.99
                    self.train(inputs, targets)
            self.save_weights("who.txt", "wih.txt")

    def test_with_mnist(self, dataset_file_name):
        test_data_file = open(dataset_file_name, "r")
        test_data_list = test_data_file.readlines()
        test_data_file.close()
        scorecard = []
        for record in test_data_list:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (numpy.asfarray(all_values[1:]) / 255 * 0.99) + 0.01
            outputs = self.query(inputs)
            label = numpy.argmax(outputs)
            if (label == correct_label):
                scorecard.append(1)
            else:
                scorecard.append(0)
        print("эффективность = ", sum(scorecard) / len(scorecard))
        return sum(scorecard) / len(scorecard)
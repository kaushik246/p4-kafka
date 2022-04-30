import os
import json
import matplotlib.pyplot as plt


class ResultSchema:
    def __init__(self, result_dict):
        self.workload = result_dict.get('workload')
        self.message_size = result_dict.get('messageSize')
        self.topics = result_dict.get('topics')
        self.partitions = result_dict.get('partitions')
        self.producersPerTopics = result_dict.get('producersPerTopics')
        self.consumersPerTopic = result_dict.get('consumersPerTopic')
        self.publishRate = result_dict.get('publishRate')
        self.consumeRate = result_dict.get('consumeRate')
        self.backlog = result_dict.get('backlog')
        self.aggregatedPublishLatencyAvg = result_dict.get('aggregatedPublishLatencyAvg')
        self.aggregatedEndToEndLatencyAvg = result_dict.get('aggregatedEndToEndLatencyAvg')

class Result:
    def __init__(self, file_path):
        self.file_path = file_path
        self.parse_data()

    def parse_data(self):
        json_file = open(self.file_path)
        self.result_dict = json.load(json_file)

    def get_metrics(self):
        pass


class Plotter:
    def __init__(self, files=[]):
        self.files = files
        self.results = []

    def fetch_results(self):
        for file in self.files:
            self.results.append(Result(file))

    def plot(self, x_label, y_label, title=''):
        x_vals = []
        y_vals = []
        for result in self.results:
            x_vals.append(result.result_dict.get(x_label))
            y_vals.append(result.result_dict.get(x_label))

        plt.plot(x_vals, y_vals)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if not title:
            title = x_label + ' vs ' + y_label
        plt.title(title)
        plt.show()

if __name__ == "__main__":
    files = ['./sample.json']
    plotter = Plotter(files=files)
    plotter.fetch_results()
    plotter.plot('messageSize', 'aggregatedEndToEndLatencyAvg')
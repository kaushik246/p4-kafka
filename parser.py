import os
import json
import matplotlib.pyplot as plt
import numpy as np
import copy
from collections import defaultdict
import argparse


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
    def __init__(self, dir_path, file_blobs=[]):
        self.file_blobs = file_blobs
        self.results = []
        self.label_mapper = {
            'messageSize': 'messageSize',
            'aggregatedEndToEndLatencyAvg': 'aggregatedEndToEndLatencyAvg'
        }
        self.dir_path = dir_path

    def fetch_results(self):
        for file_blob in self.file_blobs:
            result_blob = []
            for file in file_blob:
                result_blob.append(Result(self.dir_path+file))
            self.results.append(result_blob)

    def generate_title(self, labels):
        return ' vs '.join(labels)


    def stacked_bar_graph(self, x_label, y_label, title=""):
        x_vals = []
        y_vals = [[] for i in range(len(self.file_blobs[0]))]
        bars_count = len(self.file_blobs[0])
        for result in self.results:
            x_vals.append(result[0].result_dict.get(x_label))
            for i in range(bars_count):
                y_vals[i].append(result[i].result_dict.get(y_label))

        x = np.arange(len(x_vals))
        width = 0.1
        plt.figure()
        fig, ax = plt.subplots()
        for i in range(bars_count):
            rect = ax.bar(x + width*i - width*(bars_count-1)/2, y_vals[i], width, label="")
            ax.bar_label(rect, padding=3)

        ax.set_ylabel(self.label_mapper.get(y_label, y_label))
        ax.set_xlabel(self.label_mapper.get(x_label, x_label))
        if not title:
            ax.set_title(self.generate_title([y_label, x_label]))
        ax.set_xticks(x, x_vals)
        ax.legend()

        fig.tight_layout()
        fig.savefig(title+".jpg")

    def box_plotter(self, x_label, metric="aggregatedEndToEndLatency", title=""):

        box_dict_ref = {
            'label': '',
            'whislo': 0,
            'q1': 0,
            'med': 0,
            'q3': 0,
            'whishi': 0,
            'fliers': []
        }
        blob_size = len(self.file_blobs[0])
        if not blob_size == 1:
            raise Exception("Sorry, box plot is not supported")
            return
        boxes = []
        for file_blob in self.results:
            for result in file_blob:

                box_dict = copy.copy(box_dict_ref)
                box_dict['label'] = result.result_dict.get(x_label)
                box_dict['whislo'] = result.result_dict.get(metric+'25pct', 0)
                box_dict['q1'] = result.result_dict.get(metric+'25pct', 0)
                box_dict['med'] = result.result_dict.get(metric+'50pct', 0)
                box_dict['q3'] = result.result_dict.get(metric+'75pct', 0)
                box_dict['whishi'] = result.result_dict.get(metric+'Max', 0)
            boxes.append(box_dict)
        plt.figure()
        fig, ax = plt.subplots()

        ax.bxp(boxes, showfliers=False)

        ax.set_ylabel(self.label_mapper.get(metric, metric))
        ax.set_title(title)
        fig.savefig(title+".jpg")

    def util_percentile(self, pct_data):
        clean_pct_data = defaultdict(float)
        for key in pct_data:
            if ".0" in key:
                num = int(key.split(".")[0])
                if int(num) < 1:
                    continue
                clean_pct_data[num] = pct_data[key]
        return clean_pct_data

    def multi_line_percentile_plotter(self, y_label, title=""):
        blob_size = len(self.file_blobs[0])
        if not blob_size == 1:
            raise Exception("Sorry, box plot is not supported")
            return
        y_vals = [[0.0 for i in range(101)] for j in range(len(self.file_blobs))]
        x_vals  = [i for i in range(101)]
        for i in range(len(self.file_blobs)):
            for result in self.results[i]:
                pct_data = result.result_dict.get(y_label)
                clean_pct_data = self.util_percentile(pct_data)
                for key, val in clean_pct_data.items():
                    y_vals[i][key] = val
        plt.figure()
        for i in range(len(self.file_blobs)):
            plt.plot(x_vals[1:], y_vals[i][1:], label="line "+str(i))
        plt.legend()
        plt.xlabel('Percentile')
        plt.ylabel(y_label)
        plt.savefig(title+".jpg")

    def violin_plot(self, x_label, y_label, title=""):
        pass

    def throughput_plot(self, x_label, y_label, title=""):
        x_vals = []
        y_vals = [[] for i in range(len(self.file_blobs[0]))]
        bars_count = len(self.file_blobs[0])
        for result in self.results:
            x_vals.append(result[0].result_dict.get(x_label))
            for i in range(bars_count):
                import pdb
                pdb.set_trace()
                y_vals[i].append(np.mean(result[i].result_dict.get(y_label))*result[i].result_dict.get('messageSize'))
        x = np.arange(len(x_vals))
        width = 0.1
        plt.figure()
        fig, ax = plt.subplots()
        for i in range(bars_count):
            rect = ax.bar(x + width*i - width*(bars_count-1)/2, y_vals[i], width, label="")
            ax.bar_label(rect, padding=3)

        ax.set_ylabel(self.label_mapper.get(y_label, y_label))
        ax.set_xlabel(self.label_mapper.get(x_label, x_label))
        if not title:
            ax.set_title(self.generate_title([y_label, x_label]))
        ax.set_xticks(x, x_vals)
        ax.legend()

        fig.tight_layout()
        plt.savefig(title+".jpg")


    '''
    def simple_plot(self, x_label, y_label, title=''):
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
    dir_path = "./data/"

    file_blobs_stack_bar = [['sample.json', 'sample_2.json', 'sample.json', 'sample.json', 'sample.json'], ['sample.json', 'sample_2.json', 'sample.json', 'sample.json', 'sample.json']]
    file_blobs_box = [['sample.json'], ['sample_2.json']]
    file_blobs_multi_line = [['sample.json'], ['sample_2.json']]


    bar_graph = Plotter(dir_path, file_blobs=file_blobs_stack_bar)
    bar_graph.fetch_results()
    #bar_graph.stacked_bar_graph('messageSize', 'aggregatedPublishLatencyAvg')


    box_graph = Plotter(dir_path, file_blobs=file_blobs_box)
    box_graph.fetch_results()
    #box_graph.box_plotter('messageSize', 'aggregatedEndToEndLatency')

    multi_line = Plotter(dir_path, file_blobs=file_blobs_multi_line)
    multi_line.fetch_results()
    multi_line.multi_line_percentile_plotter('aggregatedPublishLatencyQuantiles') 
    
    '''
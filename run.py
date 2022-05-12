from parser import Plotter

if __name__ == "__main__":
    dir_path = "./data/"

    file_1 = 'max-rate-20-topics-1-partition-100b-Kafka-2022-05-10-02-56-39.json'
    file_2 = 'max-rate-20-topics-1-partition-1kb-Kafka-2022-05-10-03-14-58.json'
    file_3 = 'max-rate-20-topics-1-partition-1kb-Kafka-2022-05-10-03-43-12.json'

    file_blobs_stack_bar = [[file_1, file_2, file_3]]
    file_blobs_box = [[file1], [file2]]
    file_blobs_multi_line = [[file1], [file2]]


    bar_graph = Plotter(dir_path, file_blobs=file_blobs_stack_bar)
    bar_graph.fetch_results()
    #bar_graph.stacked_bar_graph('messageSize', 'aggregatedPublishLatencyAvg', '1')


    box_graph = Plotter(dir_path, file_blobs=file_blobs_box)
    box_graph.fetch_results()
    #box_graph.box_plotter('messageSize', 'aggregatedEndToEndLatency', '1')

    multi_line = Plotter(dir_path, file_blobs=file_blobs_multi_line)
    multi_line.fetch_results()
    multi_line.multi_line_percentile_plotter('aggregatedPublishLatencyQuantiles', '1')
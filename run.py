from parser import Plotter

if __name__ == "__main__":
    dir_path = "./data/"

    file_1 = 'max-rate-40-topics-1-partition-100b-Kafka-2022-05-11-22-31-23.json'
    file_2 = 'max-rate-40-topics-1-partition-1kb-Kafka-2022-05-11-22-42-42.json'
    file_3 = 'max-rate-20-topics-1-partition-1kb-Kafka-2022-05-10-03-43-12.json'

    file_blobs_stack_bar = [[file_1, file_2]]
    file_blobs_box = [[file_1], [file_2], [file_2]]
    file_blobs_multi_line = [[file_1], [file_2]]


    bar_graph = Plotter(dir_path, file_blobs=file_blobs_stack_bar)
    bar_graph.fetch_results()
    #bar_graph.stacked_bar_graph('messageSize', 'aggregatedPublishLatencyAvg', '1')


    box_graph = Plotter(dir_path, file_blobs=file_blobs_box)
    box_graph.fetch_results()
    #box_graph.box_plotter('messageSize', 'aggregatedEndToEndLatency', '2')

    multi_line = Plotter(dir_path, file_blobs=file_blobs_multi_line)
    multi_line.fetch_results()
    #multi_line.multi_line_percentile_plotter('aggregatedPublishLatencyQuantiles', '3')

    tp = Plotter(dir_path, file_blobs=file_blobs_box)
    tp.fetch_results()
    tp.throughput_plot('messageSize', 'publishRate', 'Throughput Plot')

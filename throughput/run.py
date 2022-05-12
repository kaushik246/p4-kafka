from parser import Plotter

if __name__ == "__main__":
    dir_path = "./data/"

    file_1 = '1p-1c-1k-10k-Kafka-2022-05-12-03-09-55.json'
    file_2 = '1p-1c-1k-20k-Kafka-2022-05-12-03-16-48.json'  
    file_3 = '1p-1c-1k-40k-Kafka-2022-05-12-03-25-59.json' 
    file_4 ='1p-1c-1k-60k-Kafka-2022-05-12-09-20-05.json'
    file_5 = '1p-1c-1k-80k-Kafka-2022-05-12-09-26-25.json'
    file_6 = '1p-1c-1k-100k-Kafka-2022-05-12-10-05-22.json'  

    file_blobs_stack_bar = [[file_1], [file_2], [file_3], [file_4], [file_5], [file_6]]
    file_blobs_box = [[file_1], [file_2], [file_2]]
    file_blobs_multi_line = [[file_1], [file_2]]


    bar_graph = Plotter(dir_path, file_blobs=file_blobs_stack_bar)
    bar_graph.fetch_results()
    bar_graph.stacked_bar_graph('givenPublishRate', 'aggregatedPublishLatencyAvg', 'aggregatedPublishLatencyAvg vs publishRate')
    bar_graph.stacked_bar_graph('givenPublishRate', 'aggregatedEndToEndLatencyAvg', 'aggregatedEndToEndLatencyAvg vs publishRate')


    box_graph = Plotter(dir_path, file_blobs=file_blobs_box)
    box_graph.fetch_results()
    box_graph.box_plotter('messageSize', 'aggregatedEndToEndLatency', '2')

    multi_line = Plotter(dir_path, file_blobs=file_blobs_multi_line)
    multi_line.fetch_results()
    #multi_line.multi_line_percentile_plotter('aggregatedPublishLatencyQuantiles', '3')

    tp = Plotter(dir_path, file_blobs=file_blobs_box)
    tp.fetch_results()
    #tp.throughput_plot('messageSize', 'publishRate', 'Throughput Plot')

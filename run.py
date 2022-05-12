from parser import Plotter

if __name__ == "__main__":
    dir_path = "./"

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
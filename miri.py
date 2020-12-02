import pm4py
from pm4py.objects.log.importer.xes import factory as xes_importer
# Import event log
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery


log_csv = pd.read_csv('./log.csv', sep=',')
log_csv.rename(columns={'Activity': 'concept:name'}, inplace=True)
log_csv.rename(columns={'Patient': 'case:concept:name'}, inplace=True)
log_csv.rename(columns={'Timestamp': 'time:timestamp'}, inplace=True)
log_csv.rename(columns={'Resource': 'org:resource'}, inplace=True)
log_csv.rename(columns={'Insurance': 'case:Insurance'}, inplace=True)
log_csv.rename(columns={'PatientName': 'case:PatientName'}, inplace=True)

log = log_converter.apply(log_csv)
print(len(log))
print(log)
# number of variants
from pm4py.statistics.traces.log import case_statistics
variants_count = case_statistics.get_variant_statistics(log)
print(variants_count)
print(len(log))
dfg = dfg_discovery.apply(log)


gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
dfg_visualization.view(gviz)

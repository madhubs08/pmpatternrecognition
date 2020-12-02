import unittest

import pm4py
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.importer.csv import factory as csv_importer

import prod.discover
import prod.transformation as trans
from prod.abstraction_support_functions import *
from utils import *


class Test_Methods(unittest.TestCase):

	event_log = ".\\testCases\\demo.xes"
	pattern_path = ".\\testCases\\userPattern.json"
	pattern_number = ['1','2','3']
	export_log = False
	export_model = False
	abstracted_traces = None
	abstracted_timestamps = None
	user_patterns = [{"ID": 1,"Name": "Group1","Pattern": ["deliver the package","shut the case"]},
	{"ID": 2,"Name": "Group2","Pattern": ["deliver the package","shut the case"]},
	{"ID": 4,"Name": "G5","Pattern": ["deliver the package"]}]


	def test_import_pattern_json(self):
		
		self.user_patterns = utils.import_pattern_json(self.pattern_path)
		self.assertIsNotNone(self.user_patterns)

		self.assertFalse(utils.import_pattern_json("./testCases/userPattern.txt"),"There exists no such file")

    
	def test_perform_abstraction(self):
		log = utils.import_log_XES(self.event_log)
		pattern_dic = read_pattern_file(self.pattern_path)
		self.assertIsNotNone(pattern_dic)

		# Extract all ids from user patterns
		ids_user_patterns = [x['ID'] for x in self.user_patterns]
		self.assertIsNotNone(ids_user_patterns)

		# read the activities and timestamps from the given log
		concatenated_traces, concatenated_timestamps = read_log(log)
		self.assertIsNotNone(concatenated_traces)
		self.assertIsNotNone(concatenated_timestamps)
		self.assertEqual(len(concatenated_traces), len(concatenated_timestamps), "Both concrete lists must be equal in length")

		# perform abstraction on user patterns
		abstracted_traces, abstracted_timestamps = \
			perform_abstractions(
							ids_user_patterns, self.user_patterns,
							concatenated_traces,
							concatenated_timestamps
							)
		self.assertIsNotNone(abstracted_traces)
		self.assertIsNotNone(abstracted_timestamps)
		self.assertEqual(len(abstracted_traces), len(abstracted_timestamps), "Both abstracted lists must be equal in length")

		self.abstracted_traces = abstracted_traces
		self.abstracted_timestamps = abstracted_timestamps

	def test_generate_transformed_log(self):
		
		self.test_perform_abstraction()
		# get transformed log
		log_content = trans.generate_transformed_log_XES(
											self.event_log,
											self.abstracted_traces,
											self.abstracted_timestamps,
											self.event_log[:-4] + "_transformed_unit_test.XES"
											)
		self.assertIsNotNone(log_content)

	def test_pattern_numbers(self):
		
		#Test Pattern numbers
		self.assertTrue(self.pattern_number)
		self.assertNotEquals(self.pattern_number, '1,2,3')
		
	def test_is_valid_user_input(self):

		self.assertTrue(utils.is_valid_user_input([]))
		self.assertTrue(utils.is_valid_user_input([{'ID':1,'Name':'Group1','Pattern':['a','b','c']}]))
		self.assertTrue(utils.is_valid_user_input([{'ID':1,'Name':'Group1','Pattern':['a','b','c']},
		{'ID':2,'Name':'Group2','Pattern':['a','b','c']}]))

		self.assertFalse(utils.is_valid_user_input({}))
		self.assertFalse(utils.is_valid_user_input([[]]))
		self.assertFalse(utils.is_valid_user_input([{'ID':1,'Pattern':['a','b','c']}]))
		self.assertFalse(utils.is_valid_user_input([{'ID':1,'Name':'Group1'}]))
		self.assertFalse(utils.is_valid_user_input([{'Name':'Group1','Pattern':['a','b','c']}]))
		self.assertFalse(utils.is_valid_user_input([{'ID':'string','Name':'Group1','Pattern':['a','b','c']}]))
		self.assertFalse(utils.is_valid_user_input([{'ID':'string','Name':'Group1','Pattern':[1,2,2]}]))
		self.assertFalse(utils.is_valid_user_input([{'ID':1,'Name':5,'Pattern':'abc'}]))
		self.assertFalse(utils.is_valid_user_input([{'ID':1,'Name':'Group1','Pattern':['a','b','c']},
		{'ID':1,'Name':'Group2','Pattern':['a','b','c']}]))
		self.assertFalse(utils.is_valid_user_input([{'ID':1,'Name':'Group1','Pattern':['a','b','c']},
		{'ID':2,'Name':'Group1','Pattern':['a','b','c']}]))

	def test_csv_run_with_unvalid_file(self) : 
		self.assertIsNone(import_csv('./testCases/outPut.csv'))

	def test_csv_run(self): 
		self.assertIsInstance(import_csv('./testCases/outputFile.csv'), pm4py.objects.log.log.EventLog)

	def test_add_classifier(self):
		event_stream = csv_importer.import_event_stream('./testCases/outputFile.csv')
		log = conversion_factory.apply(event_stream)
		self.assertIsInstance((add_classifier(log)), pm4py.objects.log.log.EventLog)

if __name__ == '__main__':
    unittest.main()
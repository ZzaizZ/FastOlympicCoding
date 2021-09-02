import urllib
import urllib.request
import re
import codecs
from .base_handler import BaseHandler
from os import path
import sublime

from ..settings import get_tests_file_path

'''
	Handler for CodeForces contest

	Implements required interface to use in the ContestHandlerCommand
'''
class CodeForces(BaseHandler):

	def __init__(self, url, base_path):
		self.valid = self.__is_valid_url(url)
		self.url = url
		self.contest_id = self.__extract_contest_id(self.url)
		self.contest_name = self.__load_contest_name(self.contest_id)
		super().__init__(base_path, self.get_basename(), self.get_contest_name())
		self.base_path = self.get_full_contest_path()
		self.tests = []


	# BASE CLASS INTERFACE
	def init_contest(self):
		self.__init_problems(self.contest_id, self.base_path)

	def get_basename(self):
		return "CodeForces"

	def get_contest_name(self):
		return self.contest_name



	# PRIVATE METHODS

	def __is_valid_url(self, url):
		return url.find('codeforces.com') != -1

	def __extract_contest_id(self, url):
		match = re.search(r'\d+', url)
		return match.group(0)

	def __load_contest_name(self, contest_id):
		contest_name_start = '<div style="padding: 4px 0 0 6px;font-size:1.4rem;position:relative;">'
		contest_name_end = '<div style="position:absolute;right:0.25em;top:0.35em;">'
		url = 'https://codeforces.com/contests/' + str(contest_id)
		req = urllib.request.urlopen(url)
		text = req.read().decode()
		title = text[text.find(contest_name_start) + len(contest_name_start):text.find(contest_name_end)].strip()
		return title

	def __init_problems(self, contest_id, base, pid='A'):
		inputs, outputs = self.__try_load_tests(contest_id, pid)
		if inputs:
			file_name = path.join(base, pid + '.cpp')
			if not path.exists(file_name):
				open(file_name, 'w').close()
			tests = [] 
			for i in range(len(inputs)):
				tests.append({
					'test': inputs[i],
					'correct_answers': [outputs[i]]
				})

			with open(get_tests_file_path(file_name), 'w') as f:
				f.write(sublime.encode_value(tests, True))

			def go(self=self, contest_id=contest_id, base=base, pid=self.__next_problem(pid)):
				self.__init_problems(contest_id, base, pid=pid)

			sublime.set_timeout_async(go)
		else:
			if len(pid) == 1:
				self.__init_problems(contest_id, base, pid + '1')
			elif pid[1] == '1':
				sublime.status_message('tests loaded')
				return
			else:
				self.__init_problems(contest_id, base, chr(ord(pid[0]) + 1))

	def __try_load_tests(self, contest_id, task_id):
		test_tokens = ['<div class="input">', '<div class="title">Input</div>', '<pre>',
		'</pre>', '</div>', '<div class="output">', '<div class="title">Output</div>',
		'<pre>', '</pre>', '</div>'
		]
		url = 'https://codeforces.com/contest/{contest_id}/problem/{task_id}'.format(
			contest_id=contest_id,
			task_id=task_id
		)
		req = urllib.request.urlopen(url)
		text = req.read().decode()
		inputs = []
		outputs = []
		state = 0
		i = 0
		while i < len(text):
			if text[i:i + len(test_tokens[state])] == test_tokens[state]:
				i += len(test_tokens[state])
				state = (state + 1) % len(test_tokens)
				if state == 3:
					inputs.append('')
				if state == 8:
					outputs.append('')
			else:
				if state == 3:
					inputs[-1] += text[i]
				if state == 8:
					outputs[-1] += text[i]
				i += 1
		for i in range(len(inputs)):
			inputs[i] = inputs[i].replace('<br />', '\n').strip()
		for i in range(len(outputs)):
			outputs[i] = outputs[i].replace('<br />', '\n').strip()
		if (len(inputs) != len(outputs)) or (not inputs): return None, None
		return inputs, outputs

	def __next_problem(self, pid):
		if len(pid) == 1: return chr(ord(pid[0]) + 1)
		return pid[0] + chr(ord(pid[1]) + 1)

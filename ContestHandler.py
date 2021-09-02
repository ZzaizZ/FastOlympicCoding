import sublime, sublime_plugin
import os
from os import path
from .ContestHandlers import codeforces
try:
	from .ContestHandlers.codeforces_submit import perform_submission
except ImportError:
	pass
from .test_manager import TestManagerCommand
from sublime import Region
from .settings import get_tests_file_path

class ContestHandlerCommand(sublime_plugin.TextCommand):

	def run(self, edit, action=None):
		if action == 'setup_contest':
			def on_done(url, self=self):
				cf = codeforces.CodeForces(url, 'contest_base')
				cf.init_contest()

			def on_change(url):
				pass

			def on_cancel():
				pass

			self.view.window().show_input_panel(
				'URL',
				'https://codeforces.com/contest/1056/problem/C',
				on_done,
				on_change,
				on_cancel
			)
		elif action == 'submit':
			for folder in self.view.window().folders():
				file = path.join(folder, '_contest.sublime-settings')
				if path.exists(file):
					settings = sublime.decode_value(open(file).read())
					break
			else:
				print('_contest.sublime-settings is not found')
				return
			code = self.view.substr(Region(0, int(1e9)))
			last = path.basename(self.view.file_name())
			problemID = path.splitext(last)[0]
			print('args', settings, problemID)
			def reduce(settings=settings, problemID=problemID, code=code):
				perform_submission(settings['contestID'], problemID, code, {
						'username': settings['cf_username'], 'password': settings['cf_password']
					}
				)
			sublime.set_timeout_async(reduce, 10)

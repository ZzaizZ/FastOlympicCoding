from abc import ABCMeta, abstractmethod
import sublime, sublime_plugin
import os
from os import path

'''
	Base class for contest handlers
	Provides the interface, that is used for setting up the contest
'''
class BaseHandler(metaclass=ABCMeta):

	def __init__(self, folc_path, handler_basename, handler_contest_name):
		self.contest_path = self.__create_path(path.expanduser('~'), [folc_path, handler_basename, handler_contest_name])
		self.__init_contest_project(self.contest_path)

	@abstractmethod
	def init_contest(self):
		pass

	@abstractmethod
	def get_basename(self) -> str:
		return "contest_BaseName"

	@abstractmethod
	def get_contest_name(self) -> str:
		return "contest_name"

	def get_full_contest_path(self):
		return self.contest_path


	def __init_contest_project(self, contest_path):
		sublime.run_command('new_window')
		pSettings = {
			'folders': [
					{
						'path': contest_path
					}
				]
			}
		sublime.active_window().set_project_data(pSettings)
		pSettingsFile = path.join(contest_path, '_contest.sublime-project')
		if not path.exists(pSettingsFile):
			with open(pSettingsFile, 'w') as f:
				f.write(sublime.encode_value(pSettings, True))
		
		fsettings = path.join(contest_path, '_contest.sublime-settings')
		if not path.exists(fsettings):
			open(fsettings, 'w').close()

	def __create_path(self, base, _path):
		for i in range(len(_path)):
			cur = path.join(base, path.join(*_path[:i + 1]))
			if not path.exists(cur):
				os.mkdir(cur)
		return path.join(base, path.join(*_path))
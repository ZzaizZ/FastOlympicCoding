from .base_handler import BaseHandler
from os import path
import sublime

class DefaultHandler(BaseHandler):
	def __init__(self, base_path, contest_name):
		self.contest_name = contest_name
		super().__init__(base_path, self.get_basename(), self.get_contest_name())

	def init_contest(self):
		pass

	def get_basename(self):
		return "DefaultContests"

	def get_contest_name(self):
		return self.contest_name

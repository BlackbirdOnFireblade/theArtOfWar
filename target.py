import numpy as np
import math

class Section(object):
	def __init__(self, begin, end, cost):
		self.begin = min(begin, end)
		self.end = max(begin, end)
		self.center = (begin + end) / 2.0
		self.cost = math.ceil(cost)
		self.quiver = None
		self.text = None

	def update(self, begin, end, cost):
		self.begin = min(begin, end)
		self.end = max(begin, end)
		self.center = (begin + end) / 2.0
		self.cost = math.ceil(cost)

	def __repr__(self):
		return "Section({}-{}=>{})".format(self.begin, self.end, self.cost)

class Target(object):
	def __init__(self, target_name, target_unitsize, timerate, is_offence = True, is_own = False):
		self.target_name = target_name
		self.target_unitsize = float(target_unitsize)
		self.timerate = timerate
		self.is_offence = is_offence
		self.is_own = is_own
		self.active = np.array([])

	def _calc_time(self, unused):
		return unused * self.timerate / 60.0 / self.target_unitsize

	def _calc_cost(self, begin, end):
		return abs(end- begin) * 60.0 * self.target_unitsize / self.timerate

	def _first(self):
		if len(self.active) == 0:
			return 0
		else:
			return np.min([a.begin for a in self.active])

	def _add(self, begin, end):
		section = Section(begin, end, self._calc_cost(begin, end))
		self.active = np.append(self.active, section)
		print("add : {}".format(self.active))
		return section

	def add(self, begin):
		following = [a.begin for a in self.active if begin <= a.begin]
		if len(following) == 0:
			return self._add(begin, 0.0)
		else:
			first = np.min(following)
			if first != begin:
				return self._add(begin, first)
			else:
				return None

	def stop(self, end):
		target_section = [a for a in self.active if a.begin < end and end < a.end]
		if len(target_section) > 0:
			target_section[0].update(target_section[0].begin, end, self._calc_cost(target_section[0].begin, end))
			print("update : {}".format(self.active))
			return target_section[0]
		else:
			return None

	def _remove(self, section):
		keep_section = np.array([])
		for a in self.active:
			if a != section:
				keep_section = np.append(keep_section, a)
		self.active = keep_section
		print("remove : {}".format(self.active))

	def remove(self, time):
		target_section = [a for a in self.active if a.begin < time and time <= a.end]
		if len(target_section) > 0:
			keep_section = np.array([])
			for a in self.active:
				if not(a.begin < time and time <= a.end):
					keep_section = np.append(keep_section, a)
			self.active = keep_section
			print("remove : {}".format(self.active))
			return target_section[0]
		else:
			return None

	def marge(self, time):
		target_section = [a for a in self.active if a.begin <= time and time <= a.end]
		if len(target_section) > 0:
			continual_section = np.array([])
			begin = target_section[0].begin
			end = target_section[0].end
			for a in self.active:
				if a != target_section[0] and (a.end == target_section[0].begin or target_section[0].end == a.begin):
					continual_section = np.append(continual_section, a)
					begin = min(begin, a.begin)
					end = max(end, a.end)
			target_section[0].update(begin, end, self._calc_cost(begin, end))
			if len(continual_section) > 0:
				for a in continual_section:
					self._remove(a)

			print("marge : {}".format(self.active))
			return target_section[0], continual_section
		else:
			return None

	def __repr__(self):
		return "Target({},{},{})".format(self.target_name, self.target_unitsize, self.is_offence)


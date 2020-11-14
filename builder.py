import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import plotutil as prj
from target import Target

BEGINNING = -45.0
ENDING = 0.0
INTERVAL = 15.0

class Builder(object):

	def __init__(self, args, offence_targets, defence_targets):
		self.args = args
		self.offence_targets = offence_targets
		self.defence_targets = defence_targets
		self.target_interval = [Target(o.target_name, o.target_unitsize, o.timerate, o.is_offence, not(o.is_own)) for o in self.offence_targets]

		self._setup()

	def _setup(self):
		self.fig = plt.figure(figsize=(24, 8))

		self.offence = self.fig.add_subplot(2, 2, 1)
		self.defence = self.fig.add_subplot(2, 2, 3)
		self.resource = self.fig.add_subplot(1, 2, 2)

		def setup_offence():
			prj.coordinate_p(self.offence, [BEGINNING - 0.2, ENDING + 0.2], [-0.4, len(self.offence_targets) - 0.6], ytitle=[s.target_name for s in self.offence_targets], ylabel="Offence", xlabel = "time left")
			self.ln_v_o = self.offence.axvline(0)
			self.ln_h_o = self.offence.axhline(-1)
			self.tx_o = self.offence.text(0 + 0.01, -1 + 0.03, "", color="blue", size=8)

		def setup_defence():
			prj.coordinate_p(self.defence, [BEGINNING - 0.2, ENDING + 0.2], [-0.4, len(self.defence_targets) - 0.6], ytitle=[s.target_name for s in self.defence_targets], ylabel="Defence", xlabel = "time left")
			self.ln_v_d = self.defence.axvline(0)
			self.ln_h_d = self.defence.axhline(-1)
			self.tx_d = self.defence.text(0 + 0.01, -1 + 0.03, "", color="blue", size=8)

		def setup_resource():
			prj.coordinate(self.resource, [BEGINNING - 0.2, ENDING + 0.2], [-self.args.resource * 0.1, self.args.resource * 1.1], ylabel="resource", xlabel = "time left")
			y_major_ticks = np.arange(round(0.0), round(self.args.resource + 500), 500)
			y_minor_ticks = np.arange(round(0.0), round(self.args.resource + 500), 100)
			self.resource.set_yticks(y_major_ticks)
			self.resource.set_yticks(y_minor_ticks, minor=True)
			x_major_ticks = np.arange(round(BEGINNING), round(ENDING), 5)
			x_minor_ticks = np.arange(round(BEGINNING), round(ENDING), 1)
			self.resource.set_xticks(x_major_ticks)
			self.resource.set_xticks(x_minor_ticks, minor=True)
			self.ln_v_r = self.resource.axvline(0)
			self.ln_h_r = self.resource.axhline(self.max_resource)
			self.tx_r = self.resource.text(0 + 0.01, -1 + 0.03, "", color="blue", size=8)
			self.tx_btw = self.resource.text(0 - 0.01, -1 - 0.03, "", ha='right', va='top', color="red", size=10)

		def extend_resource(max_val):
			self.resource.set_ylim(-self.args.resource * 0.1, max_val + self.args.resource * 0.1)
			y_major_ticks = np.arange(round(0.0), round(max_val + 500), 500)
			y_minor_ticks = np.arange(round(0.0), round(max_val + 500), 100)
			self.resource.set_yticks(y_major_ticks)
			self.resource.set_yticks(y_minor_ticks, minor=True)

		self.max_resource = self.args.resource

		setup_offence()
		setup_defence()
		setup_resource()

		def get_position(event):
			return round(event.xdata * self.args.resolution) / self.args.resolution, round(event.ydata)

		self.resource_used = np.zeros(int(abs(BEGINNING - ENDING) * self.args.resolution) + 1)

		self.recommend = np.array([])
		def view_left(left):
			for x in self.recommend:
				x.remove()
			self.recommend = np.array([])
			if left > 0:
				for i in range(len(self.offence_targets)):
					enable = self.offence_targets[i]._first() - math.floor(self.offence_targets[i]._calc_time(left) * self.args.resolution) / self.args.resolution
					x = self.offence.scatter(enable, i, marker="*", color="red", alpha=0.5)
					self.recommend = np.append(self.recommend, x)
				for i in range(len(self.defence_targets)):
					enable = self.defence_targets[i]._first() - math.floor(self.defence_targets[i]._calc_time(left) * self.args.resolution) / self.args.resolution
					x = self.defence.scatter(enable, i, marker="*", color="red", alpha=0.5)
					self.recommend = np.append(self.recommend, x)

		def calc_resource():
			resource_time = [BEGINNING + t / self.args.resolution for t in range(int(abs(BEGINNING - ENDING) * self.args.resolution) + 1)]
			resource_used = np.empty(0)
			sum_cost = 0.0
			for time in resource_time:
				offence_resource = [(o.target_name, o.target_unitsize, o.timerate, a.begin, a.end, a.cost) for o in self.offence_targets for a in o.active if a.begin < time and time <= a.end]
				defence_resource = [(o.target_name, o.target_unitsize, o.timerate, a.begin, a.end, a.cost) for o in self.defence_targets for a in o.active if a.begin < time and time <= a.end]

				delta_cost = 0.0
				delta_cost += sum(o[5] / (o[4] - o[3]) / self.args.resolution for o in offence_resource)
				delta_cost += sum(o[5] / (o[4] - o[3]) / self.args.resolution for o in defence_resource)

				sum_cost += delta_cost
				resource_used = np.append(resource_used, sum_cost)

			self.resource.cla()
			setup_resource()
			usage = max(resource_used)
			max_cost = max(usage, self.max_resource)
			if max_cost > self.args.resource:
				extend_resource(max_cost)

			upper_limit = np.full(len(resource_used), self.max_resource)
			over_limit = np.maximum(resource_used, upper_limit)
			self.resource.fill_between(list(resource_time), over_limit, y2 = upper_limit, color="red", alpha=0.25)
			self.resource.plot(list(resource_time), resource_used, color="red")
			self.resource_used = resource_used

			resource_left = self.max_resource - usage
			self.tx_btw.set_position((0 - 0.01, (self.max_resource + usage) / 2 - 0.03))
			self.tx_btw.set_text("{}".format(round(resource_left)))
			view_left(resource_left)

		calc_resource()

		self.ln_x = 0.0
		self.ln_y_o = -1.0
		self.ln_y_d = -1.0

		def motion(event):
			self.ln_y_o = -1.0
			self.ln_y_d = -1.0
			if event.inaxes == self.offence:
				x, y = get_position(event)
				self.ln_x = x
				self.ln_y_o = y
			if event.inaxes == self.defence:
				x, y = get_position(event)
				self.ln_x = x
				self.ln_y_d = y
			if event.inaxes == self.resource:
				x, y = get_position(event)
				self.ln_x = x

			self.ln_h_o.set_ydata(self.ln_y_o)
			self.ln_h_d.set_ydata(self.ln_y_d)
			self.ln_v_o.set_xdata(self.ln_x)
			self.ln_v_d.set_xdata(self.ln_x)
			self.ln_v_r.set_xdata(self.ln_x)

			if self.ln_y_o >= 0.0:
				self.tx_o.set_position((self.ln_x + 0.01, self.ln_y_o + 0.03))
				self.tx_o.set_text("[{} min]".format(round(abs(self.ln_x), 1)))
			else:
				self.tx_o.set_text("")

			if self.ln_y_d >= 0.0:
				self.tx_d.set_position((self.ln_x + 0.01, self.ln_y_d + 0.03))
				self.tx_d.set_text("[{} min]".format(round(abs(self.ln_x), 1)))
			else:
				self.tx_d.set_text("")

			self.tx_r.set_position((self.ln_x + 0.01, self.resource_used[int((self.ln_x - BEGINNING) * self.args.resolution)] + 0.03))
			self.tx_r.set_text("{} [{} min]".format(round(self.resource_used[int((self.ln_x - BEGINNING) * self.args.resolution)]), round(abs(self.ln_x), 1)))
			plt.draw()

		self._axies = [self.offence, self.defence]
		self._targets = [self.offence_targets, self.defence_targets]

		def view_interval():
			axisindex = 0
			for index in range(len(self.target_interval)):
				end = self.offence_targets[index]._first()
				begin = end - INTERVAL
				if len(self.target_interval[index].active) > 0:
					for s in self.target_interval[index].active:
						q = s.quiver
						t = s.text
						q.remove()
						t.remove()
					self.target_interval[index].active = np.array([])
				section = self.target_interval[index]._add(begin, end)
				if not section is None:
					q = prj._visual_vector(self._axies[axisindex], np.array((section.end, float(index))), np.array((section.begin, float(index))), color="gray", alpha=0.25)
					t = self._axies[axisindex].text(section.center + 0.01, index - 0.13, section.cost, color="gray", alpha=0.5, size=8)
					section.quiver = q
					section.text = t
				section = self.target_interval[index]._add(begin, 0.0)
				if not section is None:
					q = prj._visual_vector(self._axies[axisindex], np.array((section.end, float(index) - 0.15)), np.array((section.begin, float(index) - 0.15)), color="gray", alpha=0.15)
					t = self._axies[axisindex].text(section.center + 0.01, index - 0.15 - 0.13, section.cost, color="gray", alpha=0.3, size=8)
					section.quiver = q
					section.text = t

		def click_axis(event, axisindex):
			pos = get_position(event)
			index = pos[1]
			timing = pos[0]
			if event.button == 1:
				section = self._targets[axisindex][int(index)].stop(timing)
				if not section is None:
					q = section.quiver
					t = section.text
					q.set_UVC(section.end - section.begin ,0)
					t.set_text(section.cost)
					t.set_position((section.center + 0.01, index + 0.03))
				else:
					section = self._targets[axisindex][int(index)].add(timing)
					if not section is None:
						q = prj._visual_vector(self._axies[axisindex], np.array((section.begin, float(index))), np.array((section.end, float(index))))
						t = self._axies[axisindex].text(section.center + 0.01, index + 0.03, section.cost, color="blue", size=8)
						section.quiver = q
						section.text = t
				view_interval()
				calc_resource()
				plt.draw()

			elif event.button == 3:
				section = self._targets[axisindex][int(index)].remove(timing)
				if not section is None:
					q = section.quiver
					t = section.text
					q.remove()
					t.remove()
				view_interval()
				calc_resource()
				plt.draw()

		def onclick(event):
			if event.inaxes == self.offence:
				click_axis(event, 0)
			elif event.inaxes == self.defence:
				click_axis(event, 1)
			elif event.inaxes == self.resource:
				x, y = get_position(event)
				self.max_resource = round(float(y) / self.args.resource_step) * self.args.resource_step
				if self.max_resource > self.args.resource:
					extend_resource(self.max_resource)
				self.ln_h_r.set_ydata(self.max_resource)
				calc_resource()
				motion(event)
				plt.draw()

		def keypress_axis(event, axisindex):
			pos = get_position(event)
			index = pos[1]
			timing = pos[0]
			print(index, timing)
			if event.key == 'm':
				section, remove = self._targets[axisindex][int(index)].marge(timing)
				if not section is None:
					q = section.quiver
					t = section.text
					q.remove()
					t.remove()
					q = prj._visual_vector(self._axies[axisindex], np.array((section.begin, float(index))), np.array((section.end, float(index))))
					t = self._axies[axisindex].text(section.center + 0.01, index + 0.03, section.cost, color="blue", size=8)
					section.quiver = q
					section.text = t
				if not remove is None and len(remove) > 0:
					for a in remove:
						q = a.quiver
						t = a.text
						q.remove()
						t.remove()
				view_interval()
				calc_resource()
				plt.draw()

		def onkey(event):
			if event.key == 'q':
				plt.close(event.canvas.figure)
				return
			if event.inaxes == self.offence:
				keypress_axis(event, 0)
			elif event.inaxes == self.defence:
				keypress_axis(event, 1)

		motion_handler = self.fig.canvas.mpl_connect('motion_notify_event', motion)
		mouse_handler = self.fig.canvas.mpl_connect('button_press_event', onclick)
		keybord_handler = self.fig.canvas.mpl_connect('key_press_event', onkey)

	def show(self):
		plt.show()




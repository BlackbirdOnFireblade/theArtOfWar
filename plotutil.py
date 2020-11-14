# ---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 2D座標設定関数
def coordinate(axes, range_x, range_y, grid = True,
			   xyline = True, xlabel = "x", ylabel = "y"):
	axes.set_xlabel(xlabel, fontsize = 10)
	axes.set_ylabel(ylabel, fontsize = 10)
	axes.set_xlim(range_x[0], range_x[1])
	axes.set_ylim(range_y[0], range_y[1])
	if grid == True:
		axes.grid()
	if xyline == True:
		axes.axhline(0, color = "gray", alpha=0.4)
		axes.axvline(0, color = "gray", alpha=0.4)

def coordinate_p(axes, range_x, range_y, ytitle, grid = True,
			   xyline = True, xlabel = "x", ylabel = "y"):
	axes.set_xlabel(xlabel, fontsize = 10)
	axes.set_ylabel(ylabel, fontsize = 10)
	axes.set_xlim(range_x[0], range_x[1])
	axes.set_ylim(range_y[0], range_y[1])
	if grid == True:
		axes.grid()
	if xyline == True:
		axes.axhline(0, color = "gray", alpha=0.3)
		axes.axvline(0, color = "gray", alpha=0.3)

	major_ticks = np.arange(round(range_x[0]), round(range_x[1]), 5)
	minor_ticks = np.arange(round(range_x[0]), round(range_x[1]), 1)
	axes.set_xticks(major_ticks)
	axes.set_xticks(minor_ticks, minor=True)

	axes.set_yticks(range(len(ytitle)))
	axes.set_yticklabels([s for s in ytitle])

# 3D座標設定関数
def coordinate_3d(axes, range_x, range_y, range_z, grid = True):
	axes.set_xlabel("x", fontsize = 16)
	axes.set_ylabel("y", fontsize = 16)
	axes.set_zlabel("z", fontsize = 16)
	axes.set_xlim(range_x[0], range_x[1])
	axes.set_ylim(range_y[0], range_y[1])
	axes.set_zlim(range_z[0], range_z[1])
	if grid == True:
		axes.grid()
# ---------------------------------
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 2Dベクトル描画関数
def _visual_vector(axes, b, e, color = "red", alpha=0.7):
	v = e - b
	return visual_vector(axes, b, v, color, alpha)

def visual_vector(axes, loc, vector, color = "red", alpha=0.7):
	return axes.quiver(loc[0], loc[1],
			  vector[0], vector[1], color = color,
			  angles = 'xy', scale_units = 'xy', scale = 1, alpha=alpha)

# 3Dベクトル描画関数
def visual_vector_3d(axes, loc, vector, color = "red"):
	return axes.quiver(loc[0], loc[1], loc[2],
			  vector[0], vector[1], vector[2],
			  color = color, length = 1,
			  arrow_length_ratio = 0.2)
# ---------------------------------
import matplotlib.pyplot as plt
import matplotlib.patches as pltp

def visual_arc(axes, center, r, theta1, theta2, color = "red", alpha=0.7):
	arc = pltp.Arc(center, width= r*2, height=r*2, angle=0.0, theta1=theta1, theta2=theta2, color=color, alpha=alpha)
	axes.add_patch(arc)

# ---------------------------------
# ベクトル回転関数
# deg=Falseならばラジアンで角度を指定
# deg=Trueならば度数単位で角度を指定
def rotation_o(u, t, deg=False):

	# 度数単位の角度をラジアンに変換
	if deg == True:
		t = np.deg2rad(t)

	# 回転行列
	R = np.array([[np.cos(t), -np.sin(t)],
				  [np.sin(t),  np.cos(t)]])

	return  np.dot(R, u)

def translate_o(u, m):
	return u + m

def flip_y_o(u):
	return np.array((-u[0], u[1]))
# ---------------------------------

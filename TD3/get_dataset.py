#!/usr/bin/env python

from move_base_msgs.msg import MoveBaseActionGoal
from nav_msgs.msg import Odometry, OccupancyGrid
import rospy
import time
import numpy as np

class GetDatas:
	def __init__(self):
		self.create_msg_srv()
		self.total_path = 0
		self.total_maps = 0
		self.final_permap = 0
		self.tmp_map = np.zeros((384, 384))
		self.path_array = []


	def world2map(self, x_world, y_world, H, W, map_scale):
		"""
		Here we convert world coordinates to map coordinates
		"""
		Hby2 = (H - 1) / 2 if H % 2 == 1 else H // 2
		Wby2 = (W - 1) / 2 if W % 2 == 1 else W // 2
		#x_map = int(Hby2 - y_world / map_scale)
		#y_map = int(Wby2 + x_world / map_scale)
		x_map = int(Hby2 + y_world / map_scale)
		y_map = int(Wby2 + x_world / map_scale)
		return x_map, y_map

	def create_msg_srv(self):
		rospy.Subscriber("/map", OccupancyGrid, self.MapCb)
		rospy.Subscriber("/odom", Odometry, self.OdomCb)
		rospy.Subscriber("/move_base/goal", MoveBaseActionGoal, self.GoalCb)
	
	def MapCb(self, data):
		# print("======== In topic /map =========")
		map = np.array(data.data)
		map_w = data.info.width
		map_h = data.info.height
		self.final_permap = np.sum(map==-1)/(map_w*map_h)
		# print(np.sum(map==0))
		# print(np.sum(map==100))
		sums = np.sum(map==0) + np.sum(map==100)
		self.total_maps = sums
		# print(self.final_permap)
	
	def OdomCb(self, data):
		# print("======== In topic /odom =========")
		robotx = data.pose.pose.position.x
		roboty = data.pose.pose.position.y
		map_x, map_y = self.world2map(robotx, roboty, 384, 384, 0.05)
		self.tmp_map[map_x][map_y] = 1
		self.total_path = np.sum(self.tmp_map==1)
	
	def GoalCb(self, data):
		self.path_array.append(self.total_path)
		print("total path length:", self.path_array)
		self.reset()
		print("======== In topic /move_base/goal =========")
		# print(data)

		print("total explored maps:", self.total_maps)

	def reset(self):
		self.tmp_map = np.zeros((384, 384))
		self.total_path = 0
	
if __name__ == "__main__":
	rospy.init_node("GG", anonymous=True, log_level=rospy.DEBUG)
	test = GetDatas()
	rospy.spin()

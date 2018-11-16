import random

class Node(object):
	def __init__(self, key, data):
		self.key = key
		self.data = data
		self.priority = random.random()
		self.left = None
		self.right = None
	
	def rotate_right(self):
		print("rotate right "+str(self))
		assert self.left != None
		new_root = self.left
		self.left = new_root.right
		new_root.right = self
		return new_root

	def rotate_left(self):
		print("rotate left "+str(self))
		assert self.right != None
		new_root = self.right
		self.right = new_root.left
		new_root.left = self
		return new_root

	def balance(self):
		print("balance "+str(self))
		node = self
		if self.left != None and self.left.priority > self.priority:
			node = self.rotate_right()
		if self.right != None and self.right.priority > self.priority:
			node = self.rotate_left()
		return node

	def isleaf(self):
		return (self.left == None and self.right == None)
	
	def __str__(self):
		ans = "key: "+str(self.key)+" data: "+str(self.data)
		ans += "\npriority: "+str(self.priority)
		if self.left != None:
			ans += "\nleft: "+str(self.left.key)
		if self.right != None:
			ans += "\nright: "+str(self.right.key)
		ans += "\n\n"

		return ans


class Treap(object):
	def __init__(self):
		self.root = None

	def traverse(self, root):
		if root == None:
			return ""

		ans = str(root) + "\n"
		ans += self.traverse(root.left)
		ans += self.traverse(root.right)
	
		return ans

	def __str__(self):
		return self.traverse(self.root)

	def _insert(self, root, node):
		print("_insert ", root, " ", node)
		if root == None:
			return node

		if node.key < root.key:
			root.left = self._insert(root.left, node)	
		else:
			root.right = self._insert(root.right, node)	

		root = root.balance()
		return root

	def insert(self, node):
		self.root = self._insert(self.root, node)
		return 

	def _erase(self, root, node):
		if root.key > node.key:
			root.left = self._erase(root.left, node)
		elif root.key < node.key:
			root.right = self._erase(root.right, node)
		else:
			if root.isleaf():
				return None
			elif root.left == None:
				return root.right
			elif root.right == None:
				return root.left
			else:
				if root.right.priority > root.left.priority:
					root = root.rotate_left()
					root.left = self._erase(root.left, node)
				else:
					root = root.rotate_right()
					root.right = self._erase(root.right, node)

		return root

		def erase(self, node):
			self.root = self._erase(root, node)
			return 



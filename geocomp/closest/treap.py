import random
from geocomp.common.point import Point

class Node(object):
	def __init__(self, key):
		self.key = key
		self.cnt = 1;
		self.priority = random.random()
		self.left = None
		self.right = None
	
	def rotate_right(self):
		assert self.left != None
		new_root = self.left
		self.left = new_root.right
		new_root.right = self
		return new_root

	def rotate_left(self):
		assert self.right != None
		new_root = self.right
		self.right = new_root.left
		new_root.left = self
		return new_root

	def balance(self):
		node = self
		if self.left != None and self.left.priority > self.priority:
			node = self.rotate_right()
		if self.right != None and self.right.priority > self.priority:
			node = self.rotate_left()
		return node

	def isleaf(self):
		return (self.left == None and self.right == None)
	
	def __str__(self):
		ans = "key: "+str(self.key) + " cnt "+str(self.cnt)
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
	
	def _find(self, root, key):
		if(root == None): 
			return None

		ret = None
		if(key < root.key):
			ret = self._find(root.left, key)
			if(ret == None):
				ret = root.key
		elif(key > root.key):
			ret = self._find(root.right, key)
		else:
			ret = root.key

		return ret
		
	# Retorna a chave Lower Bound da key buscada, ou None se nao existir nenhum maior ou igual
	def find(self, key):
		return self._find(self.root, key)

	def findPoint(self, point):
		ret = self.find([point.y, point.x])
		if ret == None:
			return None

		ans = Point(ret[1], ret[0])
		return ans
		
	def findUpperPoint(self, point):
		ret = self.find([point.y, point.x+1])
		if ret == None:
			return None

		ans = Point(ret[1], ret[0])
		return ans
		

	def _insert(self, root, node):
		if root == None:
			return node

		if node.key < root.key:
			root.left = self._insert(root.left, node)	
		elif node.key > root.key:
			root.right = self._insert(root.right, node)	
		else:
			root.cnt += 1;

		root = root.balance()
		return root

	def insert(self, key):
		node = Node(key)
		self.root = self._insert(self.root, node)
		return 

	def insertPoint(self, point):
		self.insert([point.y, point.x])

	def _erase(self, root, key):
		if key < root.key:
			root.left = self._erase(root.left, key)
		elif key > root.key:
			root.right = self._erase(root.right, key)
		else:
			if root.cnt > 1:
				root.cnt -= 1;
				return root;
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
						root.left = self._erase(root.left, key)
					else:
						root = root.rotate_right()
						root.right = self._erase(root.right, key)

		return root

	def erase(self, key):
		self.root = self._erase(self.root, key)

	def erasePoint(self, point):
		self.erase([point.y, point.x])

	def _check(self, root):
		if root == None:
			return
		assert(root.left == None or 
		 (root.left.key < root.key and root.left.priority < root.priority));
	
		assert(root.right == None or
		 (root.right.key > root.key and root.right.priority < root.priority));

		self._check(root.left)
		self._check(root.right)
		return ;


	def check(self):
		self._check(self.root)

	def clear(self):
		self.root = None


from collections import deque


def test():
	dataset = deque()
	# dataset.append(1)
	# dataset.append(2)
	# while dataset: 
	# 	print(dataset.pop())

	with open('./TestData/15.xyz', 'r') as read_f:
		for line in read_f:
			dataset.append(line)
	with open('./TestData/15_reversed.xyz', 'w') as write_f:
		while dataset:
			write_f.write(dataset.pop())


if __name__ == '__main__':
	test()
	print('--DONE--')

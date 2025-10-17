from queue import deque


def IDS(chessboard, max_depth=50):
	init_state = chessboard.board
	result = [init_state]

	for depth in range(max_depth + 1):
		stack = deque()
		stack.append((init_state, 0))
		visited = set()

		while stack:
			node, d = stack.pop()
			node_key = tuple(map(tuple, node))
			if node_key in visited:
				continue
			visited.add(node_key)
			if not chessboard.skip:
				result.append(node)

			for state in chessboard.next_states(node):
				if chessboard.is_goal_state(state):
					node = state
					if not chessboard.skip:
						result.append(node)
					return result
				if d < depth:
					stack.append((state, d + 1))

	chessboard.running = False
	return result


import heapq
from collections import deque

# ── Search result container ──────────────────────────────────────────────────
class SearchResult:
    def __init__(self, path, actions, cost, nodes_expanded, max_frontier_size):
        self.path = path
        self.actions = actions
        self.cost = cost
        self.nodes_expanded = nodes_expanded
        self.max_frontier_size = max_frontier_size

# ── Search-tree node ─────────────────────────────────────────────────────────
class Node:
    __slots__ = ("state", "parent", "action", "g", "h", "f")

    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def path(self):
        """Trace back to root and return the list root → … → self."""
        nodes = []
        cur = self
        while cur is not None:
            nodes.append(cur)
            cur = cur.parent
        nodes.reverse()
        return nodes


# ── Abstract search strategy ─────────────────────────────────────────────────

class SearchAlgorithm:
    def __init__(self):
        self.expanded_nodes = []
        self.nodes_expanded = 0
        self.max_frontier_size = 0

    def search(self, problem):
        raise NotImplementedError

    def _build_result(self, goal_node):
        p = goal_node.path()
        return SearchResult(
            path=[n.state for n in p],
            actions=[n.action for n in p if n.action is not None],
            cost=goal_node.g,
            nodes_expanded=self.nodes_expanded,
            max_frontier_size=self.max_frontier_size,
        )


# ── Breadth-First Search ─────────────────────────────────────────────────────

class BreadthFirstSearch(SearchAlgorithm):
    def search(self, problem):
        self.expanded_nodes = []
        self.nodes_expanded = 0
        self.max_frontier_size = 0

        start = problem.get_start_state()
        root = Node(start)
        if problem.is_goal_state(start):
            return self._build_result(root)

        frontier = deque([root])
        explored = {start}
        self.max_frontier_size = 1

        while frontier:
            node = frontier.popleft()
            self.expanded_nodes.append(node)
            self.nodes_expanded += 1

            for succ, action, cost in problem.get_successors(node.state):
                if succ in explored:
                    continue
                child = Node(succ, node, action, node.g + cost)
                if problem.is_goal_state(succ):
                    self.expanded_nodes.append(child)
                    return self._build_result(child)
                frontier.append(child)
                explored.add(succ)

            if len(frontier) > self.max_frontier_size:
                self.max_frontier_size = len(frontier)

        return None


# ── A* Search ────────────────────────────────────────────────────────────────

class AStarSearch(SearchAlgorithm):
    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic

    def search(self, problem):
        self.expanded_nodes = []
        self.nodes_expanded = 0
        self.max_frontier_size = 0

        start = problem.get_start_state()
        h0 = self.heuristic(start)
        root = Node(start, g=0, h=h0)
        if problem.is_goal_state(start):
            return self._build_result(root)

        counter = 0  # tie-breaker for heapq stability
        frontier = [(root.f, counter, root)]
        best_g = {start: 0}
        explored = set()
        self.max_frontier_size = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)

            if node.state in explored:
                continue

            self.expanded_nodes.append(node)

            if problem.is_goal_state(node.state):
                return self._build_result(node)

            explored.add(node.state)
            self.nodes_expanded += 1

            for succ, action, cost in problem.get_successors(node.state):
                if succ in explored:
                    continue
                g_new = node.g + cost
                if succ not in best_g or g_new < best_g[succ]:
                    best_g[succ] = g_new
                    h = self.heuristic(succ)
                    child = Node(succ, node, action, g_new, h)
                    counter += 1
                    heapq.heappush(frontier, (child.f, counter, child))

            if len(frontier) > self.max_frontier_size:
                self.max_frontier_size = len(frontier)

        return None
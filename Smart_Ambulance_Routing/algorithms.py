from heapq import heappush, heappop
from collections import deque

def reconstruct_path(came_from, start, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur, None)
        if cur == start:
            path.append(start)
            break
    return list(reversed(path))

def bfs(city, start, goal):
    queue = deque([start])
    visited = {start}
    came_from = {start: None}

    while queue:
        u = queue.popleft()
        if u == goal:
            return reconstruct_path(came_from, start, goal), None
        for v in city.neighbors(u):
            if city.is_closed(u, v):  # استبعاد الطرق المقفولة
                continue
            if v not in visited:
                visited.add(v)
                came_from[v] = u
                queue.append(v)
    return None, "لا يوجد مسار"

def dfs(city, start, goal):
    stack = [start]
    visited = {start}
    came_from = {start: None}

    while stack:
        u = stack.pop()
        if u == goal:
            return reconstruct_path(came_from, start, goal), None
        for v in city.neighbors(u):
            if city.is_closed(u, v):
                continue
            if v not in visited:
                visited.add(v)
                came_from[v] = u
                stack.append(v)
    return None, "لا يوجد مسار"

def uniform_cost(city, start, goal):
    pq = [] # Priority Queue بتخزن النود والكوست
    heappush(pq, (0.0, start)) # ميثود بنضيف فيها النود والكوست وهي بتتكفل بترتيبهم
    came_from = {start: None}
    cost_so_far = {start: 0.0} # بنخزن فيها أقل تكلفة وصلنا فيها لكل نود

    while pq:   
        g, u = heappop(pq) # جي = الأقل تكلفة، يو = النود بتاعتها
        if u == goal:
            path = reconstruct_path(came_from, start, goal)
            return path, g
        for v in city.neighbors(u):
            if city.is_closed(u, v):
                continue
            new_cost = cost_so_far[u] + city.edge_cost(u, v)
            if v not in cost_so_far or new_cost < cost_so_far[v]:
                cost_so_far[v] = new_cost
                came_from[v] = u
                heappush(pq, (new_cost, v))
    return None, "لا يوجد مسار"

def greedy_best_first(city, start, goal):
    pq = []
    heappush(pq, (city.heuristic(start, goal), start))
    came_from = {start: None}
    visited = set()

    while pq:
        _, u = heappop(pq)
        if u == goal:
            path = reconstruct_path(came_from, start, goal)
            # التكلفة الفعلية، مبنستخدمهاش بس في السيرش بس لو عايزين نعرضها
            total = 0.0
            for i in range(len(path)-1):
                total += city.edge_cost(path[i], path[i+1])
            return path, total
        visited.add(u)
        for v in city.neighbors(u):
            if city.is_closed(u, v):
                continue
            if v not in visited:
                came_from[v] = u
                heappush(pq, (city.heuristic(v, goal), v))
    return None, "لا يوجد مسار"

def a_star(city, start, goal):
    pq = []
    heappush(pq, (0.0, start))
    came_from = {start: None}
    g_cost = {start: 0.0}

    while pq:
        _, u = heappop(pq)
        if u == goal:
            path = reconstruct_path(came_from, start, goal)
            return path, g_cost[u]
        for v in city.neighbors(u):
            if city.is_closed(u, v):
                continue
            tentative_g = g_cost[u] + city.edge_cost(u, v)
            if v not in g_cost or tentative_g < g_cost[v]:
                g_cost[v] = tentative_g
                came_from[v] = u
                f = tentative_g + city.heuristic(v, goal)  # f(n) = g(n) + h(n)
                heappush(pq, (f, v))
    return None, "لا يوجد مسار"
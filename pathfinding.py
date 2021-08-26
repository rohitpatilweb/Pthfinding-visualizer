import pygame
from queue import PriorityQueue

pygame.init()


pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 18)

width = 600
rows = 30
grid = []
win = pygame.display.set_mode((778, 600))
pygame.display.set_caption("Path Finding Visualizer")
path_color = (50, 90, 195)
back_color = (200, 200, 200)
wall_color = (40, 40, 40)
searched_color = (150, 150, 150)
fill_color = (204, 204, 179)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = back_color
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == wall_color

    def make_start(self):
        self.color = path_color

    def make_end(self):
        self.color = path_color

    def reset(self):
        self.color = back_color

    def make_visited(self):
        self.color = searched_color

    def make_unvisited(self):
        self.color = back_color

    def make_wall(self):
        self.color = wall_color

    def make_path(self):
        self.color = path_color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self):
        self.neighbours = []

        # down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  
            self.neighbours.append(grid[self.row + 1][self.col])

        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  
            self.neighbours.append(grid[self.row - 1][self.col])

        # right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  
            self.neighbours.append(grid[self.row][self.col + 1])

        # left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  
            self.neighbours.append(grid[self.row][self.col - 1])


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def findPath(start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}
    came_from = {}
    g = {}
    f = {}
    for row in grid:
        for node in row:
            g[node] = float("inf")
            f[node] = float("inf")
    g[start] = 0
    f[start] = h(start.get_position(), end.get_position())

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            end.make_end()
            reconstruct_path(came_from, end)
            return True

        for neighbour in current.neighbours:
            temp_g = g[current] + 1

            if temp_g < g[neighbour]:
                came_from[neighbour] = current
                g[neighbour] = temp_g
                f[neighbour] = temp_g + h(neighbour.get_position(), end.get_position())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)

        draw()
        if current != start:
            current.make_visited()

    return False


def findPathDijkstra(start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}
    came_from = {}
    g = {}
    for row in grid:
        for node in row:
            g[node] = float("inf")
    g[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            end.make_end()
            reconstruct_path(came_from, end)
            start.make_start()
            return True

        for neighbour in current.neighbours:
            temp_g = g[current] + 1
            if temp_g < g[neighbour]:
                came_from[neighbour] = current
                g[neighbour] = temp_g
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((g[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    
        draw()
        if current != start:
            current.make_visited()

    return False


def make_grid():
    space = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, space, rows)
            grid[i].append(node)
    return True


def draw():
    win.fill(fill_color)
    for row in grid:
        for node in row:
            node.draw(win)
            #  drawing lines
    space = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, (130, 130, 130), (0, i * space), (width, i * space))
        for j in range(rows + 1):
            pygame.draw.line(win, (130, 130, 130), (j * space, 0), (j * space, width))

    pygame.draw.line(win, (50, 50, 50), (width, 0), (width, width))
    pygame.draw.line(win, (0, 0, 0), (620, 100), (755, 100))
    pygame.draw.line(win, (0, 0, 0), (620, 140), (755, 140))
    pygame.draw.line(win, (0, 0, 0), (755, 100), (755, 140))
    pygame.draw.line(win, (0, 0, 0), (620, 100), (620, 140))
    pygame.draw.line(win, (0, 0, 0), (620, 180), (755, 180))
    pygame.draw.line(win, (0, 0, 0), (620, 250), (755, 250))
    pygame.draw.line(win, (0, 0, 0), (620, 350), (755, 350))
    pygame.draw.line(win, (0, 0, 0), (620, 180), (620, 350))
    pygame.draw.line(win, (0, 0, 0), (755, 180), (755, 350))

    pygame.draw.rect(win, (102, 179, 255), (621, 101, 134, 39))
    textsurface = myfont.render('RESET', False, (0, 0, 0))
    win.blit(textsurface, (652, 110))

    pygame.draw.rect(win, (153, 153, 102), (621, 181, 134, 69))
    textsurface = myfont.render('A* Algorithm', False, (0, 0, 0))
    win.blit(textsurface, (629, 205))

    pygame.draw.rect(win, (153, 153, 102), (621, 251, 134, 99))
    textsurface = myfont.render("Dijkstra's ", False, (0, 0, 0))
    win.blit(textsurface, (639, 265))
    textsurface = myfont.render("Algorithm", False, (0, 0, 0))
    win.blit(textsurface, (640, 295))

    pygame.display.update()


def main():
    print("dsg")
    make_grid()
    start = None
    end = None
    run = True
    started = False

    while run:
        draw()
        f = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if pygame.mouse.get_pressed()[0]:  # left button
                pos = pygame.mouse.get_pos()
                y, x = pos
                space = width // rows
                row = y // space
                col = x // space
                if (y <= 591):
                    node = grid[row][col]
                    if not start:
                        start = node
                        start.make_start()

                    elif not end:
                        end = node
                        end.make_end()

                    elif node != end and node != start:
                        node.make_wall()
                elif (y >= 620 and y <= 755):
                    if (x >= 180 and x <= 250):
                        for row in grid:
                            for node in row:
                                if (not node.is_wall() and node != start and node != end):
                                    node.make_unvisited()
                                node.update_neighbours()
                        findPath(start, end)
                    elif (x > 250 and x <= 350):
                        for row in grid:
                            for node in row:
                                if (not node.is_wall() and node != start and node != end):
                                    node.make_unvisited()
                                node.update_neighbours()
                        findPathDijkstra(start, end)
                    elif (x >= 100 and x <= 140):
                        start = None
                        end = None
                        for row in grid:
                            for node in row:
                                node.reset()

            elif pygame.mouse.get_pressed()[2]:  # right click on a node
                pos = pygame.mouse.get_pos()
                y, x = pos
                space = width // rows
                row = y // space
                col = x // space
                node = grid[row][col]
                node.reset()                   # reset that node
                if node == start:
                    start = None
                elif node == end:
                    end = None

    pygame.quit()

main()
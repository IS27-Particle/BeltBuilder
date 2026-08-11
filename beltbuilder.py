import time
import threading

class template(object):
    def __init__(self, gen=1, startlanes=1, endlanes=1):
        self.layout = [[]]
        self.generator = []
        self.items = []

    def _genmod(self, xmod, ymod):
        for gen in self.generator:
            gen.x += xmod
            gen.y += ymod

    def AddObject(self, newobj, x, y):
        # Right Size the Array
        test = self.layout.copy() # Port to Temporary Variable
        xmod = 0 # x direction modifier if value is negative
        ymod = 0 # y direction modifier if value is negative
        for i in range(0, x, -1):
            test.insert(0, 0) # Insert a blank to shift array
            xmod += 1
        x += xmod
        for i in range(0, y, -1):
            test[x].insert(0, 0)
            ymod += 1
        y += ymod
        self._genmod(xmod, ymod)
        xmod = 0
        ymod = 0
        for i in range(len(self.layout), x, 1):
            test.append([])
        for i in range(len(self.layout[x]), y, 1):
            test[x].append(0)

        if test[x][y] == 0:
            test[x][y] = newobj
            if type(newobj).__name__ == "generator":
                newobj.x, newobj.y = x, y
                self.generator.append(newobj)
            if type(newobj).__name__ == "splitter":
                if newobj.direction == 0:
                    for i in range(len(test), x+1, 1):
                        test.append([])
                    for i in range(len(test), y, 1):
                        test[x+1].append(0)
                    if test[x+1][y] == 0:
                        test[x+1][y] = (1, x, y)
                    else:
                        raise Exception('invalid location splitter - 0')
                elif newobj.direction == 1:
                    for i in range(0, y-1, -1):
                        test[x].insert(0, 0)
                        ymod += 1
                    y += ymod
                    self._genmod(xmod, ymod)
                    ymod = 0
                    if test[x][y-1] == 0:
                        test[x][y-1] = (1, x, y)
                    else:
                        raise Exception('invalid location splitter - 1')
                elif newobj.direction == 2:
                    for i in range(0, x-1, -1):
                        test.insert(0, [])
                        xmod += 1
                    x += xmod
                    self._genmod(xmod, ymod)
                    xmod = 0
                    for i in range(len(test[x-1]), y, 1):
                        test[x-1].append(0)
                    if test[x-1][y] == 0:
                        test[x-1][y] = (1, x, y)
                    else:
                        raise Exception('invalid location splitter - 2')
                elif newobj.direction == 3:
                    for i in range(len(test[x]), y+1, 1):
                        test[x].append(0)
                    if test[x][y+1] == 0:
                        test[x][y+1] = (1, x, y)
                    else:
                        raise Exception('invalid location splitter - 3')
            if type(newobj).__name__ == "underground":
                if newobj.direction == 0:
                    for i in range(len(test[x]), y+newobj.distance, 1):
                        test[x].append(0)
                    if test[x][y+newobj.distance] == 0:
                        first = -1
                        end = -1
                        inbounds = False
                        for i in range(0, y+newobj.distance, 1):
                            if i == y:
                                inbounds = True
                            if i == y+newobj.distance:
                                inbounds = False
                            if first != -1 and i == y:
                                raise Exception('invalid distance underground - 0-0')
                            if end != -1 and i == y:
                                raise Exception('invalid distance underground - 0-1')
                            if type(test[x][i]).__name__ == "underground":
                                if first == -1 and test[x][i].color == newobj.color and end == -1:
                                    if not inbounds:
                                        first = i
                                    else:
                                        raise Exception('invalid distance underground - 0-2')
                                if end != -1:
                                    if test[x][i].color == test[x][end][0]-1:
                                        end = -1
                            elif type(test[x][i]).__name__ == "tuple":
                                if first == -1 and test[x][i][0] >= 2 and test[x][i][0]-1 == newobj.color and end == -1:
                                    if not inbounds:
                                        end = i
                                    else:
                                        raise Exception('invalid distance underground - 0-3')
                                if first != -1:
                                    if test[x][i][0]-1 == test[x][first].color:
                                        first = -1
                        test[x][y+newobj.distance] = (1+newobj.color, x, y)
                    else:
                        raise Exception('invalid location underground - 0')
                elif newobj.direction == 1:
                    for i in range(len(test), x+newobj.distance, 1):
                        test.append([])
                    for i in range(len(test[x+newobj.distance]), y, 1):
                        test[x+newobj.distance].append(0)
                    if test[x+newobj.distance][y] == 0:
                        first = -1
                        end = -1
                        inbounds = False
                        for i in range(0, x+newobj.distance, 1):
                            if i == x:
                                inbounds = True
                            if i == x+newobj.distance:
                                inbounds = False
                            if first != -1 and i == x:
                                raise Exception('invalid distance underground - 1-0')
                            if end != -1 and i == x:
                                raise Exception('invalid distance underground - 1-1')
                            if type(test[i][y]).__name__ == "underground":
                                if first == -1 and test[i][y].color == newobj.color and end == -1:
                                    if not inbounds:
                                        first = i
                                    else:
                                        raise Exception('invalid distance underground - 1-2')
                                if end != -1:
                                    if test[i][y].color == test[end][y][0]-1:
                                        end = -1
                            elif type(test[i][y]).__name__ == "tuple":
                                if first == -1 and test[i][y][0] >= 2 and test[i][y][0]-1 == newobj.color and end == -1:
                                    if not inbounds:
                                        end = i
                                    else:
                                        raise Exception('invalid distance underground - 1-3')
                                if first != -1:
                                    if test[i][y][0]-1 == test[first][y].color:
                                        first = -1
                        test[x+newobj.distance][y] = (1+newobj.color, x, y)
                    else:
                        raise Exception('invalid location underground - 1')
                elif newobj.direction == 2:
                    for i in range(0, y-newobj.distance, -1):
                        test[x].insert(0, 0)
                        ymod += 1
                    y += ymod
                    self._genmod(xmod, ymod)
                    ymod = 0
                    if test[x][y-newobj.distance] == 0:
                        first = -1
                        end = -1
                        inbounds = False
                        for i in range(0, y, 1):
                            if i == y:
                                inbounds = False
                            if i == y-newobj.distance:
                                inbounds = True
                            if first != -1 and i == y - newobj.distance:
                                raise Exception('invalid distance underground - 2-0')
                            if end != -1 and i == y - newobj.distance:
                                raise Exception('invalid distance underground - 2-1')
                            if type(test[x][i]).__name__ == "underground":
                                if first == -1 and test[x][i].color == newobj.color and end == -1:
                                    if not inbounds:
                                        first = i
                                    else:
                                        raise Exception('invalid distance underground - 2-2')
                                if end != -1:
                                    if test[x][i].color == test[x][end][0]-1:
                                        end = -1
                            elif type(test[x][i]).__name__ == "tuple":
                                if first == -1 and test[x][i][0] >= 2 and test[x][i][0]-1 == newobj.color and end == -1:
                                    if not inbounds:
                                        end = i
                                    else:
                                        raise Exception('invalid distance underground - 2-3')
                                if first != -1:
                                    if test[x][i][0]-1 == test[x][first].color:
                                        first = -1
                        test[x][y-newobj.distance] = (1+newobj.color, x, y)
                    else:
                        raise Exception('invalid location underground - 2')
                elif newobj.direction == 3:
                    for i in range(0, x-newobj.distance, -1):
                        test.insert(0, [])
                        xmod += 1
                    x += xmod
                    self._genmod(xmod, ymod)
                    xmod = 0
                    for i in range(len(test[x]), y, 1):
                        test[x-newobj.distance].append(0)
                    if test[x-newobj.distance][y] == 0:
                        first = -1
                        end = -1
                        inbounds = False
                        for i in range(0, x, 1):
                            if i == x:
                                inbounds = False
                            if i == x-newobj.distance:
                                inbounds = True
                            if first != -1 and i == x - newobj.distance:
                                raise Exception('invalid distance underground - 3-0')
                            if end != 1 and i == x - newobj.distance:
                                raise Exception('invalid distance underground - 3-1')
                            if type(test[i][y]).__name__ == "underground":
                                if first == -1 and test[i][y].color == newobj.color and end == -1:
                                    if not inbounds:
                                        first = i
                                    else:
                                        raise Exception('invalid distance underground - 3-2')
                                if end != -1:
                                    if test[i][y].color == test[end][y][0]-1:
                                        end = -1
                            elif type(test[i][y]).__name__ == "tuple":
                                if first == -1 and test[i][y][0] >= 2 and test[i][y][0]-1 == newobj.color and end == -1:
                                    if not inbounds:
                                        end = i
                                    else:
                                        raise Exception('invalid distance underground - 2-3')
                                if first != -1:
                                    if test[i][y][0]-1 == test[i][first].color:
                                        first = -1
                        test[x-newobj.distance][y] = (1+newobj.color, x, y)
                    else:
                        raise Exception('invalid location underground - 3')
        self.layout = test.copy()

class item(object):
    def __init__(self, parent):
        self.start = time.time()
        self.parent = parent
        self.parent.items.append(self)

    def CheckTime(self):
        if time.time() - self.start >= 1/self.parent.speed:
            return True
        return False

    def run(self):
        while self.CheckTime():
            continue

class generator(object):
    def __init__(self, parent, beltside=0, speed=1, direction=0):
        '''
            beltside
                0 - nothing
                1 - left side
                2 - right side
                3 - both sides
            speed - relative to square in front toward direction
                1 - fill the square to limit/speed
        '''
        self.side = beltside
        self.direction = direction
        self.speed = speed
        self.x = 0
        self.y = 0
        self.parent = parent

    def AddItem(self):
        if self.direction == 0:
            if len(self.parent.layout[self.x]) < self.y + 1:
                raise Exception('This generator leads outside template - 0')
            if type(self.parent.layout[self.x][self.y + 1]) == int:
                if self.parent.layout[self.x][self.y + 1] == 0:
                    raise Exception('There is nothing here - 0')
            if type(self.parent.layout[self.x][self.y + 1]).__name__ != "destroyer":
                if self.side != 0 and (len(self.parent.layout[self.x][self.y + 1].sides[0].items) < self.parent.layout[self.x][self.y + 1].sides[0].limit and self.side != 2):
                    newitem = item(self.parent.layout[self.x][self.y + 1].sides[0])
                if self.side != 0 and (len(self.parent.layout[self.x][self.y + 1].sides[1].items) < self.parent.layout[self.x][self.y + 1].sides[1].limit and self.side != 1):
                    newitem = item(self.parent.layout[self.x][self.y + 1].sides[1])
        elif self.direction == 1:
            if len(self.parent.layout) < self.x + 1:
                raise Exception('This generator leads outside template - 1')
            if type(self.parent.layout[self.x + 1][self.y]) == int:
                if self.parent.layout[self.x + 1][self.y] == 0:
                    raise Exception('There is nothing here - 1')
            if type(self.parent.layout[self.x + 1][self.y]).__name__ != "destroyer":
                if self.side != 0 and (len(self.parent.layout[self.x + 1][self.y].sides[0].items) < self.parent.layout[self.x + 1][self.y].sides[0].limit and self.side != 2):
                    newitem = item(self.parent.layout[self.x + 1][self.y].sides[0])
                if self.side != 0 and (len(self.parent.layout[self.x + 1][self.y].sides[1].items) < self.parent.layout[self.x + 1][self.y].sides[1].limit and self.side != 1):
                    newitem = item(self.parent.layout[self.x + 1][self.y].sides[1])
        elif self.direction == 2:
            if self.y - 1 < 0:
                raise Exception('This generator leads outside template - 2')
            if type(self.parent.layout[self.x][self.y - 1]) == int:
                if self.parent.layout[self.x][self.y - 1] == 0:
                    raise Exception('There is nothing here - 2')
            if type(self.parent.layout[self.x][self.y - 1]).__name__ != "destroyer":
                if self.side != 0 and (len(self.parent.layout[self.x][self.y - 1].sides[0].items) < self.parent.layout[self.x][self.y - 1].sides[0].limit and self.side != 2):
                    newitem = item(self.parent.layout[self.x][self.y - 1].sides[0])
                if self.side != 0 and (len(self.parent.layout[self.x][self.y - 1].sides[1].items) < self.parent.layout[self.x][self.y - 1].sides[1].limit and self.side != 1):
                    newitem = item(self.parent.layout[self.x][self.y - 1].sides[1])
        elif self.direction == 3:
            if self.x - 1 < 0:
                raise Exception('This generator leads outside template - 3')
            if type(self.parent.layout[self.x - 1][self.y]) == int:
                if self.parent.layout[self.x - 1][self.y] == 0:
                    raise Exception('There is nothing here - 3')
            if type(self.parent.layout[self.x - 1][self.y]).__name__ != "destroyer":
                if self.side != 0 and (len(self.parent.layout[self.x - 1][self.y].sides[0].items) < self.parent.layout[self.x - 1][self.y].sides[0].limit and self.side != 2):
                    newitem = item(self.parent.layout[self.x - 1][self.y].sides[0])
                if self.side != 0 and (len(self.parent.layout[self.x - 1][self.y].sides[1].items) < self.parent.layout[self.x - 1][self.y].sides[1].limit and self.side != 1):
                    newitem = item(self.parent.layout[self.x - 1][self.y].sides[1])

class destroyer(object):
    def __init__(self, direction=0):
        self.direction = direction

class bside(object):
    def __init__(self, parent, speed, sideID):
        self.limit = 4
        self.speed = speed
        self.items = []
        self.parent = parent
        self.side = sideID

    def run(self):
        for item in self.items:
            item.run()
            if self.parent.direction == 0:
                if len(self.parent.parent.layout[self.x]) < self.y + 1:
                    raise Exception('This generator leads outside template - 0')
                if type(self.parent.parent.layout[self.x][self.y + 1]) == int:
                    if self.parent.parent.layout[self.x][self.y + 1] == 0:
                        raise Exception('There is nothing here - 0')
                if type(self.parent.layout[self.x][self.y + 1]).__name__ != "destroyer":
                    if (len(self.parent.parent.layout[self.x][self.y + 1].sides[0].items) < self.parent.parent.layout[self.x][self.y + 1].sides[0].limit and self.side != 2):
                        item.parent = self.parent.parent.layout[self.x][self.y + 1].sides[0]
                        self.parent.parent.layout[self.x][self.y + 1].sides[0].items.append(item)
                    if (len(self.parent.parent.layout[self.x][self.y + 1].sides[1].items) < self.parent.parent.layout[self.x][self.y + 1].sides[1].limit and self.side != 1):
                        item.parent = self.parent.parent.layout[self.x][self.y + 1].sides[1]
                        self.parent.parent.layout[self.x][self.y + 1].sides[1].items.append(item)
                else:
                    del item
            elif self.parent.direction == 1:
                if len(self.parent.parent.layout) < self.x + 1:
                    raise Exception('This generator leads outside template - 1')
                if type(self.parent.parent.layout[self.x + 1][self.y]) == int:
                    if self.parent.parent.layout[self.x + 1][self.y] == 0:
                        raise Exception('There is nothing here - 1')
                if (len(self.parent.parent.layout[self.x + 1][self.y].sides[0].items) < self.parent.parent.layout[self.x + 1][self.y].sides[0].limit and self.side != 2):
                    item.parent = self.parent.parent.layout[self.x + 1][self.y].sides[0]
                    self.parent.parent.layout[self.x + 1][self.y].sides[0].items.append(item)
                if (len(self.parent.parent.layout[self.x + 1][self.y].sides[1].items) < self.parent.parent.layout[self.x + 1][self.y].sides[1].limit and self.side != 1):
                    item.parent = self.parent.parent.layout[self.x + 1][self.y].sides[1]
                    self.parent.parent.layout[self.x + 1][self.y].sides[1].items.append(item)
            elif self.parent.direction == 2:
                if self.y - 1 < 0:
                    raise Exception('This generator leads outside template - 2')
                if type(self.parent.parent.layout[self.x][self.y - 1]) == int:
                    if self.parent.parent.layout[self.x][self.y - 1] == 0:
                        raise Exception('There is nothing here - 2')
                if (len(self.parent.parent.layout[self.x][self.y - 1].sides[0].items) < self.parent.parent.layout[self.x][self.y - 1].sides[0].limit and self.side != 2):
                    newitem = item(self.parent.parent.layout[self.x][self.y - 1].sides[0])
                if (len(self.parent.parent.layout[self.x][self.y - 1].sides[1].items) < self.parent.parent.layout[self.x][self.y - 1].sides[1].limit and self.side != 1):
                    newitem = item(self.parent.parent.layout[self.x][self.y - 1].sides[1])
            elif self.parent.direction == 3:
                if self.x - 1 < 0:
                    raise Exception('This generator leads outside template - 3')
                if type(self.parent.parent.layout[self.x - 1][self.y]) == int:
                    if self.parent.parent.layout[self.x - 1][self.y] == 0:
                        raise Exception('There is nothing here - 3')
                if (len(self.parent.parent.layout[self.x - 1][self.y].sides[0].items) < self.parent.parent.layout[self.x - 1][self.y].sides[0].limit and self.side != 2):
                    newitem = item(self.parent.parent.layout[self.x - 1][self.y].sides[0])
                if (len(self.parent.parent.layout[self.x - 1][self.y].sides[1].items) < self.parent.parent.layout[self.x - 1][self.y].sides[1].limit and self.side != 1):
                    newitem = item(self.parent.parent.layout[self.x - 1][self.y].sides[1])

class belt(object):
    def __init__(self, parent, color=1, direction=0):
        self.color = color
        self.speed = self.color * 15
        self.direction = direction
        self.count = 0
        self.sides = [bside(self, self.speed / 2, 1), bside(self, self.speed / 2, 2)]
        self.size = 1
        self.avgpermin = 0

    def run(self):
        for side in self.sides:
            side.run()

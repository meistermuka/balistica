import curses

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT

class Shell(object):

    def __init__(self, y, x, window, max_y, max_x, char='@'):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.char = char
        self.window = window
        self.direction = KEY_RIGHT
        self.nose_x = self.x + 1
        self.nose_y = self.y

        self.REV_DIR_MAP = {
            KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP,
            KEY_LEFT: KEY_RIGHT,
            KEY_RIGHT: KEY_LEFT
        }

        self.direction_map = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }

    @property
    def coord(self):
        return self.x, self.y

    def update(self):
        self.direction_map[self.direction]()

    def change_direction(self, direction):
        if direction != self.REV_DIR_MAP[direction]:
            #self.direction = direction
            self.direction_map[direction]()

    def render(self):
        self.window.addstr(self.y, self.x, self.char)
        # Nose to shoot
        self.window.addstr(self.nose_y, self.nose_x, '+')

    def move_up(self):
        self.y -= 1
        if self.y < 1 or self.nose_y < 1:
            self.y = self.max_y
            self.nose_y = self.max_y - 1

        self.nose_y = self.y - 1
        self.nose_x = self.x

    def move_down(self):
        self.y += 1
        if self.y > self.max_y or self.nose_y > self.max_y:
            self.y = 1
            self.nose_y = self.y + 1

        self.nose_y = self.y + 1
        self.nose_x = self.x

    def move_left(self):
        self.x -= 1
        if self.x < 1 or self.nose_x < 1:
            self.x = self.max_x
            self.nose_x = self.max_x - 1

        self.nose_x = self.x - 1
        self.nose_y = self.y

    def move_right(self):
        self.x += 1
        if self.x > self.max_x or self.nose_x > self.max_x:
            self.x = 1
            self.nose_x = self.x + 1

        self.nose_x = self.x + 1
        self.nose_y = self.y

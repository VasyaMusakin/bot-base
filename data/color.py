class Color:
    def green(self, c):
        return int(c // 2), int(c), int(c // 3)

    def grey(self, c):
        return int(c // 4), int(c // 4), int(c // 4)

    def purple(self, c):
        return int(c // 1.5), int(0), int(c)

    def red(self, c):
        return int(c), 0, int(c // 6)

    def blue(self, c):
        return 0, 0, int(c)

    def chek(self, num, c):
        if num == 1:
            return self.green(c)
        elif num == 2:
            return self.grey(c)
        elif num == 3:
            return self.purple(c)
        elif num == 4:
            return self.red(c)
        elif num == 5:
            return self.blue(c)
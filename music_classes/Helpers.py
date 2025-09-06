import pygame
import math
pygame.init()

def normX(screen):
    width, height = screen.get_size()
    return width/1280

def normY(screen):
    width, height = screen.get_size()
    return height/720

# --- helper functions for anti-aliased drawing ---
def aaline_thick(surface, color, start, end, width=1):
    """Draw an anti-aliased line with an approximate thickness.
    If width <= 1 uses pygame.draw.aaline, otherwise draws several
    offset aalines perpendicular to the main line to simulate thickness.
    """
    if width <= 1:
        pygame.draw.aaline(surface, color, start, end)
        return

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    # perpendicular unit vector
    px, py = -uy, ux

    # number of offsets (covering approx width pixels)
    # we center the offsets around 0
    n = int(math.ceil(width))
    # generate offsets that cover roughly the requested width
    # use symmetric integer offsets
    offsets = []
    half = (n - 1) / 2.0
    for i in range(n):
        offsets.append(i - half)

    for off in offsets:
        ox = px * off
        oy = py * off
        pygame.draw.aaline(surface, color, (start[0] + ox, start[1] + oy), (end[0] + ox, end[1] + oy))


def aarc(surface, color, rect, start_angle, end_angle, width=1, steps=60):
    x, y, w, h = rect
    cx = x + w / 2.0
    cy = y + h / 2.0
    rx = w / 2.0
    ry = h / 2.0

    # normalize angles so end >= start
    a0 = start_angle
    a1 = end_angle
    if a1 < a0:
        a1 += 2 * math.pi

    total_angle = a1 - a0
    # adapt number of steps to angular span
    steps = max(8, int(steps * (abs(total_angle) / (2 * math.pi))))
    step = total_angle / steps

    pts = []
    a = a0
    for i in range(steps + 1):
        pxp = cx + rx * math.cos(a)
        # NOTE: invert the sine term so arc orientation matches pygame.draw.arc
        pyp = cy - ry * math.sin(a)
        pts.append((pxp, pyp))
        a += step

    for i in range(len(pts) - 1):
        aaline_thick(surface, color, pts[i], pts[i + 1], width)

# --- end helpers ---


# --- debug functions ---

class RedDot():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 0, 0)  # Red color

    def show(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# --- end debug functions ---
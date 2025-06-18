import pygame as pg
from pygame.math import Vector2
from math import acos, pi, cos, sin


class Cursor:
    def __init__(self, raio, screen:pg.Surface, beta=0.0006, alpha=0.015, trail_length=6, pos0:Vector2 = Vector2(0, 0), color=(255, 255, 255)):

        self.raio = raio
        self.beta = beta
        self.alpha = alpha
        self.pos = pos0
        self.trail = [pos0.copy() for _ in range(trail_length)]
        self.trail_length = trail_length
        self.color = color
        self.screen = screen
        self.last_vel_mag = 0
        self.last_vel = Vector2(1, 0)

    def update(self, pos: Vector2, dt: float):
        self.pos = pos
        self.trail.append(pos)
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw(self, pos: Vector2, dt: float):
        self.update(pos, dt)

        velocity = (self.pos - self.trail[-3]) / (2*dt) if dt > 0 else Vector2(0, 0)
        if velocity.length() != 0:
            self.last_vel = velocity

        v_magnitude = velocity.length()
        v_magnitude = self.last_vel_mag + (v_magnitude - self.last_vel_mag) * dt * 10  # Smooth the velocity change
        if v_magnitude < 40:
            v_magnitude = 0
        self.last_vel_mag = v_magnitude

        side = 100
        scale = 2
        high_res = pg.Surface((side, side), pg.SRCALPHA)
        middle = Vector2(side / 2, side / 2)
        r = self.raio * scale / (1 + self.beta * v_magnitude)
        if v_magnitude != 0:
            velocity = self.last_vel.normalize() * v_magnitude
            d = r + v_magnitude * self.alpha * scale
            alpha = acos(r / d)
            u_vel = velocity.normalize()
            u_vel_r = u_vel * r
            p1 = middle + u_vel_r.rotate_rad(-alpha)
            p2 = middle + u_vel_r.rotate_rad(alpha)
            p3 = middle + u_vel_r.rotate_rad(pi - alpha)
            p4 = middle + u_vel_r.rotate_rad(pi + alpha)
            pg.draw.polygon(high_res, self.color, [p1, p2, middle + u_vel*d])
            pg.draw.polygon(high_res, self.color, [p3, p4, middle - u_vel*d])
        pg.draw.circle(high_res, self.color, (int(middle.x), int(middle.y)), int(r))
        high_res = pg.transform.rotozoom(high_res, 0, 1/scale)
        self.screen.blit(high_res, (self.pos.x - side / scale / 2, self.pos.y - side / scale / 2))
        if len(self.trail) > 1:
            pg.draw.lines(self.screen, self.color, False, self.trail, 2)

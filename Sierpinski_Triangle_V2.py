"""Use a click of the mouse to define a point on the plane three times.
Be sure that the three points are non-collinear so they define a triangle.
Click with the mouse a 4th time anywhere inside (or outside) the triangle.
Sierpinski's triangle will start to materialize."""

import sys
import pygame, random
pygame.init()

timex = pygame.time.Clock()
# Raise the speed to speed up the formation of the triangle.
speed = 30
screen_width = 1400*.9
screen_height = 900*.9
screen = pygame.display.set_mode([screen_width,screen_height])
screen_color = (180,180,180)
point_color = (0,0,255)
diminishing_point_color = (255,0,0)
plotted_point_radius = 1
new_point = (0,0)
num_points_so_far = 0
desired_num_points = 10000
# diminishing_points is a list containing instances of the Point class.
diminishing_points = []
# coords_of_plotted_points is a list containing tuples (coordinate pairs).
coords_of_plotted_points = []

def mouse_on_display_screen(mouse_position):
    if ((0 <= mouse_position[0] <= screen_width) and (0 <= mouse_position[1] <= screen_height)):
        return True
    else:
        return False

def add_new_point(coordinates, num_points_beyond_vertices):
    coords_of_plotted_points.append(coordinates)
    diminishing_points.append(Point(coordinates,20))
    print(f"The number of plotted points is {str(len(coords_of_plotted_points))}.")
    print(f"The number of diminishing points is {str(len(diminishing_points))}.")
    print(f"The number of points beyond the vertices is {str(num_points_beyond_vertices)}.")

def midpoint(point_A,point_B):
    x_mid = (point_A[0]+point_B[0])/2
    y_mid = (point_A[1]+point_B[1])/2
    return x_mid,y_mid

class Point:
    def __init__(self, coordinates, radius):
        self.coordinates = coordinates
        self.size = radius
    def diminish(self):
        self.size -= 1
        if self.size < 1:
            diminishing_points.remove(self)

def update_screen():
    # Plot a clear screen.
    screen.fill(screen_color)
    # Plot all coords_of_plotted_points
    for coords in coords_of_plotted_points:
        pygame.draw.circle(screen, point_color, coords, plotted_point_radius)
    # Plot all diminishing_points
    for point in diminishing_points:
        pygame.draw.circle(screen, diminishing_point_color, point.coordinates, point.size)
        point.diminish()
    # Make the most recently drawn screen visible.
    pygame.display.flip()
        
screen.fill(screen_color)

running = True

while running:
    timex.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_position = (mouse_x,mouse_y)
            if len(coords_of_plotted_points) < 3 and mouse_on_display_screen(mouse_position):
                add_new_point(mouse_position,0)
            elif len(coords_of_plotted_points) == 3 and new_point == (0,0):
                new_point = mouse_position
                add_new_point(mouse_position,1)
                num_points_so_far = 1
    if new_point != (0,0) and num_points_so_far < desired_num_points:
        num_points_so_far += 1
        random_index = random.randint(0,2)
        new_point = midpoint(new_point,coords_of_plotted_points[random_index])
        add_new_point(new_point, num_points_so_far)
    update_screen()
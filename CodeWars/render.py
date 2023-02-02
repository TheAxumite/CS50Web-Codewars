import numpy as np

import pygame

vertices = [[1, 1, 1], [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, -1]]

faces = [[0, 1, 2, 3],
         [0, 4, 5, 1],
         [0, 3, 7, 4],
         [6, 2, 1, 5],
         [6, 5, 4, 7],
         [6, 7, 3, 2]
         ]

colors = [[255, 0, 0],
          [0, 255, 0],
          [0, 0, 255],
          [255, 255, 0],
          [0, 255, 255],
          [255, 0, 255]
          ]


def projection_matrix(fov, aspect_ratio, near, far):
    fov = np.deg2rad(fov)
    t = np.tan(0.5 * (np.pi - fov))
    b = -t
    r = aspect_ratio * t
    l = -r
    
    projection = np.zeros((4, 4))
    projection[0][0] = 2.0 / (r - l)
    projection[0][2] = (r + l) / (r - l)
    projection[1][1] = 2.0 / (t - b)
    projection[1][2] = (t + b) / (t - b)
    projection[2][2] = -(far + near) / (far - near)
    projection[2][3] = -2.0 * far * near / (far - near)
    projection[3][2] = -1.0
    
    return projection



def drawPolygon(vertices, color):
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    screen.fill((255, 255, 255))

    pygame.draw.polygon(screen, color, vertices, 0)

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def transformation_matrix(translation, rotation):
    t = np.array([[1, 0, 0, translation[0]],
                  [0, 1, 0, translation[1]],
                  [0, 0, 1, translation[2]],
                  [0, 0, 0, 1]])
    
    rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(rotation[0]), -np.sin(rotation[0]), 0],
                   [0, np.sin(rotation[0]), np.cos(rotation[0]), 0],
                   [0, 0, 0, 1]])
    
    ry = np.array([[np.cos(rotation[1]), 0, np.sin(rotation[1]), 0],
                   [0, 1, 0, 0],
                   [-np.sin(rotation[1]), 0, np.cos(rotation[1]), 0],
                   [0, 0, 0, 1]])
    
    rz = np.array([[np.cos(rotation[2]), -np.sin(rotation[2]), 0, 0],
                   [np.sin(rotation[2]), np.cos(rotation[2]), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    
    r = np.dot(np.dot(rx, ry), rz)
    m = np.dot(t, r)
    
    return m

def draw3D(vertices, faces, colors):
    # Convert vertices to a numpy array
    vertices = np.array(vertices)

    # Perform transformation on vertices to place them in the camera's view
    vertices = np.dot(vertices, transformation_matrix)

    # Project vertices onto the 2D screen
    vertices = np.dot(vertices, projection_matrix)

    # Normalize vertices for display
    vertices[:, 0] /= vertices[:, 2]
    vertices[:, 1] /= vertices[:, 2]

    # Draw the faces
    for i, face in enumerate(faces):
        face_vertices = vertices[face]
        face_color = colors[i]
        drawPolygon(face_vertices, face_color)





draw3D(vertices, faces, colors)

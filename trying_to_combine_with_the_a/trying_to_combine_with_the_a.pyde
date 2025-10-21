# Olympic Rings Animation with LA28 with stylised A

# Ring colours (RGB values)
ring_colors = [            # defintion of colours for ring
    color(0, 133, 199),    # Blue
    color(0, 0, 0),        # Black
    color(213, 0, 50),     # Red
    color(244, 195, 0),    # Yellow
    color(0, 159, 61)      # Green
]
# A colours (RGB values)
a_colors = [              # Defintion of colours for the A
   color(37, 150, 190) = light_blue,   # Light blue
   color(238, 165, 11) = dark_yellow,  # Dark yellow
   color(202, 0, 28) = dark_red        # Dark red
   ]
# Animation variables
current_ring = 0
ring_progress = 0
ring_speed = 4  # degrees per frame

# L animation variables
l_progress = 0
l_phase = 0  # 0 = vertical, 1 = horizontal, 2 = finished
l_speed = 4  # degrees per frame

# A offsets
a_offsets = [(-8, -8), (0, 0), (8, 8)]

# stroke coordinates of the A 
strokes = [
((500, 600), (380, 250)),     # Right leg
((380, 250), (300, 550)),     # left leg shorter
((294, 557), (600, 300))      # diagonal stroke of A
]
# Ring settings
ring_radius = 170
spacing = ring_radius * 1.1  # overlap factor like real logo

def setup():
    size(800, 800)  # Bigger canvas with room on top
    strokeWeight(20)
    noFill()
    frameRate(60)
    strokeCap(SQUARE)
    
    global l_x, l_y
    global positions, center_x, base_y
    
    center_x = width // 2
    base_y = height - 230  # push rings down with some margin

    positions = [
        (center_x - spacing, base_y),        # Blue
        (center_x, base_y),                  # Black
        (center_x + spacing, base_y),        # Red
        (center_x - spacing/2, base_y + spacing*0.55),  # Yellow
        (center_x + spacing/2, base_y + spacing*0.55)   # Green
    ]

    # L position (above rings)
    l_x = center_x - 150
    l_y = 100

def draw():
    global current_ring, progress, l_progress, l_phase
    global l_x, l_y, positions

    background(255)

    #  Animate the L 
    stroke(0)
    strokeWeight(40)

    if l_phase == 0:  # vertical line
        line(l_x, l_y, l_x, l_y + l_progress)
        l_progress += l_speed
        if l_progress >= 120:
            l_progress = 0
            l_phase = 1

    elif l_phase == 1:  # horizontal line
        line(l_x - 20, l_y + 120, l_x + l_progress, l_y + 120)
        l_progress += l_speed
        if l_progress >= 90:
            l_progress = 0
            l_phase = 2

    elif l_phase == 2:
        # Fully draw L
        line(l_x, l_y, l_x, l_y + 120)
        line(l_x - 20, l_y + 120, l_x + 90, l_y + 120)

#  Animate the rings 
        strokeWeight(10)
        # Draw completed rings
        for i in range(current_ring):
            stroke(ring_colors[i])
            ellipse(positions[i][0], positions[i][1], ring_radius, ring_radius)

        # Animate current ring
        if current_ring < len(ring_colors):
            stroke(ring_colors[current_ring])
            arc(positions[current_ring][0], positions[current_ring][1],
                ring_radius, ring_radius, 0, radians(progress))

            progress += speed
            if progress >= 360:
                progress = 0
                current_ring += 1
        else:
            # Reset for infinite loop
            current_ring = 0
            progress = 0
            l_phase = 0

# Olympic Rings + L + A Animation (Processing.py)
# Sequence: L → A → Rings → repeat


# --- COLORS AND STYLES ---

# Define colors for the Olympic rings in RGB format
ring_colors = [
    color(0, 133, 199),    # Blue
    color(0, 0, 0),        # Black
    color(213, 0, 50),     # Red
    color(244, 195, 0),    # Yellow
    color(0, 159, 61)      # Green
]

# Define three offset colors for the "A" — this creates a multicolored 3D-like effect
a_colors = [
    color(37, 150, 190),   # Light blue
    color(238, 165, 11),   # Dark yellow
    color(202, 0, 28)      # Dark red
]

# Each color layer of the "A" will be slightly offset to give a shadow or layered effect
offsets = [(-8, -8), (0, 0), (8, 8)]


# --- ANIMATION VARIABLES ---

# Controls which part of the animation is currently running
# 0 = drawing "L", 1 = drawing "A", 2 = drawing Olympic rings
phase = 0

# L animation progress and control variables
l_progress = 0   # How far along the L is drawn
l_phase = 0      # Whether we’re drawing the vertical (0) or horizontal (1) part
l_speed = 6      # Speed of line growth

# A animation variables
a_progress = 0   # Progress of the current A stroke
a_line = 0       # Which stroke (line segment) we’re currently drawing
a_speed = 0.02   # Speed of A line drawing
a_pause = 0      # Short pause after A finishes

# Rings animation variables
ring_index = 0     # Which ring is currently being drawn
ring_progress = 0  # How much of that ring’s circle is drawn
ring_speed = 2     # Speed of ring arc growth


# --- SETUP FUNCTION ---
# This runs once at the start
def setup():
    global l_x, l_y, a_strokes, ring_positions, ring_radius, center_x, base_y
    
    size(1000, 900)         # Set the canvas to 900x800 pixels
    background(255)        # White background
    frameRate(60)          # 60 frames per second (smooth animation)
    strokeCap(SQUARE)      # Line ends are square instead of round
    strokeWeight(20)       # Default line thickness
    noFill()               # Shapes (like ellipses) will be outlined only

    # --- "L" POSITION ---
    # These coordinates control where the "L" sits on the canvas
    # It’s placed on the left and slightly below the top edge
    l_x = width // 2 - 220
    l_y = 150

    # --- "A" STROKES ---
    # Each pair of points ((x1, y1), (x2, y2)) represents one stroke (a line segment)
    # This makes up an asymmetrical "A" shape
    a_strokes = [
        ((660, 360), (580, 50)),   # Right leg (bottom to top)
        ((580, 50), (520, 300)),   # Left leg (top to bottom)
        ((504, 315), (800, 100))    # Crossbar
    ]

    # --- OLYMPIC RINGS POSITIONS ---
    # Define the center points for each of the five rings
    ring_radius = 170
    spacing = ring_radius * 1.1     # Space between rings
    center_x = width // 2
    base_y = height - 420           # Rings sit near the bottom

    ring_positions = [
        (center_x - spacing, base_y),        # Blue
        (center_x, base_y),                  # Black
        (center_x + spacing, base_y),        # Red
        (center_x - spacing/2, base_y + spacing*0.55),  # Yellow (below left)
        (center_x + spacing/2, base_y + spacing*0.55)   # Green (below right)
    ]


# --- DRAW FUNCTION ---
# Runs continuously 60 times per second, refreshing the canvas
def draw():
    global phase, l_progress, l_phase, a_progress, a_line, a_pause
    global ring_index, ring_progress

    background(255)  # Clear screen each frame (white background)
    
    # --- DRAW "L" ---
    stroke(0)        # Black color for L
    strokeWeight(50) # Thick lines for the L
    
    if l_phase == 0:
        # Draw the vertical part of the L
        line(l_x, l_y - 80, l_x, l_y + l_progress)
        l_progress += l_speed
        if l_progress >= 200:   # Once full height reached, move to next phase
            l_progress = 0
            l_phase = 1

    elif l_phase == 1:
        # Draw full vertical + partial horizontal base
        line(l_x, l_y - 80, l_x, l_y + 200)
        line(l_x - 25, l_y + 180, l_x - 25 + l_progress, l_y + 180)
        l_progress += l_speed
        if l_progress >= 180:
            l_phase = 2  # L finished drawing

    else:
        # Draw full "L" (so it stays visible)
        line(l_x, l_y - 80, l_x, l_y + 200)
        line(l_x - 25, l_y + 180, l_x + 180, l_y + 180)

    # Once L done, move to A
    if phase == 0 and l_phase == 2:
        phase = 1


    # --- DRAW "A" ---
    if phase >= 1:
        strokeWeight(20)
        # Draw all completed lines so far
        for i in range(a_line):
            draw_a_line(a_strokes[i], 1)
        
        # Draw next line progressively
        if a_line < len(a_strokes):
            draw_a_line(a_strokes[a_line], a_progress)
            a_progress += a_speed
            if a_progress >= 1:
                a_progress = 0
                a_line += 1
        elif phase == 1:
            # Add short pause before rings start
            a_pause += 1
            if a_pause > 30:
                phase = 2


    # --- DRAW OLYMPIC RINGS ---
    if phase >= 2:
        strokeWeight(10)
        # Draw all completed rings
        for i in range(ring_index):
            stroke(ring_colors[i])
            ellipse(ring_positions[i][0], ring_positions[i][1], ring_radius, ring_radius)

        # Animate next ring (arc that grows)
        if ring_index < len(ring_colors):
            stroke(ring_colors[ring_index])
            arc(ring_positions[ring_index][0], ring_positions[ring_index][1],
                ring_radius, ring_radius, 0, radians(ring_progress))
            ring_progress += ring_speed
            if ring_progress >= 360:
                ring_progress = 0
                ring_index += 1
        else:
            # Once all rings done, start over
            reset_animation()


# --- DRAW A SINGLE "A" LINE WITH COLOR OFFSETS ---
def draw_a_line(line_coords, prog):
    (x1, y1), (x2, y2) = line_coords
    # Interpolate current drawing point (so it draws gradually)
    x = x1 + (x2 - x1) * prog
    y = y1 + (y2 - y1) * prog
    
    # Draw 3 color layers with slight offsets for stylized look
    for i in range(3):
        ox, oy = offsets[i]
        stroke(a_colors[i])
        line(x1 + ox, y1 + oy, x + ox, y + oy)


# --- RESET FUNCTION ---
# Resets all progress to restart the animation loop
def reset_animation():
    global phase, l_phase, l_progress, a_progress, a_line, a_pause, ring_index, ring_progress
    phase = 0
    l_phase = 0
    l_progress = 0
    a_progress = 0
    a_line = 0
    a_pause = 0
    ring_index = 0
    ring_progress = 0

import tkinter as tk
import AppKit

# Function to create tkinter window and canvas
def create_canvas(x, y, width, height):
    root = tk.Tk()
    root.geometry(f"{int(width)}x{int(height)}+{int(x)}+{int(y)}")  # Cast values to integers
    root.attributes('-alpha', 0.5)  # Adjust transparency level
    canvas = tk.Canvas(root, width=width, height=height, bg="black")
    canvas.pack(fill="both", expand=True)
    return root, canvas

# Run on macOS
if __name__ == "__main__":
    main_screen, extended_screen = None, None
    screens = AppKit.NSScreen.screens()
    print(screens)

    for screen in screens:
        if screen.frame().origin == AppKit.NSScreen.mainScreen().frame().origin:
            main_screen = screen
            main_origin = screen.frame().origin
        else:
            extended_screen = screen
            break  # Only one extended screen expected
    main_resolution = main_screen.frame().size
    extended_resolution = extended_screen.frame().size

    print(f"Main screen resolution: {main_resolution}")
    print(f"Extended screen resolution: {extended_resolution}")
    roots = []

    # Create and position canvases on each monitor
    for screen_index, screen in enumerate(screens):
        frame = screen.frame()  # Get monitor bounds
        x, y, width, height = frame.origin.x, frame.origin.y, frame.size.width, frame.size.height
        if screen_index == 0 or extended_screen is None:  # Main monitor or single monitor case
        # Use frame for positioning and dimensions
            root, canvas = create_canvas(x, y, width, height)
        else:  # Extended monitor
        # Use extended_screen.frame() for positioning and dimensions
            if extended_screen.frame().origin.y < main_screen.frame().origin.y:
            # Extended monitor lower
                canvas_y = extended_screen.frame().origin.y

            else:
                # Extended monitor higher
                canvas_y = extended_screen.frame().origin.y - extended_screen.frame().size.height
            frame = extended_screen.frame()
            x, y, width, height = frame.origin.x, frame.origin.y, frame.size.width, frame.size.height
            root, canvas = create_canvas(x, canvas_y, width, height)
        roots.append(root)

    # Start Tkinter event loop for all windows
    for root in roots:
        root.mainloop()

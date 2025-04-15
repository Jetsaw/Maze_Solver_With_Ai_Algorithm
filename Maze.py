import tkinter as tk
from tkinter import messagebox
import time
from maze2graph import maze2graph  # Import maze2graph function
from searches import dfs, bfs  # Import bfs and dfs functions

# Global variables for storing paths
bfs_path = []
dfs_path = []

# Function to clear the previous path highlights
def clear_path(maze: list[str]):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            maze_frame.grid_slaves(row=r, column=c)[0].config(bg='white')  # Reset background color

# Function to visualize the path
def visualize_path(path: list[int], maze: list[str], color: str):
    clear_path(maze)  # Clear previous path before visualizing the new one
    for idx in path:
        r, c = divmod(idx, len(maze[0]))
        maze_frame.grid_slaves(row=r, column=c)[0].config(bg=color)  # Highlight the path
        root.update()  # Update the GUI
        time.sleep(0.4)  # Pause for half a second to visualize the step

# Run BFS and DFS
def run_algorithms():
    global bfs_path, dfs_path  # Access global paths
    try:
        rows = int(row_entry.get())
        cols = int(col_entry.get())
        if rows < 5 or rows > 10 or cols < 5 or cols > 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter row and column sizes between 5 and 10.")
        return
    
    # Get user input for the maze
    maze = []
    for r in range(rows):
        row = ''.join([entry_vars[r][c].get() for c in range(cols)])
        maze.append(row)
    
    # Convert maze to graph
    graph, start, goal = maze2graph(maze)
    
    if start is None or goal is None:
        messagebox.showerror("Error", "Maze must have one start '@' and one goal '*'.")
        return
    
    # Run BFS
    start_time = time.time()
    bfs_path = bfs(graph, start, goal)
    bfs_time = time.time() - start_time

    # Run DFS
    start_time = time.time()
    dfs_path = dfs(graph, start, goal)
    dfs_time = time.time() - start_time

    # Prepare the output
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Maze size: {rows}x{cols}\n\n")
    result_text.insert(tk.END, "Maze:\n" + "\n".join(maze) + "\n\n")
    result_text.insert(tk.END, f"Labeled Maze:\n")
    for i in range(rows):
        result_text.insert(tk.END, " ".join(str(i * cols + j) for j in range(cols)) + "\n")
    result_text.insert(tk.END, f"Start: {start}, End: {goal}\n\n")
    
    # Display graph
    result_text.insert(tk.END, "Graph Representation:\n")
    for key, value in graph.items():
        result_text.insert(tk.END, f"{key}: {value}\n")

    # Display BFS path and time
    result_text.insert(tk.END, f"\nBFS Path: {bfs_path}\n")
    result_text.insert(tk.END, f"BFS Execution Time: {bfs_time:.2f} miliseconds\n")

    # Display DFS path and time
    result_text.insert(tk.END, f"\nDFS Path: {dfs_path}\n")
    result_text.insert(tk.END, f"DFS Execution Time: {dfs_time:.2f} seconds\n")

# Dynamically generate maze table
def generate_maze_table():
    try:
        rows = int(row_entry.get())
        cols = int(col_entry.get())
        if rows < 5 or rows > 10 or cols < 5 or cols > 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter row and column sizes between 5 and 10.")
        return
    
    # Clear previous table
    for widget in maze_frame.winfo_children():
        widget.destroy()

    # Generate new table
    global entry_vars
    entry_vars = [[tk.StringVar() for _ in range(cols)] for _ in range(rows)]
    
    # Create input boxes and add key bindings
    for r in range(rows):
        for c in range(cols):
            entry = tk.Entry(maze_frame, textvariable=entry_vars[r][c], width=2)
            entry.grid(row=r, column=c)
            entry.bind("<Return>", lambda e, row=r, col=c: focus_next_entry(row, col, rows, cols))

# Automatically focus on the next input box
def focus_next_entry(row, col, max_rows, max_cols):
    if col < max_cols - 1:
        maze_frame.grid_slaves(row=row, column=col+1)[0].focus_set()
    elif row < max_rows - 1:
        maze_frame.grid_slaves(row=row+1, column=0)[0].focus_set()
    else:
        # If it's the last input box, go back to the first one
        maze_frame.grid_slaves(row=0, column=0)[0].focus_set()

# Create GUI
root = tk.Tk()
root.title(" BFS vs DFS")

# Row input
tk.Label(root, text="Enter Rows ( 5 to 10 ):").pack(pady=5)
row_entry = tk.Entry(root)
row_entry.pack()

# Column input
tk.Label(root, text="Enter Columns ( 5 to 10 ):").pack(pady=5)
col_entry = tk.Entry(root)
col_entry.pack()

# Generate maze table button
generate_button = tk.Button(root, text="Generate Maze", command=generate_maze_table)
generate_button.pack(pady=10)

# Maze table frame
maze_frame = tk.Frame(root)
maze_frame.pack()

# Run button
run_button = tk.Button(root, text="Run Algorithms", command=run_algorithms)
run_button.pack(pady=10)

# Buttons to show paths
show_bfs_button = tk.Button(root, text="Show BFS Path", command=lambda: visualize_path(bfs_path, entry_vars, 'yellow'))
show_bfs_button.pack(pady=5)

show_dfs_button = tk.Button(root, text="Show DFS Path", command=lambda: visualize_path(dfs_path, entry_vars, 'red'))
show_dfs_button.pack(pady=5)

# Display results text box
result_text = tk.Text(root, height=20, width=50)
result_text.pack(pady=10)

# Start the GUI main loop
root.mainloop()

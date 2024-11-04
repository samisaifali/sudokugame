import tkinter as tk
import random

class SudokuGame:
    def __init__(self, root):
        """Initializes the game window and components."""
        self.root = root
        self.root.title("Sudoku Game")  # Set the window title

        # Initialize the Sudoku board with zeros 
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]  # Stores the original board 
        self.solution_board = [[0 for _ in range(9)] for _ in range(9)]  # Stores the solution for validation
        self.selected_cell = (0, 0)  # Track which cell the user selects

        # Difficulty and mistake tracking
        self.difficulty = None  # No difficulty set initially
        self.max_mistakes = 0  # Set default max mistakes
        self.mistakes = 0  # Tracks the number of mistakes made by the user

        # Display error messages
        self.error_message = tk.StringVar(value="Please choose a difficulty to start the game")  # Initial message
        self.error_label = tk.Label(root, textvariable=self.error_message, fg="red", font=("Arial", 12))
        self.error_label.grid(row=2, column=0)  # Position the error message 
        
        # Timer label and setup
        self.time_elapsed = 0  # Keeps track of time in seconds
        self.timer_label = tk.Label(root, text="Time: 00:00", font=("Arial", 12))
        self.timer_label.grid(row=3, column=0)  # Position the timer 

        # Start the timer
        self.update_timer()

        # Create an empty grid on launch
        self.create_grid()

        # Call function to create the control buttons
        self.create_buttons()

    def update_timer(self):
        """Updates the timer label every second."""
        if self.difficulty:  # Only run the timer if a difficulty has been selected
            minutes = self.time_elapsed // 60  # Calculate minutes
            seconds = self.time_elapsed % 60  # Calculate seconds
            self.timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")  # Update the timer label in MM:SS
            self.time_elapsed += 1  # Increment the time counter by 1 second
        self.root.after(1000, self.update_timer)  # Schedule this method to run again after 1 second

    def create_grid(self):
        """Creates the grid for the Sudoku game."""
        self.canvas = tk.Canvas(self.root, width=450, height=450)  # Create a canvas for the 9x9 grid 
        self.canvas.grid(row=0, column=0, padx=20, pady=20)  # Position the canvas
        self.canvas.bind("<Button-1>", self.cell_clicked)  # Bind left-click to select cells
        self.root.bind("<Key>", self.number_entered)  # Bind keyboard input for entering numbers

        # Draw the lines for the grid
        for i in range(10):
            width = 3 if i % 3 == 0 else 1  # Thicker lines for the 3x3 subgrids
            self.canvas.create_line(50 * i, 0, 50 * i, 450, width=width)  # Vertical lines
            self.canvas.create_line(0, 50 * i, 450, 50 * i, width=width)  # Horizontal lines

        self.draw_board()  # Draw the initial empty board

    def draw_board(self):
        """Draws the numbers on the Sudoku grid."""
        self.canvas.delete("numbers")  # Clear any existing numbers on the grid
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num != 0:  # Only draw non-zero numbers
                    x = col * 50 + 25  # X-coordinate of the cell's center
                    y = row * 50 + 25  # Y-coordinate of the cell's center
                    self.canvas.create_text(x, y, text=str(num), tags="numbers", font=("Arial", 18),
                                            fill="black" if self.original_board[row][col] != 0 else "blue")

    def cell_clicked(self, event):
        """Handles cell selection when the user clicks on the grid."""
        if self.difficulty:  # Ensure the difficulty is selected before allowing cell interaction
            x, y = event.x, event.y
            if x < 450 and y < 450:  # Ensure the click is within the grid bounds
                col, row = x // 50, y // 50  # Calculate the cell coordinates 
                self.selected_cell = (row, col)  # Update the selected cell
                self.highlight_selected_cell()
                self.error_message.set("")  # Clear any error messages when a new cell is selected

    def highlight_selected_cell(self):
        """Highlights the currently selected cell by drawing a red rectangle around it."""
        self.canvas.delete("highlight")  # Remove any previous highlights
        row, col = self.selected_cell
        x0, y0 = col * 50, row * 50
        x1, y1 = x0 + 50, y0 + 50
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="highlight")  # Draw the highlight

    def number_entered(self, event):
        """Handles keyboard input for entering numbers into the grid."""
        if self.difficulty:  # Ensure difficulty is selected before allowing number entry
            if event.char.isdigit() and event.char != '0':  # Only allow numbers between 1 and 9
                row, col = self.selected_cell
                if self.original_board[row][col] == 0:  # Only allow changes to non-original cells
                    entered_num = int(event.char)
                    if entered_num == self.solution_board[row][col]:  # If the number is correct
                        self.board[row][col] = entered_num
                        self.draw_board()  # Redraw the board with the updated number
                    else:
                        self.mistakes += 1  # Increment mistakes
                        if self.mistakes >= self.max_mistakes:  # Check if max mistakes exceeded
                            self.end_game()  # End the game
                        else:
                            self.error_message.set(f"Incorrect number! Mistakes: {self.mistakes}/{self.max_mistakes}")

    def create_buttons(self):
        """Creates the control buttons for the game (New Game, Solve, Difficulty)."""
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        # New game button
        new_game_button = tk.Button(button_frame, text="New Game", command=self.reset_game)
        new_game_button.grid(row=0, column=0, padx=10)

        # Difficulty selection buttons
        easy_button = tk.Button(button_frame, text="Easy", command=lambda: self.set_difficulty("easy"))
        easy_button.grid(row=0, column=2, padx=10)

        medium_button = tk.Button(button_frame, text="Medium", command=lambda: self.set_difficulty("medium"))
        medium_button.grid(row=0, column=3, padx=10)

        hard_button = tk.Button(button_frame, text="Hard", command=lambda: self.set_difficulty("hard"))
        hard_button.grid(row=0, column=4, padx=10)

    def reset_game(self):
        """Resets the game and prompts the user to select a new difficulty."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]  # Reset the board
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]  # Reset the original board
        self.solution_board = [[0 for _ in range(9)] for _ in range(9)]  # Reset the solution board
        self.selected_cell = (0, 0)  # Reset the selected cell
        self.mistakes = 0  # Reset mistakes
        self.difficulty = None  # Clear difficulty
        self.error_message.set("Please choose a difficulty to start the game")  # Prompt for difficulty selection
        self.draw_board()  # Redraw the empty board
        self.time_elapsed = 0  # Reset the timer
        self.root.bind("<Key>", self.number_entered)  # Re-enable number input

    def set_difficulty(self, difficulty):
        """Sets the difficulty level, adjusts the max mistakes, and starts the game."""
        self.difficulty = difficulty
        if difficulty == "easy":
            self.max_mistakes = 5
        elif difficulty == "medium":
            self.max_mistakes = 3
        else:
            self.max_mistakes = 1
        self.mistakes = 0  # Reset mistakes for new game
        self.error_message.set(f"Difficulty set to {difficulty.capitalize()}")
        self.root.bind("<Key>", self.number_entered)  # Ensure number entry is re-enabled

        # Create the Sudoku board and start the game once difficulty is selected
        self.create_random_sudoku()

    def end_game(self):
        """Ends the game if the user exceeds the allowed number of mistakes."""
        mistake_word = "mistake" if self.mistakes == 1 else "mistakes"
        self.error_message.set(f"Game Over! You made {self.mistakes} {mistake_word}. Press 'New Game' to try again.")
        self.root.unbind("<Key>")  # Disable further input

    def create_random_sudoku(self, difficulty="medium"):
        """Generates a random Sudoku puzzle and resets the timer."""
        self.board = [[0 for _ in range(9)]]  # Reset the board
        self.generate_full_sudoku()  # Generate a full solution
        self.solution_board = [row[:] for row in self.board]  # Store the solution
        self.remove_cells(difficulty)  # Remove cells to create the puzzle
        self.original_board = [row[:] for row in self.board]  # Store the original board (unsolved)
        self.time_elapsed = 0  # Reset the timer
        self.mistakes = 0  # Reset mistakes
        self.draw_board()  # Draw the initial board after difficulty selection

    def generate_full_sudoku(self):
        """Generates a complete, valid Sudoku solution."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            self.fill_diagonal_boxes(i)  # Fill the 3x3 diagonal boxes first
        self.solve_sudoku()  # Solve the rest of the board

    def fill_diagonal_boxes(self, start):
        """Fills the diagonal boxes with random numbers."""
        nums = random.sample(range(1, 10), 9)  # Randomly sample numbers 1-9
        for i in range(3):
            for j in range(3):
                self.board[start + i][start + j] = nums[i * 3 + j]

    def is_safe(self, row, col, num):
        """Checks if its safe to place a number in a given cell."""
        # Check the row and column
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        # Check the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self):
        """Uses backtracking to solve the Sudoku puzzle."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:  # Find an empty cell
                    for num in range(1, 10):  # Try numbers 1-9
                        if self.is_safe(row, col, num):  # Check if placing the number is safe
                            self.board[row][col] = num  # Place the number
                            if self.solve_sudoku():  # Recursively try to solve the rest
                                return True
                            self.board[row][col] = 0  # Backtrack if no solution is found
                    return False  # If no number can be placed, return False
        return True  # If the board is solved, return True

    def remove_cells(self, difficulty="medium"):
        """Removes cells from the solved board to create the puzzle."""
        if difficulty == "easy":
            attempts = 40  # Fewer cells removed
        elif difficulty == "medium":
            attempts = 50  # More cells removed
        else:
            attempts = 60  # Most difficult

        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0  # Remove the number
                attempts -= 1

    def solve(self):
        """Fills the board with the correct solution."""
        self.board = [row[:] for row in self.solution_board]  # Fill the grid with the solution
        self.draw_board()  # Redraw the grid with the solution

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

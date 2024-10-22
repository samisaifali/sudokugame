import tkinter as tk
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_board = [[0 for _ in range(9)] for _ in range(9)]  # To store the solved board
        self.selected_cell = (0, 0)

        # Create an in-window label for error messages
        self.error_message = tk.StringVar()
        self.error_label = tk.Label(root, textvariable=self.error_message, fg="red", font=("Arial", 12))
        self.error_label.grid(row=2, column=0)

        # Create a timer label
        self.time_elapsed = 0  # Track time in seconds
        self.timer_label = tk.Label(root, text="Time: 00:00", font=("Arial", 12))
        self.timer_label.grid(row=3, column=0)

        # Start the timer
        self.update_timer()

        self.create_grid()
        self.create_buttons()
        self.create_random_sudoku()

    def update_timer(self):
        """Update the timer label every second."""
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
        self.time_elapsed += 1
        self.root.after(1000, self.update_timer)  # Call this function again after 1 second

    def create_grid(self):
        self.canvas = tk.Canvas(self.root, width=450, height=450)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.root.bind("<Key>", self.number_entered)

        # Draw the grid lines
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(50 * i, 0, 50 * i, 450, width=width)
            self.canvas.create_line(0, 50 * i, 450, 50 * i, width=width)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("numbers")
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num != 0:
                    x = col * 50 + 25
                    y = row * 50 + 25
                    self.canvas.create_text(x, y, text=str(num), tags="numbers", font=("Arial", 18),
                                            fill="black" if self.original_board[row][col] != 0 else "blue")

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if x < 450 and y < 450:
            col, row = x // 50, y // 50
            self.selected_cell = (row, col)
            self.highlight_selected_cell()
            # Clear error message when a new cell is selected
            self.error_message.set("")

    def highlight_selected_cell(self):
        self.canvas.delete("highlight")
        row, col = self.selected_cell
        x0, y0 = col * 50, row * 50
        x1, y1 = x0 + 50, y0 + 50
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="highlight")

    def number_entered(self, event):
        """Handles the keypress event when a number is entered."""
        if event.char.isdigit() and event.char != '0':  # Ensure number is 1-9
            row, col = self.selected_cell
            if self.original_board[row][col] == 0:  # Only allow changing non-original numbers
                entered_num = int(event.char)
                if entered_num == self.solution_board[row][col]:  # Correct number
                    self.board[row][col] = entered_num
                    self.draw_board()
                else:
                    self.error_message.set("Incorrect number! Try again.")  # Show error in label

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        new_game_button = tk.Button(button_frame, text="New Game", command=self.create_random_sudoku)
        new_game_button.grid(row=0, column=0, padx=10)

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve)
        solve_button.grid(row=0, column=1, padx=10)

    def create_random_sudoku(self, difficulty="medium"):
        self.board = [[0 for _ in range(9)]]
        self.generate_full_sudoku()
        self.solution_board = [row[:] for row in self.board]  # Store the solution
        self.remove_cells(difficulty)
        self.original_board = [row[:] for row in self.board]
        self.time_elapsed = 0  # Reset timer when new game starts
        self.draw_board()

    def generate_full_sudoku(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            self.fill_diagonal_boxes(i)
        self.solve_sudoku()

    def fill_diagonal_boxes(self, start):
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                self.board[start + i][start + j] = nums[i * 3 + j]

    def is_safe(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_safe(row, col, num):
                            self.board[row][col] = num
                            if self.solve_sudoku():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def remove_cells(self, difficulty="medium"):
        if difficulty == "easy":
            attempts = 40
        elif difficulty == "medium":
            attempts = 50
        else:
            attempts = 60
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                attempts -= 1

    def solve(self):
        self.board = [row[:] for row in self.solution_board]  # Fill the grid with the solution
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

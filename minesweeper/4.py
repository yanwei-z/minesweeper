import tkinter as tk
import random


class Minesweeper:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        #创建列表，存储棋盘状态：
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        #创建列表，存储按钮对象
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        #创建集合，存储雷的位置：
        self.mines_position = set()
        #初始化旗帜的数量：
        self.flags = set()
        self.flag_count = 0
        self.game_over = False
        self.time = 0
        self.timer_running = False
        self.time_label = None
        self.game_over_label = None

        self.create_board()
        self.place_mines()
        self.calculate_numbers()

    # 创建棋盘
    def create_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.root, text='', width=3, height=1, command=lambda r=r, c=c: self.reveal(r, c))
                button.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button

        # 创建剩余旗帜数量标签
        self.flag_label = tk.Label(self.root, text=f'Flags: {self.mines - self.flag_count}')
        self.flag_label.grid(row=self.rows, column=0, columnspan=self.cols, sticky='w')

        # 创建计时器标签
        self.time_label = tk.Label(self.root, text=f"Time: {self.time}s")
        self.time_label.grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky='w')

        # 创建重置按钮
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=self.rows + 2, column=0, columnspan=self.cols)

    # 放置雷
    def place_mines(self):
        while len(self.mines_position) < self.mines:
            position = random.randint(0, self.rows * self.cols - 1)
            r, c = divmod(position, self.cols)
            if (r, c) not in self.mines_position:
                self.mines_position.add((r, c))

    # 计算数字
    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mines_position:
                    self.board[r][c] = -1
                else:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) in self.mines_position:
                                count += 1
                    self.board[r][c] = count

    # 揭示格子
    def reveal(self, r, c):
        if self.game_over or self.buttons[r][c]['state'] == 'disabled' or (r, c) in self.flags:
            return
        if (r, c) in self.mines_position:
            self.buttons[r][c].config(text='*', bg='red')
            self.game_over = True
            self.show_all_mines()
            self.show_game_over()
            self.stop_timer()
        else:
            self.reveal_cell(r, c)

    def reveal_cell(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols) or self.buttons[r][c]['state'] == 'disabled':
            return
        self.buttons[r][c].config(state='disabled', text=str(self.board[r][c]) if self.board[r][c] != 0 else '')
        if self.board[r][c] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.reveal_cell(r + dr, c + dc)

    # 切换旗帜
    def toggle_flag(self, r, c):
        if self.game_over or self.buttons[r][c]['state'] == 'disabled':
            return
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.buttons[r][c].config(text='')
            self.flag_count -= 1
        elif self.flag_count < self.mines:
            self.flags.add((r, c))
            self.buttons[r][c].config(text='F', fg='blue')
            self.flag_count += 1
        self.flag_label.config(text=f'Flags: {self.mines - self.flag_count}')

    # 显示所有雷
    def show_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mines_position:
                    self.buttons[r][c].config(text='*', bg='red')

    def show_game_over(self):
        if not self.game_over_label:
            self.game_over_label = tk.Label(self.root, text="Game Over", fg="red", font=("Arial", 40, "bold"))
            self.game_over_label.place(relx=0.5, rely=0.5, anchor='center')

    # 启动计时器
    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    # 更新计时器
    def update_timer(self):
        if self.timer_running:
            self.time += 1
            self.time_label.config(text=f"Time: {self.time}s")
            self.root.after(1000, self.update_timer)

    # 停止计时器
    def stop_timer(self):
        self.timer_running = False

    # 重置游戏
    def reset_game(self):
        self.root.quit()
        self.root.destroy()
        self.start_game()

    def start_game(self):
        self.game_over = False
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines_position.clear()
        self.flags.clear()
        self.flag_count = 0
        self.time = 0
        self.timer_running = False
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.create_board()
        self.place_mines()
        self.calculate_numbers()
        self.start_timer()
        self.root.mainloop()


# 游戏设置
def start_game(difficulty):
    if difficulty == "easy":
        rows, cols, mines = 10, 10, 15
    elif difficulty == "medium":
        rows, cols, mines = 16, 16, 40
    else:
        rows, cols, mines = 24, 24, 99

    root = tk.Tk()
    game = Minesweeper(root, rows, cols, mines)
    root.title(f"Minesweeper - {difficulty.capitalize()} Mode")
    game.start_timer()
    root.mainloop()


# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")

    tk.Button(root, text="Easy Mode", command=lambda: start_game("easy")).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(root, text="Medium Mode", command=lambda: start_game("medium")).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(root, text="Hard Mode", command=lambda: start_game("hard")).grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()

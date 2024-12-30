import json,os,sys,random
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ModuleNotFoundError:
    os.system("pip install pyqt5")
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tic Tac Toe")
        self.setStyleSheet("background-color: green;")
        self.load_knowledge_base()
        self.i=0
        self.UiComponents()
        self.f = False
        self.showFullScreen()

    def UiComponents(self):
        self.turn = 0
        self.times = 0

        self.create_welcome_label()
        self.create_push_buttons()
        self.create_score_label()
        self.create_reset_game_button()
        self.create_exit_game_button()
        self.create_line_button()
        self.create_ai_game_button()
        self.create_2player_game_button()

    def create_welcome_label(self):
        self.welcome = QLabel("Welcome to \nTic Tac Toe", self)
        self.welcome.setGeometry(700, 65, 620, 200)
        self.welcome.setStyleSheet("QLabel {border: 6px solid black; background: red;}")
        self.welcome.setAlignment(Qt.AlignCenter)
        self.welcome.setFont(QFont('Times', 56))
    def create_push_buttons(self):
        self.push_list = []
        x, y = 180, 165

        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = QPushButton(self)
                button.setGeometry(x * i + 85, y * j + 85, 180, 165)
                button.setFont(QFont(QFont('Times', 48)))
                button.setStyleSheet("background-color: red; color: blue; border: 4px solid black;")
                button.clicked.connect(self.action_called)
                row_buttons.append(button)

            self.push_list.append(row_buttons)


    def create_score_label(self):
        self.label = QLabel(self)
        self.label.setGeometry(115, 620, 500, 105)
        self.label.setStyleSheet("QLabel {border: 6px solid black; background: yellow;}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Times', 32))
        self.label.setText("Player 1")

    def create_reset_game_button(self):
        reset_game = self.create_button("Reset-Game", 1000, 320)
        reset_game.clicked.connect(self.reset_game_action)

    def create_exit_game_button(self):
        exit_game = self.create_button("Exit-Game", 1000, 520)
        exit_game.clicked.connect(self.exit_game_action)
    def create_ai_game_button(self):
        self.ai_game = self.create_button("ai game", 700, 320)
        self.ai_game.clicked.connect(self.ai_game_action)
        self.ai_game.hide()
    def create_2player_game_button(self):
        self.player_game = self.create_button("2 player game", 700, 320)
        self.player_game.clicked.connect(self.two_player_game)

    def create_line_button(self):
        line = self.create_button("Show Engine", 700, 520)
        line.clicked.connect(self.line_action)


    def create_button(self, text, x, y):
        button = QPushButton(text, self)
        button.setGeometry(x, y, 250, 150)
        button.setFont(QFont('Times', 28))
        self.color_list="aqua HotPink chocolate yellow blue red purple orange".split()
        self.color=random.sample(self.color_list,5)
        button.setStyleSheet(f"background: {self.color[self.i]}; border: 5px solid black;")
        self.i+=1
        return button
    def ai_game_action(self):
        for i in range(3):
            for j in range(3):
                (self.push_list[i][j]).clicked.connect(self.action_called)
    def two_player_game(self):
        for i in range(3):
            for j in range(3):
                (self.push_list[i][j]).clicked.connect(self.action_called)
        
    def line_action(self):
        i,j=self.best_move()
        if i==-1 and j==-1:
            self.label.setText("on playing best moves match is draw")
        else:
            self.label.setFont(QFont('Times', 24))
        
            self.label.setText(f"the {(i)*3+j+1}th button is the best move.")
    def reset_game_action(self):
        self.turn = 0
        self.times = 0
        self.label.setText("Player 1")

        for buttons in self.push_list:
            for button in buttons:
                button.setEnabled(True)
                button.setText("")

    def exit_game_action(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Do you want to exit")
        msg.setWindowTitle("Exit Window Confirmation")
        msg.setStyleSheet("background: aqua;")
        msg.setFont(QFont('Times', 24))

        yes_button = msg.addButton(QMessageBox.Yes)
        yes_button.setFont(QFont('Times', 24))
        no_button = msg.addButton(QMessageBox.No)
        no_button.setFont(QFont('Times', 24))
        yes_button.clicked.connect(self.on_yes_clicked)
        msg.exec_()

    def on_yes_clicked(self):
        self.save_knowledge_base()
        exit()

    def save_knowledge_base(self):
        with open('record.json', 'w') as file:
            json.dump(self.knowledge_base, file)

    def train(self, user_won):
        self.knowledge_base[user_won] += 1

    def load_knowledge_base(self):
        try:
            with open(r'record.json', 'r') as file:
                self.knowledge_base = json.load(file)
        except FileNotFoundError:
            self.knowledge_base = {'X': 0, 'O': 0, 'D': 0}

    def won_game_action(self, text):
        winmsg = QMessageBox()
        winmsg.setIcon(QMessageBox.Warning)
        winmsg.setText(f"{text}\nThe Player has won: {self.knowledge_base['X']} Games\n"
                       f"The Computer has won: {self.knowledge_base['O']} Games\n"
                       f"The Computer has tied: {self.knowledge_base['D']} Games")
        winmsg.setWindowTitle("Winner Window Stats")
        winmsg.setStyleSheet("background: aqua;")
        winmsg.setFont(QFont('Times', 24))

        yes_button = winmsg.addButton(QMessageBox.Ok)
        yes_button.setFont(QFont('Times', 24))

        winmsg.exec_()

    def action_called(self):
        if self.times < 9 and not self.check_winner():
            self.times += 1
            button = self.sender()
            button.setEnabled(False)
            text = 'Player 1' if self.turn == 0 else 'AI'
            if self.turn == 0:
                button.setText("X")
                self.turn = 1
                win = self.check_winner()
                if win is False:
                    self.ai_move(True)
                    
                    self.turn = 0
            else:
                button.setText("O")
                

            win = self.check_winner()

            if win:
                if self.turn == 0:
                    text = "AI has Won"
                    self.train('O')
                else:
                    text = "Player has Won"
                    self.train('X')

                for buttons in self.push_list:
                    for push in buttons:
                        push.setEnabled(False)

                self.won_game_action(text)

            elif self.times == 9:
                text = "Match is Draw"
                self.train('D')
                self.won_game_action(text)

            if text != '':
                self.label.setText(text)
    def best_move(self, depth=9):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.push_list[i][j].text() == "":
                # Try placing the AI's symbol in the empty spot
                    self.push_list[i][j].setText("O")

                # Calculate the score for this move using the minimax algorithm with alpha-beta pruning and depth limit
                    score = self.minimax(False, float('-inf'), float('inf'), depth - 1,False)

                # Undo the move
                    self.push_list[i][j].setText("")

                # Update the best move if the current move has a higher score
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move==None:
            best_move=(-1,-1)     
        print(best_move)
        return best_move
    def ai_move(self,flag=False, depth=3):
        best_score = float('-inf')
        best_move = None

    # First, check for winning moves
        for i in range(3):
            for j in range(3):
                if self.push_list[i][j].text() == "":
                # Try placing the AI's symbol in the empty spot
                    self.push_list[i][j].setText("O")

                # Check if this move results in a win
                    if self.check_winner()==True:
                        if flag:
                            self.push_list[i][j].clicked.emit()
                        else:
                            self.push_list[i][j].setText("")
                            return i,j
                # Undo the move
                    self.push_list[i][j].setText("")

    # If no winning move, then check for blocking the player's winning move
        for i in range(3):
            for j in range(3):
                if self.push_list[i][j].text() == "":
                # Try placing the player's symbol in the empty spot
                    self.push_list[i][j].setText("X")

                # Check if this move blocks the player's win
                    if self.check_winner()==True:
                        if flag:
                            self.push_list[i][j].clicked.emit()
                        else:
                            self.push_list[i][j].setText("")
                            return i, j

                # Undo the move
                    self.push_list[i][j].setText("")

    # If no winning or blocking move, use the minimax algorithm
        for i in range(3):
            for j in range(3):
                if self.push_list[i][j].text() == "":
                # Try placing the AI's symbol in the empty spot
                    self.push_list[i][j].setText("O")

                # Calculate the score for this move using the minimax algorithm with alpha-beta pruning and depth limit
                    score = self.minimax(False, float('-inf'), float('inf'), depth - 1)

                # Undo the move
                    self.push_list[i][j].setText("")

                # Update the best move if the current move has a higher score
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        

    # Continue with your code
        if best_move:
            i, j = best_move
            if flag:
                self.push_list[i][j].clicked.emit()
            else:
                return i, j
    def minimax(self, is_maximizing, alpha, beta, depth,turn=True):
        result = self.check_winner()
        if result is not None or depth == 0:
            return self.evaluate_board()

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.push_list[i][j].text() == "":
                        self.push_list[i][j].setText(turn)
                        score = self.minimax(False, alpha, beta, depth - 1)
                        self.push_list[i][j].setText("")
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.push_list[i][j].text() == "":
                        self.push_list[i][j].setText(not(turn))
                        score = self.minimax(True, alpha, beta, depth - 1)
                        self.push_list[i][j].setText("")
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def evaluate_board(self):
        score = 0

        for line in self.push_list:
            score += self.evaluate_line(line[0].text(), line[1].text(), line[2].text())

        for j in range(3):
            column = [self.push_list[i][j].text() for i in range(3)]
            score += self.evaluate_line(column[0], column[1], column[2])

        diagonal1 = [self.push_list[i][i].text() for i in range(3)]
        diagonal2 = [self.push_list[i][2 - i].text() for i in range(3)]
        score += self.evaluate_line(diagonal1[0], diagonal1[1], diagonal1[2])
        score += self.evaluate_line(diagonal2[0], diagonal2[1], diagonal2[2])

        if self.f:
            score += 4

        center_value = self.push_list[1][1].text()
        if center_value == "O":
            score += 2
        elif center_value == "X" and not self.f:
            score -= 2

        return score

    def evaluate_line(self, cell1, cell2, cell3):
        ai_symbol, player_symbol, empty_symbol = "O", "X", ""

        if cell1 == cell2 == cell3 == ai_symbol:
            self.f = True
            return 5
        elif cell1 == cell2 == cell3 == player_symbol:
            self.f = True
            return -5
        elif (cell1 == cell2 == ai_symbol and cell3 == empty_symbol) or \
                (cell1 == cell3 == ai_symbol and cell2 == empty_symbol) or \
                (cell2 == cell3 == ai_symbol and cell1 == empty_symbol):
            self.f = True
            return 10
        elif (cell1 == cell2 == player_symbol and cell3 == empty_symbol) or \
                (cell1 == cell3 == player_symbol and cell2 == empty_symbol) or \
                (cell2 == cell3 == player_symbol and cell1 == empty_symbol):
            self.f = True
            return -10

        return 0

    def check_winner(self):
        for i in range(3):
            if self.push_list[0][i].text() == self.push_list[1][i].text() == self.push_list[2][i].text() != "":
                return True

        for i in range(3):
            if self.push_list[i][0].text() == self.push_list[i][1].text() == self.push_list[i][2].text() != "":
                return True

        if self.push_list[0][0].text() == self.push_list[1][1].text() == self.push_list[2][2].text() != "":
            return True

        if self.push_list[0][2].text() == self.push_list[1][1].text() == self.push_list[2][0].text() != "":
            return True

        return False

App = QApplication(sys.argv)
window = Window()
App.exec()
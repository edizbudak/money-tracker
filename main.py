import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QProgressBar, QComboBox
)
from PyQt5.QtCore import Qt


class MoneyTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoneyTracker - Simple Goal Saver")
        self.resize(450, 600) 
        
        self.setObjectName("MainWindow")
        self.setStyleSheet("""
            #MainWindow {
                background-color: #d7ccc8;
            }
            QLabel {
                color: #3e2723;
                font-weight: bold;
            }
        """)

        self.target_money = 0.0
        self.target_days = 1
        self.current_pool = 0.0
        self.currency_symbol = "₺"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("💰 MoneyTracker", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #3e2723; margin: 5px;")
        main_layout.addWidget(title)

        currency_layout = QHBoxLayout()
        currency_label = QLabel("Select Currency:", self)
        currency_label.setStyleSheet("font-size: 14px; color: #4e342e;")
        
        self.currency_box = QComboBox()
        self.currency_box.addItems(["TRY (₺)", "USD ($)", "EUR (€)", "GBP (£)"])
        self.currency_box.setStyleSheet("""
            QComboBox {
                background-color: #8d6e63;
                color: white;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
                border: 1px solid #5d4037;
            }
        """)
        self.currency_box.currentTextChanged.connect(self.change_currency)
        
        currency_layout.addWidget(currency_label)
        currency_layout.addWidget(self.currency_box)
        main_layout.addLayout(currency_layout)

        self.lbl_target_input = QLabel(f"Target Money ({self.currency_symbol}):")
        main_layout.addWidget(self.lbl_target_input)
        
        self.input_target = QLineEdit()
        self.input_target.setPlaceholderText("Enter target money (e.g., 5000)...")
        self.input_target.setStyleSheet("background-color: #f5f5f5; padding: 8px; border-radius: 5px; color: #3e2723; border: 1px solid #8d6e63;")
        main_layout.addWidget(self.input_target)

        lbl_days = QLabel("Target Days:")
        main_layout.addWidget(lbl_days)

        self.input_days = QLineEdit()
        self.input_days.setPlaceholderText("Enter target days (e.g., 30)...")
        self.input_days.setStyleSheet("background-color: #f5f5f5; padding: 8px; border-radius: 5px; color: #3e2723; border: 1px solid #8d6e63;")
        main_layout.addWidget(self.input_days)

        btn_calculate = QPushButton("Set Goal & Initialize")
        btn_calculate.setStyleSheet("""
            QPushButton {
                background-color: #3e2723; 
                color: #f5f5f5; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5d4037;
            }
        """)
        btn_calculate.clicked.connect(self.setup_goal)
        main_layout.addWidget(btn_calculate)

        self.lbl_daily_target = QLabel("Daily Target: Waiting for setup...", self)
        self.lbl_daily_target.setAlignment(Qt.AlignCenter)
        self.lbl_daily_target.setStyleSheet("font-size: 16px; color: #3e2723; font-weight: bold;")
        main_layout.addWidget(self.lbl_daily_target)

        self.lbl_pool_status = QLabel(f"Current Pool: 0.00 {self.currency_symbol} / 0.00 {self.currency_symbol}", self)
        self.lbl_pool_status.setAlignment(Qt.AlignCenter)
        self.lbl_pool_status.setStyleSheet("font-size: 18px; font-weight: bold; color: #3e2723;")
        main_layout.addWidget(self.lbl_pool_status)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3e2723;
                border-radius: 6px;
                text-align: center;
                background-color: rgba(245, 245, 245, 0.7);
                color: #3e2723;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #5d4037;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        self.lbl_status_message = QLabel("Set your goal to start saving! 💰", self)
        self.lbl_status_message.setAlignment(Qt.AlignCenter)
        self.lbl_status_message.setStyleSheet("color: #4e342e; font-style: italic; font-size: 14px;")
        main_layout.addWidget(self.lbl_status_message)
        action_layout = QHBoxLayout()
        
        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Amount...")
        self.input_amount.setStyleSheet("background-color: #f5f5f5; padding: 10px; border-radius: 5px; color: #3e2723; font-size: 16px; border: 1px solid #8d6e63;")
        action_layout.addWidget(self.input_amount)

        btn_add = QPushButton("Add Money")
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #6d4c41; 
                color: white; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8d6e63;
            }
        """)
        btn_add.clicked.connect(self.add_money)
        action_layout.addWidget(btn_add)

        btn_withdraw = QPushButton("Withdraw")
        btn_withdraw.setStyleSheet("""
            QPushButton {
                background-color: #4e342e; 
                color: white; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5d4037;
            }
        """)
        btn_withdraw.clicked.connect(self.withdraw_money)
        action_layout.addWidget(btn_withdraw)

        main_layout.addLayout(action_layout)
        self.setLayout(main_layout)

    def change_currency(self, text):
        if "₺" in text: self.currency_symbol = "₺"
        elif "$" in text: self.currency_symbol = "$"
        elif "€" in text: self.currency_symbol = "€"
        elif "£" in text: self.currency_symbol = "£"
        
        self.lbl_target_input.setText(f"Target Money ({self.currency_symbol}):")
        
        if self.target_money > 0:
            daily_needed = self.target_money / self.target_days
            self.lbl_daily_target.setText(f"🎯 Daily Saving Target: {daily_needed:.2f} {self.currency_symbol} / day")
        
        self.update_ui()

    def setup_goal(self):
        try:
            self.target_money = float(self.input_target.text())
            self.target_days = int(self.input_days.text())
            if self.target_days <= 0: self.target_days = 1
            
            daily_needed = self.target_money / self.target_days
            self.lbl_daily_target.setText(f"🎯 Daily Saving Target: {daily_needed:.2f} {self.currency_symbol} / day")
            self.update_ui()
        except ValueError:
            self.lbl_daily_target.setText("⚠️ Please enter valid numbers!")

    def add_money(self):
        try:
            amount = float(self.input_amount.text())
            if amount > 0:
                self.current_pool += amount
                self.input_amount.clear()
                self.update_ui()
        except ValueError:
            pass

    def withdraw_money(self):
        try:
            amount = float(self.input_amount.text())
            if amount > 0:
                self.current_pool -= amount
                if self.current_pool < 0: 
                    self.current_pool = 0
                self.input_amount.clear()
                self.update_ui()
        except ValueError:
            pass

    def update_ui(self):
        self.lbl_pool_status.setText(f"Current Pool: {self.current_pool:.2f} {self.currency_symbol} / {self.target_money:.2f} {self.currency_symbol}")
        
        if self.target_money > 0:
            percentage = int((self.current_pool / self.target_money) * 100)
            if percentage > 100: percentage = 100
            self.progress_bar.setValue(percentage)
        else:
            percentage = 0
            self.progress_bar.setValue(0)

        if percentage == 0:
            self.lbl_status_message.setText("Set your goal to start saving! 💰")
        elif percentage < 25:
            self.lbl_status_message.setText("Every journey starts with a single coin! 🚀")
        elif percentage < 75:
            self.lbl_status_message.setText("You are doing great! Keep it up! 👍")
        elif percentage < 100:
            self.lbl_status_message.setText("So close! Don't spend it on something stupid! 🔥")
        else:
            self.lbl_status_message.setText("You've officially reached your goal! 🎊")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = MoneyTracker()
    tracker.show()
    sys.exit(app.exec_())
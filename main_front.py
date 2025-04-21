import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
                            QLabel, QLineEdit, QPushButton, QFrame, QCheckBox, QListWidget,
                            QListWidgetItem, QTextEdit, QScrollArea, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal


class AuthWindow(QWidget):
    login_success = pyqtSignal(str)  # Сигнал об успешном входе

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        # self.setFixedSize(400, 600)
        self.setup_ui()

    def setup_ui(self):
        self.stacked_widget = QStackedWidget()
        
        # Создаем экраны
        self.login_screen = self.create_login_screen()
        self.register_screen = self.create_register_screen()
        
        # Добавляем экраны в stacked widget
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
    
    def create_login_screen(self):
        screen = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Логотип
        logo = QLabel()
        logo.setPixmap(QPixmap("logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        # Заголовок
        title = QLabel("Вход в аккаунт")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        # Поля ввода
        self.login_email = self.create_input("Email", QIcon("icons/email.png"))
        self.login_password = self.create_input("Пароль", QIcon("icons/lock.png"), is_password=True)
        
        # Кнопка входа
        login_btn = QPushButton("Войти")
        login_btn.setFont(QFont("Arial", 10, QFont.Bold))
        login_btn.setStyleSheet(self.get_button_style())
        login_btn.clicked.connect(self.attempt_login)
        
        # Ссылка на регистрацию
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignCenter)
        register_label = QLabel("Нет аккаунта?")
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setStyleSheet("border: none; color: #3498db;")
        register_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        register_layout.addWidget(register_label)
        register_layout.addWidget(register_btn)
        
        # Сборка экрана
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(self.login_email)
        layout.addWidget(self.login_password)
        layout.addWidget(login_btn)
        layout.addLayout(register_layout)
        
        screen.setLayout(layout)
        return screen
    
    def create_register_screen(self):
        screen = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Логотип
        logo = QLabel()
        logo.setPixmap(QPixmap("logo.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        # Заголовок
        title = QLabel("Регистрация")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        # Поля ввода
        self.reg_name = self.create_input("Имя", QIcon("icons/user.png"))
        self.reg_email = self.create_input("Email", QIcon("icons/email.png"))
        self.reg_password = self.create_input("Пароль", QIcon("icons/lock.png"), is_password=True)
        self.reg_confirm = self.create_input("Подтвердите пароль", QIcon("icons/lock.png"), is_password=True)
        
        # Чекбокс
        self.terms_check = QCheckBox("Я принимаю условия пользовательского соглашения")
        
        # Кнопка регистрации
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setFont(QFont("Arial", 10, QFont.Bold))
        register_btn.setStyleSheet(self.get_button_style())
        register_btn.clicked.connect(self.attempt_register)
        
        # Ссылка на вход
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)
        login_label = QLabel("Уже есть аккаунт?")
        login_btn = QPushButton("Войти")
        login_btn.setStyleSheet("border: none; color: #3498db;")
        login_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        login_layout.addWidget(login_label)
        login_layout.addWidget(login_btn)
        
        # Сборка экрана
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(self.reg_name)
        layout.addWidget(self.reg_email)
        layout.addWidget(self.reg_password)
        layout.addWidget(self.reg_confirm)
        layout.addWidget(self.terms_check)
        layout.addWidget(register_btn)
        layout.addLayout(login_layout)
        
        screen.setLayout(layout)
        return screen
    
    def create_input(self, placeholder, icon, is_password=False):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f5f7fa;
                border-radius: 5px;
                border: 1px solid #dfe6e9;
            }
            QFrame:hover {
                border: 1px solid #bdc3c7;
            }
        """)
        frame.setFixedHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(QSize(20, 20)))
        icon_label.setStyleSheet("padding-right: 5px;")
        
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setFont(QFont("Arial", 9))
        line_edit.setStyleSheet("background: transparent; border: none;")
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(icon_label)
        layout.addWidget(line_edit)
        frame.setLayout(layout)
        
        return frame
    
    def get_button_style(self):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1a6a9c;
            }
        """
    
    def attempt_login(self):
        email = self.login_password.findChild(QLineEdit).text()
        password = self.login_password.findChild(QLineEdit).text()
        
        # Здесь должна быть проверка в базе данных
        if email and password:
            self.login_success.emit(email)  # Отправляем сигнал об успешном входе
    
    def attempt_register(self):
        name = self.reg_name.findChild(QLineEdit).text()
        email = self.reg_email.findChild(QLineEdit).text()
        password = self.reg_password.findChild(QLineEdit).text()
        confirm = self.reg_confirm.findChild(QLineEdit).text()
        
        if password != confirm:
            print("Пароли не совпадают")
            return
        
        if not self.terms_check.isChecked():
            print("Примите условия соглашения")
            return
        
        # Здесь должна быть регистрация в базе данных
        print(f"Регистрация: {name}, {email}")
        self.stacked_widget.setCurrentIndex(0)  # Переключаемся на экран входа


class ChatWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Чат - {username}")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.setup_mock_data()
    
    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Боковая панель с контактами
        self.contacts_panel = QWidget()
        self.contacts_panel.setFixedWidth(250)
        self.contacts_panel.setStyleSheet("background-color: #f5f7fa; border-right: 1px solid #dfe6e9;")
        
        contacts_layout = QVBoxLayout()
        contacts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок
        header = QLabel("Контакты")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        header.setStyleSheet("padding: 15px; border-bottom: 1px solid #dfe6e9;")
        header.setAlignment(Qt.AlignCenter)
        
        # Список контактов
        self.contacts_list = QListWidget()
        self.contacts_list.setStyleSheet("""
            QListWidget {
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid #dfe6e9;
            }
            QListWidget::item:hover {
                background-color: #e1e5eb;
            }
            QListWidget::item:selected {
                background-color: #d1d8e0;
            }
        """)
        self.contacts_list.itemClicked.connect(self.switch_chat)
        
        contacts_layout.addWidget(header)
        contacts_layout.addWidget(self.contacts_list)
        self.contacts_panel.setLayout(contacts_layout)
        
        # Основная область чата
        self.chat_area = QWidget()
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок чата
        self.chat_header = QLabel("Выберите контакт")
        self.chat_header.setFont(QFont("Arial", 14, QFont.Bold))
        self.chat_header.setStyleSheet("padding: 15px; border-bottom: 1px solid #dfe6e9;")
        self.chat_header.setAlignment(Qt.AlignCenter)
        
        # Область сообщений
        self.messages_area = QTextEdit()
        self.messages_area.setReadOnly(True)
        self.messages_area.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 10px;
                font-size: 14px;
            }
        """)
        
        # Поле ввода сообщения
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dfe6e9;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        
        # Кнопка отправки
        send_btn = QPushButton("Отправить")
        send_btn.setFixedHeight(40)
        send_btn.setStyleSheet(self.get_button_style())
        send_btn.clicked.connect(self.send_message)
        
        # Сборка области чата
        chat_layout.addWidget(self.chat_header)
        chat_layout.addWidget(self.messages_area)
        chat_layout.addWidget(self.message_input)
        chat_layout.addWidget(send_btn)
        self.chat_area.setLayout(chat_layout)
        
        # Добавление в главный layout
        main_layout.addWidget(self.contacts_panel)
        main_layout.addWidget(self.chat_area)
        self.setLayout(main_layout)
    
    def setup_mock_data(self):
        # Моковые данные контактов
        contacts = [
            {"name": "Иван Дулин", "last_message": "Привет! Как дела?", "unread": 2},
            
        ]
        
        for contact in contacts:
            item = QListWidgetItem()
            widget = ContactWidget(contact)
            item.setSizeHint(widget.sizeHint())
            self.contacts_list.addItem(item)
            self.contacts_list.setItemWidget(item, widget)
        
        # Сохраняем историю сообщений для каждого контакта
        self.chat_history = {
            "Иван Дулин": [
                {"sender": "Иван Дулин", "text": "Привет! Как дела?))", "time": "10:30"},
            ],
            "Мария Иванова": [
                {"sender": "Мария Иванова", "text": "Документы готовы", "time": "09:15"},
                {"sender": self.username, "text": "Отлично, спасибо!", "time": "09:20"},
            ],
            # ... другие контакты
        }
    
    def switch_chat(self, item):
        contact_widget = self.contacts_list.itemWidget(item)
        self.current_contact = contact_widget.contact["name"]
        self.chat_header.setText(self.current_contact)
        self.load_chat_history()
    
    def get_button_style(self):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1a6a9c;
            }
        """
    
    def load_chat_history(self):
        self.messages_area.clear()
        if self.current_contact in self.chat_history:
            for message in self.chat_history[self.current_contact]:
                self.add_message_to_chat(message["sender"], message["text"], message["time"])
    
    def add_message_to_chat(self, sender, text, time):
        if sender == self.username:
            alignment = Qt.AlignRight
            style = """
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 8px 12px;
                margin: 5px 10px 5px 50px;
            """
        else:
            alignment = Qt.AlignLeft
            style = """
                background-color: #f1f3f4;
                color: black;
                border-radius: 10px;
                padding: 8px 12px;
                margin: 5px 50px 5px 10px;
            """
        
        cursor = self.messages_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Добавляем отправителя и время
        if sender != self.username or not hasattr(self, 'last_sender') or self.last_sender != sender:
            cursor.insertHtml(f"""
                <div style="margin: 5px 0 2px {'10px' if sender != self.username else '50px'}; 
                           font-size: 12px; color: #7f8c8d;">
                    {sender} • {time}
                </div>
            """)
        
        # Добавляем сообщение
        cursor.insertHtml(f"""
            <div style="{style}; display: inline-block; max-width: 70%;" align="{alignment}">
                {text}
            </div>
            <br>
        """)
        
        self.last_sender = sender
        self.messages_area.verticalScrollBar().setValue(self.messages_area.verticalScrollBar().maximum())
    
    def send_message(self):
        text = self.message_input.toPlainText().strip()
        if not text or not hasattr(self, 'current_contact'):
            return
        
        # Добавляем сообщение в историю
        new_message = {
            "sender": self.username,
            "text": text,
            "time": "12:00"  # Здесь должно быть реальное время
        }
        
        if self.current_contact not in self.chat_history:
            self.chat_history[self.current_contact] = []
        
        self.chat_history[self.current_contact].append(new_message)
        self.add_message_to_chat(self.username, text, "12:00")
        self.message_input.clear()


class ContactWidget(QWidget):
    def __init__(self, contact):
        super().__init__()
        self.contact = contact
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedHeight(70)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Аватарка с проверкой наличия изображения
        avatar_label = QLabel()
        try:
            avatar_pixmap = QPixmap("dulin.jpg")
            if avatar_pixmap.isNull():
                # Создаем простую круглую иконку, если файл не найден
                avatar_pixmap = QPixmap(40, 40)
                avatar_pixmap.fill(Qt.transparent)
                painter = QPainter(avatar_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setBrush(QBrush(QColor(200, 220, 240)))  # Светло-голубой фон
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, 40, 40)
                # Добавляем первую букву имени
                painter.setFont(QFont("Arial", 16, QFont.Bold))
                painter.setPen(QColor(50, 50, 50))
                painter.drawText(avatar_pixmap.rect(), Qt.AlignCenter, self.contact["name"][0].upper())
                painter.end()
            else:
                # Если файл найден, масштабируем его
                avatar_pixmap = avatar_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # Создаем круглую маску
                rounded_pixmap = QPixmap(40, 40)
                rounded_pixmap.fill(Qt.transparent)
                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setBrush(QBrush(avatar_pixmap))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, 40, 40)
                painter.end()
                avatar_pixmap = rounded_pixmap
        except Exception as e:
            print(f"Ошибка загрузки аватарки: {e}")
            # Создаем простую замену при ошибке
            avatar_pixmap = QPixmap(40, 40)
            avatar_pixmap.fill(Qt.gray)
        
        avatar_label.setPixmap(avatar_pixmap)
        avatar_label.setAlignment(Qt.AlignCenter)

        # Остальной код остается без изменений...
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(3)

        self.name_label = QLabel(self.contact["name"])
        self.name_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.name_label.setStyleSheet("color: #2c3e50;")

        self.last_msg_label = QLabel(self.contact["last_message"])
        self.last_msg_label.setFont(QFont("Arial", 9))
        self.last_msg_label.setStyleSheet("color: #7f8c8d;")
        self.last_msg_label.setMaximumWidth(380)
        self.last_msg_label.setWordWrap(True)

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.last_msg_label)

        if self.contact["unread"] > 0:
            badge_widget = QWidget()
            badge_layout = QHBoxLayout(badge_widget)
            badge_layout.setContentsMargins(0, 0, 0, 0)
            
            self.badge = QLabel(str(self.contact["unread"]))
            self.badge.setAlignment(Qt.AlignCenter)
            self.badge.setFixedSize(20, 20)
            self.badge.setStyleSheet("""
                QLabel {
                    background-color: #3498db;
                    color: white;
                    border-radius: 10px;
                    font-size: 9px;
                    font-weight: bold;
                }
            """)
            badge_layout.addWidget(self.badge)
            badge_layout.addStretch()

        layout.addWidget(avatar_label)
        layout.addWidget(info_widget)
        if self.contact["unread"] > 0:
            layout.addWidget(badge_widget)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-bottom: 1px solid #e0e0e0;
            }
            QWidget:hover {
                background-color: #f0f2f5;
            }
        """)



class MainApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.setStyleSheet("QWidget { background-color: white; }")
        
        self.auth_window = AuthWindow()
        self.auth_window.login_success.connect(self.show_chat_window)
        self.auth_window.show()
    
    def show_chat_window(self, username):
        self.auth_window.close()
        self.chat_window = ChatWindow(username)
        self.chat_window.show()


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
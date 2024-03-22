from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,  QMessageBox, QRadioButton, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QLineEdit
import json

notes = {}

app = QApplication([])
win = QWidget()

text = QTextEdit()
text.setText("Здесь будет заметка")
line = QLineEdit()
list_titles = QListWidget()
list_tags = QListWidget()
title_label = QLabel("Список заметок")
tag_label = QLabel("Список тегов")

btn_add_note = QPushButton("Создать заметку")
btn_del_note = QPushButton("Удалить заметку")
btn_save_note = QPushButton("Сохранить заметку")
btn_add_tag = QPushButton("Добавить к заметке")
btn_del_tag = QPushButton("Открепить от заметки")
btn_search = QPushButton("Искать заметки по тегам")

horizn1 = QHBoxLayout()
horizn2 = QHBoxLayout()
horizn3 = QHBoxLayout()
horizn4 = QHBoxLayout()
horizn_main = QHBoxLayout()

vert_left = QVBoxLayout()
vert_right = QVBoxLayout()

horizn1.addWidget(title_label)
horizn2.addWidget(btn_add_note)
horizn2.addWidget(btn_del_note)
horizn3.addWidget(tag_label)
horizn4.addWidget(btn_add_tag)
horizn4.addWidget(btn_del_tag)

vert_left.addWidget(text)
vert_right.addLayout(horizn1)
vert_right.addWidget(list_titles)
vert_right.addLayout(horizn2)
vert_right.addWidget(btn_save_note)
vert_right.addLayout(horizn3)
vert_right.addWidget(list_tags)
vert_right.addLayout(horizn4)
vert_right.addWidget(btn_search)
vert_right.addWidget(line)
horizn_main.addLayout(vert_left)
horizn_main.addLayout(vert_right)
win.setLayout(horizn_main)

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_titles.addItems(notes)

def show_note():
    name = list_titles.selectedItems()[0].text()
    text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])

def add_note():
    note_name, result = QInputDialog.getText(win, "Добавить заметку", "Название заметки:")
    notes[note_name] = {"текст": "", "теги": []}
    list_titles.clear()
    list_titles.addItems(notes)

def del_note():
    if list_titles.selectedItems():
        note = list_titles.selectedItems()[0].text()
        del notes[note]
        text.clear()
        list_tags.clear()
        list_titles.clear()
        list_titles.addItems(notes)
def save_note():
    if list_titles.selectedItems():
        text_str = text.toPlainText()
        note = list_titles.selectedItems()[0].text()
        notes[note]["текст"] = text_str
        with open("notes_data.json", "w") as file:
            json.dump(notes, file)

def add_tag():
    if list_titles.selectedItems():
        if line.text():
            tag = line.text()
            note = list_titles.selectedItems()[0].text()
            if not tag in notes[note]["теги"]:
                notes[note]["теги"].append(tag)
                line.clear()
                list_tags.clear()
                list_tags.addItems(notes[note]["теги"])
                with open("notes_data.json", "w") as file:
                    json.dump(notes, file)

btn_add_tag.clicked.connect(add_tag)
btn_save_note.clicked.connect(save_note)
btn_del_note.clicked.connect(del_note)
btn_add_note.clicked.connect(add_note)
list_titles.itemClicked.connect(show_note)

win.show()
app.exec()


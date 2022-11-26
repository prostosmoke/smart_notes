#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу
import json
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget, QTextEdit
import os

if not os.path.exists("notes.json"):
    notes = {
        "Добро пожаловать!": {
            "text": "Это самое лучшее приложение для заметок в мире!",
            "tags": ["добро", "инструкция"],
        }
    }
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, sort_keys=True, ensure_ascii=False)

app = QApplication([])
main_window = QWidget()

# Тут создаем все необходимые виджеты
text = QTextEdit()  # Текст статьи
articles = QListWidget()  # Список статей
tags = QListWidget() # Список тегов
add_article = QPushButton("Добавить заметку")
del_article = QPushButton("Удалить заметку")
save_article = QPushButton("Сохранить заметку")
add_tag = QPushButton("Добавить к заметке")
del_tag = QPushButton("Открепить от заметки")
filter_articles = QPushButton("Искать заметки по тегу")
tag = QLineEdit() # Поле ввода тэга для поиска или добавления
tag.setPlaceholderText("Введите тег...")
articles_title = QLabel("Список заметок")  # Заголовок списка заметок
tags_title = QLabel("Список тегов")  # Заголовок списка тэгов

# Тут располагаем виджеты
cols = QHBoxLayout()
cols.addWidget(text)
rows = QVBoxLayout()
cols.addLayout(rows)
rows.addWidget(articles_title)
rows.addWidget(articles)
row1 = QHBoxLayout()
row1.addWidget(add_article)
row1.addWidget(del_article)
rows.addLayout(row1)
rows.addWidget(save_article)
rows.addWidget(tags_title)
rows.addWidget(tags)
rows.addWidget(tag)
row2 = QHBoxLayout()
row2.addWidget(add_tag)
row2.addWidget(del_tag)
rows.addLayout(row2)
rows.addWidget(filter_articles)

# Тут работаем с данными
for f in os.listdir():
    if '.txt' in f:
        articles.addItem(f.split('.')[0])

def onClick():
    title = articles.selectedItems()[0].text()
    with open(title + '.txt' , 'r', encoding='utf-8') as f:
        a_text = f.readline()
        a_tags = f.readline().split(' ')
    tags.clear()
    tags.addItems(a_tags)
    text.setText(a_text)
articles.itemClicked.connect(onClick)

def add_article_click():
    text, ok = QInputDialog().getText(main_window, "Добавить заметку", "Название:")
    if ok:
        with open(text + '.txt', 'w', encoding='utf-8') as f:
            f.write('\n\n')
        articles.addItem(text)
add_article.clicked.connect(add_article_click)

def save_article_click():
    title = articles.selectedItems()[0].text()
    with open(title + '.txt', 'w', encoding='utf-8') as f:
        f.write(text.toPlainText())
        a_tags = list()
        for row in range(tags.count()):
            a_tags.append(tags.item(row).text())
        a_tags = ' '.join(a_tags)
        f.write(a_tags)
save_article.clicked.connect(save_article_click)

def del_article_click():
    title = articles.selectedItems()[0].text()
    res = QMessageBox.question(
        main_window, 
        "Удалить заметку", 
        "Вы хотите удалить "+title+"?",
        QMessageBox.Yes | QMessageBox.No 
    )
    if res == QMessageBox.Yes:
        os.remove(title + '.txt')
        text.setText("")
        tags.clear()
        articles.clear()
        for f in os.listdir():
            if '.txt' in f:
                articles.addItem(f.split('.')[0])
del_article.clicked.connect(del_article_click)

def add_tag_click():
    new_tag = tag.text()
    a_tags = list()
    for row in range(tags.count()):
        a_tags.append(tags.item(row).text())
    if new_tag and new_tag not in a_tags:
        tags.addItem(new_tag)
add_tag.clicked.connect(add_tag_click)

def del_tag_click():
    tag_title = tags.selectedItems()[0].text()
    a_tags = list()
    for row in range(tags.count()):
        a_tags.append(tags.item(row).text())
    a_tags.remove(tag_title)
    tags.clear()
    tags.addItems(a_tags)
del_tag.clicked.connect(del_tag_click)

def filter_articles_click():
    if filter_articles.text() == "Искать заметки по тегу":
        new_articles = []
        tag_text = tag.text()

        for fn in os.listdir():
            if '.txt' in fn:
                with open(fn , 'r', encoding='utf-8') as f:
                    f.readline()
                    a_tags = f.readline()
                if tag_text in a_tags:
                    new_articles.append(fn.split('.')[0])

        articles.clear()
        articles.addItems(new_articles)
        filter_articles.setText("Сбросить поиск")
    else:
        articles.clear()
        for f in os.listdir():
            if '.txt' in f:
                articles.addItem(f.split('.')[0])
        filter_articles.setText("Искать заметки по тегу")
    
filter_articles.clicked.connect(filter_articles_click)


main_window.setLayout(cols)
main_window.show()
app.exec_()
#затем запрограммируй демо-версию функционала

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QMessageBox
import data
def handle():
    info = textEdit.toPlainText()
    QMessageBox.about(window,
                '查询结果',
                f'''加权:{data.score_dict[info]}     
                \n排名:{data.rank_dict[info]}     '''
                )

app = QApplication()

window = QMainWindow()
window.resize(500, 400)
window.move(400, 250)
window.setWindowTitle('智算学部2024级第二学期成绩查询')

textEdit = QPlainTextEdit(window)
textEdit.setPlaceholderText("请输入姓名")
textEdit.move(10,25)
textEdit.resize(300,350)

button = QPushButton('查询', window)
button.move(360,80)
button.clicked.connect(handle)

window.show()

app.exec() 
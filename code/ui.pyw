from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel
from guess import *
import sys
import rc_guess


class MainForm(QMainWindow):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        widget = QWidget()
        self.setCentralWidget(widget)

        menu = self.menuBar()
        info = QAction('Info', self, triggered=self.info)
        menu.addAction(info)
        self.setWindowIcon(QIcon(':guess.png'))
        self.setWindowTitle('Guess')

        lay = QHBoxLayout()
        form = QVBoxLayout(widget)
        buttonbox = QHBoxLayout()

        self.view = QTextBrowser()
        self.findbutton = QPushButton('Buscar', clicked=self.apply)
        self.findbutton.setShortcut('Return')

        buttonbox.addWidget(self.findbutton)
        buttonbox.addStretch(1)

        lay.addWidget(self.mainbox)
        lay.addWidget(self.view)

        form.addLayout(lay)
        form.addLayout(buttonbox)

    def info(self):
        QMessageBox.information(self, 'Info', 'Hecho por: \naCC')

    @property
    def mainbox(self):
        box = QGroupBox('Busqueda')

        mainlayout = QGridLayout(box)
        self.my_letters = QLineEdit()
        self.label_letters = QLabel('Letras disponibles')

        self.strict_check = QCheckBox('Buscar palabras que se formen con estas letras solamente')
        self.strict_check.toggled.connect(self.fieldValidator)

        self.minvalue = QSpinBox()
        self.label_minvalue = QLabel('Longitud minima de las palabras a encontrar')

        self.maxvalue = QSpinBox()
        self.maxvalue.setValue(15)
        self.label_maxvalue = QLabel('Longitud maxima de las palabras a encontrar')

        self.min_matches = QSpinBox()
        self.min_matches.setToolTip('Si dejas este en 0 se tomara como valor el numero de letras disponibles')
        self.label_min_matches = QLabel('Numero minimo de letras a encontrar en una palabra')

        self.check_respect_word_order = QCheckBox('Modo combinacion', toggled=self.combination_checked)

        mainlayout.addWidget(self.strict_check, 0, 0, 1, 8)
        mainlayout.addWidget(self.label_min_matches, 1, 0, Qt.AlignRight)
        mainlayout.addWidget(self.min_matches, 1, 1)
        mainlayout.addWidget(self.label_minvalue, 2, 0, Qt.AlignRight)
        mainlayout.addWidget(self.minvalue, 2, 1)
        mainlayout.addWidget(self.label_maxvalue, 3, 0, Qt.AlignRight)
        mainlayout.addWidget(self.maxvalue, 3, 1)
        mainlayout.addWidget(self.label_letters, 4, 0, Qt.AlignRight)
        mainlayout.addWidget(self.my_letters, 4, 1)
        mainlayout.addWidget(self.check_respect_word_order, 5, 1)

        return box

    def fieldValidator(self):
        self.minvalue.setDisabled(self.strict_check.checkState())
        self.maxvalue.setDisabled(self.strict_check.checkState())
        self.min_matches.setDisabled(self.strict_check.checkState())
        self.check_respect_word_order.setDisabled(self.strict_check.checkState())

    def combination_checked(self):
        self.strict_check.setDisabled(self.check_respect_word_order.checkState())
        self.min_matches.setDisabled(self.check_respect_word_order.checkState())

    def apply(self):
        if self.my_letters.text() != '':
            self.view.clear()
            with open(spanish_dict, encoding='utf-8') as h:
                words = Guesser(self.my_letters.text(), h.readlines(), min_matches=self.min_matches.value(),
                                min_len=self.minvalue.value(), max_len=self.maxvalue.value(),
                                strict_len=self.strict_check.checkState())
            if self.check_respect_word_order.checkState():
                li = words.combination_matches
            else:
                li = words.get_matches()

            if li:
                for i in li:
                    self.view.append(i)
            else:
                self.view.append('No encontrado')
        else:
            self.view.clear()
            self.view.append('Introduce algunas letras')


if __name__ == '__main__':
    app = QApplication([])

    # noinspection PyBroadException
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass

    main = MainForm()
    main.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtGui
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.image = None

    def setPixmap(self, image, width, height):
        if image:
            self.image = image
            super().setPixmap(image.scaled(width, height, Qt.KeepAspectRatio))
        else:
            super().setPixmap(QPixmap())
            self.image = None

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        # Define o tamanho mínimo da janela
        self.setMinimumSize(400, 300)
        # Permite que a janela aceite arrastar e soltar arquivos de imagem
        self.setAcceptDrops(True)

        # Cria um layout de grade para organizar os widgets
        mainLayout = QGridLayout()

        # Cria um QLabel para exibir a imagem
        self.photoViewer = ImageLabel()
        # Cria um QLabel para exibir o texto "Drop Image Here"
        self.text_label = QLabel("Arraste a imagem aqui")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet('''
            QLabel {
                border: 4px dashed #aaa;  
            }
        ''')

        # Adiciona os widgets ao layout de grade
        mainLayout.addWidget(self.text_label, 0, 0, 1, 1)  # O texto ocupa a primeira célula
        mainLayout.addWidget(self.photoViewer, 0, 0, 1, 1)  # A imagem ocupa a mesma célula

        # Define o layout para a janela
        self.setLayout(mainLayout)
        # Mantém a janela sempre visível
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def dragEnterEvent(self, event):
        # Verifica se o evento contém dados de imagem e aceita o evento se for o caso
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Aceita o evento de arrastar se ele contiver dados de imagem
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Lida com o evento de soltar imagem
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        # Carrega a imagem e a exibe no QLabel
        image = QPixmap(file_path)
        self.photoViewer.setPixmap(image, self.width(), self.height())
        # Oculta o QLabel com o texto
        self.text_label.hide()

    def resizeEvent(self, event):
        # Redimensiona a imagem quando a janela é redimensionada
        width = event.size().width()
        height = event.size().height()
        self.photoViewer.setPixmap(self.photoViewer.image, width, height)
# Cria a aplicação e a janela principal
app = QApplication(sys.argv)
demo = AppDemo()
app.setWindowIcon(QIcon("icone.ico"))
demo.setWindowTitle(" ")
demo.show()
# Inicia o loop de eventos da aplicação
sys.exit(app.exec_())

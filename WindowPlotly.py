from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWidgets
import plotly.express as px


class WidgetPlotly(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        self.button.clicked.connect(self.show_graph)
        self.resize(1000,800)

    def show_graph(self):
        df = px.data.tips()
        fig = px.box(df, x="day", y="total_bill", color="smoker")
        fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()

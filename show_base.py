import sys
import glfw
import imgui
import pandas as pd
import OpenGL.GL as gl
import mysql.connector
from PyQt5 import QtWidgets
from imgui.integrations.glfw import GlfwRenderer


class TableWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Table')
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.table_widget = QtWidgets.QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.load_data()

    def load_data(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='whx051021',
            database='pywork'
        )
        
        query = "SELECT * FROM img_gl"
        data = pd.read_sql(query, connection)

        self.table_widget.setRowCount(data.shape[0])
        self.table_widget.setColumnCount(data.shape[1])
        self.table_widget.setHorizontalHeaderLabels(data.columns.tolist())

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data.iat[i, j])))

        connection.close()

def show_data_with_qt():
    app = QtWidgets.QApplication(sys.argv)
    window = TableWindow()
    window.show()
    sys.exit(app.exec_())

def show_data_with_imgui():
    if not glfw.init():
        return

    window = glfw.create_window(1000, 800, "Data Table", None, None)
    glfw.make_context_current(window)

    imgui.create_context()
    renderer = GlfwRenderer(window)

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='whx051021',
        database='pywork'
    )

    query = "SELECT * FROM img_gl"
    data = pd.read_sql(query, connection)
    connection.close()

    while not glfw.window_should_close(window):
        imgui.new_frame()

        if imgui.begin("Data Table"):
            imgui.columns(len(data.columns), "Table")

            # 设置列宽
            column_width = 150  # 设置列宽
            for i in range(len(data.columns)):
                imgui.set_column_width(i, column_width)

            # 表头
            for col in data.columns:
                imgui.text(col)
                imgui.next_column()

            # 数据行
            for index, row in data.iterrows():
                for item in row:
                    imgui.text(str(item))
                    imgui.next_column()

            imgui.columns(1)  # 结束列模式
        imgui.end()

        imgui.render()
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)
        glfw.poll_events()

    renderer.shutdown()
    glfw.terminate()

def show_data_with_pandas():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='whx051021',
        database='pywork'
    )

    query = "SELECT * FROM img_gl"
    data = pd.read_sql(query, connection)
    connection.close()

    print(data)
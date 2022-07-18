import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from screens.queue_screen import QueueScreen
from screens.login_screen import LoginScreen
from screens.main_screen import MainScreen

if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = QStackedWidget()
     
    #widget.setFixedHeight(600)
    #widget.setFixedWidth(800)

    #make sure the mapping match the amount of widgets in stack
    app_map = {'login':0, 'main':1, 'queue': 2}
    
    #Place all screens here
    widget.addWidget(LoginScreen(app_map, widget))
    widget.addWidget(MainScreen(app_map, widget))
    widget.addWidget(QueueScreen(app_map, widget))
    #widget.currentWidget
    #widget.findChild()
    #widget.childAt()


    widget.show()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting")
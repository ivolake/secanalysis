import sys

from PyQt6.QtWidgets import QApplication

from GUI import Form
# from functions import parse_args, get_yaml

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec())

    # args = parse_args(sys.argv[1:])
    # config = get_yaml(args.config_path)

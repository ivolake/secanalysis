import logging
import sys
import traceback

from PyQt6.QtWidgets import QApplication

from GUI import Form
# from functions import parse_args, get_yaml

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Form()
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        raise e

    # args = parse_args(sys.argv[1:])
    # config = get_yaml(args.config_path)

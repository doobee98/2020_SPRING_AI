import sys
from View.MainView import *
from View.SettingView import *
from PyQt5.QtWidgets import QApplication

# pyinstaller --onefile --icon="gomoku_icon.ico"  main.py

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        while True:
            # Player의 정보 설정. 이름, 제한시간, AI여부 등
            setting_view = SettingView()
            setting_view.exec_()
            black_player, white_player = setting_view.black_player, setting_view.white_player

            if setting_view.result():
                if black_player.isValid() and white_player.isValid():
                    # 플레이어 설정 후 오목게임 메인 뷰 열기
                    v = MainView()
                    v.setPlayer(black_player, Color.Black)
                    v.setPlayer(white_player, Color.White)
                    v.show()
                    v.start()
                    break
                else:
                    QMessageBox.warning(setting_view, 'Input Error', '잘못된 입력입니다.')
            else:
                exit(0)
                break
        app.exec_()
    except Exception as e:
        print(e)

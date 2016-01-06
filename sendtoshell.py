import sublime
import sublime_plugin
import subprocess

try:
    import Pywin32.setup
    from win32con import WM_KEYDOWN, WM_KEYUP, VK_RETURN, WM_CHAR
    from win32gui import FindWindow, PostMessage
    from win32api import SendMessage
except:
    print('Sendtoshell - win32 modules not found, ' +
          'install Pywin32 from package control')
    raise

from os import startfile
from time import sleep


SETTINGS_FILE = "SendToShell.sublime-settings"


def settings():
    return sublime.load_settings(SETTINGS_FILE)


class SendtoshellCommand(sublime_plugin.TextCommand):

    def string_to_paste(self):
        return settings().get("string_to_paste")

    def string_to_run(self):
        return settings().get("string_to_run")

    def powershell_startup(self):
        return settings().get("powershell_startup")

    def python_startup(self):
        return settings().get("python_startup")

    def window_title(self):
        return settings().get("window_title")

    def run(self, edit, how):
        self.send_to_powershell(how)

    def send_to_powershell(self, how):
        hwnd = FindWindow(None, self.window_title())
        if hwnd == 0:
            # no window available? Try to open a new instance
            print('Sendtoshell - no powershell found, opening new')
            startfile(self.powershell_startup())
            sleep(1.0)
            hwnd = FindWindow(None, self.window_title())
            if hwnd == 0:
                print('Sendtoshell - could not open powershell, exiting')
                return None
            self._sendmsg(hwnd, self.python_startup())
            sleep(1.0)
        if how == 'run_file':
            print('Sendtoshell - running entire file, make sure you `keyup` ' +
                  'within 0.4 seconds!')
            sleep(0.4)
            string_to_type = self.string_to_run() + ' "' + sublime.active_window().active_view().file_name() + '"'
            sublime.set_clipboard(string_to_type)
            self._sendmsg(hwnd, self.string_to_paste())
        else:
            # send selected text
            for region in self.view.sel():
                if not region.empty():
                    # Get the selected text
                    selected_text = self.view.substr(region)
                    print('Sendtoshell - pasting, make sure you `keyup` ' +
                          'within 0.4 seconds!')
                    sleep(0.4)
                    sublime.set_clipboard(selected_text)
                    self._sendmsg(hwnd, self.string_to_paste())

    def _sendmsg(self, hwnd, msg):
        for character in msg:
            SendMessage(hwnd,
                        WM_CHAR,
                        ord(character),
                        0)
        PostMessage(hwnd, WM_KEYDOWN, VK_RETURN, int('0x1C0001', 0))
        PostMessage(hwnd, WM_KEYUP, VK_RETURN, int('0xC0000001', 0))


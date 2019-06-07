import sublime
import sublime_plugin
import subprocess

try:
    import Pywin32.setup
    from win32con import WM_KEYDOWN, WM_KEYUP, VK_RETURN, WM_CHAR, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_ABSOLUTE, MOUSEEVENTF_RIGHTUP, MOUSEEVENTF_ABSOLUTE
    from win32gui import FindWindow, PostMessage, GetWindowText, GetClassName, EnumWindows, SetForegroundWindow, GetWindowRect
    from win32api import SendMessage, mouse_event, SetCursorPos, GetCursorPos
    from win32com.client import Dispatch
except:
    print('Sendtoshell - win32 modules not found, ' +
          'install Pywin32 from package control')
    raise

from os import startfile
from time import sleep

subl_handle = None
SETTINGS_FILE = "SendToShell.sublime-settings"


def enum_window_titles():
    '''
    https://stackoverflow.com/a/11511682/566035
    with modification to return a dict of {handle: (title, classname)}
    '''
    def callback(handle, data):
        title = GetWindowText(handle)
        classname = GetClassName(handle)
        if title:
            titles[handle] = (title, classname)

    titles = dict()
    EnumWindows(callback, None)
    
    return titles


def find_suspects(view=None):
    global subl_handle
    suspects = []
    titles = enum_window_titles()
    for handle, (title, classname) in sorted(titles.items(), key=lambda x: x[1][0]):
        if classname in ("ConsoleWindowClass", "PuTTY"): # look for cmd, wsl, PuTTy
            suspects.append('{0}: {1}'.format(handle, title))
        if title.endswith("- Sublime Text") and classname == "PX_WINDOW_CLASS":
            subl_handle = int(handle) # assuming only one sublime instance
    return suspects


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
        if how == 'select_shell' or not hasattr(self, 'selectedshell'):
            self.suspects = find_suspects()
            print (self.suspects)
            self.view.show_popup_menu(self.suspects, self.on_select)
        else:
            self.send_to_powershell(how)

    def on_select(self, index):
        self.selectedshell = int(self.suspects[index].split(':')[0])
        print("on_select: shell hwnd {0}, sublime hwnd {1}".format(self.selectedshell, subl_handle))

    def send_to_powershell(self, how):
        if self.selectedshell:
            hwnd = self.selectedshell
        else:
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
                else:
                    # If no selection, then select the current line like PyCharm or RStudio
                    selected_text = self.view.substr(self.view.line(region))
                    # Move the caret one line down
                    self.view.run_command("move", {"by": "lines", "forward": True, "amount": 1})

                print('Sendtoshell - pasting, make sure you `keyup` ' +
                      'within 0.4 seconds!')
                sleep(0.4)
                if settings().get("send_right_click") == 'True':
                    if settings().get("useCR") == 'True':
                        selected_text = '\r'.join(selected_text.split('\n'))
                    self._sendRclick(hwnd, selected_text)
                else:
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

    def _sendRclick(self, hwnd, msg):
        # IPython magic %paste does not work for remote ssh python 
        # or Windows Subsystem for Linux, so let's send right click using win32
        def _pasting(hwnd, msg):
            sublime.set_clipboard(msg)
            sleep(0.1) # important!
            # sending right-click to paste over
            mouse_event(MOUSEEVENTF_RIGHTDOWN|MOUSEEVENTF_ABSOLUTE, 0, 0)
            sleep(0.1) # important!
            mouse_event(MOUSEEVENTF_RIGHTUP|MOUSEEVENTF_ABSOLUTE, 0, 0)
            # send enter;  int('0x1C0001', 0) works both on WSL and cmd
            PostMessage(hwnd, WM_KEYDOWN, VK_RETURN, int('0x1C0001', 0))
            PostMessage(hwnd, WM_KEYUP, VK_RETURN, int('0xC0000001', 0))

        try:
            # https://stackoverflow.com/a/15503675/566035
            shell = Dispatch("WScript.Shell")
            shell.SendKeys('%') # Sending Alt key goes around windows security policy change
            SetForegroundWindow(hwnd)
        except:
            self.view.show_popup('Invalid handle ({})'.format(hwnd))
            return

        # move mouse to the center of that window
        oldx, oldy = GetCursorPos()
        x1,y1,x2,y2 = GetWindowRect(hwnd)
        x = int((x1+x2)/2)
        y = int((y1+y2)/2)
        SetCursorPos((x,y))
        
        lineN = len(self.view.lines(self.view.sel()[0]))
        # we need to use %cpaste magic to avoid indentation error
        # in case more than 2 lines have indentation.
        if lineN > 2:
            _pasting(hwnd, r"%cpaste")
            _pasting(hwnd, msg)
            _pasting(hwnd, "--")
        else:
            _pasting(hwnd, msg)

        # bring back the mouse cursor
        SetCursorPos((oldx,oldy))

        # bring back the focus to sublime, if subl_handle is known to the plugin
        if subl_handle:
            SetForegroundWindow(subl_handle)
            shell.SendKeys('%') # cancel the Alt key evoked menu

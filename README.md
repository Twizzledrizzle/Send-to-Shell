# Send to Shell #

_Send to Shell_ is a free plugin for [Sublime Text](http://www.sublimetext.com/) on Windows, to work nicely together with an external terminal running IPython.


## Features ##

- Puts selected text into clipboard memory, and sends by default `%Paste` to the specified terminal shell (referenced by window title).
- Shells tested
	1 PowerShell
	2 Command Prompt
	3 ConEmu
- Edit _Send to Shell_'s settings to change the following (default in ()):
	* The window title to search for ('Windows PowerShell')
	* The command to run in the shell to paste the text ('%paste')
	* The command to run if no terminal is found ('powershell')
	* The command to start python ('ipython')


## Releases ##
- 1.0.0

## Installation ##

Use the excellent [Package Control](http://wbond.net/sublime_packages/package_control) to install _Send to Shell_.

You can do a manual installation by cloning this repository into your Packages folder. Sublime Text -> Preferences -> Browse Packages...

```git clone git@github.com:https://github.com/Twizzledrizzle/Send-to-Shell```

## How-To ##


## Key Bindings ##
The default key bindings are stored at _<packages>/Send to Shell/Default.sublime-keymap_. As always, you can use your [user keymap file](http://docs.sublimetext.info/en/latest/customization/key_bindings.html) to setup your own key bindings.

**Note:** The commands from the _Send to Shell_ menu are also available through the Command Palette (<kbd>CTRL/CMD</kbd> + <kbd>SHIFT</kbd> + <kbd>P</kbd>)

## Command Reference ##


## License ##

The MIT License (MIT)

Copyright (c) 2015 TwizzleDrizzle, https://github.com/Twizzledrizzle/Send-to-Shell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


## See Also ##

For further information, please take the time to look at following links:

* Sublime Text 3: http://www.sublimetext.com/3/
* Sublime Package Control: https://sublime.wbond.net/installation

"""
###############################################################################
An extended Frame that makes window menus and toolbars automatically.
Use GuiMakerFrameMenu for embedded components (makes frame-based menus).
Use GuiMakerWindowMenu for top-level windows (makes Tk8.0 window menus).
See the self-test code (and PyEdit) for an example layout tree format.
###############################################################################
"""
import tkinter as tk                  # widget classes
from tkinter.messagebox import showinfo
import sys

class GuiMaker(tk.Frame):
    """Make Gui for default api"""

    menu_bar = []                       # class defaults
    tool_bar = []                       # change per instance in subclasses
    help_button = False                     # set these in start() if need self

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.pack(expand=tk.YES, fill=tk.BOTH)        # make frame stretchable
        self.start()                            # for subclass: set menu/tool_bar
        self.make_menu_bar()                      # done here: build menu bar
        self.make_tool_bar()                      # done here: build toolbar
        self.make_widgets()                      # for subclass: add middle part

    def make_menu_bar(self):
        """
        make menu bar at the top (Tk8.0 menus below)
        expand=no, fill=x so same width on resize
        """

        menubar = tk.Frame(self, relief=tk.RAISED, bd=2)
        menubar.pack(side=tk.TOP, fill=tk.X)

        for (name, key, items) in self.menu_bar:
            mbutton = tk.Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=tk.LEFT)
            pulldown = tk.Menu(mbutton)
            self.add_menu_items(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.help_button:
            tk.Button(menubar, text    = 'Help',
                            cursor  = 'gumby',
                            relief  = tk.FLAT,
                            command = self.help).pack(side=tk.RIGHT)

    def add_menu_items(self, menu, items):
        """ Add items for menu """
        for item in items:                     # scan nested items list
            if item == 'separator':            # string: add separator
                menu.add_separator({})
            elif isinstance(item, list):           # list: disabled item list
                for num in item:
                    menu.entryconfig(eval(num), state=tk.DISABLED)
            elif not isinstance(item[2], list):
                menu.add_command(label     = item[0],         # command:
                                 underline = item[1],         # add command
                                 command   = eval(item[2]))         # cmd=callable
            else:
                pullover = tk.Menu(menu)
                self.add_menu_items(pullover, item[2])          # sublist:
                menu.add_cascade(label     = item[0],         # make submenu
                                 underline = item[1],         # add cascade
                                 menu      = pullover)

    def make_tool_bar(self):
        """
        make button bar at bottom, if any
        expand=no, fill=x so same width on resize
        this could support images too: see Chapter 9,
        would need prebuilt gifs or PIL for thumbnails
        """
        if self.tool_bar:
            toolbar = tk.Frame(self, cursor='hand2', relief=tk.SUNKEN, bd=2)
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)
            for (name, action, where) in self.tool_bar:
                tk.Button(toolbar, text=name, command=action).pack(where)

    def make_widgets(self):
        """This method must be defined in subclass"""
        pass

    def help(self):
        """override me in subclass"""
        showinfo('Help', 'Sorry, no help for ' + self.__class__.__name__)

    def start(self):
        """override me in subclass: set menu/toolbar with self"""
        pass


###############################################################################
# Customize for Tk 8.0 main window menu bar, instead of a frame
###############################################################################

GuiMakerFrameMenu = GuiMaker           # use this for embedded component menus

class GuiMakerWindowMenu(GuiMaker):
    """GuiMaker, which use window for make menu"""
    # use this for top-level window menus
    def make_menu_bar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        for (name, key, items) in self.menu_bar:
            pulldown = tk.Menu(menubar)
            self.add_menu_items(pulldown, items)
            menubar.add_cascade(label=name, underline=key, menu=pulldown)

        if self.help_button:
            if sys.platform[:3] == 'win':
                menubar.add_command(label='Help', command=self.help)
            else:
                pulldown = tk.Menu(menubar)  # Linux needs real pull down
                pulldown.add_command(label='About', command=self.help)
                menubar.add_cascade(label='Help', menu=pulldown)


###############################################################################
# Self-test when file run standalone: 'python guimaker.py'
###############################################################################

if __name__ == '__main__':
    from guimixin import GuiMixin            # mix in a help method

    menu_bar = [
        ('File', 0,
            [('Open',  0, lambda:0),         # lambda:0 is a no-op
             ('Quit',  0, sys.exit)]),       # use sys, no self here
        ('Edit', 0,
            [('Cut',   0, lambda:0),
             ('Paste', 0, lambda:0)]) ]
    tool_bar = [('Quit', sys.exit, {'side': LEFT})]

    class TestAppFrameMenu(GuiMixin, GuiMakerFrameMenu):
        def start(self):
            self.menu_bar = menu_bar
            self.tool_bar = tool_bar

    class TestAppWindowMenu(GuiMixin, GuiMakerWindowMenu):
        def start(self):
            self.menu_bar = menu_bar
            self.tool_bar = tool_bar

    class TestAppWindowMenuBasic(GuiMakerWindowMenu):
        def start(self):
            self.menu_bar = menu_bar
            self.tool_bar = tool_bar    # guimaker help, not guimixin

    root = tk.Tk()
    TestAppFrameMenu(tk.Toplevel())
    TestAppWindowMenu(tk.Toplevel())
    TestAppWindowMenuBasic(root)
    root.mainloop()

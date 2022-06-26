import pyautogui as pag
from pywinauto.application import Application
import pywinauto
import time

procs = pywinauto.findwindows.find_elements()
app = Application(backend="uia").connect(title="motion").top_window().set_focus().activate()
pag.click(app.left + 633, app.top + 936)
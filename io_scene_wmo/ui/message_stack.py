from ..utils.misc import singleton

from typing import List, Tuple

import bpy


@singleton
class MessageStack:
    """ Used to display messages from handlers. """

    _message: List[Tuple[str, str]] = []

    def push_message(self, *,  msg: str = '', icon: str = 'INFO'):
        """
        Push message to the stack.
        :param msg: Message text.
        :param icon: Message icon.
        """
        self._message.append((msg, icon))

    @staticmethod
    def _draw(self, context):
        for msg, icon in MessageStack()._message:
            self.layout.label(text=msg, icon=icon)

    def invoke_message_box(self, title: str = 'WoW Blender Studio', icon: str = 'INFO'):
        """
        Invoke popup message box window displaying current message stack. Also clears the stack.
        :param title: Title of the message box.
        :param icon: Icon of the message box.
        """

        if not self._message:
            return

        # *** A POPUP WITH NO WINDOW IS A NULL DEREFERENCE, NOT A WARNING. ***
        # popup_menu -> UI_popup_menu_begin_ex -> ui_update_window_matrix ->
        # WM_window_pixels_x, which reads the active window with no null check. A
        # script driving Blender from --python has no active window inside a
        # depsgraph_update_post handler, so this line was an unconditional
        # EXCEPTION_ACCESS_VIOLATION (null + 0x10) the moment ANY handler pushed a
        # message - which is the crash that has been blamed on group counts, model
        # counts and one oversized asset. The message is worth having; the crash is
        # not. With no window, say it on stdout instead.
        if getattr(bpy.context, 'window', None) is None:
            for _msg, _icon in self._message:
                print('[WBS %s] %s' % (_icon, _msg))
            self._message.clear()
            return

        bpy.context.window_manager.popup_menu(self._draw, title=title, icon=icon)
        self._message.clear()



import traceback
from pathlib import Path

from PyQt6 import QtWidgets as widgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QScreen

from context import perform_mode, show_directory_path, get_show_name, current_track, tracks
from utils.track import Track, TrackException, TRACK, TEXT
from windows.perform import PerformWindow


class MainWindow(widgets.QMainWindow):
    """Main window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('LiveBeatMonitor')

        self.perform_window = PerformWindow()
        self.perform_window.perform_window_closed.connect(self.stop_perform_mode)

        container = widgets.QWidget()
        layout = widgets.QVBoxLayout()

        # Show selection menu
        show_selection_container = widgets.QWidget()
        show_selection_layout = widgets.QHBoxLayout()
        self.show_selection_label = widgets.QLabel(get_show_name())
        show_selection_button = widgets.QPushButton('Open show folder')
        show_selection_button.clicked.connect(self.open_show)
        show_selection_layout.addWidget(self.show_selection_label)
        show_selection_layout.addStretch()
        show_selection_layout.addWidget(show_selection_button)
        show_selection_container.setLayout(show_selection_layout)

        # Show items list
        self.track_list_wrapper = widgets.QScrollArea()
        self.track_list_wrapper.keyPressEvent = self.keyPressEvent
        self.show_items_list = widgets.QWidget()

        self.show_items_layout = widgets.QVBoxLayout()

        self.clear_show_items()

        self.show_items_list.setLayout(self.show_items_layout)
        self.track_list_wrapper.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.track_list_wrapper.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        size_policy = widgets.QSizePolicy()
        size_policy.setHorizontalPolicy(widgets.QSizePolicy.Policy.Expanding)
        # self.track_list_wrapper.setSizePolicy(size_policy)
        self.track_list_wrapper.setWidgetResizable(True)
        self.track_list_wrapper.setWidget(self.show_items_list)
        self.track_list_wrapper.resize(400, 800)

        # Perform button
        self.perform_button = widgets.QPushButton('Perform mode')
        self.perform_button.setCheckable(True)
        self.perform_button.clicked.connect(self.toggle_perform_mode)

        layout.addWidget(show_selection_container)
        layout.addWidget(self.track_list_wrapper)
        # layout.addStretch()
        layout.addWidget(self.perform_button)

        container.setLayout(layout)

        self.setCentralWidget(container)

    def closeEvent(self, a0):
        self.perform_window.hide()
        super().closeEvent(a0)

    def keyPressEvent(self, e: QKeyEvent):
        key = e.key()
        if key in [16777234, 16777235, 16777238]:  # Left arrow, up arrow, page up
            if current_track.get() > 0:
                current_track.set(current_track.get() - 1)
            self.update_item_selection()
        if key in [16777236, 16777237, 16777239]:  # Right arrow, down arrow, page down
            if current_track.get() < len(tracks.get()) - 1:
                current_track.set(current_track.get() + 1)
            self.update_item_selection()
        if key == 32:  # Space
            if len(tracks.get()) > 0:
                track = tracks.get()[current_track.get()]
                if track.item_type == TRACK:
                    if track.player.isPlaying():
                        track.player.pause()
                        self.perform_window.setPlayingStatus(False)
                    else:
                        track.player.play()
                        self.perform_window.setPlayingStatus(True)
        if key == 16777220:  # Return
            if len(tracks.get()) > 0:
                track = tracks.get()[current_track.get()]
                if track.item_type == TRACK:
                    track.player.stop()
                    self.perform_window.setPlayingStatus(False)
        if key == 93:  # ]
            self.perform_window.md_field.zoomIn()
        if key == 91:  # [
            self.perform_window.md_field.zoomOut()
        if key == 16777216:  # Esc
            self.toggle_perform_mode()
        if key == 79:  # O
            self.open_show()

    def toggle_perform_mode(self):
        if perform_mode.get():
            perform_mode.set(False)
            self.perform_window.hide()
        else:
            perform_mode.set(True)
            monitors = QScreen.virtualSiblings(self.screen())
            if len(monitors) > 1:
                monitor = monitors[1].availableGeometry()
                self.perform_window.move(monitor.left(), monitor.top())
            self.perform_window.showFullScreen()
        self.perform_button.setChecked(perform_mode.get())
        self.activateWindow()

    def stop_perform_mode(self):
        perform_mode.set(False)
        self.perform_window.hide()
        self.perform_button.setChecked(perform_mode.get())

    def open_show(self):
        path = widgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        show_directory_path.set(Path(path))
        self.show_selection_label.setText(get_show_name())
        self.load_show_items()

    def load_show_items(self):
        files = [f for f in show_directory_path.get().iterdir() if f.is_file()]
        print(files)
        items = list()
        for file in files:
            try:
                items.append(Track(file))
            except TrackException as e:
                dlg = widgets.QMessageBox(self)
                dlg.setWindowTitle('Error loading track: ' + str(e))
                traceback_str = 'Error loading track: ' + str(e) + '\n\n'
                traceback_str += 'File: ' + file.name + '\n\n'
                traceback_str += ''.join(traceback.format_tb(e.__traceback__))
                dlg.setText(traceback_str)
                dlg.exec()
        print(items)
        items.sort(key=lambda i: i.position)
        tracks.set(items)
        container = widgets.QWidget()
        layout = widgets.QVBoxLayout()
        for item in items:

            layout.addWidget(item.get_item_widget())

        container.setLayout(layout)
        if len(items) > 0:
            if self.show_items_layout.itemAt(0):
                self.show_items_layout.itemAt(0).widget().setParent(None)
            self.show_items_layout.addWidget(container)
            current_track.set(0)
            self.update_item_selection()

    def clear_show_items(self):
        container = widgets.QWidget()
        show_items_empty_layout = widgets.QHBoxLayout()
        show_items_empty_layout.addStretch()
        show_items_empty_layout.addWidget(
            widgets.QLabel('Track list empty')
        )
        show_items_empty_layout.addStretch()
        container.setLayout(show_items_empty_layout)
        if self.show_items_layout.itemAt(0):
            self.show_items_layout.itemAt(0).widget().setParent(None)
        self.show_items_layout.addWidget(container)

    def update_item_selection(self):
        for item in tracks.get():
            item.deactivate()
        if len(tracks.get()) > 0:
            tracks.get()[current_track.get()].activate()
        self.perform_window.update_track()


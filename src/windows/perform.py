from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from context import tracks, current_track
from utils.track import TRACK


class PerformWindow(QWidget):
    """Perform window."""

    perform_window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('LiveBeatMonitor | Perform')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowDoesNotAcceptFocus)
        self.setWindowFlag(Qt.WindowType.WindowTransparentForInput)
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        track_label_font = QFont()
        track_label_font.setBold(True)
        track_label_font.setPointSize(100)
        self.current_track_label = QLabel()
        self.current_track_label.setText('No track selected')
        self.current_track_label.setFont(track_label_font)
        self.next_track_label = QLabel()
        self.next_track_label.setText('Last track')
        self.next_track_label.setFont(track_label_font)

        self.track_beat = QLabel()
        self.track_beat.setText('00|00')
        self.track_beat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        track_beat_font = QFont()
        track_beat_font.setBold(True)
        track_beat_font.setPointSize(400)
        track_beat_font.setFamily('Monospace')
        track_beat_font.setStyleHint(QFont.StyleHint.Monospace)
        self.track_beat.setFont(track_beat_font)
        # self.track_beat.setSizePolicy()

        layout = QVBoxLayout()
        layout.addWidget(self.current_track_label)
        layout.addWidget(self.next_track_label)
        layout.addStretch()
        layout.addWidget(self.track_beat)

        self.setLayout(layout)

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.perform_window_closed.emit()

    def update_track(self):
        if len(tracks.get()) > 0:
            track = tracks.get()[current_track.get()]
            self.current_track_label.setText(
                f'#{track.position}: {track.title}',
            )
            self.update_track_beat()
            if track.item_type == TRACK:
                self.update_track_beat(track.player.position())
                track.player.positionChanged.connect(self.update_track_beat)
            try:
                next_track = tracks.get()[current_track.get() + 1]
                self.next_track_label.setText(
                    f'-> #{next_track.position}: {next_track.title}',
                )
            except IndexError:
                self.next_track_label.setText('Last track')
        else:
            self.current_track_label.setText('No track selected')

    def update_track_beat(self, position=0):
        track = tracks.get()[current_track.get()]
        if track.item_type == TRACK:
            millis = position - track.delay_seconds * 1000
            if millis < 0:
                millis = 0
            total_beat = track.bpm / 60 * millis / 1000
            beat = int(total_beat % 4) + 1
            part = int(total_beat % 16 / 4) + 1
            phrase = int(total_beat / 16) + 1
            self.track_beat.show()
            self.track_beat.setText(f'{phrase}: {part}|{beat}')
        else:
            self.track_beat.hide()

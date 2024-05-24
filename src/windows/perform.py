from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

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

        self.track_beat_container = QWidget()
        track_beat_container_layout = QVBoxLayout()

        self.track_beat = QLabel()
        self.track_beat.setText('00|00')
        self.track_beat.setStyleSheet("background-color:rgb(255,255,255); color:black;")
        self.track_beat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        track_beat_font = QFont()
        track_beat_font.setBold(True)
        track_beat_font.setPointSize(400)
        track_beat_font.setFamily('Monospace')
        track_beat_font.setStyleHint(QFont.StyleHint.Monospace)
        self.track_beat.setFont(track_beat_font)


        chords_label_font = QFont()
        chords_label_font.setBold(True)
        chords_label_font.setPointSize(60)

        self.chords_begin = QLabel()
        self.chords_begin.setText('Beginning: ')
        self.chords_begin.setFont(chords_label_font)

        self.chords_verse = QLabel()
        self.chords_verse.setText('Verse: ')
        self.chords_verse.setFont(chords_label_font)

        self.chords_chorus = QLabel()
        self.chords_chorus.setText('Chorus: ')
        self.chords_chorus.setFont(chords_label_font)

        track_beat_container_layout.addStretch()
        track_beat_container_layout.addWidget(self.chords_begin)
        track_beat_container_layout.addWidget(self.chords_verse)
        track_beat_container_layout.addWidget(self.chords_chorus)
        track_beat_container_layout.addWidget(self.track_beat)
        self.track_beat_container.setLayout(track_beat_container_layout)

        self.md_field = QTextEdit()
        self.md_field.setReadOnly(True)
        self.md_field.zoomIn(40)
        # self.md_field.sizePolicy().verticalStretch()

        # self.track_beat.setSizePolicy()

        layout = QVBoxLayout()
        layout.addWidget(self.current_track_label)
        layout.addWidget(self.next_track_label)
        # layout.addStretch()
        layout.addWidget(self.track_beat_container)
        layout.addWidget(self.md_field)
        # layout.addStretch()

        self.md_field.hide()
        self.setLayout(layout)

    def setPlayingStatus(self, is_playing):
        if is_playing:
            self.track_beat.setStyleSheet("background-color:rgb(140,0,0); color:white;")
        else:
            self.track_beat.setStyleSheet("background-color:rgb(255,255,255); color:black;")

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
            self.track_beat_container.show()
            self.md_field.hide()
            self.track_beat.setText(f'{phrase}: {part}|{beat}')
            self.chords_begin.setText('Beginning: ' + track.chords_begin)
            self.chords_verse.setText('Verse: ' + track.chords_verse)
            self.chords_chorus.setText('Chorus: ' + track.chords_chorus)
        else:
            self.track_beat_container.hide()
            self.md_field.show()
            self.md_field.setMarkdown(track.text)

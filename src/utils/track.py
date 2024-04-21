from pathlib import Path
from PyQt6 import QtWidgets as widgets
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class TrackException(Exception):
    pass


class TrackType:
    extensions: list[str]

    def __init__(self, extensions: list[str]):
        self.extensions = extensions


TRACK = TrackType(['.mp3', '.wav'])
TEXT = TrackType(['.md'])


class Track:
    path: Path
    position: int
    title: str
    item_type: TrackType
    bpm: float
    delay_seconds: float
    text: str

    def __init__(self, path: Path):
        self.path = path
        if path.is_file():
            if path.suffix in TRACK.extensions:
                self.item_type = TRACK
            elif path.suffix in TEXT.extensions:
                self.item_type = TEXT
            else:
                raise TrackException('Invalid file type')
            try:
                data = path.stem.split('-')
                self.position = int(data[0])
                self.title = data[1]
                if self.item_type == TRACK:
                    self.bpm = float(data[2])
                    self.delay_seconds = float(data[3])
            except Exception as e:
                raise TrackException(e)
            self.__item_container = widgets.QWidget()
            item_layout = widgets.QHBoxLayout()
            item_layout.addWidget(
                widgets.QLabel(f'#{self.position} - {self.title}')
            )
            item_layout.addStretch()
            if self.item_type == TRACK:
                item_layout.addWidget(
                    widgets.QLabel(f'{self.bpm} BPM')
                )
                self.player = QMediaPlayer()
                self.player.setSource(QUrl.fromLocalFile(str(self.path)))
                self.audio_output = QAudioOutput()
                self.audio_output.setVolume(50)
                self.player.setAudioOutput(self.audio_output)
            if self.item_type == TEXT:
                item_layout.addWidget(
                    widgets.QLabel(f'TEXT')
                )
                with open(self.path, 'r') as f:
                    self.text = f.read()
            self.__item_container.setLayout(item_layout)

    def __repr__(self):
        if self.item_type == TRACK:
            return f'{self.position}: {self.title} | {self.bpm} BPM'
        if self.item_type == TEXT:
            return f'{self.position}: {self.title} | TEXT'

    def get_item_widget(self):
        return self.__item_container

    def activate(self):
        pal = QPalette()
        pal.setColor(QPalette.ColorRole.Window, QColor(30, 30, 200))
        self.__item_container.setAutoFillBackground(True)
        self.__item_container.setPalette(pal)

    def deactivate(self):
        self.__item_container.setAutoFillBackground(False)



import sys
from custome_errors import *
sys.excepthook = my_excepthook
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        layout.addWidget(qt.QLabel(_("inter video URL")))
        self.videoURL=qt.QLineEdit()
        self.videoURL.setAccessibleName(_("inter video URL"))
        layout.addWidget(self.videoURL)
        layout.addWidget(qt.QLabel(_("save as")))
        self.saveAS=qt.QComboBox()
        self.saveAS.addItems([_("text"),"html","srt"])
        self.saveAS.setAccessibleName(_("save as"))
        layout.addWidget(self.saveAS)
        self.get=qt.QPushButton(_("get"))
        self.get.setDefault(True)
        self.get.clicked.connect(self.on_get)
        layout.addWidget(self.get)
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_get(self):
        videoID=""
        videoUrl=self.videoURL.text()
        if videoUrl.startswith("https://youtu.be/"):
            videoID=videoUrl.split("https://youtu.be/")[1]
        if videoID:
            try:
                html=[]
                text=[]
                srt=[]
                trans_list=YouTubeTranscriptApi.get_transcript(videoID)
                if trans_list:
                    for i, transcript in enumerate(trans_list, start=1):
                        start_time = datetime.timedelta(seconds=transcript['start'])
                        end_time = datetime.timedelta(seconds=transcript['start'] + transcript['duration'])
                        srt.append(f"{i}\n{start_time} --> {end_time}\n{transcript['text']}\n")
                        text.append(transcript['text'])
                        html.append(f"<p>{transcript['text']}</p>")
                    file=qt.QFileDialog(self)
                    file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
                    format=""
                    index=self.saveAS.currentIndex()
                    if index==0:
                        format="txt"
                    elif index==1:
                        format="html"
                    else:
                        format="srt"
                    file.setDefaultSuffix(format)
                    file.setNameFilters(["files(*.{})".format(format    )])
                    if file.exec()==file.DialogCode.Accepted:
                        with open(file.selectedFiles()[0],"w",encoding="utf-8") as result:
                            if index==0:
                                result.write("\n".join(text))
                            elif index==1:
                                result.write("\n".join(html))
                            else:
                                result.write("\n".join(srt))
                else:
                    qt.QMessageBox.information(self,_("info"),_("no subtitles fownd"))
            except Exception as error:
                print(error)
                qt.QMessageBox.warning(self,_("error"),_("please try later"))
        else:
            qt.QMessageBox.warning(self,_("error"),_("video id not fownd"))
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()
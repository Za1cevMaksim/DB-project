#design imports
import kivy
import kivymd
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import WipeTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp,sp
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import SoundFFPy

#bd imports
import db_insert
import db_select
import get_song
import other_func

user='users'
password='123456'

pauseSec=0
SoundLoader.register(SoundFFPy)
song = SoundLoader.load("")
with open('db_create.sql', 'r') as f:
    setup_sql = f.read()


#bd={31:False,"count":34,"name":"Kill you","author":"Eminem"}
#загрузка всех данных пользователя
class LoginPage(MDScreen):
    login = ObjectProperty(None)
    password = ObjectProperty(None)
    def logIn(self):
        login = self.login.text
        password = self.password.text
        users=db_select.print_users(setup_sql)

        for i in range(0,len(users)):
            if(login == users[i][0] and password==users[i][1]):
                global logged_user
                logged_user = users[i][0]
                app.root.ids.manager.transition=WipeTransition()
                app.theme_cls.theme_style=users[i][2]
                return True
        else:
            return False

class RegPage(MDScreen):

    login = ObjectProperty(None)
    password_users = ObjectProperty(None)
    def addToBase(self):
        login = self.reg_login.text
        password_users = self.reg_pass.text
        all_users=db_select.print_users(setup_sql)
        for i in range(0,len(all_users)):
            if all_users[i][0]==login:
                return False

        if login!='' and password_users!='':
            db_insert.insert_users(setup_sql, user,password, login,password_users)
            return True
        return False
class MDIconButton2(MDIconButton):
    _default_icon_pad = max(dp(48) - sp(48), 0)
    def init(self,*args,**kwargs):
        super(MDIconButton2,self).init(*args,**kwargs)
    def set_radius(self, *args) -> None:
        if self.rounded_button:
            self._radius = self.height /10

class MainPage(MDScreen):
    pass
class OptionsPage(MDScreen):
    pass
class PlaylistPage(MDScreen):
    pass
class SearchPage(MDScreen):
    pass
class DBMusicApp(MDApp):
    def isLiked(self,songname)->bool:
        res=other_func.check_favorite(setup_sql,user,password,logged_user,songname[0],songname[1])
        return res[0][0]
    def isPlaying(self)->str:
        if 1!=0:
            return "arrow-right-drop-circle-outline"
    def isShuffleDisabled(self)->str:
        if True!=True:
            return "shuffle-disabled"
        else:
            return "shuffle-variant"
    def prevPress(self,instance):
        pp=self.root.ids.keys()
        res=0
        for i in pp:
            if self.root.ids[i]==instance:
                res=i
                break
        textId = "text" + res[4:]
        target=self.root.ids[textId].text.split("\n")[0]
        for i in pp:
            if "name" in i:
                if self.root.ids[i].text==target:
                    if isinstance(song,SoundFFPy) and "play"+str(int(i[4:])-1) in pp and int(i[4:])-1>4:
                        song.stop()
                        song.unload()
                        self.playSong(self.root.ids["play"+str(int(i[4:])-1)])
    def pausePress(self,instance):
        if song.state=="play":
            song.stop()
            global pauseSec
            pauseSec = song.get_pos()
            instance.icon="arrow-right-drop-circle-outline"
        else:

            song.seek(pauseSec)
            song.play()
            instance.icon="pause-circle-outline"
        pass
    def nextPress(self,instance):
        pp=self.root.ids.keys()
        res=0
        for i in pp:
            if self.root.ids[i]==instance:
                res=i
                break
        textId = "text" + res[4:]
        target=self.root.ids[textId].text.split("\n")[0]
        for i in pp:
            if "name" in i:
                if self.root.ids[i].text==target:
                    if isinstance(song,SoundFFPy) and "play"+str(int(i[4:])+1) in pp:
                        song.stop()
                        song.unload()
                        self.playSong(self.root.ids["play"+str(int(i[4:])+1)])
    def likePress(self,instance):#чел лайкнул->в бд
        pp=self.root.ids.keys()
        res=0
        for i in pp:
            if self.root.ids[i]==instance:
                res=i
                break
        songname=[]
        songname.append(self.root.ids["name"+res[4:]].text)
        songname.append(self.root.ids["author"+res[4:]].text)
        other_func.add_favorite_song(setup_sql,user,password,logged_user,songname[0],songname[1])
        if self.isLiked(songname):
            self.root.ids[res].icon = "cards-heart"
        else:
            self.root.ids[res].icon = "cards-heart-outline"

    def repeatPress(self,instance):

        if isinstance(song,SoundFFPy) and song.loop:
            song.loop=False
            instance.icon="repeat-off"
        elif isinstance(song,SoundFFPy):
            song.loop=True
            instance.icon="repeat"

    def playSong(self,instance):
        pp=self.root.ids.keys()
        res=0
        for i in pp:
            if self.root.ids[i]==instance:
                res=i
                break
        songname=[self.root.ids["name"+str(res)[4:]].text,self.root.ids["author"+str(res)[4:]].text]
        path = get_song.fin(setup_sql,user,password,songname[0],songname[1])
        global song
        song = SoundLoader.load(path)
        song.play()
        for i in range(5):
            self.root.ids["play"+str(i)].icon="pause-circle-outline"
            self.root.ids["text"+str(i)].text=songname[0]+"\n"+songname[1]
    def toAllList(self,instance):
        self.root.ids.manager.current="all"
        self.root.ids.allPage.galllayout = MDGridLayout(cols=4, padding=2,size_hint=(1, None))
        self.root.ids.allPage.galllayout.bind(minimum_height=self.root.ids.allPage.galllayout.setter("height"))

        bd=other_func.search_song(setup_sql,user,password,logged_user,"")
        print(bd[0])
        for i in range(len(bd)):
            playbtn = MDIconButton2(icon="arrow-right-drop-circle-outline", icon_size="32sp", on_press=self.playSong)
            nameLab2 = MDLabel(text=bd[i][1], halign="center")
            authorLab = MDLabel(text=bd[i][2], halign="center")
            if(bd[i][3]==True):
                like = MDIconButton2(icon="cards-heart", icon_size="32sp", on_press=self.likePress)
            else:
                like = MDIconButton2(icon="cards-heart-outline", icon_size="32sp", on_press=self.likePress)
            self.root.ids.allPage.galllayout.add_widget(playbtn)
            self.root.ids.allPage.galllayout.add_widget(nameLab2)
            self.root.ids.allPage.galllayout.add_widget(authorLab)
            self.root.ids.allPage.galllayout.add_widget(like)
            self.root.ids["play"+str(i+5+len(bd)+100)]=playbtn
            self.root.ids["name" + str(i + 5+len(bd)+100)]=nameLab2
            self.root.ids["author" + str(i + 5+len(bd)+100)]=authorLab
            self.root.ids["like" + str(i + 5+len(bd)+100)]=like
        if "scroll3" in self.root.ids.keys():
            self.root.ids.allFlayout.remove_widget(self.root.ids.scroll3)
        self.root.ids.allPage.scroll3 = MDScrollView(size_hint=(0.7, None), size=(0.7 * self.root.width, 0.8 * self.root.height - self.root.ids.prev0.height),pos_hint={"x": 0.3, "y": self.root.ids.prev0.height / self.root.height}, bar_width=5,bar_pos_y="right", bar_color=(171 / 255, 177 / 255, 177 / 255, 0.42))
        self.root.ids["scroll3"] = self.root.ids.allPage.scroll3
        self.root.ids.allPage.scroll3.add_widget(self.root.ids.allPage.galllayout)
        self.root.ids.allFlayout.add_widget(self.root.ids.allPage.scroll3)
    def toPlaylist(self,instance):
        self.root.ids.manager.current="play"
        self.root.ids.playPage.glayout = MDGridLayout(cols=4, padding=2,size_hint=(1, None))
        self.root.ids.playPage.glayout.bind(minimum_height=self.root.ids.playPage.glayout.setter("height"))

        bd=other_func.return_favorite(setup_sql,user,password,logged_user)

        for i in range(len(bd)):
            playbtn = MDIconButton2(icon="arrow-right-drop-circle-outline", icon_size="32sp", on_press=self.playSong)
            nameLab2 = MDLabel(text=bd[i][0], halign="center")
            authorLab = MDLabel(text=bd[i][1], halign="center")
            like = MDIconButton2(icon="cards-heart", icon_size="32sp", on_press=self.likePress)
            self.root.ids.playPage.glayout.add_widget(playbtn)
            self.root.ids.playPage.glayout.add_widget(nameLab2)
            self.root.ids.playPage.glayout.add_widget(authorLab)
            self.root.ids.playPage.glayout.add_widget(like)
            self.root.ids["play"+str(i+5)]=playbtn
            self.root.ids["name" + str(i + 5)]=nameLab2
            self.root.ids["author" + str(i + 5)]=authorLab
            self.root.ids["like" + str(i + 5)]=like
        if "scroll" in self.root.ids.keys():
            self.root.ids.flayout.remove_widget(self.root.ids.scroll)
        self.root.ids.playPage.scroll = MDScrollView(size_hint=(0.7, None), size=(0.7 * self.root.width, 0.8 * self.root.height - self.root.ids.prev0.height),pos_hint={"x": 0.3, "y": self.root.ids.prev0.height / self.root.height}, bar_width=5,bar_pos_y="right", bar_color=(171 / 255, 177 / 255, 177 / 255, 0.42))
        self.root.ids["scroll"] = self.root.ids.playPage.scroll
        self.root.ids.playPage.scroll.add_widget(self.root.ids.playPage.glayout)
        self.root.ids.flayout.add_widget(self.root.ids.playPage.scroll)


    def search_by_text(self,search_text):
        if search_text!="":
            self.root.ids.search_label.text=search_text
            self.root.ids.manager.current="search"

            self.root.ids.searchPage.searchGlayout = MDGridLayout(cols=4, padding=2, size_hint=(1, None))
            self.root.ids.searchPage.searchGlayout.bind(minimum_height=self.root.ids.searchPage.searchGlayout.setter("height"))
            bd=other_func.search_song(setup_sql,user,password,logged_user,search_text)
            for i in range(len(bd)):
                if bd[i][3]:
                    playbtn = MDIconButton2(icon="arrow-right-drop-circle-outline", icon_size="32sp", on_press=self.playSong)
                    nameLab2 = MDLabel(text=bd[i][1], halign="center")
                    authorLab = MDLabel(text=bd[i][2], halign="center")
                    like = MDIconButton2(icon="cards-heart", icon_size="32sp", on_press=self.likePress)
                    self.root.ids.searchPage.searchGlayout.add_widget(playbtn)
                    self.root.ids.searchPage.searchGlayout.add_widget(nameLab2)
                    self.root.ids.searchPage.searchGlayout.add_widget(authorLab)
                    self.root.ids.searchPage.searchGlayout.add_widget(like)
                    self.root.ids["play" + str(i + 5+len(bd))] = playbtn
                    self.root.ids["name" + str(i + 5+len(bd))] = nameLab2
                    self.root.ids["author" + str(i + 5+len(bd))] = authorLab
                    self.root.ids["like" + str(i + 5+len(bd))] = like
            if "scroll2" in self.root.ids.keys():
                self.root.ids.searchFlayout.remove_widget(self.root.ids.scroll2)
            self.root.ids.searchPage.scroll2 = MDScrollView(size_hint=(0.7, None), size=(0.7 * self.root.width, 0.8 * self.root.height - self.root.ids.prev0.height), pos_hint={"x": 0.3,"y": self.root.ids.prev0.height / self.root.height},bar_width=5, bar_pos_y="right", bar_color=(171 / 255, 177 / 255, 177 / 255, 0.42))
            self.root.ids["scroll2"] = self.root.ids.searchPage.scroll2
            self.root.ids.searchPage.scroll2.add_widget(self.root.ids.searchPage.searchGlayout)
            self.root.ids.searchFlayout.add_widget(self.root.ids.searchPage.scroll2)

    def search_by_textall(self,search_text):
        if search_text!="":
            self.root.ids.search_label.text=search_text
            self.root.ids.manager.current="search"

            self.root.ids.searchPage.searchGlayout = MDGridLayout(cols=4, padding=2, size_hint=(1, None))
            self.root.ids.searchPage.searchGlayout.bind(minimum_height=self.root.ids.searchPage.searchGlayout.setter("height"))
            bd=other_func.search_song(setup_sql,user,password,logged_user,search_text)
            for i in range(len(bd)):
                if bd[i][3]:
                    playbtn = MDIconButton2(icon="arrow-right-drop-circle-outline", icon_size="32sp", on_press=self.playSong)
                    nameLab2 = MDLabel(text=bd[i][1], halign="center")
                    authorLab = MDLabel(text=bd[i][2], halign="center")
                    like = MDIconButton2(icon="cards-heart", icon_size="32sp", on_press=self.likePress)
                    self.root.ids.searchPage.searchGlayout.add_widget(playbtn)
                    self.root.ids.searchPage.searchGlayout.add_widget(nameLab2)
                    self.root.ids.searchPage.searchGlayout.add_widget(authorLab)
                    self.root.ids.searchPage.searchGlayout.add_widget(like)
                    self.root.ids["play" + str(i + 5+len(bd))] = playbtn
                    self.root.ids["name" + str(i + 5+len(bd))] = nameLab2
                    self.root.ids["author" + str(i + 5+len(bd))] = authorLab
                    self.root.ids["like" + str(i + 5+len(bd))] = like
            if "scroll2" in self.root.ids.keys():
                self.root.ids.searchFlayout.remove_widget(self.root.ids.scroll2)
            self.root.ids.searchPage.scroll2 = MDScrollView(size_hint=(0.7, None), size=(0.7 * self.root.width, 0.8 * self.root.height - self.root.ids.prev0.height), pos_hint={"x": 0.3,"y": self.root.ids.prev0.height / self.root.height},bar_width=5, bar_pos_y="right", bar_color=(171 / 255, 177 / 255, 177 / 255, 0.42))
            self.root.ids["scroll2"] = self.root.ids.searchPage.scroll2
            self.root.ids.searchPage.scroll2.add_widget(self.root.ids.searchPage.searchGlayout)
            self.root.ids.searchFlayout.add_widget(self.root.ids.searchPage.scroll2)

    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="BlueGray"
        return Builder.load_file("design.kv")
if __name__=='__main__':
    app=DBMusicApp()
    app.run()
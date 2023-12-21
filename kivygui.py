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

#bd imports
import db_insert
import db_select
import main

user='users'
password='123456'


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
    password = ObjectProperty(None)
    def addToBase(self):
        login = self.reg_login.text
        password = self.reg_pass.text
        all_users=db_select.print_users(setup_sql)
        for i in range(0,len(all_users)):
            if all_users[i][0]==login:
                return False

        if login!='' and password!='':
            db_insert.insert_users(setup_sql, login, password)
            return True
        return False
class MDIconButton2(MDIconButton):
    _default_icon_pad = max(dp(48) - sp(48), 0)
    def init(self,*args,**kwargs):
        super(MDIconButton2,self).init(*args,**kwargs)
    def set_radius(self, *args) -> None:
        if self.rounded_button:
            self._radius = self.height /10

#here's methods for all screens, that have player underneath

class MainTemplate(MDScreen):
    def isLiked(self,id)->str:
        id=id.split("text")[1]
        if self.root.ids["shuffle"+id].icon!="shuffle-disabled":
            return "cards-heart"
        else:
            return "cards-heart-outline"
    def isPlaying(self)->str:
        if 1!=0:
            return "arrow-right-drop-circle-outline"
    def isShuffleDisabled(self)->str:
        if bd[31]!=True:
            return "shuffle-disabled"
        else:
            return "shuffle-variant"
    def prevPress(self,instance):
        pass
    def pausePress(self,instance):
        pass
    def nextPress(self,instance):
        pass
    def likePress(self,instance):#чел лайкнул->в бд
        pass
    def shufflePress(self,instance):
        pass
    pass

#so there's no need in code for next class
class MainPage(MainTemplate):
    pass
class OptionsPage(MainTemplate):
    pass
class PlaylistPage(MainTemplate):
    pass
class SearchPage(MainTemplate):
    pass
class DBMusicApp(MDApp):
    def isLiked(self)->str:
        if False==False:
            return "cards-heart"
        else:
            return "cards-heart-outline"
    def isPlaying(self)->str:
        if 1!=0:
            return "arrow-right-drop-circle-outline"
    def isShuffleDisabled(self)->str:
        if True!=True:
            return "shuffle-disabled"
        else:
            return "shuffle-variant"
    def prevPress(self,instance):
        pass
    def pausePress(self,instance):
        pass
    def nextPress(self,instance):
        pass
    def likePress(self,instance):#чел лайкнул->в бд
        pass
    def shufflePress(self,instance):
        pass
    def playSong(self,instance):
        pp=self.root.ids.keys()
        res=0
        for i in pp:
            if self.root.ids[i]==instance:
                res=i
                break
        for i in range(4):
            self.root.ids["play"+str(i)].icon="pause-circle-outline"
            self.root.ids["like"+str(i)].icon=self.isLiked()
            self.root.ids["text"+str(i)].text=self.root.ids["name"+str(res)[4:]].text+"\n"+self.root.ids["author"+str(res)[4:]].text
        pass
    def toPlaylist(self,instance):
        self.root.ids.manager.current="play"
        self.root.ids.playPage.glayout = MDGridLayout(cols=4, padding=2,size_hint=(1, None))
        self.root.ids.playPage.glayout.bind(minimum_height=self.root.ids.playPage.glayout.setter("height"))

        bd=main.return_favorite(setup_sql,user,password,logged_user)

        for i in range(len(bd)):
            playbtn = MDIconButton2(icon="arrow-right-drop-circle-outline", icon_size="32sp", on_press=self.playSong)
            nameLab2 = MDLabel(text=bd[i][0], halign="center")
            authorLab = MDLabel(text=bd[i][1], halign="center")
            like = MDIconButton2(icon="cards-heart", icon_size="32sp", on_press=self.root.ids.playPage.likePress)
            self.root.ids.playPage.glayout.add_widget(playbtn)
            self.root.ids.playPage.glayout.add_widget(nameLab2)
            self.root.ids.playPage.glayout.add_widget(authorLab)
            self.root.ids.playPage.glayout.add_widget(like)
            self.root.ids["play"+str(i+4)]=playbtn
            self.root.ids["name" + str(i + 4)]=nameLab2
            self.root.ids["author" + str(i + 4)]=authorLab
            self.root.ids["like" + str(i + 4)]=like
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
            for i in range(bd["count"]):
                playbtn = MDIconButton2(icon=self.root.ids.searchPage.isPlaying(), icon_size="32sp",
                                        on_press=self.root.ids.searchPage.pausePress)
                nameLab2 = MDLabel(text=bd["name"] + str(i), halign="center")
                authorLab = MDLabel(text=bd["author"], halign="center")
                like = MDIconButton2(icon=self.root.ids.searchPage.isLiked(), icon_size="32sp",
                                     on_press=self.root.ids.searchPage.likePress)
                self.root.ids.searchPage.searchGlayout.add_widget(playbtn)
                self.root.ids.searchPage.searchGlayout.add_widget(nameLab2)
                self.root.ids.searchPage.searchGlayout.add_widget(authorLab)
                self.root.ids.searchPage.searchGlayout.add_widget(like)
            self.root.ids.searchPage.scroll = MDScrollView(size_hint=(0.7, None), size=(0.7 * self.root.width, 0.8 * self.root.height - self.root.ids.prev0.height), pos_hint={"x": 0.3,"y": self.root.ids.prev0.height / self.root.height},bar_width=5, bar_pos_y="right", bar_color=(171 / 255, 177 / 255, 177 / 255, 0.42))
            self.root.ids.searchPage.scroll.add_widget(self.root.ids.searchPage.searchGlayout)
            self.root.ids.searchFlayout.add_widget(self.root.ids.searchPage.scroll)

            pass
    def build(self):
        self.favorite=4
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="BlueGray"
        return Builder.load_file("design.kv")
if __name__=='__main__':
    app=DBMusicApp()
    app.run()
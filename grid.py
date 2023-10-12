#!/usr/bin/python

import wx
import random

class Example(wx.Frame): 
   
    def __init__(self, parent, title): 
      super(Example, self).__init__(parent, title = title,size = (500,500)) 
      self.InitUI() 
      self.Centre() 
      self.Show()

    def refresh_all(self):
        for i in range(0,81): 
            self.button[i].SetBackgroundColour(self.list[i])

    def reset_all(self):
        self.clicked_id = 81
        self.list = ["empty" for i in range(81)]
        self.path = [0 for i in range(81)]
        self.x = [0 for i in range(81)]
        self.y = [0 for i in range(81)]
        self.z_east = [0 for i in range(81)]
        self.z_west = [0 for i in range(81)]
        self.score = 0
        self.new_grid()
        self.refresh_all()

    def check_grid(self):
        empty_list = []
        for i in range(0,81):
            if self.list[i] == "empty":
                empty_list.append(i)
        print(empty_list)
        if len(empty_list) < 3:
            msg = 'Game over!' + 'Score: ' + str(self.score) 
            wx.MessageBox(msg, 'Info', wx.OK | wx.ICON_INFORMATION)
            print("game over!")
            self.reset_all()
            
    def new_grid(self):
        color_list = ["red", "tan", "yellow", "green", "brown", "blue", "pink"]
        empty_list = []
        for i in range(0,81):
            if self.list[i] == "empty":
                empty_list.append(i)
        print(empty_list)
        if len(empty_list) < 3:
            msg = 'Game over!' + '  Score: ' + str(self.score) 
            wx.MessageBox(msg, 'Info', wx.OK | wx.ICON_INFORMATION)
            print("game over!")
            self.reset_all()
        else:
            for j in range(0,3):
                index = random.choice(empty_list)
                self.list[index] = random.choice(color_list)
                empty_list.remove(index)

    def scan_x(self):
        for i in range(0,9):
            for j in range(0,9):
                x = i*9+j
                color = self.list[x]
                if color == "empty":
                    self.x[x] = 0
                else:
                    count=1
                    k=j+1
                    while k < 9:
                        if color == self.list[i*9+k]:
                            count=count+1
                            k=k+1
                        else:
                            break
                    self.x[x] = count

    def scan_y(self):
        for i in range(0,9):
            for j in range(0,9):
                y = i+j*9
                color = self.list[y]
                if color == "empty":
                    self.y[y] = 0
                else:
                    count=1
                    k=j+1
                    while k < 9:
                        if color == self.list[i+k*9]:
                            count=count+1
                            k=k+1
                        else:
                            break
                    self.y[y] = count

    def scan_z_east(self):
        for i in range(0,9):
            for j in range(0,9):
                z = i+j*9
                color = self.list[z]
                if color == "empty":
                    self.z_east[z] = 0
                else:
                    count=1
                    m=j+1
                    n=i+1
                    while m < 9 and n < 9:
                        if color == self.list[n+m*9]:
                            count=count+1
                            m=m+1
                            n=n+1
                        else:
                            break
                    self.z_east[z] = count

    def scan_z_west(self):
        for i in range(0,9):
            for j in range(0,9):
                z = i+j*9
                color = self.list[z]
                if color == "empty":
                    self.z_west[z] = 0
                else:
                    count=1
                    m=j+1
                    n=i-1
                    while m < 9 and n >= 0:
                        if color == self.list[n+m*9]:
                            count=count+1
                            m=m+1
                            n=n-1
                        else:
                            break
                    self.z_west[z] = count

    def add_score(self,x):
        self.score = self.score + int(x*10)

    def clear_all(self):
        for i in range(0,81):
            x=self.x[i]
            y=self.y[i]
            z_east=self.z_east[i]
            z_west=self.z_west[i]           
            if x > 4:
                for j in range(i,i+x):
                    self.list[j] = "empty"
                    self.x[j] = 0
                self.add_score(x)
            if y > 4:
                for j in range(i,i+y*9,9):
                    self.list[j] = "empty"
                    self.y[j] = 0
                self.add_score(y)
            if z_east > 4:
                for j in range(i,i+10*z_east,10):
                    self.list[j] = "empty"
                    self.z_east[j] = 0
                self.add_score(z_east)
            if z_west > 4:
                for j in range(i,i+8*z_west,8):
                    self.list[j] = "empty"
                    self.z_west[j] = 0
                self.add_score(z_west)

    def scan_all(self):
        self.scan_x()
        self.scan_y()
        self.scan_z_east()
        self.scan_z_west()
        self.clear_all()

    def one_step(self, begin, end):
        self.path[begin] = 1
        y = int(begin/9)
        x = int(begin%9)
        print(begin,x,y)
        buddy_grid=[]
        if y-1 >= 0:
            buddy_grid.append(int(x + 9*(y-1)))
        if x+1 < 9:
            buddy_grid.append(int((x+1) + 9*y))
        if y+1 < 9:
            buddy_grid.append(int(x + 9*(y+1)))
        if x-1 >= 0:
            buddy_grid.append(int((x-1) + 9*y))
        print(buddy_grid)
        buddy_grid=[x for x in buddy_grid if x >= 0]
        buddy_grid=[x for x in buddy_grid if x < 82]
        print(buddy_grid)
        buddy_grid=[x for x in buddy_grid if self.list[x] == "empty"]
        buddy_grid=[x for x in buddy_grid if self.path[x] == 0]
        print(buddy_grid)

        if len(buddy_grid) == 0:
           return "finish"

        for x in buddy_grid:
            self.path[x] = 2
            self.button[x].SetBackgroundColour("grey")
        
        for x in range(len(self.path)):
            if self.path[x] == 2:
                self.one_step(x, end)
      
      # clicked_id为81的情况下：
      #     如果目标格非empty，则记录clicked_id
      #     如果目标格为empty，则不响应
      # clicked_id小于81的情况下：
      # 如果目标格非empty，
      #     如果目标格与clicked_id相同，则用户重复单击某格，clicked_id保持不变
      #     如果目标格与clicked_id不同，则用户调整出发点，clicked_id变化
      # 如果目标格为empty
      #     判断是否可以到达？如果不可达，则出发点不变，clicked_id保持不变
      #     如果可达，则移动，判断是否消除，计分，随机产生三个新的颜色格

    def onButton(self, event):
      ID=event.GetEventObject().GetLabel()
      print(ID)
      clicked_id = int(ID)
      if self.clicked_id == 81:
         if self.list[clicked_id] != "empty":
            self.clicked_id = clicked_id
            self.button[clicked_id].SetForegroundColour("white")
         else:
            print("this is empty")
            #do nothing

      elif self.clicked_id < 81:
         if self.list[clicked_id] != "empty":
            if self.clicked_id == clicked_id:
               print("do nothing")
            else:
               self.button[self.clicked_id].SetForegroundColour("black")
               self.clicked_id = clicked_id
               self.button[clicked_id].SetForegroundColour("white")
         else:
            begin=self.clicked_id
            end = clicked_id
            print(begin, end)
            self.path = [0 for i in range(81)]
            self.one_step(begin, end)
            if self.path[end] == 1: #find the way
                self.button[self.clicked_id].SetForegroundColour("black")
                self.clicked_id = 81
                self.list[end] = self.list[begin]
                self.list[begin] = "empty"
                self.refresh_all()
                self.scan_all()
                print(self.x)
                print(self.y)
                print(self.z_east)
                print(self.z_west)
                print(self.list)
                self.new_grid()
                self.refresh_all()
                self.scan_all()
                self.refresh_all()
                self.check_grid()
                print(self.path)
                self.path = [0 for i in range(81)]
                print("--ok--")
            else:
                print("cannot find way!!!")

      else: #id > 81 
         print("something wrong!!!")
    
      self.statusBar.SetStatusText("SCORE: " + str(self.score))
      print("Button pressed")

    def onToolBar(self,event):
        print(event.GetId())
        self.reset_all()

    def show_popup(self):
        # 创建一个弹出窗口
        popup = wx.PopupWindow(self.panel, size=(200, 100))
        popup.SetPosition((150, 150))
        popup.SetBackgroundColour(wx.Colour(255, 255, 255))
        popup.SetForegroundColour(wx.Colour(0, 0, 0))
        # 在弹出窗口中添加文本
        text = wx.StaticText(popup, label='Hello, World!', pos=(50, 30))
        # 显示弹出窗口
        popup.Show()

    def InitUI(self):
      self.panel = wx.Panel(self) 
      self.gs = wx.GridSizer(9, 9, 1, 1)

      self.clicked_id = 81
      self.list = ["empty" for i in range(81)]
      self.path = [0 for i in range(81)]
      self.x = [0 for i in range(81)]
      self.y = [0 for i in range(81)]
      self.z_east = [0 for i in range(81)]
      self.z_west = [0 for i in range(81)]
      self.score = 0
      self.button = []

      for i in range(0,81): 
         button = wx.Button(self.panel,label = str(i),style=wx.BORDER_NONE)
         #button = wx.BitmapButton(p,id=i,bitmap=wx.Bitmap('法师 (小) (小).jpg'))
         self.button.append(button)
         self.button[i].Bind(wx.EVT_BUTTON, self.onButton, self.button[i])
         self.gs.Add(self.button[i],0,wx.EXPAND) 
         self.panel.SetSizer(self.gs) 
      
      self.statusBar = self.CreateStatusBar()
      self.toolBar = self.CreateToolBar()
      self.toolBar.AddSimpleTool(101, wx.Bitmap('法师.jpg'))
      self.toolBar.Realize()
      self.Bind(wx.EVT_TOOL, self.onToolBar)
      self.new_grid() 
      self.refresh_all()

app = wx.App() 
Example(None, title = 'Grid Demo') 
app.MainLoop()


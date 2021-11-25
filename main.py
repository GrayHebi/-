import BD
from tkinter import *
from tkinter import messagebox as mb
import json
#Создаем окно приложения
win = Tk()
win.title('Учет расходов')
win.geometry("900x650")
#Список глобальных переменных
admin = None
user = None
ServerPageVar = None
LogPageVar = None
RegPageVar = None
MainPageVar = None
WinVar = None
#Класс страницы регистрации администратора
class ServerPage(Frame):
    def __init__(self, root):
        self.root = root
        self.main = Frame(self.root)
        LbHost = Label(self.main,text="IP")
        self.EntHost = Entry(self.main,width=30)
        LbPort = Label(self.main,text="Порт")
        self.EntPort = Entry(self.main,width=30)
        LbAdmin = Label(self.main,text="Логин администратора")
        self.EntAdmin = Entry(self.main,width=30)
        LbPassword = Label(self.main,text="Пароль")
        self.EntPassword = Entry(self.main,width=30, show='*')
        BtnSubmit = Button(self.main, text="Готово", command=self.SubmitBtn)
        self.main.pack(pady=180)
        LbHost.pack()
        self.EntHost.pack(pady=5)
        LbPort.pack()
        self.EntPort.pack(pady=5)
        LbAdmin.pack()
        self.EntAdmin.pack(pady=5)
        LbPassword.pack()
        self.EntPassword.pack(pady=5)
        BtnSubmit.pack()
    #Метод привязанный к кнопке, регестрирует администратора
    def SubmitBtn(self):
        global admin
        global LogPageVar
        #Создание локального файла с данными администратора
        file = open('admin.json','w')
        data = {'host':self.EntHost.get(),'port':self.EntPort.get(),'admin':self.EntAdmin.get(),'pass':self.EntPassword.get()}
        json.dump(data, file)
        file.close
        try:
            admin = BD.UserBD(self.EntHost.get(),int(self.EntPort.get()),self.EntAdmin.get(),self.EntPassword.get())
            try:
                admin.CreateAdminBD()
            except:
                pass
            LogPageVar = LogPage(self.root)
            self.main.destroy()
        except BD.pymysql.OperationalError as e:
            mb.showerror(
            "Ошибка", 
            str(e))
#Класс страницы входа для пользователя
class LogPage(Frame):
    def __init__(self, root):
        self.root = root
        self.main = Frame(self.root)
        LbLogin = Label(self.main,text="Логин")
        self.EntLogin = Entry(self.main,width=30)
        LbPassword = Label(self.main,text="Пароль")
        self.EntPassword = Entry(self.main,width=30, show='*')
        BtnLogin = Button(self.main, text="Войти", width=12, command=self.LogBtn)
        BtnReg = Button(self.main, text="Создать\nпользователя", command=self.RegBtn)
        self.main.pack(pady=200)
        LbLogin.pack()
        self.EntLogin.pack(pady=5)
        LbPassword.pack()
        self.EntPassword.pack(pady=5)
        BtnLogin.pack(pady=5)
        BtnReg.pack(pady=5)
    #Метод перехода на страницу регистрации
    def RegBtn(self):
        global RegPageVar
        RegPageVar = RegPage(self.root)
        self.main.destroy()
    #Метод входа в учетную запись
    def LogBtn(self):
        global admin
        global user
        global RegPageVar
        global MainPageVar
        UserData = admin.GetUserData()
        for Data in UserData:
            if ((Data[0]==self.EntLogin.get())and(Data[1]==self.EntPassword.get())):
                user = BD.UserBD(admin.host, admin.port,self.EntLogin.get(),self.EntPassword.get())
                MainPageVar = MainPage(self.root)
                self.main.destroy()
#Класс страницы регистрации
class RegPage(Frame):
    def __init__(self, root):
        self.root = root
        self.main = Frame(self.root)
        LbLogin = Label(self.main,text="Логин")
        self.EntLogin = Entry(self.main,width=30)
        LbPassword = Label(self.main,text="Пароль")
        self.EntPassword = Entry(self.main,width=30, show='*')
        LbRePassword = Label(self.main,text="Повторите пароль")
        self.EntRePassword = Entry(self.main,width=30, show='*')
        BtnReg = Button(self.main, text="Готово", command=self.RegBtn)
        BtnExit = Button(self.main, text="Назад", command=self.ExitBtn)
        self.main.pack(pady=200)
        LbLogin.pack()
        self.EntLogin.pack(pady=5)
        LbPassword.pack()
        self.EntRePassword.pack(pady=5)
        LbRePassword.pack()
        self.EntPassword.pack(pady=5)
        BtnReg.pack()
        BtnExit.pack(pady=5)
    #Метод возврата на страницу входа
    def ExitBtn(self):
        global LogPageVar
        LogPageVar = LogPage(self.root)
        self.main.destroy()
    #Метод регистрации пользователя
    def RegBtn(self):
        global admin
        global LogPageVar
        if (self.EntPassword.get()==self.EntRePassword.get()):
            tmp = admin.CreateUser(self.EntLogin.get(),self.EntRePassword.get())
            #Проверка на ошибки создания пользователя
            if (tmp==None):
                LogPageVar = LogPage(self.root)
                self.main.destroy()
            else:
                mb.showerror(
                    "Ошибка", 
                    str(tmp))
            
        else:
            mb.showerror(
                "Ошибка", 
                "Пароли не совпадают!")
#Класс окна со списком расходов
class MainPage(Frame):
    def __init__(self, root):
        self.root = root
        self.main = Frame(self.root)
        self.LiBProduct = Listbox(self.main,width=74,font=("Courier"), height=20,selectmode=SINGLE)
        child = Frame(self.main)
        BtnAdd = Button(child,width=15,  text="Добавить", command=self.AddBtn)
        BtnTransform = Button(child,width=15,  text="Изменить", command=self.UpdateBtn)
        BtnDel = Button(child,width=15,  text="Удалить", command=self.DelBtn)
        BtnStat = Button(child,width=15,  text="Статистика", command=self.StatBtn)
        BtnExit = Button(child,width=15,  text="Выйти", command=self.ExitBtn)
        self.main.pack(side=LEFT)
        self.LiBProduct.pack(side=LEFT)
        child.pack(side=RIGHT)
        BtnAdd.pack()
        BtnTransform.pack()
        BtnDel.pack()
        BtnStat.pack()
        BtnExit.pack(pady=20)
        self.UpdateLiB()
    #Метод открытия окна со статистикой расходов
    def StatBtn(self):
        global WinVar
        WinVar = StatisticWin()
    #Метод открытия окна для записи товара
    def AddBtn(self):
        global WinVar
        WinVar = AddWin()
    #Метод открытия окна изменения записи товара
    def UpdateBtn(self):
        global WinVar
        data = user.GetProductsData(self.GetSelectRow())
        WinVar = UpdeteWin(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4])
    #Метод возврата на страницу входа
    def ExitBtn(self):
        global LogPageVar
        user = None
        LogPageVar = LogPage(self.root)
        self.main.destroy()
    #Метод удаления записи
    def DelBtn(self):
        user.DeleteProduct(self.GetSelectRow())
        self.UpdateLiB()
    #Метод обновления списка товаров
    def UpdateLiB(self):
        self.LiBProduct.delete(0, END)
        ProductsData = user.GetProductsData()
        for Data in ProductsData:
            tmp = list(Data)
            tmp[0] = ("{:20}".format(tmp[0]))
            tmp[1] = ("{:<5d}".format(tmp[1]))
            tmp[2] = ("{:<7d}".format(tmp[2]))
            tmp[3] = ("{:20}".format(tmp[3]))
            tmp[4] = ("{:%Y-%m-%d}".format(tmp[4]))
            self.LiBProduct.insert(END, ''.join(tmp))
    #Метод получения данных выбранной записи
    def GetSelectRow(self):
        Data = self.LiBProduct.get(self.LiBProduct.curselection())
        name = Data[:19]
        name = name.strip()
        date = Data[-10:]
        return (name, date)
#Класс окна добавления записи
class AddWin:
    def __init__(self):
        self.main = Toplevel()
        self.main.geometry('300x300')
        LbName = Label(self.main,text="Название")
        self.EntName = Entry(self.main,width=30)
        LbCol = Label(self.main,text="Количество")
        self.EntCol = Entry(self.main,width=30)
        LbPrice = Label(self.main,text="Цена")
        self.EntPrice = Entry(self.main,width=30)
        LbCateg = Label(self.main,text="Категория")
        self.EntCateg = Entry(self.main,width=30)
        LbDate = Label(self.main,text="Дата покупки")
        self.EntDate = Entry(self.main,width=30)
        BtnAdd = Button(self.main,width=15,  text="Добавить", command=self.AddBtn)
        LbName.pack()
        self.EntName.pack()
        LbCol.pack()
        self.EntCol.pack()
        LbPrice.pack()
        self.EntPrice.pack()
        LbCateg.pack()
        self.EntCateg.pack()
        LbDate.pack()
        self.EntDate.pack()
        BtnAdd.pack()
    #Метод добавления записи в базу данных
    def AddBtn(self):
        global user
        global MainPageVar
        user.InsertIntoUserBD(self.EntName.get(),self.EntCol.get(),self.EntPrice.get(),self.EntCateg.get(),self.EntDate.get())
        MainPageVar.UpdateLiB()
        self.main.destroy()
#Класс окна изменения записи
class UpdeteWin:
    def __init__(self, name, col, price, categ, date):
        self.name = name
        self.date = str(date)
        self.main = Toplevel()
        self.main.geometry('300x300')
        LbName = Label(self.main,text="Название: {}".format(self.name))
        LbDate = Label(self.main,text="Дата покупки: {}".format(self.date))
        LbCol = Label(self.main,text="Количество")
        self.EntCol = Entry(self.main,width=30)
        LbPrice = Label(self.main,text="Цена")
        self.EntPrice = Entry(self.main,width=30)
        LbCateg = Label(self.main,text="Категория")
        self.EntCateg = Entry(self.main,width=30,)
        BtnUpdate = Button(self.main,width=15,  text="Изменить", command=self.UpdateBtn)
        LbName.pack()
        LbDate.pack()
        LbCol.pack()
        self.EntCol.pack()
        LbPrice.pack()
        self.EntPrice.pack()
        LbCateg.pack()
        self.EntCateg.pack()
        BtnUpdate.pack()
        self.EntCol.insert(0,col)
        self.EntPrice.insert(0,price)
        self.EntCateg.insert(0,categ)
    #Метод изменения записи в базе данных
    def UpdateBtn(self):
        global user
        global MainPageVar
        user.UpdateProduct(self.name,self.date,self.EntCol.get(),self.EntPrice.get(),self.EntCateg.get())
        MainPageVar.UpdateLiB()
        self.main.destroy()
#Класс окна статистики
class StatisticWin:
    def __init__(self):
        self.main = Toplevel()
        self.main.geometry('400x400')
        self.LiBProduct = Listbox(self.main,width=40,font=("Courier"), height=20,selectmode=BROWSE)
        self.LiBProduct.pack()
        frame = Frame(self.main)
        LbFirstDate = Label(frame,text="От: ")
        self.FirstDate = Entry(frame,width=10)
        LbSecondDate = Label(frame,text="До: ")
        self.SecondDate = Entry(frame,width=10)
        BtnSubmit = Button(frame, text="Создать", command=self.SubmitBtn)
        frame.pack()
        LbFirstDate.pack(side=LEFT)
        self.FirstDate.pack(side=LEFT)
        LbSecondDate.pack(side=LEFT)
        self.SecondDate.pack(side=LEFT)
        BtnSubmit.pack(side=LEFT)
    #Метод отображения статистики в виде списка
    def SubmitBtn(self):
        self.LiBProduct.delete(0, END)
        ProductsData = user.GetStatisticDate(self.FirstDate.get(),self.SecondDate.get())
        for Data in ProductsData:
            tmp = "{}:".format(Data)+str(ProductsData[Data])
            self.LiBProduct.insert(END, tmp)
#Начало работы программы
try:
    #Попытка открыть файл с данными администратора
    file = open('admin.json','r')
    #При отсутствии файла открытие страницы регистрации администратора
    if (file==None):
        ServerPageVar = ServerPage(win)
    else:
        #Создание экземпляра класса база данных администратора и пререход на страницу входа
        data = json.load(file)
        admin = BD.UserBD(data['host'],int(data['port']),data['admin'],data['pass'])
        LogPageVar = LogPage(win)
    file.close()
    #При неверных данных открытие страницы регистрации администратора
except:
    ServerPageVar = ServerPage(win)


#Создание графического интерфейса
win.mainloop()
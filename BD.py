import pymysql
#Класс для работы с базой данных
class UserBD:
    def __init__(self, host, port,user,passwd):
        #В init подключаемся к серверу и создаем курсор для работы с теминалом
        self.con = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   passwd=passwd)
        self.host = host
        self.port = port
        self.user = user
        self.mycursor = self.con.cursor()
    #Функция для создания пользователя выполняется от имени администратора MySql сервера
    def CreateUser(self, name, password):
        try:
            self.mycursor.execute("CREATE USER '"+name+"'@'"+self.host+"' IDENTIFIED BY '"+password+"';")
        except pymysql.OperationalError as e:
            return e
        self.mycursor.execute('CREATE DATABASE '+name+';')
        self.mycursor.execute("GRANT ALL ON "+name+" . * TO '"+name+"'@'"+self.host+"';")
        self.mycursor.execute('FLUSH PRIVILEGES;')
        self.mycursor.execute('USE '+name+';')
        Create = 'CREATE TABLE products(product_id INT NOT NULL AUTO_INCREMENT,product_name VARCHAR(20) NOT NULL,product_col INT NOT NULL, price INT NOT NULL, product_categ VARCHAR(20), bay_date DATE NOT NULL,PRIMARY KEY (product_id));'
        self.mycursor.execute(Create)
        self.mycursor.execute('USE Users;')
        Create = "INSERT INTO users(user_name, user_pass) VALUES('"+name+"', '"+password+"');"
        self.mycursor.execute(Create)
        self.con.commit()
    #Функция для создания табицы с данными пользователей выполняется от имени администратора MySql сервера
    def CreateAdminBD(self):
        self.mycursor.execute('CREATE DATABASE Users;')
        self.mycursor.execute('USE Users;')
        Create = 'CREATE TABLE users(user_id INT NOT NULL AUTO_INCREMENT,user_name VARCHAR(100) NOT NULL,user_pass VARCHAR(100) NOT NULL ,PRIMARY KEY (user_id));'
        self.mycursor.execute(Create)
    #Функция для получения списка пользователей выполняется от имени администратора MySql сервера
    def GetUserData(self):
        self.mycursor.execute('USE Users;')
        Command = "Select user_name, user_pass FROM users;"
        self.mycursor.execute(Command)
        res = self.mycursor.fetchall()
        self.con.commit()
        return res
    #Функция для записи продукта пользователя выполняется от имени пользователя
    def InsertIntoUserBD(self,name,col,price,categ,date):
        self.mycursor.execute('USE '+self.user+';')
        Create = "INSERT INTO products(product_name, product_col, price, product_categ, bay_date) VALUES('"+name+"', '"+col+"', '"+price+"', '"+categ+"', '"+date+"');"
        self.mycursor.execute(Create)
        self.con.commit()
    #Функция для получения списка продуктов пользователя выполняется от имени пользователя
    def GetProductsData(self, data=None):
        self.mycursor.execute('USE '+self.user+';')
        #Если аргумент функции не задан находим все
        if (data==None):
            Command = "Select product_name, product_col, price, product_categ, bay_date FROM products ORDER BY bay_date;"
        else:
            Command = "Select product_name, product_col, price, product_categ, bay_date FROM products WHERE product_name='"+data[0]+"' AND bay_date='"+data[1]+"';"
        self.mycursor.execute(Command)
        res = self.mycursor.fetchall()
        self.con.commit()
        return res
    #Функция для удаления продукта выполняется от имени пользователя
    def DeleteProduct(self,data):
        self.mycursor.execute('USE '+self.user+';')
        self.mycursor.execute("DELETE FROM products WHERE product_name='"+data[0]+"' AND bay_date='"+data[1]+"';")
        self.con.commit()
    #Функция для изменения записи пользователя выполняется от имени пользователя
    def UpdateProduct(self,name,date,col,price,categ):
        self.mycursor.execute('USE '+self.user+';')
        self.mycursor.execute("UPDATE products set product_col = '"+col+"', price='"+price+"', product_categ='"+categ+"' WHERE product_name='"+name+"' AND bay_date='"+date+"';")
        self.con.commit()
    #Функция для получения словаря категория=цена_за_единицу*количество за определенный период выполняется от имени пользователя
    def GetStatisticDate(self, datef, datet):
        Gateg = []
        Data = {}
        self.mycursor.execute('USE '+self.user+';')
        #Если вторая дата не указана ищем от первой даты до последней записи
        if (datet==''):
            Command = "Select product_col, price, product_categ FROM products WHERE bay_date >= '"+datef+"';"
        else:
            Command = "Select product_col, price, product_categ FROM products WHERE bay_date BETWEEN '"+datef+"' AND '"+datet+"';"
        self.mycursor.execute(Command)
        res = self.mycursor.fetchall()
        for i in res:
            Gateg.append(i[2])
        Gateg = list(set(Gateg))
        for i in Gateg:
            Data[i] = 0
        for i in res:
            Data[i[2]] += (i[0]*i[1])
        return Data
    #Функция закрытия базы данных
    def __del__(self):
        try:
            self.con.close()
        except:
            pass
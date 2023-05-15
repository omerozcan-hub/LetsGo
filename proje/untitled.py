import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView, QFileDialog, QWidget

class Ui_Form(QWidget):

    varInfo = 0  # hesap id
    var1Info = 0  # urun id
    img = ""

### temizleme ###

    def temiz(self):
            self.img = ""

            ### ilanlarım sayfası
            self.lineEdit_7.setText('')
            self.lineEdit_5.setText('')
            self.textEdit_2.setText('')
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.comboBox_4.setCurrentIndex(0)
            self.comboBox_5.setCurrentIndex(0)

            ### ilan verme sayfası
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.textEdit.setText('')
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.comboBox_2.setCurrentIndex(0)

            ### login
            self.le3.setText('')
            self.le4.setText('')
            self.le5.setText('')

### hesap içi butonlar ##

    def Ilanlarim(self):
            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()

            curs.execute('''SELECT Baslik,Fiyat FROM Urun WHERE id_user=?''', (self.varInfo,))
            result = curs.fetchall()

            self.tableWidget_14.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_14.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_14.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_14.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)

            conn.close()

    def IlanSil(self):
            row_number = self.tableWidget_14.currentRow()
            column_number = self.tableWidget_14.currentColumn()
            word = self.tableWidget_14.item(row_number, column_number).text()

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()

            curs.execute('''DELETE FROM Urun WHERE id_user=? AND (Baslik=? OR Fiyat=?)''', (self.varInfo, word, word,))
            conn.commit()
            conn.close()
            self.Ilanlarim()

    def IlanEdit(self):
            row_number = self.tableWidget_14.currentRow()
            column_number = self.tableWidget_14.currentColumn()
            word = self.tableWidget_14.item(row_number, column_number).text()

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()

            curs.execute(
                    '''SELECT Baslik,Fiyat,Durum,Aciklama,id_urun,Sehir,Kategori FROM Urun WHERE id_user=? AND (Baslik=? OR Fiyat=?)''',
                    (self.varInfo, word, word))
            data = curs.fetchone()

            self.lineEdit_7.setText(data[0])
            self.lineEdit_5.setText(str(data[1]))

            if data[2] == 'Yeni':
                    self.checkBox_4.setChecked(True)
            elif data[2] == '2.el':
                    self.checkBox_4.setChecked(True)
            else:
                    pass

            self.textEdit_2.setText(data[3])
            self.var1Info = data[4]

            curs.execute('''SELECT id_sehir FROM Sehir WHERE Sehiradi=?''',(data[5],))
            sehirid = curs.fetchone()

            if sehirid != None:
                    index=sehirid[0]-1
                    print(index)
                    self.comboBox_4.setCurrentIndex(index)
            else:
                    pass


            curs.execute('''SELECT Kategori_id FROM Kategori WHERE Kategori_ad=?''', (data[6],))
            kid = curs.fetchone()
            if kid != None:
                    print(kid)
                    index = int(kid[0]) - 1
                    self.comboBox_5.setCurrentIndex(index)
            else: pass

            conn.commit()
            conn.close()

    def IlanGunc(self):
            baslik = self.lineEdit_7.text()
            fiyat = self.lineEdit_5.text()
            aciklama = self.textEdit_2.toPlainText()

            if self.checkBox_4.isChecked():
                    durum = 'Yeni'
            elif self.checkBox_3.isChecked():
                    durum = '2.el'
            else:
                    durum = ''

            sehir= self.comboBox_4.currentText()
            kategori= self.comboBox_5.currentText()
            print(kategori)
            print(sehir)

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()

            if len(self.img) > 0:
                    curs.execute('''UPDATE Urun SET Baslik=?,Fiyat=?,Durum=?,Aciklama=?,Foto=?,Kategori=?,Sehir=? WHERE id_urun=?''',
                                 (baslik, fiyat, durum, aciklama, self.img, self.var1Info,kategori,sehir))
                    conn.commit()
                    print(baslik, fiyat, durum, aciklama, self.img, self.var1Info)
            else:
                    curs.execute('''UPDATE Urun SET Baslik=?,Fiyat=?,Durum=?,Aciklama=?,Kategori=?,Sehir=? WHERE id_urun=?''',
                                 (baslik, fiyat, durum, aciklama,kategori,sehir, self.var1Info))
                    conn.commit()
                    print(baslik, fiyat, durum, aciklama,kategori,sehir, self.var1Info)

            conn.close()
            self.Ilanlarim()

    def CheckBox_Group(self):
            if self.checkBox.isChecked():
                    self.checkBox_2.setChecked(False)
                    return (self.checkBox.text())
            elif self.checkBox_2.isChecked():
                    self.checkBox.setChecked(False)
                    return (self.checkBox_2.text())
            else:
                    pass

    def IlanVer(self):
            baslik = self.lineEdit_2.text()
            sehir = self.comboBox_2.currentText()
            kategori = self.comboBox_3.currentText()
            fiyat = self.lineEdit_3.text()
            durum = self.CheckBox_Group()
            foto = self.img
            aciklama = self.textEdit.toPlainText()
            userid = self.varInfo

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''INSERT INTO Urun(Baslik,Fiyat,Durum,Aciklama,Kategori,id_user,Sehir,Foto) VALUES(?,?,?,?,?,?,?,?)''',
                         (baslik, fiyat, durum, aciklama,kategori, userid, sehir, foto))
            conn.commit()
            conn.close()

            self.lineEdit_2.setText('')
            self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_3.setText('')
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.textEdit.setText('')

    def Cikis(self):
            self.OButton_Show()
            self.HButton_Hide()
            self.groupBox.hide()

    def HesapInfo(self):
            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''SELECT * FROM User WHERE id_user=? ''', (self.varInfo,))
            kdata = curs.fetchone()
            print(self.varInfo)
            print(kdata)
            self.label_67.setText(kdata[1])
            self.label_68.setText(kdata[2])
            self.label_69.setText(str(kdata[5]))
            self.label_73.setText(kdata[3])
            self.label_74.setText(kdata[4])

            conn.close()

            ###

    def toHesapInfo(self):
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget_3.setCurrentIndex(2)
            self.HesapInfo()

    def toFavori(self):
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget_3.setCurrentIndex(3)
            self.Fav()

    def toIlanlar(self):
            self.Ilanlarim()
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget_3.setCurrentIndex(1)

    def toIlanVer(self):
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget_3.setCurrentIndex(0)

### favori ###

    def Fav(self):
            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()

            curs.execute(
                    '''SELECT Urun.Baslik,Urun.Fiyat,Urun.Aciklama FROM Urun JOIN Fav ON Urun.id_urun=Fav.id_urun WHERE Fav.id_user=?''',
                    (self.varInfo,))
            result = curs.fetchall()

            if (len(result) > 0):
                    self.tableWidget_13.setRowCount(0)
                    for row_number1, row_data1 in enumerate(result):
                            self.tableWidget_13.insertRow(row_number1)
                            for column_number1, data1 in enumerate(row_data1):
                                    self.tableWidget_13.setItem(row_number1, column_number1,
                                                                QtWidgets.QTableWidgetItem(str(data1)))

                    header = self.tableWidget_13.horizontalHeader()
                    header.setSectionResizeMode(0, QHeaderView.Stretch)
                    header.setSectionResizeMode(1, QHeaderView.Stretch)
                    header.setSectionResizeMode(2, QHeaderView.Stretch)

                    conn.close()
            else:
                    pass

    def FavSil(self):
            rowN = self.tableWidget_13.currentRow()
            columN = self.tableWidget_13.currentColumn()
            word = self.tableWidget_13.item(rowN, columN).text()

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''SELECT id_urun FROM Urun WHERE Baslik=? OR Fiyat=? OR Aciklama=?''', (word, word, word))
            uid = curs.fetchone()

            curs.execute('''DELETE FROM Fav WHERE id_urun=? AND id_user''', (uid, self.varInfo))

            conn.commit()
            conn.close()
            self.Fav()

    def favEkle(self):
            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            # baslik = self.label_42.text()

            print(self.var1Info)
            curs.execute('''INSERT INTO Fav(id_urun,id_user) VALUES(?,?)''', (self.var1Info, self.varInfo))

            conn.commit()
            conn.close()

    def favKontrol(self):
            if self.checkBox_5.isChecked():
                    self.favEkle()
            else:
                    pass

    def Details_F(self):
            row = self.tableWidget_13.currentRow()
            column = self.tableWidget_13.currentColumn()
            s1 = self.tableWidget_13.item(row, column).text()

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''SELECT * FROM Urun WHERE Baslik=? OR Aciklama=? OR Fiyat=?''', (s1, s1, s1))
            urun_data = curs.fetchone()

            foto = urun_data[8]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(foto, 'webp')
            eval('self.label_72.setPixmap(pixmap)')

            var1Info = urun_data[0]
            self.label_42.setText(urun_data[1])
            fiyat = str(urun_data[2]) + ' TL'
            self.label_43.setText(fiyat)
            self.label_44.setText(urun_data[3])
            self.label_45.setText(urun_data[4])
            conn.close()
            self.tabWidget.setCurrentIndex(0)
            self.toIncele()

### hesap ###

    def OButton_Hide(self):
            self.pushButton_3.hide()
            self.pushButton_11.hide()

    def OButton_Show(self):
            self.pushButton_3.show()
            self.pushButton_11.show()

    def HButton_Hide(self):
            self.checkBox_5.hide()
            self.pushButton_43.hide()
            self.pushButton_44.hide()

    def HButton_Show(self):
            self.checkBox_5.show()
            self.pushButton_43.show()
            self.pushButton_44.show()

    def Hesap_Button(self):

            if self.HesapB_count % 2 == 0:
                    self.groupBox.show()
            elif self.HesapB_count % 2 == 1:
                    self.groupBox.hide()
            else:
                    print('Hesap_Button hata')

            self.HesapB_count += 1

### ürün incele ###

    def anasayfa_urunler(self):
            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''SELECT Foto,Baslik,Fiyat,id_urun FROM Urun ''')

            # self.label_6.setPixmap(pix)
            # self.pushButton_26.setText(data[1]+'\n'+str(data[2])+'  TL')

            for x in range(16):
                    data = curs.fetchone()
                    foto = data[0]
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(foto, 'webp')

                    eval('self.lb' + str(x + 1) + '.setPixmap(pixmap)')
                    b = data[1] + '\n' + str(data[2]) + '  TL'
                    eval('self.B' + str(x + 1) + '.setText(b)')
            conn.close()

    def Incele(self, buttonadi):
            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            idu = int(buttonadi)
            self.var1Info = idu

            curs.execute('''SELECT * FROM Urun WHERE id_urun=?''', (idu,))
            urun_i = curs.fetchone()

            foto = urun_i[8]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(foto, 'webp')
            self.label_72.setPixmap(pixmap)

            self.label_42.setText(urun_i[1])
            fiyat = str(urun_i[2]) + ' TL'
            self.label_43.setText(fiyat)
            self.label_44.setText(urun_i[3])
            self.label_45.setText(urun_i[4])
            self.toIncele()
            conn.close()

    def Image_load(self):

            img = QFileDialog.getOpenFileName(self, 'Open file', 'urunler/', "Image files (*.jpg *.png *.webp)")

            with open(img[0], 'rb') as file:
                    photo_img = file.read()

            self.img = photo_img

    def Details_S(self):
            row = self.tableWidget_12.currentRow()
            column = self.tableWidget_12.currentColumn()
            s1 = self.tableWidget_12.item(row, column).text()

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''SELECT * FROM Urun WHERE Baslik=? OR Aciklama=? OR Fiyat=?''', (s1, s1, s1))
            urun_data = curs.fetchone()
            foto = urun_data[8]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(foto, 'webp')
            eval('self.label_72.setPixmap(pixmap)')

            var1Info = urun_data[0]
            self.label_42.setText(urun_data[1])
            fiyat = str(urun_data[2]) + ' TL'
            self.label_43.setText(fiyat)
            self.label_44.setText(urun_data[3])
            self.label_45.setText(urun_data[4])
            conn.close()
            self.Hide_search()
            self.toIncele()

### kayıt ###

    def registercheck(self):
            print('kayıt ol butonuna basıldı')
            adsoyad = self.le1.text()
            username = self.le2.text()
            telnumber = self.le3_2.text()
            email = self.le4_2.text()
            password = self.le5_2.text()

            conn = sqlite3.connect('../data.db')
            conn.execute("""INSERT INTO user( ad_soyad, username, telnumber, email, password) VALUES(?,?,?,?,?)""",
                         (adsoyad, username, telnumber, email, password))

            conn.commit()
            self.label_75.setHidden(False)
            conn.close()

### login ###

    def logincheck(self):
            telnumber = self.le3.text()
            email = self.le4.text()
            password = self.le5.text()

            connection = sqlite3.connect('../data.db')
            curs = connection.cursor()

            curs.execute(
                    ''' SELECT id_user,telnumber,email,password FROM user WHERE telnumber =? AND email =? AND password =?''',
                    (telnumber, email, password))
            result = curs.fetchone()

            self.varInfo = int(result[0])

            if (len(result) > 0):
                    print('User Found!')
                    self.label_47.setHidden(True)
                    self.OButton_Hide()
                    self.HButton_Show()
                    self.toMain()

            else:
                    print('User Not Found')
                    self.label_47.setHidden(False)
            connection.close()

### sehir ###

    def Show_combobox_sehir(self):
            self.db = sqlite3.connect('../data.db')
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT Sehiradi FROM Sehir''')
            data = self.cur.fetchall()
            self.comboBox.clear()
            for il in data:
                    self.comboBox.addItem(il[0])
                    self.comboBox_2.addItem(il[0])
                    self.comboBox_4.addItem(il[0])
            self.db.close()

### kategoriler ###

    def Show_combobox_kategori(self):
            self.db = sqlite3.connect('../data.db')
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT Kategori_Ad FROM Kategori''')
            data = self.cur.fetchall()
            for il in data:
                    self.comboBox_3.addItem(il[0])
                    self.comboBox_5.addItem(il[0])
            self.db.close()

    def TKtoS(self):

            conn = sqlite3.connect('../data.db')
            curs = conn.cursor()
            curs.execute('''SELECT Kategori_ad FROM Kategori ''')
            urun_data = curs.fetchall()

            if len(self.tableWidget.selectedItems()) > 0:
                    search_word = urun_data[0][0]
            elif len(self.tableWidget_2.selectedItems()) > 0:
                    search_word = urun_data[1][0]
            elif len(self.tableWidget_3.selectedItems()) > 0:
                    search_word = urun_data[2][0]
            elif len(self.tableWidget_4.selectedItems()) > 0:
                    search_word = urun_data[3][0]
            elif len(self.tableWidget_5.selectedItems()) > 0:
                    search_word = urun_data[4][0]
            elif len(self.tableWidget_6.selectedItems()) > 0:
                    search_word = urun_data[5][0]
            elif len(self.tableWidget_7.selectedItems()) > 0:
                    search_word = urun_data[6][0]
            elif len(self.tableWidget_8.selectedItems()) > 0:
                    search_word = urun_data[7][0]
            elif len(self.tableWidget_9.selectedItems()) > 0:
                    search_word = urun_data[8][0]
            elif len(self.tableWidget_10.selectedItems()) > 0:
                    search_word = urun_data[9][0]
            else:
                    print('no selection')

            print(search_word)
            curs.execute('''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=?''',
                         (str(search_word), str(search_word),))
            u_data = curs.fetchall()

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(u_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            conn.close()
            self.Hide_TK()
            self.Show_search()

    def KButton_A(self):
            search_word = 'Araba'
            print(search_word)

            conn = sqlite3.connect('../data.db')
            urun_data = conn.execute('''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=?''',
                                     (search_word, search_word))

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(urun_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.Show_search()
            conn.close()

    def KButton_T(self):
            search_word = 'Telefon'
            conn = sqlite3.connect('../data.db')
            urun_data = conn.execute('''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=?''',
                                     (search_word, search_word))

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(urun_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.Show_search()
            conn.close()

    def KButton_E(self):
            search_word = 'Elektronik'
            conn = sqlite3.connect('../data.db')
            urun_data = conn.execute('''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=?''',
                                     (search_word, search_word))

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(urun_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.Show_search()
            conn.close()

    def KButton_M(self):
            search_word = 'Motosiklet'
            conn = sqlite3.connect('../data.db')
            urun_data = conn.execute('''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=?''',
                                     (search_word, search_word))

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(urun_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.Show_search()
            conn.close()

    def KButton_Ev(self):
            search_word = 'Ev Eşyaları'
            print(search_word)

            conn = sqlite3.connect('../data.db')
            urun_data = conn.execute('''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=?''',
                                     (search_word, search_word))

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(urun_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.Show_search()
            conn.close()

    def Show_TK(self):
            self.groupBox_2.show()

    def Hide_TK(self):
            self.groupBox_2.hide()

    def onDisplay_Araba(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT A_ad FROM K_Araba'
            result = conn.execute(content1)

            self.tableWidget.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget.setItem(row_number1, column_number1,
                                                     QtWidgets.QTableWidgetItem(str(data1)))

            # tablo sütunlarını genişlet
            header = self.tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Telefon(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT T_ad FROM K_Telefon'
            result = conn.execute(content1)

            self.tableWidget_2.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_2.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_2.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_2.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Ev(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT E_ad FROM K_Ev'
            result = conn.execute(content1)

            self.tableWidget_3.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_3.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_3.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_3.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Elektronik(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT E_ad FROM K_Elektronik'
            result = conn.execute(content1)

            self.tableWidget_4.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_4.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_4.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_4.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Motosiklet(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT M_ad FROM K_Motosiklet'
            result = conn.execute(content1)

            self.tableWidget_5.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_5.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_5.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_5.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_DigerA(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT D_ad FROM K_DAraçlar'
            result = conn.execute(content1)

            self.tableWidget_6.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_6.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_6.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_6.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Bebek(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT B_ad FROM K_Bebek'
            result = conn.execute(content1)

            self.tableWidget_7.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_7.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_7.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_7.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Spor(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT S_ad FROM K_Spor'
            result = conn.execute(content1)

            self.tableWidget_8.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_8.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_8.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_8.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Hobi(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT H_ad FROM K_Hobi'
            result = conn.execute(content1)

            self.tableWidget_9.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_9.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_9.setItem(row_number1, column_number1,
                                                       QtWidgets.QTableWidgetItem(str(data1)))
            header = self.tableWidget_9.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

    def onDisplay_Giyim(self):
            conn = sqlite3.connect('../data.db')
            content1 = 'SELECT G_ad FROM K_Giyim'
            result = conn.execute(content1)

            self.tableWidget_10.setRowCount(0)
            for row_number1, row_data1 in enumerate(result):
                    self.tableWidget_10.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_10.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_10.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            conn.close()

### search ###

    def Show_search(self):
            self.groupBox_3.show()

    def Hide_search(self):
            self.groupBox_3.hide()

    def Search(self):
            conn = sqlite3.connect('../data.db')
            sbaslik = self.lineEdit.text()
            sehir = self.comboBox.currentText()

            urun_data = conn.execute(
                    '''SELECT Baslik,Aciklama,Fiyat FROM urun WHERE Baslik=? OR Kategori=? AND Sehir=?''',
                    (sbaslik, sbaslik, sehir))

            self.tableWidget_12.setRowCount(0)
            for row_number1, row_data1 in enumerate(urun_data):
                    self.tableWidget_12.insertRow(row_number1)
                    for column_number1, data1 in enumerate(row_data1):
                            self.tableWidget_12.setItem(row_number1, column_number1,
                                                        QtWidgets.QTableWidgetItem(str(data1)))

            header = self.tableWidget_12.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            conn.close()

### yönlendirici button fonksiyonları ###

    def toMain(self):
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget_2.setCurrentIndex(0)
            self.checkBox_5.setChecked(False)
            self.temiz()

    def toGiris(self):
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget_2.setCurrentIndex(2)

    def toKayit(self):
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget_2.setCurrentIndex(3)

    def toIncele(self):
            self.tabWidget_2.setCurrentIndex(1)

### Constructor ve buttonlar ###

    def Cons(self):
            self.tabWidget.tabBar().setVisible(False)
            self.groupBox.hide()
            self.groupBox_2.hide()
            self.groupBox_3.hide()
            self.label_47.hide()
            self.label_75.hide()
            self.Show_combobox_sehir()
            self.Show_combobox_kategori()
            self.onDisplay_Araba()
            self.onDisplay_Telefon()
            self.onDisplay_Ev()
            self.onDisplay_Hobi()
            self.onDisplay_Spor()
            self.onDisplay_Bebek()
            self.onDisplay_DigerA()
            self.onDisplay_Motosiklet()
            self.onDisplay_Elektronik()
            self.onDisplay_Giyim()
            self.anasayfa_urunler()
            self.HButton_Hide()

    def Buttons(self):
            self.pushButton.clicked.connect(self.toMain)
            self.pushButton_3.clicked.connect(self.toGiris)
            self.pushButton_11.clicked.connect(self.toKayit)

            self.pushButton_2.clicked.connect(self.Show_search)
            self.pushButton_14.clicked.connect(self.Hide_search)
            self.pushButton_2.clicked.connect(self.Search)

            self.pushButton_5.clicked.connect(self.Show_TK)
            self.pushButton_10.clicked.connect(self.Hide_TK)
            self.pushButton_24.clicked.connect(self.TKtoS)

            self.pushButton_13.clicked.connect(self.Details_S)

            self.pushButton_12.clicked.connect(self.logincheck)
            self.pushButton_15.clicked.connect(self.registercheck)

            self.pushButton_4.clicked.connect(self.KButton_A)
            self.pushButton_8.clicked.connect(self.KButton_T)
            self.pushButton_6.clicked.connect(self.KButton_E)
            self.pushButton_7.clicked.connect(self.KButton_M)
            self.pushButton_9.clicked.connect(self.KButton_Ev)

            self.pushButton_43.clicked.connect(self.Hesap_Button)
            self.HesapB_count = 0

            self.B1.clicked.connect(lambda: self.Incele(1))
            self.B2.clicked.connect(lambda: self.Incele(2))
            self.B3.clicked.connect(lambda: self.Incele(3))
            self.B4.clicked.connect(lambda: self.Incele(4))
            self.B5.clicked.connect(lambda: self.Incele(5))
            self.B6.clicked.connect(lambda: self.Incele(6))
            self.B7.clicked.connect(lambda: self.Incele(7))
            self.B8.clicked.connect(lambda: self.Incele(8))
            self.B9.clicked.connect(lambda: self.Incele(9))
            self.B10.clicked.connect(lambda: self.Incele(10))
            self.B11.clicked.connect(lambda: self.Incele(11))
            self.B12.clicked.connect(lambda: self.Incele(12))
            self.B13.clicked.connect(lambda: self.Incele(13))
            self.B14.clicked.connect(lambda: self.Incele(14))
            self.B15.clicked.connect(lambda: self.Incele(15))
            self.B16.clicked.connect(lambda: self.Incele(16))

            self.checkBox_5.stateChanged.connect(self.favKontrol)

            self.pushButton_40.clicked.connect(self.toHesapInfo)
            self.pushButton_41.clicked.connect(self.toFavori)
            self.pushButton_42.clicked.connect(self.toIlanlar)
            self.pushButton_39.clicked.connect(self.Cikis)
            self.pushButton_44.clicked.connect(self.toIlanVer)

            self.pushButton_17.clicked.connect(self.Image_load)
            self.pushButton_16.clicked.connect(self.IlanVer)

            self.pushButton_19.clicked.connect(self.Image_load)
            self.pushButton_25.clicked.connect(self.IlanEdit)
            self.pushButton_20.clicked.connect(self.IlanSil)
            self.pushButton_23.clicked.connect(self.IlanGunc)

            self.pushButton_22.clicked.connect(self.FavSil)
            self.pushButton_21.clicked.connect(self.Details_F)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1310, 912)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 1310, 911))
        self.label.setStyleSheet("background-color:rgb(233, 237, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(250, 10, 251, 41))
        self.comboBox.setStyleSheet("border-radius:15px;\n"
"font-style:italic;\n"
"font:bold;")
        self.comboBox.setObjectName("comboBox")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(980, 10, 181, 41))
        self.pushButton_2.setStyleSheet("background-color:white;")
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/anasayfa/pic/buyutec.webp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(40, 39))
        self.pushButton_2.setAutoRepeat(False)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 10, 171, 41))
        self.pushButton.setStyleSheet("")
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/anasayfa/pic/LOGO.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(170, 170))
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(580, 10, 381, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 1311, 851))
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, -30, 1311, 881))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(-10, 0, 1311, 841))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-image:url(:/back/pic/wallpapers/w1.jpg);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_9.setGeometry(QtCore.QRect(920, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet("color:red;\n"
"border-radius:20px;\n"
"background-color:rgb(198, 243, 255);")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_7.setGeometry(QtCore.QRect(780, 10, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("color:red;\n"
"border-radius:20px;\n"
"background-color:rgb(198, 243, 255);")
        self.pushButton_7.setObjectName("pushButton_7")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea.setGeometry(QtCore.QRect(10, 330, 1281, 491))
        self.scrollArea.setStyleSheet("background-color:rgb(241, 239, 255);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1279, 489))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.B12 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B12.setFont(font)
        self.B12.setText("")
        self.B12.setFlat(True)
        self.B12.setObjectName("B12")
        self.gridLayout.addWidget(self.B12, 6, 3, 1, 1)
        self.lb12 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb12.sizePolicy().hasHeightForWidth())
        self.lb12.setSizePolicy(sizePolicy)
        self.lb12.setText("")
        self.lb12.setScaledContents(True)
        self.lb12.setObjectName("lb12")
        self.gridLayout.addWidget(self.lb12, 5, 3, 1, 1)
        self.B5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B5.setFont(font)
        self.B5.setText("")
        self.B5.setFlat(True)
        self.B5.setObjectName("B5")
        self.gridLayout.addWidget(self.B5, 4, 0, 1, 1)
        self.lb10 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb10.sizePolicy().hasHeightForWidth())
        self.lb10.setSizePolicy(sizePolicy)
        self.lb10.setText("")
        self.lb10.setScaledContents(True)
        self.lb10.setObjectName("lb10")
        self.gridLayout.addWidget(self.lb10, 5, 1, 1, 1)
        self.lb11 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb11.sizePolicy().hasHeightForWidth())
        self.lb11.setSizePolicy(sizePolicy)
        self.lb11.setText("")
        self.lb11.setScaledContents(True)
        self.lb11.setObjectName("lb11")
        self.gridLayout.addWidget(self.lb11, 5, 2, 1, 1)
        self.B4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B4.setFont(font)
        self.B4.setText("")
        self.B4.setFlat(True)
        self.B4.setObjectName("B4")
        self.gridLayout.addWidget(self.B4, 1, 3, 1, 1)
        self.lb9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb9.sizePolicy().hasHeightForWidth())
        self.lb9.setSizePolicy(sizePolicy)
        self.lb9.setText("")
        self.lb9.setScaledContents(True)
        self.lb9.setObjectName("lb9")
        self.gridLayout.addWidget(self.lb9, 5, 0, 1, 1)
        self.lb14 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb14.sizePolicy().hasHeightForWidth())
        self.lb14.setSizePolicy(sizePolicy)
        self.lb14.setText("")
        self.lb14.setScaledContents(True)
        self.lb14.setObjectName("lb14")
        self.gridLayout.addWidget(self.lb14, 7, 1, 1, 1)
        self.lb6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb6.sizePolicy().hasHeightForWidth())
        self.lb6.setSizePolicy(sizePolicy)
        self.lb6.setText("")
        self.lb6.setScaledContents(True)
        self.lb6.setObjectName("lb6")
        self.gridLayout.addWidget(self.lb6, 2, 1, 1, 1)
        self.lb7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb7.sizePolicy().hasHeightForWidth())
        self.lb7.setSizePolicy(sizePolicy)
        self.lb7.setText("")
        self.lb7.setScaledContents(True)
        self.lb7.setObjectName("lb7")
        self.gridLayout.addWidget(self.lb7, 2, 2, 1, 1)
        self.lb5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb5.sizePolicy().hasHeightForWidth())
        self.lb5.setSizePolicy(sizePolicy)
        self.lb5.setText("")
        self.lb5.setScaledContents(True)
        self.lb5.setObjectName("lb5")
        self.gridLayout.addWidget(self.lb5, 2, 0, 1, 1)
        self.lb8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb8.sizePolicy().hasHeightForWidth())
        self.lb8.setSizePolicy(sizePolicy)
        self.lb8.setText("")
        self.lb8.setScaledContents(True)
        self.lb8.setObjectName("lb8")
        self.gridLayout.addWidget(self.lb8, 2, 3, 1, 1)
        self.B9 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B9.setFont(font)
        self.B9.setText("")
        self.B9.setFlat(True)
        self.B9.setObjectName("B9")
        self.gridLayout.addWidget(self.B9, 6, 0, 1, 1)
        self.B11 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B11.setFont(font)
        self.B11.setText("")
        self.B11.setFlat(True)
        self.B11.setObjectName("B11")
        self.gridLayout.addWidget(self.B11, 6, 2, 1, 1)
        self.B7 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B7.setFont(font)
        self.B7.setText("")
        self.B7.setFlat(True)
        self.B7.setObjectName("B7")
        self.gridLayout.addWidget(self.B7, 4, 2, 1, 1)
        self.B8 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B8.setFont(font)
        self.B8.setText("")
        self.B8.setFlat(True)
        self.B8.setObjectName("B8")
        self.gridLayout.addWidget(self.B8, 4, 3, 1, 1)
        self.B2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B2.setFont(font)
        self.B2.setText("")
        self.B2.setFlat(True)
        self.B2.setObjectName("B2")
        self.gridLayout.addWidget(self.B2, 1, 1, 1, 1)
        self.B3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B3.setFont(font)
        self.B3.setText("")
        self.B3.setFlat(True)
        self.B3.setObjectName("B3")
        self.gridLayout.addWidget(self.B3, 1, 2, 1, 1)
        self.B10 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B10.setFont(font)
        self.B10.setText("")
        self.B10.setFlat(True)
        self.B10.setObjectName("B10")
        self.gridLayout.addWidget(self.B10, 6, 1, 1, 1)
        self.B6 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B6.setFont(font)
        self.B6.setText("")
        self.B6.setFlat(True)
        self.B6.setObjectName("B6")
        self.gridLayout.addWidget(self.B6, 4, 1, 1, 1)
        self.lb1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb1.sizePolicy().hasHeightForWidth())
        self.lb1.setSizePolicy(sizePolicy)
        self.lb1.setText("")
        self.lb1.setScaledContents(True)
        self.lb1.setObjectName("lb1")
        self.gridLayout.addWidget(self.lb1, 0, 0, 1, 1)
        self.lb13 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb13.sizePolicy().hasHeightForWidth())
        self.lb13.setSizePolicy(sizePolicy)
        self.lb13.setText("")
        self.lb13.setScaledContents(True)
        self.lb13.setObjectName("lb13")
        self.gridLayout.addWidget(self.lb13, 7, 0, 1, 1)
        self.lb2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb2.sizePolicy().hasHeightForWidth())
        self.lb2.setSizePolicy(sizePolicy)
        self.lb2.setText("")
        self.lb2.setScaledContents(True)
        self.lb2.setObjectName("lb2")
        self.gridLayout.addWidget(self.lb2, 0, 1, 1, 1)
        self.lb4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb4.sizePolicy().hasHeightForWidth())
        self.lb4.setSizePolicy(sizePolicy)
        self.lb4.setText("")
        self.lb4.setScaledContents(True)
        self.lb4.setObjectName("lb4")
        self.gridLayout.addWidget(self.lb4, 0, 3, 1, 1)
        self.lb3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb3.sizePolicy().hasHeightForWidth())
        self.lb3.setSizePolicy(sizePolicy)
        self.lb3.setText("")
        self.lb3.setScaledContents(True)
        self.lb3.setObjectName("lb3")
        self.gridLayout.addWidget(self.lb3, 0, 2, 1, 1)
        self.B1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B1.setFont(font)
        self.B1.setText("")
        self.B1.setFlat(True)
        self.B1.setObjectName("B1")
        self.gridLayout.addWidget(self.B1, 1, 0, 1, 1)
        self.lb15 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb15.sizePolicy().hasHeightForWidth())
        self.lb15.setSizePolicy(sizePolicy)
        self.lb15.setText("")
        self.lb15.setScaledContents(True)
        self.lb15.setObjectName("lb15")
        self.gridLayout.addWidget(self.lb15, 7, 2, 1, 1)
        self.lb16 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb16.sizePolicy().hasHeightForWidth())
        self.lb16.setSizePolicy(sizePolicy)
        self.lb16.setText("")
        self.lb16.setScaledContents(True)
        self.lb16.setObjectName("lb16")
        self.gridLayout.addWidget(self.lb16, 7, 3, 1, 1)
        self.B13 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B13.setFont(font)
        self.B13.setText("")
        self.B13.setFlat(True)
        self.B13.setObjectName("B13")
        self.gridLayout.addWidget(self.B13, 8, 0, 1, 1)
        self.B14 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B14.setFont(font)
        self.B14.setText("")
        self.B14.setFlat(True)
        self.B14.setObjectName("B14")
        self.gridLayout.addWidget(self.B14, 8, 1, 1, 1)
        self.B15 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B15.setFont(font)
        self.B15.setText("")
        self.B15.setFlat(True)
        self.B15.setObjectName("B15")
        self.gridLayout.addWidget(self.B15, 8, 2, 1, 1)
        self.B16 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.B16.setFont(font)
        self.B16.setText("")
        self.B16.setFlat(True)
        self.B16.setObjectName("B16")
        self.gridLayout.addWidget(self.B16, 8, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_4.setGeometry(QtCore.QRect(340, 10, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("color:red;\n"
"border-radius:20px;\n"
"background-color:rgb(198, 243, 255);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("color:red;\n"
"border-radius:20px;\n"
"background-color:rgb(198, 243, 255);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_6.setGeometry(QtCore.QRect(640, 10, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("color:red;\n"
"border-radius:20px;\n"
"background-color:rgb(198, 243, 255);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_8.setGeometry(QtCore.QRect(480, 10, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet("color:red;\n"
"border-radius:20px;\n"
"background-color:rgb(198, 243, 255);")
        self.pushButton_8.setObjectName("pushButton_8")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(290, 60, 741, 271))
        self.label_5.setStyleSheet("background-image:url(:/anasayfa/pic/gorsel1.jpg);")
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/anasayfa/pic/gorsel1.jpg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 40, 1251, 761))
        self.groupBox_2.setStyleSheet("background-color:rgb(255, 220, 220);")
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_10.setGeometry(QtCore.QRect(140, 0, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(40, 50, 241, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(40, 300, 241, 191))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_3.setGeometry(QtCore.QRect(40, 510, 241, 241))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_4.setGeometry(QtCore.QRect(340, 50, 241, 331))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(1)
        self.tableWidget_4.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        self.tableWidget_5 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_5.setGeometry(QtCore.QRect(340, 410, 241, 241))
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(1)
        self.tableWidget_5.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(0, item)
        self.tableWidget_6 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_6.setGeometry(QtCore.QRect(640, 40, 241, 211))
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(1)
        self.tableWidget_6.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(0, item)
        self.tableWidget_7 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_7.setGeometry(QtCore.QRect(640, 280, 241, 241))
        self.tableWidget_7.setObjectName("tableWidget_7")
        self.tableWidget_7.setColumnCount(1)
        self.tableWidget_7.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_7.setHorizontalHeaderItem(0, item)
        self.tableWidget_8 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_8.setGeometry(QtCore.QRect(640, 540, 241, 211))
        self.tableWidget_8.setObjectName("tableWidget_8")
        self.tableWidget_8.setColumnCount(1)
        self.tableWidget_8.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_8.setHorizontalHeaderItem(0, item)
        self.tableWidget_9 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_9.setGeometry(QtCore.QRect(930, 40, 241, 301))
        self.tableWidget_9.setObjectName("tableWidget_9")
        self.tableWidget_9.setColumnCount(1)
        self.tableWidget_9.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_9.setHorizontalHeaderItem(0, item)
        self.tableWidget_10 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_10.setGeometry(QtCore.QRect(930, 380, 241, 301))
        self.tableWidget_10.setObjectName("tableWidget_10")
        self.tableWidget_10.setColumnCount(1)
        self.tableWidget_10.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_10.setHorizontalHeaderItem(0, item)
        self.pushButton_24 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_24.setGeometry(QtCore.QRect(270, 0, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_24.setFont(font)
        self.pushButton_24.setStyleSheet("background-color:rgb(206, 217, 255);")
        self.pushButton_24.setObjectName("pushButton_24")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_3.setGeometry(QtCore.QRect(1080, 10, 101, 41))
        self.pushButton_3.setStyleSheet("color:brown;\n"
"border-radius:15;\n"
"background-color:rgb(248, 255, 180);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_11.setGeometry(QtCore.QRect(1190, 10, 101, 41))
        self.pushButton_11.setStyleSheet("color:brown;\n"
"border-radius:15;\n"
"background-color:rgb(248, 255, 180);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_43 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_43.setGeometry(QtCore.QRect(1140, 20, 151, 31))
        self.pushButton_43.setStyleSheet("color:brown;\n"
"background-color:rgb(248, 255, 180);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_43.setFlat(False)
        self.pushButton_43.setObjectName("pushButton_43")
        self.groupBox = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox.setGeometry(QtCore.QRect(1140, 50, 151, 131))
        self.groupBox.setStyleSheet("color:brown;\n"
"background-color:rgb(248, 255, 180);\n"
"font-size:20px;\n"
"font:bold;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 157, 134))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_40 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_40.setStyleSheet("color:brown;\n"
"background-color:rgb(207, 215, 255);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_40.setObjectName("pushButton_40")
        self.verticalLayout.addWidget(self.pushButton_40)
        self.pushButton_41 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_41.setStyleSheet("color:brown;\n"
"background-color:rgb(207, 215, 255);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_41.setObjectName("pushButton_41")
        self.verticalLayout.addWidget(self.pushButton_41)
        self.pushButton_42 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_42.setStyleSheet("color:brown;\n"
"background-color:rgb(207, 215, 255);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_42.setObjectName("pushButton_42")
        self.verticalLayout.addWidget(self.pushButton_42)
        self.pushButton_39 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_39.setStyleSheet("color:brown;\n"
"background-color:rgb(207, 215, 255);\n"
"font-size:20px;\n"
"font:bold;")
        self.pushButton_39.setObjectName("pushButton_39")
        self.verticalLayout.addWidget(self.pushButton_39)
        self.pushButton_44 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_44.setGeometry(QtCore.QRect(1140, 60, 151, 31))
        self.pushButton_44.setStyleSheet("color:brown;\n"
"border-radius:15;\n"
"background-color:rgb(248, 255, 180);\n"
"font-size:20px;\n"
"font:bold;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/anasayfa/pic/cam.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_44.setIcon(icon2)
        self.pushButton_44.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_44.setObjectName("pushButton_44")
        self.label_2.raise_()
        self.pushButton_9.raise_()
        self.pushButton_7.raise_()
        self.scrollArea.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_8.raise_()
        self.label_5.raise_()
        self.pushButton_3.raise_()
        self.pushButton_11.raise_()
        self.pushButton_43.raise_()
        self.pushButton_44.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setStyleSheet("font: 63 14pt \"Yu Gothic UI Semibold\";")
        self.tab_4.setObjectName("tab_4")
        self.label_4 = QtWidgets.QLabel(self.tab_4)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 1301, 851))
        self.label_4.setStyleSheet("background-image:url(:/back/pic/wallpapers/w1.jpg);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_72 = QtWidgets.QLabel(self.tab_4)
        self.label_72.setGeometry(QtCore.QRect(80, 150, 541, 441))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_72.sizePolicy().hasHeightForWidth())
        self.label_72.setSizePolicy(sizePolicy)
        self.label_72.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_72.setStyleSheet("background-color:white;")
        self.label_72.setText("")
        self.label_72.setScaledContents(True)
        self.label_72.setObjectName("label_72")
        self.label_38 = QtWidgets.QLabel(self.tab_4)
        self.label_38.setGeometry(QtCore.QRect(680, 160, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.tab_4)
        self.label_39.setGeometry(QtCore.QRect(680, 260, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.tab_4)
        self.label_40.setGeometry(QtCore.QRect(680, 340, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.tab_4)
        self.label_41.setGeometry(QtCore.QRect(680, 420, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.label_41.setFont(font)
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.tab_4)
        self.label_42.setGeometry(QtCore.QRect(850, 160, 411, 41))
        self.label_42.setText("")
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.tab_4)
        self.label_43.setGeometry(QtCore.QRect(810, 260, 241, 41))
        self.label_43.setText("")
        self.label_43.setObjectName("label_43")
        self.label_44 = QtWidgets.QLabel(self.tab_4)
        self.label_44.setGeometry(QtCore.QRect(860, 340, 311, 41))
        self.label_44.setText("")
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.tab_4)
        self.label_45.setGeometry(QtCore.QRect(800, 420, 481, 51))
        self.label_45.setText("")
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(self.tab_4)
        self.label_46.setGeometry(QtCore.QRect(600, 60, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.label_46.setFont(font)
        self.label_46.setStyleSheet("font-size:26px;")
        self.label_46.setObjectName("label_46")
        self.checkBox_5 = QtWidgets.QCheckBox(self.tab_4)
        self.checkBox_5.setGeometry(QtCore.QRect(680, 510, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName("checkBox_5")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.label_70 = QtWidgets.QLabel(self.tab_5)
        self.label_70.setGeometry(QtCore.QRect(0, 0, 1301, 851))
        self.label_70.setStyleSheet("background-image:url(:/back/pic/wallpapers/w2.jpg);")
        self.label_70.setText("")
        self.label_70.setObjectName("label_70")
        self.le5 = QtWidgets.QLineEdit(self.tab_5)
        self.le5.setGeometry(QtCore.QRect(550, 510, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le5.setFont(font)
        self.le5.setStyleSheet("border-radius:15;")
        self.le5.setText("")
        self.le5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le5.setObjectName("le5")
        self.le4 = QtWidgets.QLineEdit(self.tab_5)
        self.le4.setGeometry(QtCore.QRect(550, 460, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le4.setFont(font)
        self.le4.setStyleSheet("border-radius:15;\n"
"place-holder:username;")
        self.le4.setText("")
        self.le4.setObjectName("le4")
        self.label_48 = QtWidgets.QLabel(self.tab_5)
        self.label_48.setGeometry(QtCore.QRect(550, 140, 221, 221))
        self.label_48.setStyleSheet("background-image:url(:/girisyap/pic/girisyap/avatar.png);\n"
"border-radius:25%;")
        self.label_48.setText("")
        self.label_48.setPixmap(QtGui.QPixmap(":/girisyap/pic/avatar.png"))
        self.label_48.setScaledContents(True)
        self.label_48.setObjectName("label_48")
        self.le3 = QtWidgets.QLineEdit(self.tab_5)
        self.le3.setGeometry(QtCore.QRect(550, 420, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le3.setFont(font)
        self.le3.setStyleSheet("border-radius:15;\n"
"place-holder:username;")
        self.le3.setText("")
        self.le3.setObjectName("le3")
        self.label_47 = QtWidgets.QLabel(self.tab_5)
        self.label_47.setGeometry(QtCore.QRect(550, 550, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_47.setFont(font)
        self.label_47.setStyleSheet("color:red;\n"
"font:italic;\n"
"")
        self.label_47.setObjectName("label_47")
        self.label_49 = QtWidgets.QLabel(self.tab_5)
        self.label_49.setGeometry(QtCore.QRect(590, 370, 151, 41))
        self.label_49.setStyleSheet("color:white;")
        self.label_49.setObjectName("label_49")
        self.pushButton_12 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_12.setGeometry(QtCore.QRect(600, 580, 131, 31))
        self.pushButton_12.setStyleSheet("border-radius:15;\n"
"background-color:white;\n"
"color:black;")
        self.pushButton_12.setObjectName("pushButton_12")
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_71 = QtWidgets.QLabel(self.tab_6)
        self.label_71.setGeometry(QtCore.QRect(0, 0, 1301, 851))
        self.label_71.setStyleSheet("background-image:url(:/back/pic/wallpapers/w2.jpg);")
        self.label_71.setText("")
        self.label_71.setObjectName("label_71")
        self.le3_2 = QtWidgets.QLineEdit(self.tab_6)
        self.le3_2.setGeometry(QtCore.QRect(550, 480, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le3_2.setFont(font)
        self.le3_2.setStyleSheet("border-radius:15;\n"
"place-holder:username;")
        self.le3_2.setText("")
        self.le3_2.setObjectName("le3_2")
        self.le1 = QtWidgets.QLineEdit(self.tab_6)
        self.le1.setGeometry(QtCore.QRect(550, 380, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le1.setFont(font)
        self.le1.setStyleSheet("border-radius:15;\n"
"place-holder:username;")
        self.le1.setObjectName("le1")
        self.le4_2 = QtWidgets.QLineEdit(self.tab_6)
        self.le4_2.setGeometry(QtCore.QRect(550, 530, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le4_2.setFont(font)
        self.le4_2.setStyleSheet("border-radius:15;\n"
"place-holder:username;")
        self.le4_2.setText("")
        self.le4_2.setObjectName("le4_2")
        self.le2 = QtWidgets.QLineEdit(self.tab_6)
        self.le2.setGeometry(QtCore.QRect(550, 430, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le2.setFont(font)
        self.le2.setStyleSheet("border-radius:15;\n"
"place-holder:username;")
        self.le2.setObjectName("le2")
        self.le5_2 = QtWidgets.QLineEdit(self.tab_6)
        self.le5_2.setGeometry(QtCore.QRect(550, 580, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.le5_2.setFont(font)
        self.le5_2.setStyleSheet("border-radius:15;")
        self.le5_2.setText("")
        self.le5_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le5_2.setObjectName("le5_2")
        self.label_50 = QtWidgets.QLabel(self.tab_6)
        self.label_50.setGeometry(QtCore.QRect(580, 330, 141, 51))
        self.label_50.setStyleSheet("color:white;")
        self.label_50.setObjectName("label_50")
        self.pushButton_15 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_15.setGeometry(QtCore.QRect(580, 660, 131, 31))
        self.pushButton_15.setStyleSheet("border-radius:15;\n"
"background-color:white;\n"
"color:black;")
        self.pushButton_15.setObjectName("pushButton_15")
        self.label_51 = QtWidgets.QLabel(self.tab_6)
        self.label_51.setGeometry(QtCore.QRect(540, 110, 221, 221))
        self.label_51.setStyleSheet("background-image:url(:/girisyap/pic/girisyap/avatar.png);\n"
"border-radius:25%;")
        self.label_51.setText("")
        self.label_51.setPixmap(QtGui.QPixmap(":/girisyap/pic/avatar.png"))
        self.label_51.setScaledContents(True)
        self.label_51.setObjectName("label_51")
        self.label_75 = QtWidgets.QLabel(self.tab_6)
        self.label_75.setGeometry(QtCore.QRect(570, 620, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_75.setFont(font)
        self.label_75.setStyleSheet("color:green;\n"
"font:italic;\n"
"")
        self.label_75.setObjectName("label_75")
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_3.setGeometry(QtCore.QRect(0, -30, 1311, 871))
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.label_52 = QtWidgets.QLabel(self.tab_7)
        self.label_52.setGeometry(QtCore.QRect(0, 0, 1311, 861))
        self.label_52.setStyleSheet("background-image:url(:/back/pic/wallpapers/w4.jpg);\n"
"background-size: cover;\n"
"background-position: center;\n"
"")
        self.label_52.setText("")
        self.label_52.setObjectName("label_52")
        self.label_56 = QtWidgets.QLabel(self.tab_7)
        self.label_56.setGeometry(QtCore.QRect(490, 370, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_56.setFont(font)
        self.label_56.setStyleSheet("color:gray;")
        self.label_56.setObjectName("label_56")
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab_7)
        self.checkBox_2.setGeometry(QtCore.QRect(750, 370, 101, 31))
        self.checkBox_2.setStyleSheet("color:white;")
        self.checkBox_2.setObjectName("checkBox_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_7)
        self.lineEdit_2.setGeometry(QtCore.QRect(460, 140, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("border-radius:15px;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_16 = QtWidgets.QPushButton(self.tab_7)
        self.pushButton_16.setGeometry(QtCore.QRect(590, 740, 161, 51))
        self.pushButton_16.setStyleSheet("border-radius:15px;\n"
"background-color:gray;\n"
"font:bold;\n"
"font-size:20;\n"
"color:white;")
        self.pushButton_16.setObjectName("pushButton_16")
        self.label_57 = QtWidgets.QLabel(self.tab_7)
        self.label_57.setGeometry(QtCore.QRect(400, 50, 561, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_57.setFont(font)
        self.label_57.setStyleSheet("color:white;\n"
"font: 18pt \"Times New Roman\";")
        self.label_57.setObjectName("label_57")
        self.textEdit = QtWidgets.QTextEdit(self.tab_7)
        self.textEdit.setGeometry(QtCore.QRect(400, 470, 551, 231))
        self.textEdit.setStyleSheet("border-radius:10px;\n"
"font-size:20px;")
        self.textEdit.setObjectName("textEdit")
        self.pushButton_17 = QtWidgets.QPushButton(self.tab_7)
        self.pushButton_17.setGeometry(QtCore.QRect(490, 420, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_17.setFont(font)
        self.pushButton_17.setStyleSheet("border-radius:15px;\n"
"background-color:rgb(252, 247, 255);\n"
"")
        self.pushButton_17.setObjectName("pushButton_17")
        self.checkBox = QtWidgets.QCheckBox(self.tab_7)
        self.checkBox.setGeometry(QtCore.QRect(660, 370, 71, 31))
        self.checkBox.setStyleSheet("color:white;")
        self.checkBox.setObjectName("checkBox")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_7)
        self.lineEdit_3.setGeometry(QtCore.QRect(460, 260, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("border-radius:15px;")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_7)
        self.comboBox_2.setGeometry(QtCore.QRect(460, 190, 391, 41))
        self.comboBox_2.setStyleSheet("border-radius:15px;\n"
"background-color:white;")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_7)
        self.comboBox_3.setGeometry(QtCore.QRect(460, 310, 391, 41))
        self.comboBox_3.setStyleSheet("border-radius:15px;\n"
"background-color:white;")
        self.comboBox_3.setObjectName("comboBox_3")
        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.label_53 = QtWidgets.QLabel(self.tab_8)
        self.label_53.setGeometry(QtCore.QRect(-10, -10, 1311, 861))
        self.label_53.setStyleSheet("background-image:url(:/back/pic/wallpapers/w4.jpg);\n"
"background-size: cover;\n"
"background-position: center;\n"
"")
        self.label_53.setText("")
        self.label_53.setObjectName("label_53")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_8)
        self.lineEdit_5.setGeometry(QtCore.QRect(770, 290, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setStyleSheet("border-radius:15px;")
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_18 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_18.setGeometry(QtCore.QRect(900, 700, 161, 51))
        self.pushButton_18.setStyleSheet("border-radius:15px;\n"
"background-color:gray;\n"
"font:bold;\n"
"font-size:20;")
        self.pushButton_18.setObjectName("pushButton_18")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_8)
        self.textEdit_2.setGeometry(QtCore.QRect(710, 490, 551, 171))
        self.textEdit_2.setStyleSheet("border-radius:10px;\n"
"font-size:20px;")
        self.textEdit_2.setObjectName("textEdit_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.tab_8)
        self.checkBox_3.setGeometry(QtCore.QRect(1050, 400, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setStyleSheet("color:white;")
        self.checkBox_3.setObjectName("checkBox_3")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_8)
        self.lineEdit_7.setGeometry(QtCore.QRect(770, 180, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setStyleSheet("border-radius:15px;")
        self.lineEdit_7.setText("")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_58 = QtWidgets.QLabel(self.tab_8)
        self.label_58.setGeometry(QtCore.QRect(800, 400, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_58.setFont(font)
        self.label_58.setStyleSheet("color:gray;")
        self.label_58.setObjectName("label_58")
        self.pushButton_19 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_19.setGeometry(QtCore.QRect(770, 440, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_19.setFont(font)
        self.pushButton_19.setStyleSheet("border-radius:15px;\n"
"background-color:gray;\n"
"font:bold;\n"
"color:white;")
        self.pushButton_19.setObjectName("pushButton_19")
        self.checkBox_4 = QtWidgets.QCheckBox(self.tab_8)
        self.checkBox_4.setGeometry(QtCore.QRect(960, 400, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setStyleSheet("color:white;")
        self.checkBox_4.setObjectName("checkBox_4")
        self.label_59 = QtWidgets.QLabel(self.tab_8)
        self.label_59.setGeometry(QtCore.QRect(590, 60, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_59.setFont(font)
        self.label_59.setStyleSheet("color:white;\n"
"font: 18pt \"Times New Roman\";")
        self.label_59.setObjectName("label_59")
        self.tableWidget_11 = QtWidgets.QTableWidget(self.tab_8)
        self.tableWidget_11.setGeometry(QtCore.QRect(30, 170, 631, 491))
        self.tableWidget_11.setObjectName("tableWidget_11")
        self.tableWidget_11.setColumnCount(2)
        self.tableWidget_11.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_11.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_11.setHorizontalHeaderItem(1, item)
        self.tableWidget_11.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_11.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_11.horizontalHeader().setStretchLastSection(False)
        self.pushButton_20 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_20.setGeometry(QtCore.QRect(280, 690, 161, 51))
        self.pushButton_20.setStyleSheet("border-radius:15px;\n"
"background-color:gray;\n"
"font:bold;\n"
"font-size:20;\n"
"color:white;")
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_23 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_23.setGeometry(QtCore.QRect(900, 700, 161, 51))
        self.pushButton_23.setStyleSheet("border-radius:15px;\n"
"background-color:gray;\n"
"font:bold;\n"
"font-size:20;")
        self.pushButton_23.setObjectName("pushButton_23")
        self.tableWidget_14 = QtWidgets.QTableWidget(self.tab_8)
        self.tableWidget_14.setGeometry(QtCore.QRect(30, 170, 631, 491))
        self.tableWidget_14.setObjectName("tableWidget_14")
        self.tableWidget_14.setColumnCount(2)
        self.tableWidget_14.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_14.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_14.setHorizontalHeaderItem(1, item)
        self.tableWidget_14.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_14.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_14.horizontalHeader().setStretchLastSection(False)
        self.pushButton_25 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_25.setGeometry(QtCore.QRect(670, 360, 51, 51))
        self.pushButton_25.setStyleSheet("border-radius:15px;\n"
"background-color:rgb(240, 219, 255);\n"
"font:bold;\n"
"font-size:20;\n"
"color:rgb(140, 8, 255);")
        self.pushButton_25.setObjectName("pushButton_25")
        self.comboBox_4 = QtWidgets.QComboBox(self.tab_8)
        self.comboBox_4.setGeometry(QtCore.QRect(770, 230, 391, 41))
        self.comboBox_4.setStyleSheet("border-radius:15px;\n"
"background-color:white;")
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_5 = QtWidgets.QComboBox(self.tab_8)
        self.comboBox_5.setGeometry(QtCore.QRect(770, 340, 391, 41))
        self.comboBox_5.setStyleSheet("border-radius:15px;\n"
"background-color:white;")
        self.comboBox_5.setObjectName("comboBox_5")
        self.tabWidget_3.addTab(self.tab_8, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.label_60 = QtWidgets.QLabel(self.tab_10)
        self.label_60.setGeometry(QtCore.QRect(-10, 0, 1311, 861))
        self.label_60.setStyleSheet("background-image:url(:/back/pic/wallpapers/w5.jpg);\n"
"\n"
"")
        self.label_60.setText("")
        self.label_60.setObjectName("label_60")
        self.label_61 = QtWidgets.QLabel(self.tab_10)
        self.label_61.setGeometry(QtCore.QRect(540, 90, 231, 51))
        self.label_61.setStyleSheet("font: italic 22pt \"Times New Roman\";\n"
"color:white;")
        self.label_61.setObjectName("label_61")
        self.label_62 = QtWidgets.QLabel(self.tab_10)
        self.label_62.setGeometry(QtCore.QRect(390, 250, 231, 51))
        self.label_62.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.tab_10)
        self.label_63.setGeometry(QtCore.QRect(400, 180, 231, 51))
        self.label_63.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_63.setObjectName("label_63")
        self.label_64 = QtWidgets.QLabel(self.tab_10)
        self.label_64.setGeometry(QtCore.QRect(390, 320, 231, 51))
        self.label_64.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_64.setObjectName("label_64")
        self.label_65 = QtWidgets.QLabel(self.tab_10)
        self.label_65.setGeometry(QtCore.QRect(390, 390, 231, 51))
        self.label_65.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_65.setObjectName("label_65")
        self.label_66 = QtWidgets.QLabel(self.tab_10)
        self.label_66.setGeometry(QtCore.QRect(390, 470, 231, 51))
        self.label_66.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_66.setObjectName("label_66")
        self.label_67 = QtWidgets.QLabel(self.tab_10)
        self.label_67.setGeometry(QtCore.QRect(640, 180, 311, 51))
        self.label_67.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_67.setText("")
        self.label_67.setObjectName("label_67")
        self.label_68 = QtWidgets.QLabel(self.tab_10)
        self.label_68.setGeometry(QtCore.QRect(640, 250, 311, 51))
        self.label_68.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_68.setText("")
        self.label_68.setObjectName("label_68")
        self.label_69 = QtWidgets.QLabel(self.tab_10)
        self.label_69.setGeometry(QtCore.QRect(640, 320, 311, 51))
        self.label_69.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_69.setText("")
        self.label_69.setObjectName("label_69")
        self.label_73 = QtWidgets.QLabel(self.tab_10)
        self.label_73.setGeometry(QtCore.QRect(640, 390, 311, 51))
        self.label_73.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_73.setText("")
        self.label_73.setObjectName("label_73")
        self.label_74 = QtWidgets.QLabel(self.tab_10)
        self.label_74.setGeometry(QtCore.QRect(640, 470, 311, 51))
        self.label_74.setStyleSheet("font: italic 16pt \"Times New Roman\";\n"
"color:white;")
        self.label_74.setText("")
        self.label_74.setObjectName("label_74")
        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.label_55 = QtWidgets.QLabel(self.tab_11)
        self.label_55.setGeometry(QtCore.QRect(0, 0, 1311, 861))
        self.label_55.setStyleSheet("background-image:url(:/back/pic/wallpapers/w5.jpg);\n"
"\n"
"")
        self.label_55.setText("")
        self.label_55.setObjectName("label_55")
        self.tableWidget_13 = QtWidgets.QTableWidget(self.tab_11)
        self.tableWidget_13.setGeometry(QtCore.QRect(50, 110, 921, 661))
        self.tableWidget_13.setStyleSheet("background-color:white;")
        self.tableWidget_13.setObjectName("tableWidget_13")
        self.tableWidget_13.setColumnCount(3)
        self.tableWidget_13.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_13.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_13.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_13.setHorizontalHeaderItem(2, item)
        self.label_3 = QtWidgets.QLabel(self.tab_11)
        self.label_3.setGeometry(QtCore.QRect(600, 30, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:rgb(235, 255, 254);\n"
"")
        self.label_3.setObjectName("label_3")
        self.pushButton_21 = QtWidgets.QPushButton(self.tab_11)
        self.pushButton_21.setGeometry(QtCore.QRect(1030, 310, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_21.setFont(font)
        self.pushButton_21.setStyleSheet("border-radius:15px;\n"
"background-color:rgb(255, 243, 254);")
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_22 = QtWidgets.QPushButton(self.tab_11)
        self.pushButton_22.setGeometry(QtCore.QRect(1030, 410, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_22.setFont(font)
        self.pushButton_22.setStyleSheet("border-radius:15px;\n"
"background-color:rgb(255, 243, 254);")
        self.pushButton_22.setObjectName("pushButton_22")
        self.tabWidget_3.addTab(self.tab_11, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(150, 50, 1061, 761))
        self.groupBox_3.setStyleSheet("background-color:rgb(218, 216, 255);")
        self.groupBox_3.setObjectName("groupBox_3")
        self.tableWidget_12 = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget_12.setGeometry(QtCore.QRect(40, 50, 751, 681))
        self.tableWidget_12.setDragDropOverwriteMode(True)
        self.tableWidget_12.setWordWrap(True)
        self.tableWidget_12.setObjectName("tableWidget_12")
        self.tableWidget_12.setColumnCount(3)
        self.tableWidget_12.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_12.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_12.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_12.setHorizontalHeaderItem(2, item)
        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_13.setGeometry(QtCore.QRect(810, 280, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_13.setFont(font)
        self.pushButton_13.setStyleSheet("border-radius:15;\n"
"background-color:rgb(253, 242, 255);")
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_14 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_14.setGeometry(QtCore.QRect(810, 370, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_14.setFont(font)
        self.pushButton_14.setStyleSheet("border-radius:15;\n"
"background-color:rgb(253, 242, 255);")
        self.pushButton_14.setObjectName("pushButton_14")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.Cons()
        self.Buttons()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox.setToolTip(_translate("Form", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Araba, Telefon, Bisisklet ve daha fazlası"))
        self.pushButton_9.setText(_translate("Form", "Ev Eşyaları"))
        self.pushButton_7.setText(_translate("Form", "Motosiklet"))
        self.pushButton_4.setText(_translate("Form", "Araba"))
        self.pushButton_5.setText(_translate("Form", "Tüm Kategoriler"))
        self.pushButton_6.setText(_translate("Form", "Elektronik"))
        self.pushButton_8.setText(_translate("Form", "Telefon"))
        self.groupBox_2.setTitle(_translate("Form", "Tüm"))
        self.pushButton_10.setText(_translate("Form", "/\\"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Araba"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Telefon"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Ev Eşyaları"))
        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Elektronik"))
        item = self.tableWidget_5.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Motosiklet"))
        item = self.tableWidget_6.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Diğer Araçlar"))
        item = self.tableWidget_7.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Bebek ve Çocuk"))
        item = self.tableWidget_8.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Spor ve Outdoor"))
        item = self.tableWidget_9.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Hobi ve Eğlence"))
        item = self.tableWidget_10.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Giyim ve Aksesuar"))
        self.pushButton_24.setText(_translate("Form", "Git"))
        self.pushButton_3.setText(_translate("Form", "Giriş Yap"))
        self.pushButton_11.setText(_translate("Form", "Kayıt Ol"))
        self.pushButton_43.setText(_translate("Form", "Hesap"))
        self.pushButton_40.setText(_translate("Form", "Hesap Bilgileri"))
        self.pushButton_41.setText(_translate("Form", "Favoriler"))
        self.pushButton_42.setText(_translate("Form", "İlanlarım"))
        self.pushButton_39.setText(_translate("Form", "Çıkış Yap"))
        self.pushButton_44.setText(_translate("Form", "Sat"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("Form", "anasayfa"))
        self.label_38.setText(_translate("Form", "İlan Başlığı     :"))
        self.label_39.setText(_translate("Form", "Fiyat        :"))
        self.label_40.setText(_translate("Form", "Durumu        :"))
        self.label_41.setText(_translate("Form", "Açıklama :"))
        self.label_46.setText(_translate("Form", "Ürün Detayları"))
        self.checkBox_5.setText(_translate("Form", "Favorilere Ekle"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("Form", "incele"))
        self.le5.setPlaceholderText(_translate("Form", "Parola"))
        self.le4.setPlaceholderText(_translate("Form", "Email"))
        self.le3.setPlaceholderText(_translate("Form", "Telefon Numarası"))
        self.label_47.setText(_translate("Form", "Kullanıcı Bilgileri Bulunamadı !!!"))
        self.label_49.setToolTip(_translate("Form", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_49.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">GİRİŞ YAP  </span></p><p><br/></p></body></html>"))
        self.pushButton_12.setText(_translate("Form", "Giriş Yap"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Form", "giris"))
        self.le3_2.setPlaceholderText(_translate("Form", "Telefon Numarası"))
        self.le1.setPlaceholderText(_translate("Form", "Ad Soyad"))
        self.le4_2.setPlaceholderText(_translate("Form", "Email"))
        self.le2.setPlaceholderText(_translate("Form", "Kullanıcı Adı"))
        self.le5_2.setPlaceholderText(_translate("Form", "Parola"))
        self.label_50.setToolTip(_translate("Form", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_50.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">KAYIT OL  </span></p><p><br/></p></body></html>"))
        self.pushButton_15.setText(_translate("Form", "Kayıt Ol"))
        self.label_75.setText(_translate("Form", "Kayıt İşleminiz Başarılı"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("Form", "kayıt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.label_56.setText(_translate("Form", "Ürün Durumu  :"))
        self.checkBox_2.setText(_translate("Form", "2.El"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "  İlan Başlığı"))
        self.pushButton_16.setText(_translate("Form", "İlan Ver"))
        self.label_57.setText(_translate("Form", "Kullanmadığın  Eşyalarını Değerlendirebilirsin"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:20px; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p></body></html>"))
        self.textEdit.setPlaceholderText(_translate("Form", "İlan Açıklama"))
        self.pushButton_17.setText(_translate("Form", "Görsel Yükle"))
        self.checkBox.setText(_translate("Form", "Yeni"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "  Fiyat"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), _translate("Form", "ekle"))
        self.lineEdit_5.setPlaceholderText(_translate("Form", "  Fiyat"))
        self.pushButton_18.setText(_translate("Form", "Güncelle"))
        self.textEdit_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:20px; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p></body></html>"))
        self.textEdit_2.setPlaceholderText(_translate("Form", "İlan Açıklama"))
        self.checkBox_3.setText(_translate("Form", "2.El"))
        self.lineEdit_7.setPlaceholderText(_translate("Form", "  İlan Başlığı"))
        self.label_58.setText(_translate("Form", "Ürün Durumu  :"))
        self.pushButton_19.setText(_translate("Form", "Görsel Yükle"))
        self.checkBox_4.setText(_translate("Form", "Yeni"))
        self.label_59.setText(_translate("Form", "Aktif İlanlarınız"))
        item = self.tableWidget_11.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Başlık"))
        item = self.tableWidget_11.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Fiyat"))
        self.pushButton_20.setText(_translate("Form", "Sil"))
        self.pushButton_23.setText(_translate("Form", "Güncelle"))
        item = self.tableWidget_14.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Başlık"))
        item = self.tableWidget_14.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Fiyat"))
        self.pushButton_25.setText(_translate("Form", "->"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_8), _translate("Form", "sil"))
        self.label_61.setText(_translate("Form", "Hesap Bilgileri"))
        self.label_62.setText(_translate("Form", "Kullanıcı Adı         :"))
        self.label_63.setText(_translate("Form", "Ad Soyad              :"))
        self.label_64.setText(_translate("Form", "Telefon Numarası  :"))
        self.label_65.setText(_translate("Form", "E-Mail                   :"))
        self.label_66.setText(_translate("Form", "Parola                   :"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), _translate("Form", "hesap"))
        item = self.tableWidget_13.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Başlık"))
        item = self.tableWidget_13.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Fiyat"))
        item = self.tableWidget_13.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Açıklama"))
        self.label_3.setText(_translate("Form", "Favoriler"))
        self.pushButton_21.setText(_translate("Form", "Ürünü İncele"))
        self.pushButton_22.setText(_translate("Form", "Ürünü Favorilerden Kaldır"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_11), _translate("Form", "favoriler"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
        self.groupBox_3.setTitle(_translate("Form", "Arama"))
        self.tableWidget_12.setSortingEnabled(False)
        item = self.tableWidget_12.horizontalHeaderItem(0)
        item.setText(_translate("Form", "İlandaki Ürünler"))
        item = self.tableWidget_12.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Açıklama"))
        item = self.tableWidget_12.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Fiyat"))
        self.pushButton_13.setText(_translate("Form", "Ürünü İncele"))
        self.pushButton_14.setText(_translate("Form", "Geri"))

import pro

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowTitle('LetsGo')
    Form.setWindowIcon(QIcon('pic/cam.jpg'))
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

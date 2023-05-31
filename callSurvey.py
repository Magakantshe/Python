import sys
from PyQt4 import QtSql, QtGui
from survey import *
from AddData import Ui_Dialog as addSurveyDialog
from viewSurveyData import Ui_Dialog as viewSurveyDataDialog

def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    db.setHostName('localhost')
    db.setDatabaseName('survey')
    db.setUserName('root')
    db.setPassword('elia')
    db.open()
    print (db.lastError().text())
    return True
class MyForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL('clicked()'), self.viewSurvey)
        QtCore.QObject.connect(self.ui.pushButton_2,QtCore.SIGNAL('clicked()'), self.viewData)
        
        
    def viewSurvey(self):
        dataDialog = AddDataDialog()
        dataDialog.exec_()
        
    def viewData(self):
        viewDialog = viewDataDialog()
        viewDialog.exec_()

class AddDataDialog(QtGui.QDialog):
    isEdit = False
    
    def __init__(self, contactnumber="", parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = addSurveyDialog()
        self.ui.setupUi(self)
        #button connect 
        QtCore.QObject.connect(self.ui.submitData,
                               QtCore.SIGNAL('clicked()'), self.submit)

        self.model = QtSql.QSqlQueryModel(self)

        if contactnumber != "":
            self.isEdit = True
            self.model.setQuery(
                """select * from students where StudentID = '%s' """
                %contactnumber)
            self.survey = self.model.record(0)
            
            
            self.ui.lineEditSurname.setText(
                self.student.value("surname"))
            self.ui.lineEditNames.setText(
                self.student.value("firstnames"))
            self.ui.lineEditDate.setDate(self.student.value("date").date())
            self.ui.lineEditAge.setText(str(age))
                        
          

    def submit(self):
        
        if self.isEdit:
            self.model.setQuery("""UPDATE students set surname = '%s',
                firstnames = '%s', date = '%s',
                WHERE contactnumber = '%s' """
                                %(self.ui.lineEditSurname.text(),
                                self.ui.lineEditNames.text(),
                                self.ui.lineEditDate.text(),
                                self.ui.lineEditAge.text()))
        else:
            self.model.setQuery("""INSERT INTO students(surname,
                firstnames,contactnumber,date, age)
                VALUES('%s', '%s', '%s', '%s', %d)"""
                                %(self.ui.lineEditSurname.text(),
                                self.ui.lineEditNames.text(),
                                self.ui.lineEditContact.text(),
                                self.ui.lineEditDate.text(),
                                int(self.ui.lineEditAge.text())))
                     
        if (self.ui.radioEat1.isChecked()):
            count1=0
        elif(self.ui.radioEat2.isChecked()):
            count1=1
        elif(self.ui.radioEat3.isChecked()):
            count1=2
        elif(self.ui.radioEat4.isChecked()):
            count1=3
        elif(self.ui.radioEat5.isChecked()):
            count1=4
            
        if(self.ui.radioMovie1.isChecked()):
            count2=0
        elif(self.ui.radioMovie2.isChecked()):
            count2=1
        elif(self.ui.radioMovie3.isChecked()):
            count2=2
        elif(self.ui.radioMovie4.isChecked()):
            count2=3
        elif(self.ui.radioMovie5.isChecked()):
            count2=4
            
        if(self.ui.radioTv1.isChecked()):
            count3=0
        elif(self.ui.radioTv2.isChecked()):
            count3=1
        elif(self.ui.radioTv3.isChecked()):
            count3=2
        elif(self.ui.radioTv4.isChecked()):
            count3=3
        elif(self.ui.radioTv5.isChecked()):
            count3=4
            
        if(self.ui.radioRadio1.isChecked()):
            count4=0
        elif(self.ui.radioRadio2.isChecked()):
            count4=1
        elif(self.ui.radioRadio3.isChecked()):
            count4=2
        elif(self.ui.radioRadio4.isChecked()):
            count4=3
        elif(self.ui.radioRadio5.isChecked()):
            count4=4
        self.modelUpdate1 = QtSql.QSqlQueryModel(self) 
        self.modelUpdate1.setQuery("""INSERT INTO scale
                                  VALUES('%s',%d,%d,%d,%d)"""
                                  %(self.ui.lineEditContact.text(),count1,
                                    count2,count3,count4))

        pizza = self.ui.checkPizza.isChecked()
        pasta = self.ui.checkPasta.isChecked()
        pap = self.ui.checkPap.isChecked()
        chicken = self.ui.checkChicken.isChecked()
        beef = self.ui.checkBeef.isChecked()
        other = self.ui.checkOther.isChecked()
        self.modelUpdate2 = QtSql.QSqlQueryModel(self)
        self.modelUpdate2.setQuery("""INSERT INTO food
                                  VALUES('%s',%r, %r,%r,%r,%r,%r)"""
                                  %(self.ui.lineEditContact.text(),pizza,pasta,pap,
                                    chicken, beef,other))
        
        self.accept()
        
class viewDataDialog(QtGui.QDialog):
    def __init__(self, contactnumber="", parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = viewSurveyDataDialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.btOk,
                               QtCore.SIGNAL('clicked()'), self.accept)

        self.model = QtSql.QSqlQueryModel(self)
        self.model.setQuery("""SELECT * FROM students""")

        # Total number of surveys
        totalSurveys = self.model.rowCount()
                
        # calculate average age
        if (totalSurveys!=0):
            totalAge = 0
            for i in range(self.model.rowCount()):
                age = self.model.record(i).value("age")
                totalAge = totalAge + age
            averageAge = round(totalAge/(totalSurveys))
        else:
            averageAge = 0

        # max age
        self.model = QtSql.QSqlQueryModel(self)
        self.model.setQuery("""SELECT MAX(age) FROM students""")
        if (totalSurveys== 0):
            maxAge = 0
        else:
            maxAge = self.model.record(0).value("max(age)")
        

        # min age
        self.model = QtSql.QSqlQueryModel(self)
        self.model.setQuery("""SELECT MIN(age) FROM students""")
        if (totalSurveys== 0):
            mimAge = 0
        else:
            mimAge = self.model.record(0).value("min(age)")

        

        # Pecerntage
        
        self.model = QtSql.QSqlQueryModel(self)
        self.model.setQuery("""SELECT pizza FROM food WHERE pizza""")
        totalPizza = self.model.rowCount()
        percentagePizza = 0.0
        if (totalSurveys!=0):
            percentagePizza = round((totalPizza/totalSurveys)*100,1)
        else:
            pecerntagePizza = 0.0
            
        
        self.model = QtSql.QSqlQueryModel(self)
        self.model.setQuery("""SELECT pasta FROM food WHERE pasta""")
        totalPasta = self.model.rowCount()
        percentagePasta = 0.0
        if (totalSurveys!=0):
            percentagePasta = round((totalPasta/totalSurveys)*100,1)
        else:
            percentagePasta = 0.0

        self.model = QtSql.QSqlQueryModel(self)
        self.model.setQuery("""SELECT papandwors FROM food WHERE papandwors""")
        totalPap = self.model.rowCount()
        percentagePap = 0.0
        if (totalSurveys!=0):
            percentagePap = round((totalPap/totalSurveys)*100,1)
        else:
            pecerntagePap = 0.0

        self.ui.pizzaText.setText(str(percentagePizza))
        self.ui.pastaText.setText(str(percentagePasta))
        self.ui.papText.setText(str(percentagePap))

        # rating querys
        
        self.modelRate1 = QtSql.QSqlQueryModel(self)
        self.modelRate2 = QtSql.QSqlQueryModel(self)
        self.modelRate3 = QtSql.QSqlQueryModel(self)
        self.modelRate4 = QtSql.QSqlQueryModel(self)
        self.modelRate5 = QtSql.QSqlQueryModel(self)
        
        self.modelRate1.setQuery("""SELECT eat FROM scale WHERE eat = 0""")
        self.modelRate2.setQuery("""SELECT eat FROM scale WHERE eat = 1""")
        self.modelRate3.setQuery("""SELECT eat FROM scale WHERE eat = 2""")
        self.modelRate4.setQuery("""SELECT eat FROM scale WHERE eat = 3""")
        self.modelRate5.setQuery("""SELECT eat FROM scale WHERE eat = 4""")

        
        totalEatRate1 = self.modelRate1.rowCount()
        totalEatRate2 = self.modelRate2.rowCount()
        totalEatRate3 = self.modelRate3.rowCount()
        totalEatRate4 = self.modelRate4.rowCount()
        totalEatRate5 = self.modelRate5.rowCount()

        if (totalSurveys!=0):
            averageEat = round((1*totalEatRate1+2*totalEatRate2+3*totalEatRate3+
                           4*totalEatRate4+5*totalEatRate5)/totalSurveys,1)
        else:
            averageEat = 0.0
        self.modelRate1.setQuery("""SELECT movie FROM scale WHERE movie = 0""")
        self.modelRate2.setQuery("""SELECT movie FROM scale WHERE movie = 1""")
        self.modelRate3.setQuery("""SELECT movie FROM scale WHERE movie = 2""")
        self.modelRate4.setQuery("""SELECT movie FROM scale WHERE movie = 3""")
        self.modelRate5.setQuery("""SELECT movie FROM scale WHERE movie = 4""")

        totalMovieRate1 = self.modelRate1.rowCount()
        totalMovieRate2 = self.modelRate2.rowCount()
        totalMovieRate3 = self.modelRate3.rowCount()
        totalMovieRate4 = self.modelRate4.rowCount()
        totalMovieRate5 = self.modelRate5.rowCount()

        
        if (totalSurveys!=0):
            averageMovie = round((1*totalMovieRate1+2*totalMovieRate2+3*totalMovieRate3+
                           4*totalMovieRate4+5*totalMovieRate5)/totalSurveys,1)
        else:
            averageMovie =0.0
            
        self.modelRate1.setQuery("""SELECT tv FROM scale WHERE tv = 0""")
        self.modelRate2.setQuery("""SELECT tv FROM scale WHERE tv = 1""")
        self.modelRate3.setQuery("""SELECT tv FROM scale WHERE tv = 2""")
        self.modelRate4.setQuery("""SELECT tv FROM scale WHERE tv = 3""")
        self.modelRate5.setQuery("""SELECT tv FROM scale WHERE tv = 4""")

        totalTvRate1 = self.modelRate1.rowCount()
        totalTvRate2 = self.modelRate2.rowCount()
        totalTvRate3 = self.modelRate3.rowCount()
        totalTvRate4 = self.modelRate4.rowCount()
        totalTvRate5 = self.modelRate5.rowCount()

        if (totalSurveys!=0):
            averageTv = round((1*totalTvRate1+2*totalTvRate2+3*totalTvRate3+
                           4*totalTvRate4+5*totalTvRate5)/totalSurveys,1)
        else:
            averageTv=0.0
            
        self.modelRate1.setQuery("""SELECT radio FROM scale WHERE radio = 0""")
        self.modelRate2.setQuery("""SELradio FROM scale WHERE radio = 1""")
        self.modelRate3.setQuery("""SELECT radio FROM scale WHERE radio = 2""")
        self.modelRate4.setQuery("""SELECT radio FROM scale WHERE radio = 3""")
        self.modelRate5.setQuery("""SELECT radio FROM scale WHERE radio = 4""")

        totalRadioRate1 = self.modelRate1.rowCount()
        totalRadioRate2 = self.modelRate2.rowCount()
        totalRadioRate3 = self.modelRate3.rowCount()
        totalRadioRate4 = self.modelRate4.rowCount()
        totalRadioRate5 = self.modelRate5.rowCount()

        if (totalSurveys!=0):
            averageRadio = round((1*totalRadioRate1+2*totalRadioRate2+3*totalRadioRate3+
                           4*totalRadioRate4+5*totalRadioRate5)/totalSurveys,1)
        else:
            averageRadio=0.0

       
        self.ui.surveysText.setText(str(totalSurveys))
        self.ui.averageAgeText.setText(str(averageAge))
        self.ui.maxAgeText.setText(str(maxAge))
        self.ui.minAgeText.setText(str(mimAge))



        self.ui.eatText.setText(str(averageEat))
        self.ui.movieText.setText(str(averageMovie))
        self.ui.tvText.setText(str(averageTv))
        self.ui.radioText.setText(str(averageRadio))
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not createConnection():
        sys.exit(1)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

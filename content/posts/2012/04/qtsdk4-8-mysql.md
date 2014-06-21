Title: QT SDK4.8加载mysql驱动
Date: 2012-04-20 19:09
Author: Altynai
Category: Code
Tags: C/C++
Slug: qtsdk4-8-mysql

应该有很多人和我一样，在这个蛋疼的问题上纠结了很久 = =
因为能搜到的信息都是老版本的信息（多是2009年左右的信息），都没什么用。

直接切入正题。

先说下【我的环境】`win7 + QTSDK4.8 + mysql 5.5 + vs2010(编译器)`

我的QT路径为：**E:\\QtSDK\\Desktop\\Qt\\4.8.0\\msvc2010**

mysql路径为：**E:\\Sever\_AMD\\mysql\\MySQL Server 5.5**

具体步骤如下：

- 先下载 [qt-everywhere-opensource-src-4.8.0.zip][] 解压后把该文件夹下面的整个src文件夹复制到QT路径中

- 复制mysql路径下面的`include`和`lib`文件夹到**一个没有空格**的路径下（比如`C:\mysql`）
这步的原因是mysql的默认安装路径中含有空格，这会造成qmake的失败 = =
如果你选的安装路径没有空格，则可以忽略这一步

- 在开始菜单中打开Qt 4.8.0 for Desktop (MSVC 2010)

- cd到`你的QT路径\src\plugins\sqldrivers\mysql`（例如我的路径即为`E:\QtSDK\Desktop\Qt\4.8.0\msvc2010\src\plugins\sqldrivers\mysql`）

- `qmake "INCLUDEPATH+=C:\mysql\include" "LIBS+=C:\mysql\lib\libmysql.lib" mysql.pro`
这个时候在`你的QT路径\src\plugins\sqldrivers\mysql`下面，会出现MakeFile等文件。同时把`C:\mysql\lib\libmysql.lib`复制到`system32`中!

- 打开vs2010控制台，cd到`你的QT路径\src\plugins\sqldrivers\mysql`，然后输入`nmake & nmake release`，在debug和release文件夹下能找到以下文件，把这4个文件复制到`你的QT路径\plugins\sqldrivers`

        :::cpp
        qsqlmysqld4.dll
        qsqlmysqld4.lib
        qsqlmysql4.dll
        qsqlmysql4.lib

- 随便找一个Qt控制台工程，在工程文件.pro中加入一句代码`QT += sql`，然后将`main.cpp`改为：

        :::cpp
        #include <QtGui/QApplication>
        #include <QTextCodec>
        #include <QDebug>
        #include <QSqlDriver>
        #include <QSqlDatabase>

        int main(int argc, char *argv[])
        {
            QCoreApplication a(argc, argv);
            qDebug() << "Available drivers:";
            QStringList drivers = QSqlDatabase::drivers();
            foreach(QString driver, drivers)
            qDebug() << "\t" << driver;
            return a.exec();
        }

运行结果中出现mysql即可。

![][3]

  [qt-everywhere-opensource-src-4.8.0.zip]: http://download.qt.nokia.com/qt/source/qt-everywhere-opensource-src-4.8.0.zip
  [1]: http://altynai.me/wp-content/uploads/2012/04/1.jpg
  [2]: http://altynai.me/wp-content/uploads/2012/04/2.jpg
  [3]: http://altynai.me/wp-content/uploads/2012/04/3.jpg

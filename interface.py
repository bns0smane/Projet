from tkinter import *
from IEEEE import *
from scopus import *
from espaceNET import *
from Springeer import *
from pubmed import *
import tkinter as tk
window=tk.Tk()
btn=tk.Button(window, 
          height = 100, 
          width = 20)

window.title('Scraping from web')
window.geometry("500x200")
window.configure(background="#80ada7")
lbl=Label(window, text="Scraping interface...",bg="#80ada7", fg='black', font=("calibri 11", 16))
lbl.place(x=160, y=10)


searchBar=Entry(window, text="keyWord", bd=5,bg="#79918d", fg='white',justify=CENTER,font=("calibri 11 bold", 12))
searchBar.place(x=150, y=50)

chkValue = tk.BooleanVar() 
chkValue1 = tk.BooleanVar() 
chkValue2 = tk.BooleanVar() 
chkValue3 = tk.BooleanVar() 
chkValue4 = tk.BooleanVar() 

def IEE():
    test=chkValue.get()
    key=searchBar.get()
    # print(key)
    if test==False:
        IEEE(key)
    else:
        print('IEEE not working')
    print('**************************************')


def scopuss():
    test=chkValue1.get()
    # print(test)
    key=searchBar.get()
    # print(key)
    if test==False:
        scopus(key)
    else:
        print('scopus not working')
    print('**************************************')

    
def espacenet():
    test=chkValue2.get()
    # print(test)
    key=searchBar.get()
    # print(key)
    if test==False:
        espaceNet(key)
    else:
        print('EspaceNet not working')
    print('**************************************')

def Springer():
    test=chkValue3.get()
    # print(test)
    key=searchBar.get()
    # print(key)
    if test==False:
        springerr(key)
    else:
        print('Springer not working')
    print('**************************************')

def PUBMED():
    test=chkValue4.get()
    # print(test)
    key=searchBar.get()
    # print(key)
    if test==False:
        PubMed(key)
    else:
        print('PubMed not working')
    print('**************************************')

var = tk.BooleanVar()
var1 = tk.BooleanVar()
var2 = tk.BooleanVar()
var3 = tk.BooleanVar()
var4 = tk.BooleanVar()

vars = [var,var1,var2,var3,var4]


chkExample = tk.Checkbutton(window, text='IEEE',bg="#80ada7",activebackground="#80ada7",variable=var, font=("calibri 11", 10),selectcolor="#79918d") 
# chkExample.pack()
chkExample.place(x=140, y=90)

chkExample1 = tk.Checkbutton(window, text='Scopus',bg="#80ada7",activebackground="#80ada7",variable=var1, font=("calibri 11", 10),selectcolor="#79918d") 
# chkExample1.pack()
chkExample1.place(x=220, y=90)

chkExample2 = tk.Checkbutton(window, text='EspaceNet',bg="#80ada7",activebackground="#80ada7",variable=var2, font=("calibri 11", 10),selectcolor="#79918d") 
# chkExample2.pack()
chkExample2.place(x=300, y=90)

chkExample2 = tk.Checkbutton(window, text='Springer',bg="#80ada7",activebackground="#80ada7",variable=var3, font=("calibri 11", 10),selectcolor="#79918d") 
# chkExample2.pack()
chkExample2.place(x=140, y=110)

chkExample2 = tk.Checkbutton(window, text='PubMed',bg="#80ada7",activebackground="#80ada7",variable=var4, font=("calibri 11", 10),selectcolor="#79918d") 
# chkExample2.pack()
chkExample2.place(x=220, y=110)

def chekingIEE():
    if vars[0].get():
        var=IEE()
    else:
        var=vars[0].get()
    return var

def chekingScopus():
    if vars[1].get():
        var1=scopuss()
    else:
        var1=vars[1].get()
    return var1

def chekingENet():
    if vars[2].get():
        var2=espacenet()
    else:
        var2=vars[2].get()
    return var2

def chekingspringer():
    if vars[3].get():
        var3=Springer()
    else:
        var3=vars[3].get()
    return var3

def chekingPM():
    if vars[4].get():
        var4=PUBMED()
    else:
        var4=vars[4].get()
    return var4
# allFCT=lambda:[scopuss(),IEE()]
# data=
btn=Button(window, text="Search",bg ='#79918d',fg='black', height = 1, width = 8,activebackground="#79918d",command=lambda:[chekingScopus(),chekingENet(),chekingIEE(),chekingspringer(),chekingPM()])
btn.pack()
btn.place(x=220, y=160)

window.mainloop()
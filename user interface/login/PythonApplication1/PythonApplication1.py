from tkinter import *
root =Tk()
root.geometry("500x300")

Label(root, text= " Registartion ", font = "arial 15 bold").grid(row = 0, column=3)

name = Label(root, text = "Name")
phone = Label(root, text = "Phone")
gender = Label(root, text = "Gender")
age = Label(root, text = "Age")

name.grid(row =2, column = 2)
phone.grid(row =3, column = 2)
gender.grid(row =4, column = 2)
age.grid(row =5, column = 2)


root.mainloop()


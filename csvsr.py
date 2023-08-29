from tkinter import * 
from config_tk import *
import csv ,sys
from tkinter import  ttk , filedialog as fd ,messagebox as msg
from _entry import scroll_text
import pandas as pd

root = Tk()
root.title(title)
root["bg"] = root_bg
root.geometry(geo)
# root.iconbitmap(icon)

count_row =1
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview" , background = "#1F252A",
	font = font, foreground = "#fff" , selectbackground = "#000")

def clear(e=None):
	for x in range(1,count_row):
		tv.selection_set(x)
		see =tv.selection()
		tv.delete(see[0])

def read_setup(fpath):
	global count_row , headers , path
	path = fpath
	try:
		df = pd.read_csv(fpath)
		df =  df.shape
		msg.showinfo(fpath , '%s row ,%s column' % (df))
		file = open(fpath)
		reader = csv.reader(file)
		headers = next(reader)
		data = [row for row in reader]
		"""setup headers """
		try:
			clear()
		except :
			pass
		tv.heading("#0" , text = 'row')
		tv.configure(column = (headers))
		for header in headers :
			tv.heading(header , text = header)
		id = 1
		"""setup rows"""
		for row in data :
			tv.insert('' , id , id , text = id)
			for i , header in  enumerate(headers):
				tv.set( id, header , row[i])
			count_row +=1
			id +=1
		"""size of the columns"""
		headers.append('#0')
		for header in headers :
			tv.column(header, width=100)

	except :
		pass
add =100
def expand():
	global add
	add +=20
	headers.append('#0')
	for header in headers :
		tv.column(header, width=add)
def shrink():
	global add
	add -=20
	headers.append('#0')
	for header in headers :
		tv.column(header, width=add)

def about_page():	
	myself = """\
csv sheet reader 1.0.0\n
for information contact :
author :%s
email :%s
	""" % (author , email)
	msg._show("about" , myself ,"info" ,"ok")

def show_row(e):
	try:
		low = Tk()
		low.title(title)
		low.iconbitmap(icon)
		see =tv.selection()
		file = open(path)
		reader = csv.reader(file)
		headers = next(reader)
		data = [row for row in reader]

		text = scroll_text(low , font = font ,  bg = "#1F252A" , fg = '#fff')
		text.pack()
		i = 1
		for row in data:
			if i == int(see[0]) :
				for header , row in zip(headers , row):

					text.insert(INSERT , str(header).upper() +' : '+str(row)+'\n' )
			i +=1
	except :
		low.destroy()
		msg.showerror('Error' , 'the Table is Empty !')

def setup_path(e =None):
	path = fd.askopenfilename(title = "Select CSV File",initialdir = Extra[0],
	filetypes = (('comma separated values', '*.csv' , ),("all files" , '*.*')))
	read_setup(path)

"""widget configuration"""
menu = Menu(root , tearoff = 0)
menu.add_command(label = 'open' , command = setup_path )
menu.add_command(label = 'Expand' , command = expand)
menu.add_command(label = 'Shrink' , command = shrink)
menu.add_command(label = 'about' , command = about_page)

side_bar= Scrollbar(root )
# horizontal_bar= Scrollbar(root)

tv = ttk.Treeview(root,yscrollcommand = side_bar.set )
side_bar.configure(command = tv.yview)

tv.place(relx = 0 ,rely = 0  , relheight = 1  , relwidth = 0.975)
side_bar.pack(side  = "right" , fill = Y)

try:
	read_setup(sys.argv[1])
except :
	pass

root.bind("<Alt-o>",setup_path )
root.bind('<Alt-x>' , clear )
root.bind('<Return>' , show_row )

root.config(menu = menu)

root.mainloop()

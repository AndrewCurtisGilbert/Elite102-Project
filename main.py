from collections.abc import Collection
import sqlite3
from tkinter import *

## creating a new user account
def create_new_account():
  """
  Create new account with zero balance.
  Return the account number just created.
  """
  global user_name, pin
  ## collecting user data
  user_name = input("Enter your name: ")
  pin = int(input("Enter your desired pin: "))
  cursor.execute("""
    INSERT INTO accounts (
      pin, user_name, current_balance
      ) 
    VALUES (?, ?, 0.0);
  """, (pin, user_name))
  # always call commit when updating table
  connection.commit()

  # to retreive the last inserted account number
  # MySQL has equivalent function: LAST_INSERT_ID()
  cursor.execute("SELECT last_insert_rowid();")
  last_id = cursor.fetchall()[0][0]
  print('your account id number is : ' + str(last_id))

def check_balance():
  """
  Check balance by account number and pin. 
  Return None if account_num + pin is invalid.
  """
  global account_num,pin
  cursor.execute("""
  SELECT current_balance
  FROM accounts
  WHERE account_num = ? AND pin = ?
  ;
  """, (account_num, pin)
  )
  results = cursor.fetchall()
  if len(results) != 1:
    return None
  return results[0][0]
def deposit():
  """
  Deposit amount to current_balance.
  """
  global account_num,pin
  amount = float(input("Enter the amount to deposit: "))
  cursor.execute("""
  UPDATE accounts
  SET current_balance = current_balance + ?
  WHERE account_num = ? AND pin = ?
  ;
  """, (amount, account_num, pin))
  connection.commit()
def withdraw():
  """
  Withdraw amount from current_balance.
  """
  global account_num,pin
  amount = float(input("Enter the amount to withdraw: "))
  
  cursor.execute("""
  UPDATE accounts
  Set current_balance = current_balance - ?
  WHERE account_num = ? AND pin = ? AND current_balance >= ?
  ;
  """, (amount, account_num, pin, amount))
  connection.commit()
def menu_display():
  """
  creates the account menu tkiner window that includes withdraw and deposit buttons
  also creates base account design
  """
  # start of design
  root = Tk()   ## reinstating new window
  canvas = Canvas(root, width = 1000, height = 300) # creating a canvas
  canvas2 = Canvas(root, width = 1000, height = 300, bg = 'skyblue',bd = 10) # creating current bal canvas
  seperator = Canvas(root, width = 1000, height = 10, bg = 'black') # seperator line horizontally
  vert_seperator = Canvas(root,width = 10, height = 130, bg = 'black') # seperator line vertically
  canvas.create_text(55, 20, text="account", font=('Helvetica', 20) ) # account label
  canvas.create_text(270, 150, text="Please Choose an Option") # prompt
  canvas2.create_text(140, 200, text="current balance ", font=('Helvetica', 20,) ) # current bal label
  canvas2.create_text(150, 250, text=str(check_balance()), font=('Helvetica', 20) ) # adds current bal to canvas2
  canvas2.place(x=275,y=-180) # bal canvas placement
  canvas.place(x=0,y=0) # overall canvas placement
  seperator.place(x=0,y=130) # adding sperator horizontal1023
  vert_seperator.place(x = 275, y = 0) #  adding vert seperator
  root.geometry('1000x1000')  # window size
  # end of design
  btn = Button(root, text = 'withdraw',height = 5,width = 30, bd = '10',command = lambda: (withdraw(), menu_display())) # withdraw button
  btn2 = Button(root,text = "deposit",height = 5,width = 30, bd = '10', command = lambda: (deposit(),menu_display())) # deposit button
  info_btn1 = Button(root,text = "change info",height = 2,width = 10, bd = '10', command = lambda: (root.destroy(),change_info()))
  info_btn2 = Button(root,text = "delete acc",height = 2,width = 10, bd = '10', command = lambda: (confirmation()))
  info_btn1.place(x=10,y=35)
  info_btn2.place(x=130,y=35)
  btn.place(x = 135, y = 175)    # placement of the withdraw button
  btn2.place(x=135,y=300)     # placement of the deposit button
  root.mainloop() # keep window open
def sign_in():
  global account_num,pin
  account_num = int(account_num_entry.get())
  pin = int(pin_entry.get())
  root.destroy()
  menu_display()
def change_info():
  new_pin = int(input("enter new pin: "))
  Change_pin(new_pin)

def Change_pin(x):
  print(x)
  global account_num,pin
  cursor.execute("""
  UPDATE accounts
  Set pin = ?
  WHERE account_num = ? AND pin = ?
  ;
  """, (x, account_num, pin))
  pin = x
  connection.commit()
  menu_display()
def confirmation():
  yes = input("are you sure you want to delete your account? ( yes or no ): ")
  global account_num,pin
  if( yes == 'yes'):
    print("deleted")
    cursor.execute("""
  DELETE FROM accounts
  WHERE pin = ? AND account_num = ?;""",(pin, account_num))
    connection.commit()


# test cas id 1024 pin is 1111
account_num = None
pin = None
# creating server connection
connection = sqlite3.connect('storage.sqlite')
cursor = connection.cursor()

# initial setup - create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts 
(
  account_num INTEGER PRIMARY KEY,
  pin INTEGER,
  user_name TEXT,
  current_balance REAL
);
""")
root = Tk()   # declaring window           
root.geometry('500x800') # window parameters

# greeting entry box
canvas = Canvas(root, width = 500, height = 200)
canvas.create_text(75, 30 ,text="Sign in!", font = ('Helvetica', 30))
canvas.place(x=0,y=0)

# account number entry box + text
canvas.create_text(105, 90 ,text="Enter your account number")
pin_entry = Entry()
pin_entry.config(font = 'Ariel 20')
pin_entry.config(width = 20)
pin_entry.place(x=20,y=200)

# pin entry box + text
canvas.create_text(95, 190 ,text="Enter your accounts pin")
account_num_entry = Entry()
account_num_entry.config(font = 'Ariel 20')
account_num_entry.config(width = 20)
account_num_entry.place(x=20,y=100)

# create new account button
new_acc_btn = Button(root, text = 'new account', bd = '10',font = ('ariel 20', 15) ,command = lambda: (create_new_account(),root.destroy()))
new_acc_btn.place(x = 160, y = 475)

# create sign in button
sign_in_btn = Button(root, text = 'sign in', bd = '10',font = ('ariel 20', 15), command = lambda: (sign_in(),root.destroy()))
sign_in_btn.place(x = 190, y = 375)
root.mainloop() # running the window

# after user account selected option


import psycopg2

kel = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5432"
)

cur=kel.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contact (
    cnumber INT PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    address VARCHAR(80)
)
""")
print("✅ Table created successfully!")
kel.commit()


def task(n):
    if (n==1):
        """ cnumber | cname | email | address
                245 | skill | @4324 | jjjjjj
                """
        cur.execute("SELECT * FROM contact")
        rows=(cur.fetchall())
        print(rows)
        print("\nContact details")
        for row in rows:
            print(row)

    elif (n==2):
        #it is for insert contact into table
        number = int(input("Enter number: "))
        name = str(input("Enter name: "))
        email = str(input("Enter email: "))
        address = str(input("Enter address: "))
        query = "INSERT INTO contact (cnumber, cname, email , address) VALUES (%s, %s, %s, %s)"
        values = (number, name, email, address)
        cur.execute(query, values)
    
        kel.commit()
               
        print("✅ Data inserted successfully!") 

    elif (n==3):
        m=int(input("1.Update number, 2.Update Name, 3.Update Email, 4.Update Address: "))
        if (m==1):
            update_number=int(input("Enter the number to be updated: "))
            cur.execute("SELECT * FROM contact WHERE cnumber ={}".format(update_number))
            change_number=cur.fetchone()
            if change_number:
                number_updated=int(input("Enter new number: "))
                cur.execute("UPDATE contact SET cnumber = %s WHERE cnumber = %s", (number_updated,update_number))
                kel.commit()
                print("Number has been updated")   
            else:
                print("Provided number is not exist")
        elif (m==2):
            update_name=str(input("Enter the name to be updated: "))
            cur.execute("SELECT * FROM contact WHERE cname = {}".format(update_name))
            change_name=cur.fetchone()
            if change_name:
                name_updated=str(input("Enter new name: "))
                cur.execute("UPDATE contact SET cname = %s WHERE cname = %s",(name_updated,update_name))
                kel.commit()
                print("Name has been changed")
            else:
                print("Provided name is not exist")
        elif (m==3):
            update_email=str(input("Enter the email to be updated: "))
            cur.execute("SELECT * FROM contact WHERE email={}".format(update_email))
            change_email=cur.fetchone()
            if change_email:
                email_updated=str(input("Enter new contact number: "))
                cur.execute("UPDATE contact SET email = %s WHERE email = %s",(email_updated,update_email))
                kel.commit()
                print("Email has been changed")
            else:
                print("Provided email is not exist")
        elif (m==4):
            update_address=str(input("Enter the address to be updated: "))
            cur.execute("SELECT * FROM contact WHERE address={}".format(update_address))
            change_address=cur.fetchone()
            if change_address:
                address_updated=str(input("Enter new address: "))
                cur.execute("UPDATE contact SET address = %s WHERE address =%s",(address_updated,update_address))
                kel.commit()
                print("Address has been changed")
            else:
                print("Provided Address is not exist")
    elif (n==4):
        delete_number=int(input("Enter contact number: "))
        try:
            delete_number_query="DELETE FROM contact WHERE cnumber = {}".format(delete_number)
            cur.execute(delete_number_query)
            print("✅ Contact details deleted successfully!")
            kel.commit()
        except:
            print("Entered Email is not in the list")
    else :
        print("Enter correct task number")


n=int(input("What do you want to do? 1.Read, 2.Create, 3.Update, 4.Delete : "))
task(n)

cur.close()
kel.close()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

# -------------------------#
#  1️⃣ FastAPI setup
# -------------------------#
app = FastAPI()

# -------------------------#
#  2️⃣ Database connection function
# -------------------------#
def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="12345678"
        )
        print("✅ Database connection successful")

        # ✅ Auto create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS contacts (
            contact_number BIGINT PRIMARY KEY,
            contact_name VARCHAR(100),
            email VARCHAR(150),
            address TEXT
        );
        """
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()

        return connection
    except Exception as e:
        print("❌ Error connecting to DB:", e)
        #program should stop if code is wrong and show internal server error to user
        return None


# -------------------------#
#  3️⃣ Pydantic model (Input JSON format)
# -------------------------#
class Contact(BaseModel):
    contact_number: int
    contact_name: str
    email: str
    address: str


# -------------------------#
#  4️⃣ GET: View all contacts
# -------------------------#
@app.get("/contacts")
def get_contacts():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM contacts;")
        rows = cur.fetchall()
        conn.close()
        return {"contacts": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------#
#  5️⃣ POST: Add a new contact
# -------------------------#
@app.post("/contacts")
def add_contact(contact: Contact):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """INSERT INTO contacts (contact_number, contact_name, email, address)
                   VALUES (%s, %s, %s, %s);"""
        cur.execute(query, (contact.contact_number, contact.contact_name, contact.email, contact.address))
        conn.commit()
        conn.close()

        return {"message": "✅ Contact added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------#
#  6️⃣ PUT: Update contact (based on primary key)
# -------------------------#
@app.put("/contacts/{contact_number}")
def update_contact(contact_number: int, contact:Contact):
    try:
        # input validation codes need to be added here
        conn = get_connection()
        cur = conn.cursor()

        query = """UPDATE contacts
                   SET contact_name=%s, email=%s, address=%s
                   WHERE contact_number=%s;"""
        cur.execute(query, (contact.contact_name, contact.email, contact.address, contact_number))
        conn.commit()
        conn.close()

        return {"message": f"✅ Contact {contact_number} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------#
#  7️⃣ DELETE: Delete contact by contact_number
# -------------------------#
@app.delete("/contacts/{contact_number}")
def delete_contact(contact_number: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM contacts WHERE contact_number=%s;", (contact_number,))
        conn.commit()
        conn.close()

        return {"message": f"🗑️ Contact {contact_number} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------#
#  8️⃣ Run Server Command (Terminal)
# -------------------------#
# Run this in VS Code terminal:
# uvicorn filename:app --reload
# Example: uvicorn main:app --reload
from flask import Flask, request, jsonify
import mysql.connector as mc
import db_configuration


app = Flask(__name__)


def mysql_db_connection():
    return mc.connect(
        host=db_configuration.db_host,
        user=db_configuration.db_user,
        password=db_configuration.db_password,
        database=db_configuration.db_name
    )

"""
this api demonstrates about ACID properties of sql:
- Atomicity: It ensures either all operations succeed, or none at all.
- Consistency: Ensures that the database remains in a valid state before and after a transaction.
- Isolation: Keeps transactions independent from one another.
- Durability: Guarantees once a transaction is committed, the changes are permanent, even if the system crashes.
"""
@app.route("/transfer", methods = ["POST"])
def transfer():
    try:
        data = request.get_json()
        sender_id = data["sender_id"]
        receiver_id = data["receiver_id"]
        balance = data["balance"]
        con = mysql_db_connection()
        cursor = con.cursor()
        try:
            if not all([sender_id, receiver_id, balance]):
                return jsonify({"error: missing sender_id or receiver_id or balance"})
            # start transaction
            con.start_transaction()
            cursor.execute("select * from users where id=%s", (sender_id,))
            sender = cursor.fetchone() # fetchone gives single row as a tuple if exists else None
            if not sender:
                raise Exception("sender not found")
            if balance > sender[2]:
                raise Exception("balance is insufficient")
            cursor.execute("select * from users where id=%s", (receiver_id,))
            receiver = cursor.fetchone()
            if not receiver:
                raise Exception("receiver not found")
            # deduct from the sender
            cursor.execute("update users set balance = balance - %s where id = %s", (balance, sender_id))
            # add to the receiver
            cursor.execute("update users set balance = balance + %s where id = %s", (balance, receiver_id))
            con.commit() # durability i.e., once the transaction is commited changes are permanent
            return jsonify({"message": "Transaction is successful"})
        except Exception as e:
            con.rollback()
            return jsonify({"message": f'transaction unsuccessful at stage 2: {str(e)}'})
    except Exception as e:
        return jsonify({"message": f'transaction unsuccessful at stage 1: {str(e)}'})
    finally:
        con.close()
        cursor.close()


if __name__ == "__main__":
    app.run(debug=True)
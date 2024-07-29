from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os 
 

load_dotenv()
app = Flask(__name__)

cuenta = os.getenv('CORREO_ELECTRONICO')
password = os.getenv('PASSWORD')
 
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        proveedor = data.get('proveedor')
        destinatario = data.get('destinatario')
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')
 
        if not all([proveedor, destinatario, asunto, mensaje]):
            return jsonify({"error": "Missing required fields"}), 400
 
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = cuenta
        msg['To'] = destinatario
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(cuenta, password)
            server.sendmail(cuenta, destinatario, msg.as_string())
           
        return jsonify({"message": "Email sent successfully"}), 200
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500
       
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3636,debug=True)
import yfinance as yf
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración
CEDAERS = ["AAPL", "MSFT", "GOOGL"]
CRYPTOS = ["BTC-USD", "ETH-USD"]
EMAIL = "martinmatias@outlook.com"

def obtener_datos():
    cedear_data = yf.download(CEDAERS, period="5d")['Close'].iloc[-1].to_dict()
    cripto_data = yf.download(CRYPTOS, period="5d")['Close'].iloc[-1].to_dict()
    return cedear_data, cripto_data

def generar_html(cedears, criptos):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("informe.html")
    return template.render(cedears=cedears, criptos=criptos)

def enviar_mail(html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Informe Financiero Diario"
    msg["From"] = "tucuenta@gmail.com"
    msg["To"] = EMAIL
    msg.attach(MIMEText(html, "html"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("tucuenta@gmail.com", "tupassword")
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    cedears, criptos = obtener_datos()
    html = generar_html(cedears, criptos)
    enviar_mail(html)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yfinance as yf
import requests
from datetime import datetime

# === CONFIGURACIÓN ===
REMITENTE = "martinmatias@outlook.com"
DESTINATARIO = "martinmatias@outlook.com"
CLAVE_APP_OUTLOOK = "Benjamin0803"  # Reemplazar con tu clave de aplicación Outlook
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

CEDEARS = ['GGAL.BA', 'MELI.BA', 'BMA.BA', 'TSLA', 'AAPL']
CRIPTOS = ['bitcoin', 'ethereum', 'solana']

# === FUNCIONES ===
def obtener_datos_cedears():
    info = []
    for ticker in CEDEARS:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            precio = hist['Close'].iloc[-1]
            info.append((ticker, round(precio, 2)))
    return info

def obtener_datos_criptos():
    r = requests.get("https://api.coingecko.com/api/v3/simple/price",
                     params={"ids": ','.join(CRIPTOS), "vs_currencies": "usd"})
    data = r.json()
    return [(cripto.title(), data[cripto]['usd']) for cripto in CRIPTOS]

def generar_html(cedears, criptos):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    html = f"""
    <html>
    <body style="font-family: Arial;">
        <h2>📊 Informe Financiero Diario</h2>
        <p><strong>Fecha:</strong> {fecha}</p>

        <h3>💼 CEDEARs</h3>
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
            <tr><th>Ticker</th><th>Precio</th></tr>
    """
    for ticker, precio in cedears:
        html += f"<tr><td>{ticker}</td><td>USD {precio}</td></tr>"

    html += """
        </table>
        <h3>🪙 Criptomonedas</h3>
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
            <tr><th>Cripto</th><th>Precio</th></tr>
    """
    for cripto, precio in criptos:
        html += f"<tr><td>{cripto}</td><td>USD {precio}</td></tr>"

    html += """
        </table>
        <p style="margin-top:20px">⏱️ Este informe es generado automáticamente todos los días.</p>
    </body>
    </html>
    """
    return html

def enviar_email(html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "📥 Informe Financiero Diario"
    msg['From'] = REMITENTE
    msg['To'] = DESTINATARIO

    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(REMITENTE, CLAVE_APP_OUTLOOK)
        server.send_message(msg)

# === FLUJO PRINCIPAL ===
if __name__ == "__main__":
    cedears = obtener_datos_cedears()
    criptos = obtener_datos_criptos()
    html = generar_html(cedears, criptos)
    enviar_email(html)
    print("✅ Informe enviado correctamente.")

import resend
import random

def numero_verificador():
        numero_aleatorio = random.randint(100000, 999999)
        return numero_aleatorio
    
numero_aleatorio=numero_verificador()
#numero_auxiliar=numero_aleatorio
# Construye el mensaje HTML incluyendo el número aleatorio
html_message = f"<p> Your verification random number is:<strong> {numero_aleatorio}</strong></p>"
resend.api_key = "re_HqdgrUpk_Gs3C3K9dcLCjQJzc9hW23CuG"
r = resend.Emails.send({
    "from": "passsecure@resend.dev",
    "to": "jhonsebastianhf@gmail.com",
    "subject": "Verificar contraseña",
    "html": html_message
})

a=input("escribe el numero randon: ")
a=int(a)
if numero_aleatorio == a :
    print("exito")


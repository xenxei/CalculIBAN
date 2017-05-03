# -*- coding: utf-8 -*-

from openerp import models, fields, api

class calculiban(models.Model):
	_name = 'calculiban2'
	numCuenta = fields.Char(string = "Numero de cuenta: ", required = True) 
	IBAN = fields.Float(string = "El teu IBAN es: ", readonly = True)
	pais="es"

	@api.one
	def calculiban(self):
		numero = self.numCuenta
        numero = numero.replace("IBAN", "")
        numero = numero.replace(" ", "")
        numero = numero.replace("-", "")

        ccc = numero[-20:]
        ccc = ccc.replace("IBAN", "")
        ccc = ccc.replace(" ", "")
        ccc = ccc.replace("-", "")

        separador = "-"
        items = ccc[0:4] + separador + ccc[4:8] + separador + ccc[8:10] + separador + ccc[10:20]

        modulos = [(2**x)%11 for x in range(10)]

        suma = 0

        cifras1 = items[0]+items[1]
        cifras2 = items[3]
        cantidad1 = 10 - len(cifras1)
        cantidad2 = 10 - len(cifras2)
        ceros1 = "0"*cantidad1
        ceros2 = "0"*cantidad2
        cifras1 = str(ceros1+cifras1)
        cifras2 = str(ceros2+cifras2)
        for cifra,modulo in zip(cifras1, modulos):
            suma += int(cifra) * modulo
        control1 = suma %11

        suma = 0

        for cifra,modulo in zip(cifras2, modulos):
            suma += int(cifra) * modulo
        control2 = suma %11

        if control1<2:
            control11 = control1
        else:
            control11 = 11-control1

        if control2 < 2:
            control22 = control2
        else:
            control22 = 11-control2

        dc = str(control11 + control22)
	pais = "es"
	pais = pais.upper()
	LETRAS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	items = []
	for cifra in pais:
		posicion = LETRAS.find(cifra)
		items.append(str(posicion) if posicion >= 0 else "-")
		value = "".join(items)
	cifras = ccc + value +"00"

	cuenta = 13
	resto = 0
	i=0
	divisor = 97
	while i<len(cifras):
		dividendo = str(resto) + cifras[i: i+cuenta]
		resto = int(dividendo) % divisor
		i+= cuenta
	cifras = (98-resto)
	cantidad = 2 - len(cifras)
	ceros = "0"*cantidad
	final = pais+ceros+str(cifras)+ccc

	final = final.replace("IBAN", "")
	final = final.replace(" ", "")
	final = final.replace("-", "")
	items = []
	for i in range(6): items.append(iban[i*4: (i+1)*4])
	final.join(items)

	self.IBAN = final

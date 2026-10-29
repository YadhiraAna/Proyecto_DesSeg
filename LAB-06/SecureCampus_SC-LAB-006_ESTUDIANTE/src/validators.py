from decimal import Decimal, InvalidOperation

#from decimal import Decimal
#import decimal
#SE TIENE QUE IR HACIENDO LAS VALIDACIONES PRIMERO QUE EL NUMERO ESTE ENTRE 0 Y 100, LUEGO QUE NO TENGA MAS DE 2 DECIMALES, LUEGO QUE NO SEA BOOLEANO, LUEGO QUE NO SEA NULO, LUEGO QUE NO SEA TEXTO NO NUMERICO, LUEGO QUE NO SEA NAN O INFINITY.
#def validar_calificacion(valor):
#    # TODO: rechazar valores nulos, booleanos, texto no numérico, NaN, Infinity, fuera de 0..100 y >2 decimales.
    # No redondear entradas incorrectas.
#    return Decimal(str(valor))


#def validar_calificacion(valor):
#    numero =decimal(str(valor))
#    if(numero < 0 or numero > 100):
#        raise ValueError("fuera de rango, la calificación debe estar entre 0 y 100")
#    return Decimal(str(valor))

from decimal import Decimal, InvalidOperation

from decimal import Decimal, InvalidOperation


def validar_calificacion(valor):
    # Se verifica si el valor es nulo; si es así, se lanza una excepción ValueError.
    if valor is None:
        raise ValueError("El valor no puede ser nulo")
    # Se verifica si el valor es un booleano; si es así, se lanza una excepción ValueError.
    if isinstance(valor, bool):
        raise ValueError("El valor no puede ser booleano")
    try:
        # Se intenta convertir el valor a un objeto Decimal para poder realizar las validaciones posteriores.
        numero = Decimal(str(valor))
    except InvalidOperation:
        # Cuando el valor no es un número válido, se lanza una excepción ValueError.
        raise ValueError("El valor no es un número válido")
    # Se verifica si el número es NaN o Infinity; si es así, se lanza una excepción ValueError.
    if numero.is_nan() or numero.is_infinite():
        raise ValueError("El valor no puede ser NaN o Infinity")
    # El número debe estar entre 0 y 100; si no lo está, se lanza una excepción ValueError.
    if numero < 0 or numero > 100:
        raise ValueError(
            "Fuera de rango, la calificación debe estar entre 0 y 100"
        )
    # Se verifica si el número tiene más de 2 decimales; si es así, se lanza una excepción ValueError.
    if numero.as_tuple().exponent < -2:#con exponent se obtiene el exponente del número decimal, que indica cuántos dígitos hay después del punto decimal. Si el exponente es menor que -2, significa que hay más de 2 dígitos después del punto decimal.
        raise ValueError(
            "El valor no puede tener más de 2 decimales"
        )
    # Si todas las validaciones son correctas, se devuelve el valor convertido a Decimal.
    return numero

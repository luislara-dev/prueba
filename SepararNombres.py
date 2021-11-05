def SepararNombres( nombre ):
    """
    Autor original en código PHP: eduardoromero.
    https://gist.github.com/eduardoromero/8495437
    
    Separa los nombres y los apellidos y retorna una tupla de tres
    elementos (string) formateados para nombres con el primer caracter
    en mayuscula. Esto es suponiendo que en la cadena los nombres y 
    apellidos esten ordenados de la forma ideal:
 
    1- primer apellido.
    2- segundo apellido.
    3- nombre o nombres.
 
    Separar nombres( '' )
    >>> ('Primer Apellido', 'Segundo Apellido', 'Nombres')
    """
 
    # Separar el nombre completo en espacios.
    tokens = nombre.split(" ")
 
    # Lista donde se guarda las palabras del nombre.
    names = []
 
    # Palabras de apellidos y nombres compuestos.
    especial_tokens = ['da', 'de', 'di', 'do', 'del', 'la', 'las', 
    'le', 'los', 'mac', 'mc', 'van', 'von', 'y', 'i', 'san', 'santa']
 
    prev = ""
    for token in tokens:
        _token = token.lower()
 
        if _token in especial_tokens:
            prev += token + " "
 
        else:
            names.append(prev + token)
            prev = ""
 
    num_nombres = len(names)
    nombres, apellido1, apellido2 = "", "", ""
 
    # Cuando no existe nombre.
    if num_nombres == 0:
        nombres = ""
 
    # Cuando el nombre consta de un solo elemento.
    elif num_nombres == 1:
        apellido1 = names[0]
 
    # Cuando el nombre consta de dos elementos.
    elif num_nombres == 2:
        apellido1 = names[0]
        apellido2 = names[1]
 
    # Cuando el nombre consta de tres elementos.
    elif num_nombres == 3:
        apellido1 = names[0]
        apellido2 = names[1]
        nombres = names[2]
    # Cuando el nombre consta de más de tres elementos.
    elif num_nombres == 4:
        apellido1 = names[0]
        apellido2 = names[1]
        nombres = names[2] + " " + names[3]
    elif num_nombres == 5:
        apellido1 = names[0]
        apellido2 = names[1]
        nombres = names[2] + " " + names[3] + " " + names[4]
      # Establecemos las cadenas con el primer caracter en mayúscula.
    nombres = nombres.title()
    apellido1 = apellido1.title()
    apellido2 = apellido2.title()
 
    return (apellido1, apellido2, nombres)

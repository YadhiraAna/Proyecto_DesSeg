# ==========================================
# VERSIONES INICIALES 
# ==========================================

# Versión inicial comentada de la función de modificación
#def puede_modificar(user, student_id, group_id, con):
    # Nota tipo TODO que describe la regla de negocio original que debía cumplir esta función
#    # TODO: solo profesor asignado al grupo Y estudiante inscrito en él.
#    return True

# Versión inicial comentada de la función de consulta
#def puede_consultar(user, student_id, group_id, con):
    # Nota tipo TODO que describe los permisos de consulta esperados originalmente
#    # TODO: estudiante propio e inscrito, o profesor asignado al grupo con estudiante inscrito.
#    return True


# ==========================================
# FUNCIONES AUXILIARES PRIVADAS
# ==========================================

def _inscrito(con, student_id, group_id):
    """
    Función auxiliar privada para verificar si un estudiante está inscrito en un grupo.
    """
    # Ejecuta una consulta SQL segura en la tabla 'enrollments' buscando coincidencias de estudiante y grupo
    return con.execute('SELECT 1 FROM enrollments WHERE student_id=? AND group_id=?',
                       (student_id, group_id)).fetchone() is not None
    # .fetchone() extrae el primer resultado y 'is not None' devuelve True si existe el registro, o False si no.


def _profesor_del_grupo(con, user, group_id):
    """
    Función auxiliar privada para verificar si el usuario actual es profesor y está asignado al grupo.
    """
    # Verifica dos condiciones: que el rol del usuario sea 'profesor' Y que exista el grupo asignado a su ID
    return user['role'] == 'profesor' and con.execute(
        'SELECT 1 FROM groups WHERE id=? AND professor_id=?',
        (group_id, user['id'])).fetchone() is not None
    # Si la primera condición es falsa, ocurre un cortocircuito y no se ejecuta la consulta SQL.


# ==========================================
# FUNCIONES PRINCIPALES DE AUTORIZACIÓN
# ==========================================

def puede_modificar(user, student_id, group_id, con):
    """
    Función principal que determina si un usuario tiene permisos para MODIFICAR.
    """
    # Solo se permite al profesor asignado y si el alumno está inscrito.
    # Retorna True únicamente si ambas funciones auxiliares devuelven True simultáneamente.
    return _profesor_del_grupo(con, user, group_id) and _inscrito(con, student_id, group_id)


def puede_consultar(user, student_id, group_id, con):
    """
    Función principal que determina si un usuario tiene permisos para CONSULTAR.
    """
    #  Si el estudiante no está inscrito en el grupo, se rechaza la consulta de inmediato.
    if not _inscrito(con, student_id, group_id):
        return False
        
    # Si el usuario que solicita la consulta tiene el rol de 'estudiante'...
    if user['role'] == 'estudiante':
        # ...solo se le permite ver sus propios datos (su id debe coincidir con el student_id consultado).
        return user['id'] == student_id      # solo la propia
        
    # Si el usuario no es un estudiante (por ejemplo, es profesor), se valida si es el profesor del grupo.
    return _profesor_del_grupo(con, user, group_id)
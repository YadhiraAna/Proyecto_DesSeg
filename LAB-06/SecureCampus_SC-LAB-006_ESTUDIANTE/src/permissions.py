#def puede_modificar(user,student_id,group_id,con):
    # TODO: solo profesor asignado al grupo Y estudiante inscrito en él.
#    return True

#def puede_consultar(user,student_id,group_id,con):
    # TODO: estudiante propio e inscrito, o profesor asignado al grupo con estudiante inscrito.
#    return True

def _inscrito(con, student_id, group_id):
    return con.execute('SELECT 1 FROM enrollments WHERE student_id=? AND group_id=?',
                       (student_id, group_id)).fetchone() is not None

def _profesor_del_grupo(con, user, group_id):
    return user['role'] == 'profesor' and con.execute(
        'SELECT 1 FROM groups WHERE id=? AND professor_id=?',
        (group_id, user['id'])).fetchone() is not None

def puede_modificar(user, student_id, group_id, con):
    # Solo profesor asignado al grupo Y alumno inscrito. Admin y estudiante: denegado.
    return _profesor_del_grupo(con, user, group_id) and _inscrito(con, student_id, group_id)

def puede_consultar(user, student_id, group_id, con):
    if not _inscrito(con, student_id, group_id):
        return False
    if user['role'] == 'estudiante':
        return user['id'] == student_id      # solo la propia
    return _profesor_del_grupo(con, user, group_id)
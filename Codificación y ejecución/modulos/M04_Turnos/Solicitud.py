from datetime import datetime

class Solicitud:

    def _init__(self, codigo, usuario_codigo, recurso_codigo, fecha=None):
        self.codigo = codigo
        self.usuario_codigo = usuario_codigo
        self.recurso_codigo = recurso_codigo
        self.fecha = fecha if fecha else datetime.now()
        self.estado = "En espera"

    def otorgar(self):
        self.estado = "Otorgado"

    def cancelar(self):
        self.estado = "Cancelado"

    def reiniciar(self):
        self.estado = "En espera"

    def __str__(self):
        return f"Solicitud({self.codigo}: {self.usuario_codigo}, {self.estado})"

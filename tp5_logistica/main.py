from persistencia.repositorio_archivo import RepositorioArchivo
from servicios.sistema_logistica import SistemaLogistica
from interfaz.menu_consola import MenuConsola


def main():
    repositorio = RepositorioArchivo("datos/datos_logistica.json")
    sistema = SistemaLogistica(repositorio)
    menu = MenuConsola(sistema)

    menu.iniciar()


if __name__ == "__main__":
    main()
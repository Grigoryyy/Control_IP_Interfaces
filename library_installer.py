import importlib


def check_library(library):
    try:
        importlib.import_module(library)
        return True
    except ImportError:
        return False


def install_library(library):
    try:
        import pip
        pip.main(['install', library])
        return True
    except Exception:
        return False


required_libraries = {
    'Flask': 'flask',
    'Flask-Login': 'flask_login',
    'psycopg2-binary': 'psycopg2-binary'
}

for library_name, library in required_libraries.items():
    if check_library(library):
        print(f'{library_name} library is already installed')
    else:
        print(f'Installing {library_name} library...')
        if install_library(library):
            print(f'{library_name} library has been successfully installed')
        else:
            print(f'Failed to install {library_name} library')
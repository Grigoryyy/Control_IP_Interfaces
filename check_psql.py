import subprocess


def check_postgresql():
    # Проверяем наличие PostgreSQL
    try:
        subprocess.check_output(["which", "psql"])
        return "PostgreSQL уже установлен"
    except subprocess.CalledProcessError:
        return "PostgreSQL не установлен"


def install_postgresql():
    check = check_postgresql()
    if check == "PostgreSQL не установлен":
        user_input = input("Install Postgresql? y/n ")
        if user_input == "y":
            try:
                subprocess.call(["sudo", "apt", "update"])
                subprocess.call(["sudo", "apt-get", "install", "postgresql", "postgresql-contrib"])
                print("PostgreSQL успешно установлен")
            except subprocess.CalledProcessError:
                print("Возникла ошибка при установке PostgreSQL")
        elif user_input == "n":
            print("Вы отказались от установки PostgreSQL")
        else:
            print("Ошибка ввода")
    else:
        print(check)


install_postgresql()

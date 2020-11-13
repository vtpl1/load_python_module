import os


def get_folder(sub_folder) -> str:
    session_folder = os.path.join(os.getcwd(), sub_folder)
    if os.path.exists(session_folder):
        print("{} folder exists in {}".format(sub_folder, session_folder))
    else:
        try:
            os.makedirs(session_folder)
            print("{} folder created in {}".format(sub_folder, session_folder))
        except OSError as e:
            print(e)
            raise
    return session_folder


def get_session_folder() -> str:
    return get_folder("session")


def get_app_folder() -> str:
    return get_folder("app")


def get_progress_folder() -> str:
    return get_session_folder()


def get_config_folder() -> str:
    return get_session_folder()

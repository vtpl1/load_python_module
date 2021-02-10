import os
import time


def get_folder(sub_folder) -> str:
    session_folder = os.path.join(os.getcwd(), sub_folder)
    if not os.path.exists(session_folder):
        try:
            os.makedirs(session_folder)
            print("{} folder created in {}".format(sub_folder, session_folder))
        except OSError as e:
            print(e)
            raise
    return session_folder + os.path.sep


def get_folder_dont_create(sub_folder) -> str:
    session_folder = os.path.join(os.getcwd(), sub_folder)
    if not os.path.exists(session_folder):
        pass
    return session_folder + os.path.sep


def get_va_session_name() -> str:
    return get_session_folder() + "va_session"


def get_va_session_yaml_name() -> str:
    return get_session_folder() + "va_session.yaml"


def get_va_session_override_yaml_name() -> str:
    return get_session_folder() + "va_session_override.yaml"


def get_va_session_running_yaml_name() -> str:
    return get_session_folder() + "va_session_running.yaml"


def get_session_yaml_folder() -> str:
    return get_folder("override")


def get_session_folder() -> str:
    return get_folder("session")


def get_app_folder() -> str:
    return get_folder("app")


def get_dump_folder() -> str:
    return get_folder("resLoc")


def get_progress_folder() -> str:
    return get_session_folder()


def get_data_folder() -> str:
    return get_folder("persistent")

def get_images_folder() -> str:
    return get_folder("images")

def get_config_folder() -> str:
    return get_session_folder()


def get_temp_file_name() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def get_final_file_name(initial_file_name: str) -> str:
    return initial_file_name + "_" + time.strftime("%Y%m%d-%H%M%S")


def get_models_folder() -> str:
    return get_folder("models")

def get_id():
    return int(round(time.time() * 1000000))


def get_current_time():
    return int(round(time.time() * 1000))


def get_current_time_sec():
    return int(round(time.time()))


def change_from_nake_case_to_camel_case(in_str: str) -> str:
    # saving first and rest using split()
    init, *temp = in_str.split('_')
    # using map() to get all words other than 1st
    # and titlecasing them
    return ''.join([init.lower(), *map(str.title, temp)])


def change_from_camel_case_to_snake_case(in_str: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in in_str]).lstrip('_')


def struct_to_dict(struct):
    result = {}

    #print struct
    def get_value(value):
        if (type(value) not in [int, float, bool]) and not bool(value):
            # it's a null pointer
            value = None
        elif type(value) is bytes and len(value) > 0:
            value = value.decode("utf-8")
        elif hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            #print value
            value = get_array(value)
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = struct_to_dict(value)
        return value

    def get_array(array):
        ar = []
        for value in array:
            value = get_value(value)
            ar.append(value)
        return ar

    for field_name, _ in struct._fields_:
        value = getattr(struct, field_name)
        # if the type is not a primitive and it evaluates to False ...
        value = get_value(value)
        result[change_from_camel_case_to_snake_case(field_name)] = value
    return result

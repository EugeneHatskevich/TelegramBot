def delete_object(object_list: list, chat_id: int):
    for elem in object_list:
        if elem.profile.external_id == chat_id:
            elem.delete()

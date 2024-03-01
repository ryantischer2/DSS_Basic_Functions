import uuid

uuid2test = "04459846-7e50-41ee-b51d-6876614d076a"
uuid2fail = "04459846-7e50-41ee-b51d-6876614d076"

def is_uuid(uuid_2_test, version):

    try:
        uuid_data = uuid.UUID(uuid_2_test, version=4)
        return str(uuid_data) == uuid_2_test

    except ValueError:
        return False


print (is_uuid(uuid2test,4))
print (is_uuid(uuid2fail, 4))
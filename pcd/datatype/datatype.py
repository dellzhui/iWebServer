from interface.datatype.datatype import JsonDatatypeBase


class DeviceRegisiterDataType(JsonDatatypeBase):
    def __init__(self, DeviceType, Mac, SerialNumber=None):
        self.DeviceType = DeviceType
        self.Mac = Mac
        self.SerialNumber = SerialNumber

    def __str__(self):
        return self.to_json()

# https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#iZqoAUDZjokXtzfkaGiYqg
class CreateContainerDataType(JsonDatatypeBase):
    def __init__(self, roomIdStr: str, roomJoinPin, macAddress, email):
        self.roomId: str = roomIdStr
        self.joinPin = roomJoinPin
        self.localMac = macAddress
        self.UserEmail = email
        self.jobName = None

        if(email != None and '@' in email):
            self.jobName = email.split('@')[0]

    def __str__(self):
        return self.to_json()


# https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#6BDw9WT2SpktspRtzjZhDk
class DestroyContainerDataType(JsonDatatypeBase):
    def __init__(self, nameSpace, email):
        self.namespace = nameSpace
        self.UserEmail = email
        self.jobName = None

        if(email != None and '@' in email):
            self.jobname = email.split('@')[0]

    def __str__(self):
        return self.to_json()

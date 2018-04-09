class GeneralInfo():
    def __init__(self, uuid, name, phone_num="", address="", dob="", data_type="general_info", access_class_id=1):
        self.uuid = uuid
        self.name = name
        self.phone_num = phone_num
        self.address = address
        self.dob = dob
        self.data_type = data_type
        self.access_class_id = access_class_id

    @staticmethod
    def general_info_parser(patient_uuid, patient_data):

        general_info = GeneralInfo(uuid = patient_uuid,
                    name = getattr(patient_data, "name"),
                    phone_num = getattr(patient_data, "phone_num") if getattr(patient_data, "phone_num") else "",
                    address = getattr(patient_data, "address") if getattr(patient_data, "address") else "",
                    dob = getattr(patient_data, "dob") if getattr(patient_data, "dob") else "")
        return general_info




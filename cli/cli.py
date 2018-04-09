import json
import logging
import argparse
import uuid
import general_info


logging.basicConfig(level=logging.DEBUG, file="cli.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def parse_file_json(file_name):
    with open(file_name) as fp:
        content = json.load(fp)
    return content


class PatientData(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser("./cli.py --file=input_file_with_patient_info")
    argparser.add_argument('--in-file', '-i', action='store', help='input file name')
    argparser.add_argument('--patient', '-p', action='store_true', help="patient info")
    argparser.add_argument('--actor', '-a', action='store_true', help="actor info")

    args = argparser.parse_args()
    if not args.in_file:
        argparser.error("Input file is required")
    file_content = parse_file_json(args.in_file)
    if args.patient:
        patient_uuid = str(uuid.uuid4())
        patient_data = PatientData(file_content)
        general_info = general_info.GeneralInfo.general_info_parser(patient_uuid, patient_data)
        general_info_json = json.dumps(general_info.__dict__)


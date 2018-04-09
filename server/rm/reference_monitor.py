import json
from boto3.dynamodb.conditions import Key, Attr

# from boto3 import resource
import logging


LEVEL = "level"
CATEGORY = "category"
SUBJECT_TABLE_NAME = "Subjects"
ROLE_PERMISSION_TABLE_NAME = "RolePermissions"
OBJECT_TABLE_NAME = "Objects"
OBJECT_ACCESS_LIST_TABLE_NAME = ""


class ReferenceMonitor:
    def __init__(self, dynamo_db):
        """

        :param dynamo_db: boto3.resource
        """
        self.subject_table = dynamo_db.Table(SUBJECT_TABLE_NAME)
        self.role_permission_table = dynamo_db.Table(ROLE_PERMISSION_TABLE_NAME)
        self.object_table = dynamo_db.Table(OBJECT_TABLE_NAME)
        self.object_access_list_table = dynamo_db.Table(OBJECT_ACCESS_LIST_TABLE_NAME)

    def verify(self, subject_permission, object_access_list):
        """
        :param subject_permission: permission of subject
        :type subject_permission: json
        :param object_access_list: object access of list
        :type object_access_list: json
        :return: boolean
        """
        for permission in subject_permission:
            for access in object_access_list:
                if permission[LEVEL] == object_access_list[LEVEL] and \
                        permission[CATEGORY] == object_access_list[CATEGORY]:
                    return True
        return False

    def get_permissions_from_uuid(self, uuid):
        """

        :param uuid:
        :return:josn
        """

        res = self.subject_table.query(KeyConditionExpression=Key(uuid))
        role_permission_id = res["permissions"]
        res = self.role_permission_table.query(KeyConditionExpression=Key(role_permission_id))
        logging.debug(str(res))
        return res["permissions"]

    def authorized(self, subejct_uuid, object_uuid):
        """

        :param subejct_uuid:
        :param object_uuid:
        :returns: list of json object
        :return: list
        """
        subject_permissions = self.get_permissions_from_uuid(subejct_uuid)
        results = self.object_table.query(KeyConditionExpression=Key(object_uuid))
        logging.debug(repr(results))
        allowed_object_data = []
        for res in results:
            access_class_id = res["access_class_id"]
            access_classes = self.object_access_list_table.query(KeyConditionExpression=Key(access_class_id))
            logging.debug("Object access list: {}".format(access_classes))
            object_access_allowed = self.verify(subject_permissions, access_classes)
            if object_access_allowed:
                del res['uuid']
                allowed_object_data.append(res)
        if allowed_object_data:
            logging.info("Allowing the access to object of UUID: {} for subject: {}".format(object_uuid, subejct_uuid))
            logging.info("Access allowed because subejct permissions are : {}".format(subject_permissions))
            logging.info("Data on which access is allowed are: {}".fomrat(repr(allowed_object_data)))
        return allowed_object_data

# -*- coding: utf-8 -*-
"""
Implementation of the POST Service
"""
from plone.restapi.services import Service
from plone.restapi.deserializer import json_body

from zope.component import getUtility
from clms.statstool.utility import IDownloadStatsUtility


class RegisterItemPost(Service):
    """ post service """

    def reply(self):
        """ json response """
        body = json_body(self.request)

        start = body.get("Start")
        user = body.get("User")
        dataset = body.get("Dataset")
        transformation_data = body.get("TransformationData")
        task_id = body.get("TaskID")
        transformation_duration = body.get("TransformationDuration")
        transformation_size = body.get("TransformationSize")
        transformation_result_data = body.get("TransformationResultData")
        successful = body.get("Successful")

        response_json = {}
        response_json["Start"] = start
        response_json["User"] = user
        response_json["Dataset"] = dataset
        response_json["TaskID"] = task_id
        response_json["TransformationData"] = transformation_data
        response_json["TransformationDuration"] = transformation_duration
        response_json["TransformationSize"] = transformation_size
        response_json["TransformationResultData"] = transformation_result_data
        response_json["Successful"] = successful

        utility = getUtility(IDownloadStatsUtility)
        response_json = utility.register_item(response_json)

        self.request.response.setStatus(201)
        return response_json

# -*- coding: utf-8 -*-
"""
Each time we need to interact with the utility we need to get it and call the relevant method.
In this example we call the "register_item" method.
It's Plone REST API's best practice to send all parameters as JSON in the body, see Plone REST
API's documentation regarding content-manipulation here:
https://plonerestapi.readthedocs.io/en/latest/content.html#content-manipulation
Thus as a first thing to retrieve the information is to convert that JSON information in the body
to a python dict, and we are using the json_body(self.request) to achieve that.
After doing all the relevant operations we should set the HTTP status of the response (by default
it will be an HTTP 200 OK), and return the JSON information needed by as a python dict. Plone REST API
will handle that dict and encode it as a proper JSON response.
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

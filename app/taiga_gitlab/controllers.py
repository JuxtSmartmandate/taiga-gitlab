from flask import Blueprint, Response, request
import json
import configparser
import os
import logging
from app import app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

taiga_gitlab = Blueprint('taiga_gitlab', __name__, url_prefix="/taiga-gitlab")


@taiga_gitlab.route('/', methods=['GET', 'POST'])
def gitlab_view():
    if request.method == 'GET':
        return Response("It's working!!!.")

    if request.method == 'POST':
        incoming_data = json.loads(request.data.decode('utf-8'))
        logger.debug(incoming_data)
        if "type" in incoming_data:
            if incoming_data["type"] == "userstory" and incoming_data["action"] == "create":
                taiga_project_id = incoming_data["data"]["project"]["id"]

                projects_config_file_path = app.config.get("PROJECTS_CONFIG_FILE_PATH")

                if projects_config_file_path:
                    if os.path.isfile(projects_config_file_path):
                        projects_config = configparser.ConfigParser()
                        projects_config.read(projects_config_file_path)
                        if "taiga_gitlab_projects_id_mapping" in projects_config:
                            projects_mapping = projects_config["taiga_gitlab_projects_id_mapping"].get("mappings")
                            projects_mapping_dict = {}
                            for each_mapping in projects_mapping.split(";"):
                                each_mapping_splitted = each_mapping.split(":")
                                if len(each_mapping_splitted) == 2:
                                    projects_mapping_dict[int(each_mapping_splitted[0])] = int(each_mapping_splitted[1])

                            if taiga_project_id in projects_mapping_dict:
                                logging.debug(taiga_project_id, projects_mapping_dict)

                        else:
                            logger.error("No taiga_gitlab_projects_id_mapping section defined in {0} ".format(projects_config_file_path))

                    else:
                        logger.error("No projects config file path found")
        logger.debug(incoming_data)
        return Response("It's working!!!.")

    return Response()

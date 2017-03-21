from flask import Blueprint, Response, request
import json
import logging
from app import app
import gitlab
import traceback

LOG_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

taiga_gitlab = Blueprint('taiga_gitlab', __name__, url_prefix="/taiga-gitlab")


@taiga_gitlab.route('/', methods=['GET', 'POST'])
def gitlab_view():
    if request.method == 'GET':
        return Response("It's working!!!.")

    if request.method == 'POST':
        response_dict = {}
        incoming_data = json.loads(request.data.decode('utf-8'))
        gitlab_project_id = request.args.get("gitlab_project_id")
        gitlab_access_token = app.config.get("GITLAB_PERSONAL_ACCESS_TOKEN")
        gitlab_url = app.config.get("GITLAB_URL")

        if "type" in incoming_data:
            if incoming_data["type"] == "userstory" and incoming_data["action"] == "create":
                if gitlab_access_token and gitlab_url:
                    if gitlab_project_id:
                        story_subject = incoming_data["data"]["subject"]
                        story_description = incoming_data["data"]["description"]
                        gl = gitlab.Gitlab(gitlab_url, gitlab_access_token)
                        try:
                            gl_issue = gl.project_issues.create({'title': story_subject, 'description': story_description}, project_id=gitlab_project_id)
                        except Exception as e:
                            response_dict["error"] = "Could not add issue in gitlab"
                            response_dict["error_trace"] = traceback.format_stack()
                            logger.error(e)
                        else:
                            response_dict["success"] = True
                    else:
                        response_dict["error"] = "Gitlab project ID not provided in WEBHOOK URL."
                else:
                    response_dict["error"] = "Gitlab access token or gitlab url not configured."


        response = app.response_class(
            response=json.dumps(response_dict),
            status=200,
            mimetype='application/json'
        )

        return response

    return Response()

import json
import os

import jinja2
import markdown
import markdown.extensions.fenced_code
from flask import Blueprint, abort, jsonify, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, close_room, disconnect, emit, join_room, leave_room, rooms
from jinja2 import TemplateNotFound
from mTree.components.registry import Registry
from mTree.development.mtree_configuration import MTreeConfiguration
from mTree.server.actor_system_connector import ActorSystemConnector
from mTree.simulation.mes_simulation_library import MESSimulationLibrary

subject_area = Blueprint("subject_area", __name__, template_folder="subject_templates")

subject_area.jinja_loader = jinja2.ChoiceLoader(
    [
        subject_area.jinja_loader,
        jinja2.PackageLoader("mTree", "subject_interface/subject_templates"),
        # jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
    ]
)

MTree_configuration = MTreeConfiguration()
SUBJECT_IDS = MTree_configuration.instance.subject_ids


@subject_area.route("/", defaults={"page": "index"}, methods=["GET", "POST"])
@subject_area.route("/<page>")
def subject_landing_page(page):
    # if 'subject-id' in session.keys():
    #     subject_id = session['subject-id']
    #     return render_template('subject_viewer.html', subject_id=subject_id)

    if request.method == "POST":
        subject_id = request.form["subject-id"]
        if subject_id in SUBJECT_IDS:
            # session['subject-id'] = subject_id
            return render_template("subject_viewer.html", subject_id=subject_id)
        else:
            return render_template("subject_landing.html", error="Invalid Subject ID")
    else:
        return render_template("subject_landing.html")

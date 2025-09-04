from flask import Flask

from mongodb.DocumentStore import DocumentStore


class ProjectManager:
    def __init__(self, db: DocumentStore.Database):
        self.__db = db

    def register_routes(self, app: Flask) -> None:
        @app.route('/project/<string:project_name>', methods=['POST'])
        def create_project(project_name):
            # TODO: Duplicate name error handling.
            self.__db.create_collection(project_name)
            return {"success": True, "project": project_name}, 201

        @app.route('/projects', methods=['GET'])
        def list_projects():
            collections = self.__db.get_collection_names()
            return {"projects": collections}, 200

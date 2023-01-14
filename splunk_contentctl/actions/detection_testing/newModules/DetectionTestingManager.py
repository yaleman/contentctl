from splunk_contentctl.objects.test_config import TestConfig
from splunk_contentctl.objects.app import App
import pathlib
import os
from splunk_contentctl.helper.utils import Utils
from urllib.parse import urlparse

CONTAINER_APP_PATH = pathlib.Path("apps")


class DetectionTestingManager:
    def __init__(self, config: TestConfig):
        self.config = config
        self.stage_apps()

        pass

    def create_DetectionTestingInfrastructureObjects(self):
        pass

    def createThreads(self):
        pass

    def get_app_from_splunkbase(self, app: App, target_directory: pathlib.Path):
        print(f"App {app.title} will be downloaded by the container at runtime")

    def get_app_from_local_path(self, app: App, target_directory: pathlib.Path):
        if app.local_path is None:
            raise (
                Exception(
                    f"Error: cannot copy app {app.title} from local.  local_path is None"
                )
            )

        path_to_local_file = pathlib.Path(app.local_path)
        path_to_destination = target_directory.joinpath(path_to_local_file.name)
        Utils.copy_local_file(
            str(path_to_local_file), str(path_to_destination), verbose_print=True
        )

    def get_app_from_http_path(self, app: App, target_directory: pathlib.Path):
        if app.http_path is None:
            raise (
                Exception(
                    f"Error: cannot download app {app.title} from http.  http_path is None"
                )
            )
        # print(f"Downloading http app [{app.title} - {app.release}]...", end="")
        path_on_server = str(urlparse(app.http_path).path)
        # Get just the filename from that path
        filename = pathlib.Path(path_on_server).name
        destination_path = target_directory.joinpath(filename)
        Utils.download_file_from_http(
            app.http_path, destination_path.as_posix(), verbose_print=True
        )

    def get_app(self, app: App, target_directory: pathlib.Path):
        if app.must_download_from_splunkbase:
            # This app will be downloaded by the container
            self.get_app_from_splunkbase(app, target_directory)
        elif app.local_path is not None:
            self.get_app_from_local_path(app, target_directory)
        elif app.http_path:
            self.get_app_from_http_path(app, target_directory)
        else:
            raise (
                Exception(
                    f"Error: Unable to get app {app.title} - no Splunkbase info, local_path, or http_path"
                )
            )

    def stage_apps(self):

        try:
            # Make sure the directory exists.  If it already did, that's okay. Don't delete anything from it
            # We want to re-use previously downloaded apps
            os.makedirs(CONTAINER_APP_PATH, exist_ok=True)

        except Exception as e:
            raise (
                Exception(
                    f"Error: When trying to make the {CONTAINER_APP_PATH}: [{str(e)}]"
                )
            )

        alphabetically_sorted_apps = sorted(self.config.apps, key=lambda a: a.title)

        # Get all the other apps
        app_exceptions: list[str] = []
        for app in alphabetically_sorted_apps:
            try:
                self.get_app(app, CONTAINER_APP_PATH)
            except Exception as e:
                app_exceptions.append(
                    f"Error: Unable to stage app for installation: [{str(e)}"
                )
        if len(app_exceptions) == 0:
            print(
                f"[{len(self.config.apps)}] apps processed successfully for installation"
            )
            return
        else:
            exceptions_string = "\n\t - ".join(app_exceptions)
            raise (
                Exception(
                    f"Error: Unable to stage {len(app_exceptions)} apps for installation:\n\t - {exceptions_string}"
                )
            )
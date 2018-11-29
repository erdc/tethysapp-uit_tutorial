from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class UitPlusTutorial(TethysAppBase):
    """
    Tethys app class for UITPlus Tutorial.
    """

    name = 'UITPlus Tutorial'
    index = 'uit_plus_tutorial:home'
    icon = 'uit_plus_tutorial/images/icon.gif'
    package = 'uit_plus_tutorial'
    root_url = 'uit-plus-tutorial'
    color = '#d35400'
    description = 'Demonstrates how to use the UITPlus Tethys jobs interface.'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    PROVIDER_NAME = 'UITPlus'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='uit-plus-tutorial',
                controller='uit_plus_tutorial.controllers.home'
            ),
            UrlMap(
                name='run_job',
                url='uit-plus-tutorial/run-job',
                controller='uit_plus_tutorial.controllers.run_job'
            ),
            UrlMap(
                name='status',
                url='uit-plus-tutorial/status',
                controller='uit_plus_tutorial.controllers.status'
            ),
        )

        return url_maps

    def custom_settings(self):
        """
        Example custom_settings method.
        """
        custom_settings = (
            CustomSetting(
                name='project_id',
                type=CustomSetting.TYPE_STRING,
                description='Project ID on the UIT supercomputing resources.',
                required=True
            ),
        )

        return custom_settings

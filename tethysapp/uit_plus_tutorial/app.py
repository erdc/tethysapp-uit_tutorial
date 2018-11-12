from tethys_sdk.base import TethysAppBase, url_map_maker


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
        )

        return url_maps

"""This XBlock provides syntax highlighting via the PrismJS library"""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String


class PrismXBlock(XBlock):
    """
    Provide syntax highlighting within a code editor 
    """

    display_name = String(help="The display name for this component.",
                          default="Syntax Highlighter",
                          scope=Scope.settings)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the PrismXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/prism.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/prism.css"))
        frag.add_javascript(self.resource_string("static/js/src/prism.js"))
        frag.initialize_js('PrismXBlock')
        return frag


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PrismXBlock",
             """<prism/>
             """),
            ("Multiple PrismXBlock",
             """<vertical_demo>
                <prism/>
                <prism/>
                <prism/>
                </vertical_demo>
             """),
        ]

"""This XBlock provides syntax highlighting via the PrismJS library"""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
# from xblockutils.studio_editable import StudioEditableXBlockMixin, loader


class PrismXBlock(XBlock):
    """
    Provide syntax highlighting within a code editor 
    """

    display_name = String(
        help="The display name for this component.",
        default="Syntax Highlighter",
        scope=Scope.settings
    )

    code_data = String(
        help="Code contents to display within editor",
        default="print('hello world')",
        scope=Scope.content
    )

    #these are placeholders for now
    language = String(
        help="Language selector for code within editor",
        default='python',
        values=[
            {'display_name': 'python', 'value': 'python'},
            {'display_name': 'javascript', 'value': 'javascript'},
        ],
        scope=Scope.settings
    )

    # theme_selector = String(
    #     help="Theme selector to select prism theme",
    #     default="light",
    #     values=[
    #         {'display_name': 'light', 'value': 'light'},
    #         {'display_name': 'dark', 'value': 'light'}
    #     ],
    #     scope=Scope.settings
    # )

    # height = Integer(

    # )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        Return a fragment that contains the editor with code for student view.
        """
        html = self.resource_string("static/html/lms.html")
        frag = Fragment(html.format(self=self))

        frag.add_css(self.resource_string("static/css/dark.css"))
        frag.add_javascript(self.resource_string("static/js/src/dark.js"))
        frag.initialize_js('PrismXBlock')
        return frag

    def studio_view(self, context=None):
        """
        Return a fragment that contains the editor with code for studio view.
        """
        html = self.resource_string("static/html/studio.html")
        frag = Fragment(html.format(self=self))

        frag.add_css(self.resource_string("static/css/dark.css"))
        frag.add_javascript(self.resource_string("static/js/src/dark.js"))
        frag.initialize_js('PrismXBlockStudio')
        return frag
         

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Update saved code input with new code input
        """
        self.code_data = data['content']
        
        return {'content': self.code_data}

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

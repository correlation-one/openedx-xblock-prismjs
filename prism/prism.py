"""This XBlock provides syntax highlighting via the PrismJS library"""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblockutils.resources import ResourceLoader

class PrismXBlock(XBlock):
    """
    Provide syntax highlighting within a code editor 
    """

    xblock_loader = ResourceLoader(__name__)

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

    LANGUAGE_CHOICES = [
        {'display_name': 'python', 'value': 'python'},
        {'display_name': 'javascript', 'value': 'javascript'},
    ]

    #these are placeholders for now
    language = String(
        help="Language selector for code within editor",
        default='python',
        values=LANGUAGE_CHOICES,
        scope=Scope.settings
    )

    THEME_CHOICES = [
        {'display_name': 'light', 'value': 'light'},
        {'display_name': 'dark', 'value': 'dark'},
    ]
    
    theme = String(
        help="Theme selector to select prism theme",
        default="dark",
        values=THEME_CHOICES,
        scope=Scope.settings
    )

    height = Integer(
        help="Height of code editor (px)",
        default=450,
        scope=Scope.settings
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        Return a fragment that contains the editor with code for student view.
        """
        frag = Fragment()
        frag.add_content(self.xblock_loader.render_django_template(
            'static/html/lms.html', 
            context={'self':self}
        ))

        frag.add_css(self.resource_string("static/css/dark.css"))
        frag.add_javascript(self.resource_string("static/js/src/dark.js"))
        frag.initialize_js('PrismXBlock')
        return frag

    def studio_view(self, context=None):
        """
        Return a fragment that contains the editor with code for studio view.
        """
        frag = Fragment()
        frag.add_content(self.xblock_loader.render_django_template(
            'static/html/studio.html', 
            context={'self':self}
        ))

        frag.add_css(self.resource_string("static/css/dark.css"))
        frag.add_javascript(self.resource_string("static/js/src/dark.js"))
        frag.initialize_js('PrismXBlockStudio')
        return frag  

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Update saved code input with new code input
        """
        self.display_name = data.get('display_name')
        self.code_data = data.get('code_data')
        self.language = data.get('language')
        self.theme = data.get('theme')
        self.height = data.get('height')
        
        return {'result': 'success'}

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

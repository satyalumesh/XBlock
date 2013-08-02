"""Content-oriented XBlocks."""
from xml.etree import ElementTree
from string import Template

from .core import XBlock, String, Scope
from .fragment import Fragment


class HelloWorldBlock(XBlock):
    """A simple block: just show some fixed content."""
    def fallback_view(self, view_name, context):
        return Fragment(u"Hello, world!")


class HtmlBlock(XBlock):
    """Render content as HTML.

    The content can have $PLACEHOLDERS, which will be substituted with values
    from the context.

    """

    content = String(help="The HTML to display", scope=Scope.content, default=u"<b>DEFAULT</b>")

    def fallback_view(self, view_name, context):
        return Fragment(Template(self.content).substitute(**context))

    def load_xml(self, xml, parent_id=None, create_block_func=None):
        root_tag_len = len(xml.tag)
        full_xml_str = ElementTree.tostring(xml, encoding='utf-8')
        content_str = full_xml_str[root_tag_len + 2:-(root_tag_len + 3)]
        self.content = unicode(content_str, encoding='utf-8').strip()
        if parent_id:
            self.parent = parent_id

    def dump_xml(self):
        el = ElementTree.Element('html')
        el.text = self.content
        return el
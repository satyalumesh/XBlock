"""Content-oriented XBlocks."""
from string import Template

from lxml import etree

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
        start_tag_len, end_tag_len = len(xml.tag) + 2, len(xml.tag) + 3
        full_xml_str = etree.tostring(xml, encoding='utf-8')
        self.content = full_xml_str.strip()[start_tag_len:-end_tag_len]
        if parent_id:
            self.parent = parent_id

    def dump_xml(self, get_block_func):
        """Dump our content as a CDATA portion inside <html></html> tags. This
        is so we can accomodate semi-broken HTML that isn't legal XML, but this
        currently causes undesired double escaping.
        """
        el = etree.Element('html')
        el.text = etree.CDATA(self.content)
        return el
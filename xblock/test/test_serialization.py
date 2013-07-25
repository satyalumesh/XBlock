"""Tests serialization and deserialization of XBlocks"""
# Allow accessing protected members for testing purposes
# pylint: disable=W0212
from mock import patch, MagicMock
# Nose redefines assert_equal and assert_not_equal
# pylint: disable=E0611
from nose.tools import assert_in, assert_equals, assert_raises, \
    assert_not_equals
# pylint: enable=E0611
from datetime import datetime

from xblock.core import XBlock, XBlockSaveError
from xblock.runtime import RuntimeSystem
#from xblock.serialization import load_xml

# This is such a totally wrong import -- replace with some mock or default
# Runtime
#from workbench.runtime import WorkbenchRuntime
# from runtime import Runtime

# def test_html_xblock_from_xml():
#     # Tests that we can load a XBlock from 
#     SIMPLE_HTML = u"""
#         <html>
#             <p>Hello <b>world!</b> </p>
#         </html>
#     """
#     html_block = load_xml(SIMPLE_HTML, Runtime)
#     assert_equals(html_block.content, u"<p>Hello <b>world!</b> </p>")

def test_sequence_from_xml():
    SEQ_HTML = u"""
        <sequence foo="bar">
            <vertical>
                <html><p>Hello World!</p></html>
            </vertical>
            <vertical>
                <html><p>Aloha ka kou!</p></html>
                <html><p>Aloha a hui hou!</p></html>
            </vertical>
        </sequence>
    """
    system = RuntimeSystem()
    seq_block = system.load_xml(SEQ_HTML)

    assert_equals(seq_block.foo, u"bar")
    assert_equals(len(seq_block.children), 2)

    print seq_block.children

    seq_block.save()

    print system._kv_store.d



    1/0

#    seq_block.dump([Scope.content, Scope.settings], format="xml")

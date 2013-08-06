"""Tests serialization and deserialization of XBlocks"""
# Allow accessing protected members for testing purposes
# pylint: disable=W0212
from mock import patch, MagicMock
# Nose redefines assert_equal and assert_not_equal
# pylint: disable=E0611
from nose.tools import assert_in, assert_is_none, assert_equals, \
                       assert_raises, assert_not_equals
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

def test_deserialize_simple_attributes():
    # Since this uses Sequences, I suppose it should be in the Workbench tests
    # instead? Not sure how we'd test any kind of serialization in the core
    # unless we have some core XBlocks...?

    # Sequence tag with some Korean text in the title.
    SEQ_XML = u"""<sequence title="I'm a \ud55c\uad6d\uc5b4 Sequence!"/>"""
    system = RuntimeSystem()
    seq_block = system.load_xml(SEQ_XML)
    assert_equals(seq_block.title, u"I'm a \ud55c\uad6d\uc5b4 Sequence!")

    BAD_ATTR_SEQ_XML = u"""<sequence not_real_attr="You can't do this!"/>"""
    assert_raises(ValueError, system.load_xml, BAD_ATTR_SEQ_XML)

    NO_ATTR_SEQ_XML = u"""<sequence/>"""
    untitled_seq_block = system.load_xml(NO_ATTR_SEQ_XML)
    assert_equals(untitled_seq_block.title, u"")


def test_deserialize_children():
    SEQ_XML = u"""
        <sequence title="Greetings">
            <html><h1>hi world!</h1></html>
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
    seq_block = system.load_xml(SEQ_XML)

    # Check the number of children
    assert_equals(len(seq_block.children), 3)
    assert_is_none(seq_block.parent)

    # Dig down into the first child
    first_vertical = system.get_block(seq_block.children[0])
    assert_equals(first_vertical.content, u"<h1>hi world!</h1>")
    assert_equals(first_vertical.parent, seq_block.id)

    # Dig down further into the third child (vertical) and its two HTML children
    second_vertical = system.get_block(seq_block.children[2])
    assert_equals(len(second_vertical.children), 2)
    second_hawaiian_greeting = system.get_block(second_vertical.children[1])
    assert_equals(second_hawaiian_greeting.content, u"<p>Aloha a hui hou!</p>")
    assert_equals(second_hawaiian_greeting.parent, second_vertical.id)


def test_serialize_children():
    pass


def test_serialize_attributes():
    pass
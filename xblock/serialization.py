"""
Serialization for XBlock
"""
from xml.etree import ElementTree

from core import XBlock

def load_xml(xml, runtime_cls, model_data=None, student_id=None):
    """
    Given a chunk of XML, a Runtime class, model_data, and a student_id,
    return a completely initialized XBlock subclass.

    `xml` is either a `basestring` with XML content, or an 

    TODO:
    * Selecting which XBlock class to load should be a runtime decision
    * Default Runtime
    * Default Model Data?

    """
    # Find the right class to load. This should probably be a Runtime
    # System decision in the end?
    if isinstance(xml, basestring):
        root = ElementTree.fromstring(xml)
    else:
        root = xml # TODO: Make this smarter later
    
    block_cls = XBlock.load_class(root.tag)
    runtime = runtime_cls() # block_cls, student ID at some point
    
    # Model data should come from the runtime?
    model_data = model_data or {}

    block = block_cls(runtime, model_data)

    # FIXME: This definitely doesn't belong here... maybe as a method
    #        in the Runtime? The incrementer is currently in Usage.
    #        cale: yes, we can put this in the runtime
    def register_child_func(block, child_xml_node):
        return 1 # Yes, all children are getting ID of 1. Placeholder.

    block.load_xml(root, register_child_func)

    return block

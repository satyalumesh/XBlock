"""
Serialization for XBlock
"""
from xml.etree import ElementTree

from core import XBlock


# Want a model_data generator, not a model_data, because you need a model_data
# per block

# pass func that takes a def id and usage id -> returns runtime and model_data
#
# load_xml(xml, runtime_system)
#
# TODO: Handle borked input without dying horribly

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


# def load_xml(xml, system):
#     # Accept either a string or XML Element
#     root = ElementTree.fromstring(xml) if isinstance(xml, basestring) else xml
#     block = system.create_block(root.tag)
#     block.load_xml(root, system.register)
# 
#     return block


# # Temp home
# class WorkbenchRuntimeSystem(RuntimeSystem):
#     """
#     kv_store needs a way to generate IDs
# 
#     Each RuntimeSystem is its own namespace, block_id name calls, addressing, depth
#     by :, chaining with other RuntimeSystems with / so:
# 
#     edu.mit.eng.eecs.6002x.industry.spring2013/some:block:name?
# 
# 
#     edu.mit.eng.eecs.6002x.industry.spring2013/Lecture_1/HW1:P2
# 
# 
#     XBlock __init__s are really, really cheap.
# 
#     XBlocks cannot serialize their own relationships.
#     """
#     ############ RuntimeSystem standard methods we're implementing #############
# 
#     def register(self, xml):
#         self._unparsed_nodes[self._create_block_id()] = 
# 
# 
#     ############ Our own helper methods #############
# 
#     def _create_block_id(self):
#         return BlockID(next(self._ids), next(self._ids))
# 
# 
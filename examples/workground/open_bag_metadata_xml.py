from h5py import File
from lxml import etree, __version__ as lxml_version

bag_path = r"C:\code\cpp\BAG\examples\sample-data\sample-1.5.0.bag"

strip_x00 = True

print("lxml version: %s" % lxml_version)
print("libxml version: %s" % (etree.LIBXML_COMPILED_VERSION, ))

bag = File(bag_path, 'r')
xml = bag["BAG_root/metadata"][:].tobytes()
if strip_x00:
    xml = xml.strip(b'\x00')
xml_tree = etree.fromstring(xml)

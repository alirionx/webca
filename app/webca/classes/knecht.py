
from cadb import cadb
from cadb import cert_tool

# myCaDb = cadb('/home/ubuntu/cadb')
# # chkRes = myCaDb.check_cadb()
# # if not chkRes:
# #   myCaDb.create_cadb()



myCertTool = cert_tool('root')
#myCertTool.set_crypto_para("keylen", 4096)

myCertTool.generate_rsa_pkey()
myCertTool.set_cert_attrib("country", "DE")
myCertTool.set_cert_attrib("city", "Stuttgart")
myCertTool.set_cert_attrib("state", "Baden Württemberg")
myCertTool.set_cert_attrib("organization", "AppScape")
myCertTool.set_cert_attrib("orgunit", "LAB")
myCertTool.set_cert_attrib("commonname", "app-scape.lab")
myCertTool.print_cert_data()   
myCertTool.generate_root_cert()
 
#myCertTool.print_cert_dump()

certDump = myCertTool.get_cert_dump()
if certDump:
  caKey = certDump["key"]
  caCert = certDump["cert"]
else:
  exit()

print(caKey, caCert)

#-CREATE EXAMPLE---
myCaDb = cadb('/home/ubuntu/cadb')
myCaDb.set_cadata("name", "my first ca")
myCaDb.set_cadata("contact", "ichus")
myCaDb.set_cadata("comment", "es kann nur besser werden")
if myCaDb.create_ca():
  myCaDb.insert_root_cert(caKey, caCert)


#ALS NÄCHSTES LOAD CA FROM DB EXAMPLE---



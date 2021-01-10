
#-Import required Modules--------------------------------
import os
import sys
from datetime import datetime
from colorama import Fore, Back, Style
import json
import sqlite3
from OpenSSL import crypto

#-Global Vars--------------------------------------------
CurPath = os.path.dirname(os.path.realpath(__file__))
dbFileName = "authorities.db"
dbMainTbl = "authorities"
dbCreateName = "cadb_statements.sql"


#-The Cert Tool Class------------------------------------------------
class cert_tool:

  #-Initial definitions---------------------------
  certParas = {
    "type": crypto.TYPE_RSA,
    "keylen": 2048
  }
  certDefi = {
    "country": {      # Alias: C
      "type": str,
      "manda": True
    },
    "state": {        # Alias: ST
      "type": str,
      "manda": True
    },
    "city": {         # Alias: L
      "type": str,
      "manda": True
    },
    "organization": { # Alias: O
      "type": str,
      "manda": True
    },
    "orgunit": {      # Alias: OU
      "type": str,
      "manda": False
    },
    "commonname": {   # Alias: CN
      "type": str,
      "manda": True
    },
    "email": {        # Alias: emailAddress
      "type": str,
      "manda": False
    }
  }
  certData = {
  }
  certDump = {
    "key": None,
    "cert": None
  }

  #-------------------------
  def __init__(self, certType ):
    self.certData["type"] = certType 
    print(Fore.GREEN + "- new "+certType+" certificate object created" + Style.RESET_ALL)


  #-The Methods-----------------------------------
  def set_crypto_para(self, key, val):
    if key in self.certParas:
      self.certParas[key] = val
    else:
      print(Fore.RED + "  : set_crypto_para: invalid parameter: "+key + Style.RESET_ALL)
      return False

  #------------------------------
  def print_cert_data(self ):
    jsonOut = json.dumps(self.certData, indent=2)
    print(jsonOut)

  def print_cert_dump(self ):
    #jsonOut = json.dumps(self.certDump, indent=2)
    #print(jsonOut)
    print(self.certDump["key"])
    print(self.certDump["cert"])

  def get_cert_dump(self ):
    if type(self.certDump["key"]) == str and type(self.certDump["cert"]) == str:
      return self.certDump
    else:
      print(Fore.RED + "  : get_cert_dump: key and/or certificate not available"+ Style.RESET_ALL)
      return False
    
 
  #------------------------------
  def set_cert_attrib(self, key, val):
    chk = False
    if key in self.certDefi: 
      if type(val) == self.certDefi[key]["type"]:
        self.certData[key] = val
        chk = True
    
    if not chk:
      print("  : set_cert_attrib: "+Fore.RED+" invalid attribute: "+key + Style.RESET_ALL)
    
    return chk

  #------------------------------
  def generate_rsa_pkey(self ):

    pKeyObj = crypto.PKey()
    pKeyObj.generate_key(self.certParas["type"], self.certParas["keylen"])
    pKeyBytStr = crypto.dump_privatekey(crypto.FILETYPE_PEM, pKeyObj)
    pKeyStr = str(pKeyBytStr, "utf-8")
    
    self.certDump["key"] = pKeyStr
    return pKeyStr


  def generate_root_cert(self ):
    for key, defi in self.certDefi.items():
      if defi["manda"] and key not in self.certData:
        print("  : generate_root_cert: "+Fore.RED+" please set attribute: "+key+" first" + Style.RESET_ALL)
        return False
      elif not defi["manda"] and key not in self.certData: #SCHROTT!!!
        self.certData[key] = " "

    if not str(self.certDump["key"]).startswith("-----BEGIN PRIVATE KEY-----"):
      print("  : generate_root_cert: "+Fore.RED+" please create private key first" + Style.RESET_ALL)
      return False
    else:
      pKeyStr = self.certDump["key"]

    pKey = crypto.load_privatekey(crypto.FILETYPE_PEM, pKeyStr)
    certObj = crypto.X509()
    certObj.get_subject().C = self.certData["country"]
    certObj.get_subject().ST = self.certData["state"]
    certObj.get_subject().L = self.certData["city"]
    certObj.get_subject().O = self.certData["organization"]
    certObj.get_subject().OU = self.certData["orgunit"]
    certObj.get_subject().CN = self.certData["commonname"]
    certObj.get_subject().emailAddress = self.certData["email"]
    certObj.set_serial_number(1000)
    certObj.gmtime_adj_notBefore(0)
    certObj.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years expiry date
    certObj.set_issuer(certObj.get_subject())  # self-sign this certificate

    certObj.set_pubkey(pKey)
    certObj.sign(pKey, 'sha256')

    certBytStr = crypto.dump_certificate(crypto.FILETYPE_PEM, certObj)
    certStr = str(certBytStr, "utf-8")
    
    self.certDump["cert"] = certStr
    return certStr



#-The CA Database Class----------------------------------------------
class cadb:
  
  #-Initial definitions---------------------------
  caId = None
  caDefi = {
    "name": {
      "type": str,
      "manda": True
    },
    "contact": {
      "type": str,
      "manda": False
    },
    "comment": {
      "type": str,
      "manda": False
    }
  }
  caData = {}

  def __init__(self, path ):
    self.wrkPath = path
    self.dbFilePath = os.path.join(path, dbFileName)
    if not self.check_cadb():
      self.create_cadb()
    
    print(Fore.GREEN + "- new authorities object created" + Style.RESET_ALL)
    
  #-Helpers and tools------------------------
  def dict_factory(sel, cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d

  #----------------------------
  def create_sql_cursor(self ):
    sqlCon = sqlite3.connect(self.dbFilePath, isolation_level=None)
    sqlCon.row_factory = self.dict_factory
    sqlCurs = sqlCon.cursor()
    return sqlCurs

  #----------------------------
  def check_cadb(self ):
    if not os.path.isdir(self.wrkPath):
      os.mkdir(self.wrkPath)
    
    try:
      sqlCon = sqlite3.connect(self.dbFilePath)
      sqlCon.row_factory = self.dict_factory
      sqlCurs = sqlCon.cursor()
      sqlRes = sqlCurs.execute('PRAGMA table_info(%s);' %dbMainTbl)
    except:
      return False
    
    colChk = ["id", "name",	"created", "contact", "comment" ]
    colAry = []
    for row in sqlRes:
      colAry.append(row['name'])
    #print(colAry)
    for col in colChk:
      if col not in colAry:
        return False

    return True

  #----------------------------
  def create_cadb(self, chk=False ):
    if chk:
      chkRes = self.check_cadb()
      if chkRes: 
        print('  : create_cadb: ' + Fore.YELLOW + 'Authority database already exists' + Style.RESET_ALL)
        return True
    
    flPath = os.path.join(CurPath, dbCreateName)
    flObj = open(flPath, "r")
    flStr = flObj.read()
    qryAry = flStr.split(";")

    sqlCurs = self.create_sql_cursor()
    for qry in qryAry:
      sqlCurs.execute(qry + ";")
  

  #-The Methods-----------------------------------
  def set_cadata_timestamp(self ):
    now = datetime.now()
    timeStampStr = now.strftime("%Y-%m-%d %H:%M:%S")
    self.caData["created"] = timeStampStr

  #-------------------------------
  def set_cadata(self, key, val):
    if key in self.caDefi and type(val) == str and len(val) > 0:
      self.caData[key] = val
    else:
      print("  : set_cadata: "+Fore.YELLOW+" unable to set parameter: "+key + Style.RESET_ALL)
      return False

  #-------------------------------
  def create_ca(self ):
    for key, defi in self.caDefi.items():
      if defi["manda"] and key not in self.caData:
        print("  : create_ca: "+Fore.RED+" please set parameter: "+key+" first" + Style.RESET_ALL)
        return False

    self.set_cadata_timestamp()

    colAry = []
    valAry = []

    for key, val in self.caData.items():
      colAry.append(key)
      valAry.append(val)
    
    colStr = ", ".join(colAry)
    valStr = "'"+"', '".join(valAry)+"'"

    sqlCurs = self.create_sql_cursor()
    try:
      sqlCurs.execute('INSERT INTO '+dbMainTbl+' ('+colStr+') VALUES('+valStr+');')
      #print('INSERT INTO '+dbMainTbl+' ('+colStr+') VALUES('+valStr+');')
    except Exception as e:
      print('Error: '+ str(e))
      return False
      
    self.caId = sqlCurs.lastrowid
    #print(self.caId)
    return True

  #-------------------------------
  def insert_root_cert(self, pKey, rCert ):
    #print(self.caId)
    if type(self.caId) != int:
      print("  : insert_root_cert: "+Fore.RED+" no ca loaded" + Style.RESET_ALL)
      return False   
    else:
      caIdStr = str(self.caId)

    try:
      crypto.load_privatekey(crypto.FILETYPE_PEM, pKey)
      crypto.load_certificate(crypto.FILETYPE_PEM, rCert)
    except Exception as e:
      print('Error: '+ str(e))
      return False
    
    sqlCurs = self.create_sql_cursor()
    try:
      sqlCurs.execute("UPDATE "+dbMainTbl+" SET key = '"+pKey+"', cert = '"+rCert+"' WHERE id = "+caIdStr+" ;")
    except Exception as e:
      print('Error: '+ str(e))
      return False
    
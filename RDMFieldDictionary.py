class RDMFieldDictionary:
    _dict = {}
    _enum = {}
    def __init__(self, rdmFieldDictFile, enumtypeFile):
        self.rdmFieldDictFile = rdmFieldDictFile
        self.enumtypeFile = enumtypeFile
        self._loadRDMFieldDictionary()
        self._loadEnumType()

    def GetExpanedEnumString(self, name, enumid):
        if name in self._dict.keys():
            if(self._dict[name]["enum"]==None):
                return None
            
            if enumid in self._enum[self._dict[name]["enum"]].keys():
                return self._enum[self._dict[name]["enum"]][enumid]["str"]
            else:
                return None
        else:
            return None

    def GetFieldByName(self, name):
        if name in self._dict.keys():
            return self._dict[name]
        else:
            return None

    def _loadEnumType(self):
        fieldList = []
        enumList={}
        file1 = open(self.enumtypeFile, 'r') 
        while True: 
            line = file1.readline() 
            if not line: 
                break
    
            if line.startswith("!"):
                continue

            if line.startswith(" ") == False:
                if enumList != {}:
                    self._enum[fieldList[0]] = enumList
                    enumList = {}
                    for name in fieldList:
                        self._dict[name]["enum"] = fieldList[0]
                    fieldList = []

                fieldList.append(line.split()[0])
            else:
                enum_id = line.lstrip().split()[0]
                if(line.lstrip().split()[1].startswith("#")):
                    first_hash = line.find("#")
                    second_hash = line.find("#",first_hash+1)+1
                    enum_expand = line[first_hash:second_hash]
                    enum_description = line[second_hash:].lstrip()
                    #print("'",enum_expand,"'", enum_description)
                else:
                    first_doublequote = line.find("\"")
                    second_doublequote = line.find("\"",first_doublequote+1)
                    enum_expand = line[first_doublequote+1:second_doublequote].strip()
                    enum_description = line[second_doublequote+1:].lstrip()
                    #print("'",enum_expand,"'", enum_description)

                enumList[int(enum_id)] = {"enum": enum_id,
                                     "str": enum_expand,
                                     "description": enum_description}
                
                #first_dquote = line.find("\"")

                #print(enumid)
                #start_offset = len(field_name)
                #first_dquote = line.find("\"")
    
                #field_description = line[start_offset:].lstrip().split("\"")[1]  
                #start_offset = line.find("\"",line.find("\"")+1)+1
                #sub_line = line[start_offset:]

                #sub_str = sub_line.lstrip().split()

        file1.close()

    def _loadRDMFieldDictionary(self):
        file1 = open(self.rdmFieldDictFile, 'r') 

        while True: 
            line = file1.readline() 
            if not line: 
                break
    
            if line.startswith("!"):
                continue
    
            field_name = line.split()[0]
            start_offset = len(field_name)
            first_dquote = line.find("\"")
    
            field_description = line[start_offset:].lstrip().split("\"")[1]  
            start_offset = line.find("\"",line.find("\"")+1)+1
            sub_line = line[start_offset:]

            sub_str = sub_line.lstrip().split()
            field_id = sub_str[0]
            ripple_to = sub_str[1]
            field_type = sub_str[2]
            if field_type == "ENUMERATED":
                field_length = sub_str[3]+":"+sub_str[5]
                rwf_type = sub_str[7]
                rwf_length = sub_str[8]
            else:
                field_length = sub_str[3]
                rwf_type = sub_str[4]
                rwf_length = sub_str[5]
    
            self._dict[field_name] = {"name":field_name,
                                      "decscription": field_description,
                                      "id": field_id,
                                      "ripple": ripple_to,
                                      "type": field_type,
                                      "length": field_length,
                                      "rwftype": rwf_type,
                                      "rwflength": rwf_length,
                                      "enum": None
                                      }
        file1.close() 
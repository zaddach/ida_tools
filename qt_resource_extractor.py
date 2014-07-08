MANGLED_qRegisterResourceData_FUNCTION_NAMES = ["__Z21qRegisterResourceDataiPKhS0_S0_"]

class QResourceRoot():
    def __init__(self, tree_ptr, names_ptr, data_ptr):
        self._tree_ptr = tree_ptr
        self._data_ptr = data_ptr
        self._names_ptr = names_ptr
        
    def findOffset(self, node):
        return node * 14
        
    def children(self, node):
        ret = []
        if node != -1 and self.isDirectory(node): #Directory
            offset = self.findOffset(node) + 4 + 2
            child_count = struct.unpack(">L", self.tree(offset, 4))[0]
            child_off = struct.unpack(">L", self.tree(offset + 4, 4))[0]
            
            for i in range(child_off, child_off + child_count):
                ret.append(i)
        return ret
        
    def getAllLeafs(self):
        todo_nodes = [(i, "/" + self.name(i)) for i in self.children(0)]
        all_nodes = []
        while todo_nodes:
            cur_node = todo_nodes.pop()
            if not self.isDirectory(cur_node[0]):
                all_nodes.append(cur_node)
            todo_nodes += [(i, cur_node[1] + "/" + self.name(i)) for i in self.children(cur_node[0])]
        return all_nodes
            
            
    def name(self, node):
        offset = self.findOffset(node)
        
        name_offset = struct.unpack(">L", self.tree(offset, 4))[0]
        name_length = struct.unpack(">H", self.names(name_offset, 2))[0]
        
        name_offset += 2
        name_offset += 4 #Jump past hash
        
        return self.names(name_offset, name_length * 2).decode("utf_16_be")
        
    def flags(self, node):
        if node == -1:
            return 0
        offset = self.findOffset(node) + 4 #jump past name
        return struct.unpack(">H", self.tree(offset, 2))[0]
        
    def isDirectory(self, node):
        return self.flags(node) & 0x2 != 0
        
    def isCompressed(self, node):
        return self.flags(node) & 0x1 != 0
        
    def data(self, node):
        if node == -1:
            return ""
            
        if not self.isDirectory(node): #Not directory
            offset = self.findOffset(node) + 4 #jump past name
            offset += 2 
            offset += 4 #jump past locale
            data_offset = struct.unpack(">L", self.tree(offset, 4))[0]
            data_length = struct.unpack(">L", self.payloads(data_offset, 4))[0]
            return self.payloads(data_offset + 4, data_length)
        return ""
        
    def tree(self, start, length):
        return "".join(map(lambda x: chr(Byte(x)), range(self._tree_ptr + start, self._tree_ptr + start + length)))
        
    def names(self, start, length):
        return "".join(map(lambda x: chr(Byte(x)), range(self._names_ptr + start, self._names_ptr + start + length)))
        
    def payloads(self, start, length):
        return "".join(map(lambda x: chr(Byte(x)), range(self._data_ptr + start, self._data_ptr + start + length)))
        
def get_resource_root():
    print("WARNING: Finding caller arguments of qRegisterResourceData not implemented, using fixed ones only suitable for LIFX update")
    return QResourceRoot(0x10001D3C0, 0x10001D450, 0x10001D590)
    for func in Functions():
        if GetFunctionName(func) in MANGLED_qRegisterResourceData_FUNCTION_NAMES:
            for caller in CodeRefsTo(func, 0):
                if "si" in GetRegisterList() and "r15" in GetRegisterList(): #Binary is x86_64
                    pass
                    #TODO: Go back from here and find function arguments
                    #rsi contains tree_ptr
                    #rdx contains names_ptr
                    #rcx contains data_ptr
                    #edi is version (must be 1)
                else:
                    assert(False) #Not implemented for this processor
                
def dump_all_resources(path):
    q_resource_tree = get_resource_root()
    for leaf in q_resource_tree.getAllLeafs():
        file_path = os.path.join(path, leaf[1][1:])
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, 'wb') as file:
            file.write(q_resource_tree.data(leaf[0]))

    
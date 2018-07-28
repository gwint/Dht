include "shared.thrift"
typedef string UserID

exception SystemException {
  1: optional string message
}

struct NodeData {
  1: list<RFile> data;
}

struct RFileMetadata {
  1: optional string filename;
  2: optional i32 version;
  3: optional UserID owner;
  4: optional string contentHash;
}

struct RFile {
  1: optional RFileMetadata meta;
  2: optional string content;
}

struct NodeID {
  1: string id;
  2: string ip;
  3: i32 port;
}

service FileStore extends shared.SharedService {
  void addNode(1: string host, 2: i32 port)
    throws (1: SystemException systemException),

  void writeFile(1: RFile rFile)
    throws (1: SystemException systemException),
  
  RFile readFile(1: string filename, 2: UserID owner)
    throws (1: SystemException systemException),

  void setFingertable(1: list<NodeID> node_list),
  
  NodeID findSucc(1: string key) 
    throws (1: SystemException systemException),

  NodeID findPred(1: string key) 
    throws (1: SystemException systemException),

  NodeID getNodeSucc() 
    throws (1: SystemException systemException),

  NodeData getFiles()
    throws (1: SystemException systemException),

  void addFile(1: RFile file)
    throws (1: SystemException systemException),

  void removeFile(1: string hash)
    throws (1: SystemException systemException)

}

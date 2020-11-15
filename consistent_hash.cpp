#include<iostream>
#include<limits.h>
#include<algorithm>
#include<functional>
#include<string>
#include<sstream>
#include<utility>
#include<array>
#include<vector>
using namespace std;

struct server {
  string id;
  int pos_id;
};

string getString(int i)
{
  stringstream ss;
  ss<<i;
  return ss.str();
}

class LoadBalancer{
  // data members
  private:
    // hash function
    hash <string> h;
    // number of servers
    int num_servers;
    // array of worker nodes
    array < pair<server*,bool>,360> hashRing;
    // number of replicas
    int num_rep;
    // member functions
    private:
      void initialiseHashRing();
      void initialiseReplica(string,int);
      string findNearestServer(int);
    public:
      LoadBalancer(int,int);
      string assignServer(string);
      void serverStatus();
      string generateRandomRequest();
      void changeServer(int,int);
};

LoadBalancer :: LoadBalancer(int num_servers,int num_rep)
{
  this->num_servers = num_servers;
  this->num_rep = num_rep;
  initialiseHashRing();
  cout<<"..........................................................\n";
  cout<<"load balancer initialised and displaying server status\n";
  serverStatus();
}

void LoadBalancer :: initialiseHashRing()
{
  // hashring forms cicle
  for(int i=0;i<360;i++)
  {
    hashRing[i].first = NULL;
    hashRing[i].second = false;
  }
  for(int i=0;i<this->num_servers;i++)
  {
    server *node = new server;
    node->id = getString(i);
    node->pos_id = h(node->id)%360;
    this->hashRing[node->pos_id].first = node;
    hashRing[node->pos_id].second = false;  
    initialiseReplica(node->id,node->pos_id);
  }
}

void LoadBalancer :: initialiseReplica(string id,int pos)
{
  int temp_pos=pos;
  int dist = 360/num_servers;
  for (int i=0;i<num_rep;i++)
  { 
    temp_pos=temp_pos+dist;
    if(!hashRing[temp_pos].first)
    {
      server *repl = new server;
      repl->id = id;
      repl->pos_id = temp_pos;
      hashRing[temp_pos].first = repl;
      hashRing[temp_pos].second = true; 
    }
  }
}

void LoadBalancer :: serverStatus()
{
  cout<<"total number of servers "<<num_servers<<"\n";
  cout<<"..............................................\n";
  for(int i=0;i<360;i++)
  {
    if (hashRing[i].first)
    {
      cout<<"replicated server : "<<hashRing[i].second<<" server number "<<this->hashRing[i].first->id<<" mapped to "<<this->hashRing[i].first->pos_id<<" in hash ring\n";
    }
  }
  cout<<"...............................................\n";
}

string LoadBalancer :: generateRandomRequest()
{
  unsigned r = rand();
  return getString(r);
}

string LoadBalancer :: assignServer(string req_id)
{
  int pos = h(req_id)%360;
  return findNearestServer(pos);
} 

string LoadBalancer :: findNearestServer(int pos)
{
  bool f=false;
  for(int i=0;i<360;i++)
    if(hashRing[i].first)
      f=true;
  if(f==false)
  {
    cout<<"no server nodes exists\n";
    exit(0);
  }
  while(true)
  {
    // if the position hashed has server and posid of server equals postion
    if(hashRing[pos].first && pos==hashRing[pos].first->pos_id)
      return hashRing[pos].first->id;
    // if pos has server
    else if(hashRing[pos].first)
      return hashRing[pos].first->id;
    // search server in next location
    pos++;
    // boundary condn for circular search
    if(pos==360)
      pos=0;
  }    
}

void LoadBalancer :: changeServer(int n,int c)
{
    if(c==1)
    {
      this->num_servers = this->num_servers + n;
      initialiseHashRing();
      serverStatus();
    }
    else
    {
      if(n > num_servers)
      {
        cout<<"error : number of servers to be removed greater than existing server\n";
        exit(0);
      }
      num_servers = num_servers - n;
      initialiseHashRing();
      serverStatus();
    }
    
}
int main()
{
  int num_req;
  LoadBalancer lb(10,3);
  vector < pair<string,string> > mapper;
  cout<<"enter the avg. number of requests to be processed\n";
  cin>>num_req;
  cout<<".................................................\n";
  cout<<"Generating random requests and displaying the server mapped to requests\n";
  cout<<".................................................\n";
  for(int i=0;i<num_req;i++)
  {
    string req_id = lb.generateRandomRequest();
    //cout<<"request id : "<<req_id<<"\n";
    string node_id = lb.assignServer(req_id);
    pair <string,string> p;
    p.first = req_id;
    p.second = node_id;
    mapper.push_back(p);
    cout<<"request id "<<req_id<<" mapped to server id "<<node_id<<"\n";
  }
  int val;
  cout<<".................................................\n";
  cout<<"change number of servers\n1 - add server\n2 - remove server\n3 - no change\n";
  cout<<".................................................\n";
  cin>>val;
  switch (val)
  {
  case 1: cout<<"enter no of servers to be added\n";
          int n1;
          cin>>n1;
          lb.changeServer(n1,1);
          break;
  case 2: cout<<"enter no of servers to be removed\n";
          int n2;
          cin>>n2;
          lb.changeServer(n2,2);
          break;
  case 3:
          break;
  }
  if(val==1 || val==2)
  {
    cout<<"reallocating requests\n";
    cout<<".................................................\n";
    for(int i=0;i<mapper.size();i++)
    {
      string req_id = mapper[i].first;
      string node_id = lb.assignServer(req_id);
      mapper[i].second = node_id;
      cout<<"request id "<<req_id<<" reallocated to server id "<<node_id<<"\n";      
    }    
  }
  return 0;  
}

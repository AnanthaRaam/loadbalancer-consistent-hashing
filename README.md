# loadbalancer-consistent-hashing
## Introduction
When we are dealing with distributed system ( having multiple instances of databases also called nodes ) it is very important to distribute the incoming requests evenly among availabe nodes.If not all requests will be processed by any particular node which creates problem of **network hotspots**.So to avoid hotspots loadbalancer is used to balance the load among nodes.The very basic idea of loadbalancer is hashing which has certain limitations when the nature of distributed system is dynamic.Consistent hashing is a upgraded method of normal hashing technique that solves the problem.


## Problems with  mod n hashing :
**n** represents number of nodes

Generally requests will be hashed based on unique value like userid to generate key and map to the server based on that key.Once a request is mapped to a node all the data related
to the user is cached on that particular node.Since because userid of a request will not change frequently and data is cached retrieval will be faster.

### Horizontal Scaling : 
But if we try to add or remove nodes from existing pool of nodes then amount of requests reallocated is high because of change in **n** and it affects the cached data already presents.

### Distribution of Requests :
Moreover the requests that get distributed using **mod n** are not uniform enough so it creates problem of **hotspots**.

So to overcome these limitations consistent hashing is introduced.

## Consistent Hashing

# loadbalancer-consistent-hashing

## Problems with  modn hashing :
### Horizontal Scaling : 
If we try to add or remove servers from existing pool of servers then amount of requests reallocated is high and it affects the cached data already presents.
### Distribution of Requests :
Generally the requests that get distributed are not uniform enough so it creates problem of <b>hotspots</b>

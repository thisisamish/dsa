# BFS/Level Order Traversal of Graph

Problem Statement: We are given a 0-index based connected graph (could have zero nodes) in the form of an adjacency list/adjacency matrix. Find the bfs/level order traversal of this graph.

Code available in: C++

Difficulty: Easy

Tags: Graph, BFS, Level Order Traversal

Pre-requisites: Adjacency List, Adjacency Matrix

## Approach

1. Process nodes level by level using a queue.
2. For each level, loop through the current queue size, collect the nodes, and enqueue unvisited neighbors.

> There would be slight differences in how we handle `0-index` based graphs vs `1-index` based graphs as well as adjacency list graphs vs adjacency matrix graphs. Code for `0-index` based adjacency list and adjacency matrix graphs are given below. We are assuming we have `n` nodes numbered from `0` to `n - 1`.

> For disconnected graphs, we have to run bfs on every node. That is a very specific case and is not relevant here.

## Code

## C++

### When Adjacency List is given

Time Complexity: $O(V + E)$

Space Complexity: $O(V)$

```cpp
class Solution {
public:
    vector<vector<int>> bfs(vector<vector<int>>& adjList) {
        int n = adjList.size();
        vector<vector<int>> levels;

        if (n == 0) {
            return levels;
        }
        
        vector<bool> visited(n, false);

        queue<int> q;
        q.push(0);
        visited[0] = true;

        while (!q.empty()) {
            int size = q.size();
            vector<int> level;

            for (int i = 0; i < size; i++) {
                int node = q.front();
                q.pop();
                level.push_back(node);
                
                for (int nei : adjList[node]) {
                    if (!visited[nei]) {
                        q.push(nei);
                        visited[nei] = true;
                    }
                }
            }
            levels.push_back(level);
        }
        return levels;
    }
};
```

### When Adjacency Matrix is given

Time Complexity: $O(V^2)$

Space Complexity: $O(V)$

```cpp
class Solution {
public:
    vector<vector<int>> bfs(vector<vector<int>>& adjMat) {
        int n = adjMat.size();
        vector<vector<int>> levels;

        if (n == 0) {
            return levels;
        }
        
        vector<bool> visited(n, false);

        queue<int> q;
        q.push(0);
        visited[0] = true;

        while (!q.empty()) {
            int size = q.size();
            vector<int> level;

            for (int i = 0; i < size; i++) {
                int node = q.front();
                q.pop();
                level.push_back(node);

                for (int j = 0; j < n; j++) {
                    if (adjMat[node][j] == 1 && !visited[j]) {
                        q.push(j);
                        visited[j] = true;
                    }
                }
            }
            levels.push_back(level);
        }
        return levels;
    }
};
```

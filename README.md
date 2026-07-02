# Smart Ambulance Routing System

## Overview

This project implements a Smart Ambulance Routing System using Artificial Intelligence search algorithms to determine the optimal route for emergency vehicles within a city map.

The city is modeled as a graph where intersections are represented as nodes and roads are represented as edges with attributes such as distance, traffic conditions, and road availability. Users can select a starting location and a destination, and the system calculates the best route using different search strategies.

## Features

- Interactive graphical user interface (GUI)
- Dynamic selection of ambulance and destination locations
- Graph-based city representation
- Route visualization on the city map
- Comparison of multiple AI search algorithms
- Route cost and distance calculation

## Algorithms Implemented

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)
- Greedy Best-First Search
- A* Search

## Heuristic Function

The A* and Greedy Search algorithms use Euclidean Distance as a heuristic function to estimate the remaining distance to the destination and improve search efficiency.

## Technologies Used

- Python
- PyQt5
- NetworkX
- Matplotlib

## Project Workflow

1. Create a graph-based city map.
2. Select the ambulance starting point.
3. Select the destination location.
4. Choose a search algorithm.
5. Compute the optimal route.
6. Display the resulting path and route statistics.

## Results

The system allows users to compare the behavior and performance of different search algorithms in emergency routing scenarios by analyzing:

- Selected path
- Total travel distance
- Route cost
- Search efficiency

## Objective

The main objective of this project is to demonstrate how Artificial Intelligence search techniques can support emergency response systems by identifying efficient routes under different road and traffic conditions.

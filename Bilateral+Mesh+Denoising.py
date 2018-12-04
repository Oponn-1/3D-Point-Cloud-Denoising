'''
    Bilateral Mesh Denoising Implementation
    
    This is an implementation of the algorithm presented in 
    'Bilateral Mesh Denoising' by Fleishman et. all. 
    
    Author: Andres De La Fuente
    
    No existing code was found for the algorithm, so this implementation is from scratch,
    and thus has some inefficiencies that could be improved:
    
        - The search for points within the neighborhood
            - Currently the time complexity of this is O(n) which makes the 
                whole algorithm an O(n^2).
            - This inefficiency stems from searching every point.
            - Implementing some kind of bounding box tree
                could reduce this to O(n*log(n)). 
                
        - NOTE: The above issue is currently addressed in the code by only searching 
            through the points from the neighboring triangles used to calculate the
            normal. This reduces the search to O(c), a constant time complexity,
            at the cost of potentially not being a complete search.
            The assumption is that no points that are outside of this geometric
            neighborhood will be closer to the vertex than those that are inside
            the neighborhood.
            
        - Subsampling methodology
            - Currently, the inefficiency of the Delaunay triangulation is worked around
                by subsampling the points (every 10th point in this case)
            - The method of subsampling could be replaced with a more sophisticated one
                that might reduce the chance of losing important information
            - The large amount of data from our specific input files mitigates this risk, however
                
    This code uses the scipy Delaunay triangulation 
    implementation to turn an input list of points into a mesh, which is 
    required for the operations of this algorithm.
    
''' 
from scipy.spatial import Delaunay
import numpy as np
import math

f = open('1.xyz','r')

p = []

# Number of passes through the mesh
iterations = 1

# Create array with points read from file
for l in f:
    row = l.split()
    p.append([row[0], row[1], row[2]])
    # in case there are two 'columns' of points in the input 
    # which is the case with our .xyz files
    if (len(row) == 6):
        p.append([row[3], row[4], row[5]])

points = np.array(p)

# Subsampling must be done because Delaunay triangulation is very slow otherwise
points = points[::20]

print("Points Loaded")



# Generate triangulation of the points, QJ ensures all points are used
tri = Delaunay(points[:-1], qhull_options="Qbb Qc Qz Q12 QJ Qt")

print("Triangulation Complete")



''' 
Function: neighborhood_radius
Use: calculate a neighborhood radius (this is what sigma_c is set to)
Parameters...
v: vertex from which min distance will be calculated
'''
def neighborhood_radius(v):
    # determine neighboring triangles to the vertex
    triangle = tri.find_simplex(v)
    neighbors = tri.neighbors[triangle]
    # set upper bound
    maximum = 1e10
    # find smallest gap between neighboring points
    for n in neighbors:
        if (n != -1):
            for p in tri.simplices[n]:
                dist = np.linalg.norm(v-p)
                if ((dist > 0) and (dist < maximum)):
                    maximum = dist
    return maximum

''' 
Function: calc_normal
Use: calculate the normal at a vertex from its neighbor triangles
Parameters...
v: vertex for which normal will be calculated
degree: how many times to add an extra set of neighbors
'''
def calc_normal(v, degree):
    # determine neighboring triangles to the vertex
    triangle = tri.find_simplex(v)
    neighbors = tri.neighbors[triangle]
    
    # add the next degree of neighbors for more robustness
    for d in range(degree):
        extra = []
        for n in neighbors:
            if (n != -1):
                extra.append(tri.neighbors[triangle])
        neighbors = np.append(neighbors, np.unique(extra))
                               
    # prepare to average their normals
    normal_sum = [0, 0, 0]
    count = 0
    # calculate each normal
    for n in neighbors:
        if (n != -1):
            s = tri.simplices[n]
            v1 = points[s[0]] - points[s[1]]
            v2 = points[s[0]] - points[s[2]]
            crossp = np.cross(v1, v2)
            normal_sum[0] += crossp[0]
            normal_sum[1] += crossp[1]
            normal_sum[2] += crossp[2]
            count += 1
    # average and normalize the normal
    normal_average = [n / count for n in normal_sum]
    normal = np.linalg.norm(normal_average)
    normal_normalized = [n / normal for n in normal_average]
    
    # list the points within this neighborhood for faster searching
    neighbor_points = []
    for n in neighbors:
        if (n != -1):
            for s in tri.simplices[n]:
                neighbor_points.append(s)
    neighbor_points = np.unique(neighbor_points)
    
    return normal_normalized, neighbor_points

'''
Below is the implementation of the algorithm itself
'''
iterations = 2
points = points.astype(np.float)
# Vertex modification passes
for i in range(iterations):
    new_points = []
    index = 0
    # algorithm parameters, set for each vertex below
    sigma_c = 0 
    sigma_s = 0
    for p in points:
        # calculate normal
        normal, neighbor_points = calc_normal(p, 2)
        # calculate sigma_c...................
        sigma_c = neighborhood_radius(p)
        # get neighbor points
        neighbors = []
        for y in neighbor_points:
            v = points[y]
            dist = np.linalg.norm(p-v)
            if (dist < 2*sigma_c):
                neighbors.append(v)
        # calculate sigma_s....................
        average_offset = 0
        offsets = []
        # calculate average offset
        for n in neighbors:
            t = np.linalg.norm([x * np.dot((n - p), normal) for x in normal]);
            t = math.sqrt(t*t);
            average_offset += t;
            offsets.append(t);
        average_offset /= len(neighbors)
        # calculate standard deviation
        o_sum = 0
        for o in offsets:
            o_sum += (o - average_offset) * (o - average_offset)
        o_sum /= len(offsets)
        sigma_s = math.sqrt(o_sum)
        # enforce a bottom bound on sigma_c
        minimum = 1.0e-12
        if (sigma_s < minimum):
            sigma_s = minimum
        # calculate movement..................
        total = 0
        normalizer = 0
        for n in neighbors:
            t = np.linalg.norm(n - p)
            h = np.linalg.norm([x * np.dot((n - p), normal) for x in normal]);
            wc = math.exp((-1*t*t)/(2 * sigma_c *sigma_c));
            ws = math.exp((-1*h*h)/(2 * sigma_s *sigma_s));
            total += wc * ws * h;
            normalizer += wc * ws;
        # add new position
        factor = total/normalizer
        modification = [n * factor for n in normal]
        new_point = p + modification
        new_points.append(new_point)
        index += 1
    # update positions
    points = np.array(new_points)
    points = points.astype(np.float)
    
# write the data in .xyz format to a file
save_file = open("clean.xyz", "w")
save_file.write("")
save_file = open("clean.xyz", "a")
for p in points: 
    save_file.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")

print("Done!")
            
        


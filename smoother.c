#include <gts.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>

///////////////// NON ITERATIVE FEATURE PRESERVING MESH SMOOTHING /////////////////////////
//
//	This is an implementation of the mesh smoothing algorithm described in 
//	the eponymous publication from MIT. The code is elaborates on Thuis Jone's
//	original implementation. 
//


///////////////////////// Global Variables //////////////////////////
//
//	mollified_hash:		This is the hash table where the 'mollified' version of
//				the mesh is stored after the first, non-altering run.
//
//	new_position_hash:	This is the hash table where the altered positions of
//				each point are stored in order to actually shift them 
//				simultaneously
//
//	num_verts:		The number of vertices in the mesh.
//
//	tree:			The tree used for the bounding box search.
//
//	sigma_f:		The first parameter for the distribution function chosen.
//
//	sigma_g:		The second parameter for the distribution function chosen.
//
//	sigma_m:		bull shit
//
//	cutoff:			The maximum distance for neighbor triangles.
//
//	dist_mode:		The distribution function chosen. This determines which
//				function is used to weight the modifications.


static GHashTable *mollified_hash, *new_position_hash;
static gint num_verts;
static GNode *tree;
static gdouble sigma_f, sigma_g, sigma_m, cutoff;
static int dist_mode;


////////////////////////////////////////////////////////////////////
//	
//	Name:	gaussian2
//
//	Use:	Calculates the value of the gaussian distribution
//		at the given x.
//
//	Parameters...
//	x:	The variable passed into the distribution function.
//
//	sigma:	Parameter of the gaussian distribution.
//

gdouble gaussian2(double x, double sigma)
{
	return (exp(- x / (2 * sigma * sigma)));
}

////////////////////////////////////////////////////////////////////
//
//	Name:	exp_dist
//
//	Use:	Calculates the value of the exponential distribution
//		at the given x.
//
//	Parameters...
//	x:	The variable passed into the distribution function.
//
//	sigma:	Parameter of the exponential distribution.

gdouble exp_dist(double x, double sigma)
{
	return (sigma * (exp(-sigma * x)));
}

////////////////////////////////////////////////////////////////////
//
//	Name:	box_by_centroid
//
//	Use:	generates bounding boxes for the triangles of the mesh
//
//	Parameters...
//	item:	each triangle being boxed
//
//	data:	pointer to list that will be used for the bounding
//		box tree

gint 
box_by_centroid(gpointer item, gpointer data)
{
  GtsTriangle *t = item;
  GSList *l = * (GSList **) data;
  GtsVertex *v1, *v2, *v3;
  gdouble centroid[3];
  
  // get this triangle's vertices
  gts_triangle_vertices(t, &v1, &v2, &v3);
  // calculate average for x, y, and z of each vertex
  centroid[0] = (GTS_POINT(v1)->x + 
                 GTS_POINT(v2)->x + 
                 GTS_POINT(v3)->x) / 3.0;
  centroid[1] = (GTS_POINT(v1)->y + 
                 GTS_POINT(v2)->y + 
                 GTS_POINT(v3)->y) / 3.0;
  centroid[2] = (GTS_POINT(v1)->z + 
                 GTS_POINT(v2)->z + 
                 GTS_POINT(v3)->z) / 3.0;
  
  // get pointer for list beginning with new bounding box added
  l = g_slist_prepend(l, gts_bbox_new(gts_bbox_class(),
                                      t,
                                      centroid[0], centroid[1], centroid[2],
                                      centroid[0], centroid[1], centroid[2]));
  // set the argument pointer to this new beginning of the list
  * (GSList **) data = l;

  return (0);
}

////////////////////////////////////////////////////////////////////
//
//	Name:	project_to_tri 
//	
//	Use:	caluclate the projection of a point to a triangle
//
//	Parameters...
//	p:		vertex to project
//
//	centroid:	triangle centroid
//
//	v1, v2, v3:	vertices of the triangle
//
//	x, y , z:	the projection cooridnates

void
project_to_tri(GtsVertex *p,
               gdouble centroid[3],
               GtsVertex *v1, GtsVertex *v2, GtsVertex *v3,
               gdouble *x, gdouble *y, gdouble *z)
{
  GtsVector vcp, v12, v13, normal;
  gdouble dotvcpn;
  
  // calculate distance from point to triangle centroid
  vcp[0] = GTS_POINT(p)->x - centroid[0];
  vcp[1] = GTS_POINT(p)->y - centroid[1];
  vcp[2] = GTS_POINT(p)->z - centroid[2];

  // calculate two vectors on the triangle
  gts_vector_init(v12, GTS_POINT(v1), GTS_POINT(v2));
  gts_vector_init(v13, GTS_POINT(v1), GTS_POINT(v3));
  
  // calculate the normal vector of the triangle
  gts_vector_cross(normal, v12, v13);
  gts_vector_normalize(normal);

  // calculate projection length
  dotvcpn = gts_vector_scalar(vcp, normal);

  // calculate projection coordinates 
  *x = GTS_POINT(p)->x - dotvcpn * normal[0];
  *y = GTS_POINT(p)->y - dotvcpn * normal[1];
  *z = GTS_POINT(p)->z - dotvcpn * normal[2];
}

#define DIST(a,b,c) ((a)*(a)+(b)*(b)+(c)*(c))

////////////////////////////////////////////////////////////////////
//
//	Name:	filter
//	
//	Use:	Calculates the shift to be made for a given point
//
//	Parameters...
//	cur_vert:	vertex to be moved
//
//	weighted_pos:	new position
//
//	k:		sum of weights
//
//	tree:		bounding box tree for triangle search
//
//	spatial_sigma:	parameter for neighborhood cutoff
//
//	influence_sigma: weight for projection distances
void
filter(GtsVertex *cur_vert, GtsVertex *weighted_pos, gdouble *k,
       GNode *tree,
       gdouble spatial_sigma, gdouble influence_sigma, 
       GHashTable *vertex_map)
{
  gdouble dmin, dmax;

  // calculate min and max distances 
  gts_bbox_point_distance2(GTS_BBOX(tree->data), GTS_POINT(cur_vert),
                           &dmin, &dmax);
  if (dmin > (cutoff * cutoff)) return;

  if (G_NODE_IS_LEAF(tree)) {
    // get the bounded triangle and its properties
    GtsTriangle *t = GTS_BBOX(tree->data)->bounded;
    GtsVertex *v1, *v2, *v3;
    gdouble centroid[3];
    gdouble px, py, pz;
    gdouble w = 0.0;
    gdouble area;

    area = gts_triangle_area(t);

    gts_triangle_vertices(t, &v1, &v2, &v3);
    
    // calculate centroid of triangle
    centroid[0] = (GTS_POINT(v1)->x + 
                   GTS_POINT(v2)->x + 
                   GTS_POINT(v3)->x) / 3.0;
    centroid[1] = (GTS_POINT(v1)->y + 
                   GTS_POINT(v2)->y + 
                   GTS_POINT(v3)->y) / 3.0;
    centroid[2] = (GTS_POINT(v1)->z + 
                   GTS_POINT(v2)->z + 
                   GTS_POINT(v3)->z) / 3.0;

    // look up vertices of mollified triangle if mollification has been done
    if (vertex_map) {
      v1 = g_hash_table_lookup(vertex_map, v1);
      v2 = g_hash_table_lookup(vertex_map, v2);
      v3 = g_hash_table_lookup(vertex_map, v3);
    }

    // project to triangle based on original centroid position, but mollified normal 
    project_to_tri(cur_vert,
                   centroid,
                   v1, v2, v3,
                   &px, &py, &pz);

    if (influence_sigma > 0.0) {
	// calculate projection distance 
      	gdouble pdist = DIST(px - GTS_POINT(cur_vert)->x,
                          	 py - GTS_POINT(cur_vert)->y,
                          	 pz - GTS_POINT(cur_vert)->z);
	// gaussian distribution for weights
      	if (dist_mode == 1) {
      		w = area * gaussian2(dmin, spatial_sigma) * gaussian2(pdist, influence_sigma);
  	}
	// exponential distribution for weights
  	if (dist_mode == 2) {
  		w = area * exp_dist(dmin, spatial_sigma) * exp_dist(pdist, influence_sigma);
  	}
    } else {
	// don't calculate projection distance if no weight assigned to it
    	if (dist_mode == 1) {
		w = area * gaussian2(dmin, spatial_sigma);
	}
	if (dist_mode == 2) {
		w = area * exp_dist(dmin, spatial_sigma);
	}
    }

    GTS_POINT(weighted_pos)->x += w * px;
    GTS_POINT(weighted_pos)->y += w * py;
    GTS_POINT(weighted_pos)->z += w * pz;
    *k += w;

  } else {
    // if bounding box does not represent a single triangle, look at each child in the tree
    filter(cur_vert, weighted_pos, k,
           g_node_first_child(tree),
           spatial_sigma, influence_sigma,
           vertex_map);
    filter(cur_vert, weighted_pos, k,
           g_node_nth_child(tree, 1),
           spatial_sigma, influence_sigma,
           vertex_map);
  }
}
       
////////////////////////////////////////////////////////////////////
//
//	Name:	mollify_vertex
//
//	Use:	calculate changes for each vertex to store in 
//		a hash table. No actual modification is done.
//
//	Parameters...
//	item:	vertex to be moved
//
//	data:	

gint
mollify_vertex(gpointer item, gpointer data)
{
  GtsVertex *v = item, *new_pos;
  gdouble k;

  // vertex counter
  static gint vnum = 0;
  gint i;

  // status bar 
  vnum++;
  if (!(vnum % 1000)) {
    fprintf(stderr, "Mollifying:[");
    for(i = 0; i < (65 * vnum) / num_verts; i++) 
      fprintf(stderr, "#");
    for(; i < 65; i++) 
      fprintf(stderr, " ");
    fprintf(stderr, "]\r");
  }
  if (vnum == num_verts) fprintf(stderr, "\n");

  new_pos = gts_vertex_new(gts_vertex_class(),
                           0.0, 0.0, 0.0);
  // sum of weights
  k = 0.0;
  // calculate movements
  filter(v, new_pos, &k, tree, sigma_m, 0.0, NULL);

  // scale by sum of weights if anything influenced this point
  if (k > 0.0) {
    GTS_POINT(new_pos)->x /= k;
    GTS_POINT(new_pos)->y /= k;
    GTS_POINT(new_pos)->z /= k;
  } else {
    GTS_POINT(new_pos)->x = GTS_POINT(v)->x;
    GTS_POINT(new_pos)->y = GTS_POINT(v)->y;
    GTS_POINT(new_pos)->z = GTS_POINT(v)->z;
  }

  // track each change with its original vertex in this hash
  g_hash_table_insert(mollified_hash, v, new_pos);

  return (0);
}

////////////////////////////////////////////////////////////////////
//
//	Name:	filter_vertex
//
//	Use:	caluclates the changed position of each point
//
//	Parameters...
//	item:	vertex to be moved
//
//	data:	

gint
filter_vertex(gpointer item, gpointer data)
{
  GtsVertex *v = item, *new_pos;
  gdouble k;

  // vertex counter
  static gint vnum = 0;
  gint i;

  // status bar 
  vnum++;
  if (!(vnum % 1000)) {
    fprintf(stderr, "Moving:[");
    for(i = 0; i < (65 * vnum) / num_verts; i++) 
      fprintf(stderr, "#");
    for(; i < 65; i++) 
      fprintf(stderr, " ");
    fprintf(stderr, "]\r");
  }
  if (vnum == num_verts) fprintf(stderr, "\n");

  new_pos = gts_vertex_new(gts_vertex_class(),
                           0.0, 0.0, 0.0);
  // sum of weights
  k = 0.0;
  // actually calculate the modification
  filter(v, new_pos, &k, tree, sigma_f, sigma_g, mollified_hash);

  // scale by sum of weights if anything influenced this point
  if (k > 0.0) {
    GTS_POINT(new_pos)->x = GTS_POINT(new_pos)->x / k;
    GTS_POINT(new_pos)->y = GTS_POINT(new_pos)->y / k;
    GTS_POINT(new_pos)->z = GTS_POINT(new_pos)->z / k;
  } else {
    GTS_POINT(new_pos)->x = GTS_POINT(v)->x;
    GTS_POINT(new_pos)->y = GTS_POINT(v)->y;
    GTS_POINT(new_pos)->z = GTS_POINT(v)->z;
  }
  
  // record the new position with its original vertex in the hash table
  g_hash_table_insert(new_position_hash, v, new_pos);

  return (0);
}

gint
move_vertex(gpointer item, gpointer data)
{
  GtsVertex *v = item, *new_pos;

  new_pos = g_hash_table_lookup(new_position_hash, v);

  GTS_POINT(v)->x = GTS_POINT(new_pos)->x;
  GTS_POINT(v)->y = GTS_POINT(new_pos)->y;
  GTS_POINT(v)->z = GTS_POINT(new_pos)->z;

  return (0);
}

int main (int argc, char * argv[])
{
  GtsFile *fp;
  GtsSurface *s;
  GtsSurfaceQualityStats qstats;
  time_t start;
  GSList *trilist = NULL;


  // Error message for wrong usage
  if (argc != 4) {
    fprintf(stderr, "Usage %s sigma_f sigma_g dist_mode < in.gts > out.gts\n",
            argv[0]);
    exit (-1);
  }

  // read surface in 
  s = gts_surface_new (gts_surface_class (),
		       gts_face_class (),
		       gts_edge_class (),
		       gts_vertex_class ());
  fp = gts_file_new (stdin);
  if (gts_surface_read (s, fp)) {
    fprintf(stderr, "input not a valid GTS file\n");
    return 1; // failure 
  }

  gts_surface_quality_stats(s, &qstats);
  gts_surface_print_stats(s, stderr);

  // read command line arguments
  sigma_f = atof(argv[1]);
  sigma_g = atof(argv[2]);
  dist_mode = atof(argv[3]);
  printf("# sigma_f %f   sigma_g %f\n", sigma_f, sigma_g);

  // scale by mean edge length
  sigma_f *= qstats.edge_length.mean;
  sigma_g *= qstats.edge_length.mean;

  cutoff = 2.0 * sigma_f;
  sigma_m = sigma_f / 2.0;

  // create bounding boxes for the triangles
  gts_surface_foreach_face(s, box_by_centroid, &trilist);

  // turn the above into a tree for searching
  tree = gts_bb_tree_new(trilist);

  // initialize hashes to store mollified points and changed points
  mollified_hash = g_hash_table_new(NULL, NULL);
  new_position_hash = g_hash_table_new(NULL, NULL);
  num_verts = gts_surface_vertex_number(s);

  start = time(NULL);
  // generate 'mollified' normals
  gts_surface_foreach_vertex(s, mollify_vertex, NULL);
  // calculate changes based on 'mollified' normals
  gts_surface_foreach_vertex(s, filter_vertex, NULL);
  // shift all points 
  gts_surface_foreach_vertex(s, move_vertex, NULL);

  printf("# time taken: %d secs\n", (guint) (time(NULL) - start));

  gts_surface_write(s, stdout);

  return 0; // success 
}


import numpy as np
from scipy.spatial import Delaunay
import csv


def powerset_indices(num_elements):
  index_lists = []
  for i in range(1, 2**num_elements):
    charlist = list(bin(i)[2:])
    bitlist = [int(x) for x in charlist]
    bitlist.reverse()
    indices = np.flatnonzero(bitlist).tolist()
    index_lists.append(indices)
  return index_lists

def generate_other_points(point):
  other_points = []
  dim = len(point)
  index_lists = powerset_indices(dim)
  for indices in index_lists:
    point_copy = point.copy()
    for i in indices:
      if (point_copy[i]>0)
        point_copy[i]=0
    if point_copy!=point:
      other_points.append(point_copy)
  return other_points


def flesh_out_dominance(points):
  more_points = []
  for point in points:
    more_points.extend(generate_other_points(point))
  more_points.extend(points) 
  return more_points

def remove_duplicates(points):
  b_set = set(tuple(x) for x in points)
  b = [ list(x) for x in b_set ]
  return b


def in_hull(p, hull):
    from scipy.spatial import Delaunay
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull, qhull_options="QJ")
    return hull.find_simplex(p)>=0

def find_row_dominations(rows):
  dominated_rows = []
  dim = len(rows[0])
  numvec = len(rows)
  pset_indices = powerset_indices(numvec)
  for i in range(numvec):
    for indices in pset_indices:
      if i not in indices and len(indices)>1:
        other_vectors = [rows[i] for i in indices]
        other_vectors = flesh_out_dominance(other_vectors)
        other_vectors = remove_duplicates(other_vectors)
        other_vectors.extend(flesh_out_dominance([[-10000]*dim]))
        current_vector = rows[i]
        k = 0
        while (len(other_vectors)<5):
          other_vectors.append([0.5* m for m in other_vectors[k]])
          other_vectors=remove_duplicates(other_vectors)
        print(current_vector)
        print(other_vectors)
        print(in_hull(current_vector, other_vectors))
        if (in_hull(current_vector, other_vectors)):
          dominated_rows.append([i, indices])
  return dominated_rows
      
def find_dominations(rows, columns):
  dominated_rows = find_row_dominations(rows)
  for dominated_row in dominated_rows:
    print(f"row {dominated_row[0]} is dominated by {dominated_row[1:]}")

  columnsnp = np.array(columns)
  columnsnp = columnsnp.transpose()
  columns = columnsnp.tolist()
  print("f")
  print(columns)
  dominated_columns = find_row_dominations(columns)
  for dominated_column in dominated_columns:
    print(f"column {dominated_column[0]} is dominated by {dominated_column[1:]}")

with open('rowpayoffs.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  row_utility_vectors = [[int(i) for i in v] for v in reader]


with open('columnpayoffs.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  column_utility_vectors = [[int(i) for i in v] for v in reader]

tested = [[3, 3]]
print(flesh_out_dominance([[4, 2], [2, 4], [0, 0], [0, 0]]))


find_dominations(row_utility_vectors, column_utility_vectors)

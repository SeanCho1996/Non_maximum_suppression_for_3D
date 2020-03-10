#include <pybind11/pybind11.h>
#include <vector>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace std;

struct bb_score
{
	vector<vector<float>> res_box;
	vector<float> res_score;
};

vector<int> argsort(const vector<float>& a) {
	int Len = a.size();
	vector<int> idx(Len, 0);
	for (int i = 0; i < Len; i++) {
		idx[i] = i;
	}
	sort(idx.begin(), idx.end(), 
		[&a](int pos1, int pos2) {return (a[pos1] < a[pos2]); });
	return idx;
}

bb_score nms_3d(vector<vector<float>>& boxes, vector<float>& scores, float iou_threshold) {
	// initialize result
	bb_score res;
	res.res_box = vector<vector<float>>();
	res.res_score = vector<float>();

	// if no entry boxes, return empty list
	if (boxes.empty()) {
		return res;
	}

	// extarct coordinates of each bounding box
	vector<float> front_bottom_left_x;
	vector<float> front_bottom_left_y;
	vector<float> front_bottom_left_z;
	vector<float> back_top_right_x;
	vector<float> back_top_right_y;
	vector<float> back_top_right_z;
	for (size_t i = 0; i < boxes.size(); i++) {
		vector<float> sub_box = boxes[i];
		front_bottom_left_x.push_back(sub_box[0]);
		front_bottom_left_y.push_back(sub_box[1]);
		front_bottom_left_z.push_back(sub_box[2]);
		back_top_right_x.push_back(sub_box[3]);
		back_top_right_y.push_back(sub_box[4]);
		back_top_right_z.push_back(sub_box[5]);
	}

	// compute volume of bounding boxes
	vector<float> volumes;
	for (size_t i = 0; i < boxes.size(); i++) {
		volumes.push_back((back_top_right_x[i] - front_bottom_left_x[i]) * 
						  (back_top_right_y[i] - front_bottom_left_y[i]) * 
						  (back_top_right_z[i] - front_bottom_left_z[i]));
	}

	// sort score in order to extract the most potential bounding box
	vector<int> order = argsort(scores);

	// initialize result bounding box & its score
	vector<vector<float>> res_boxes;
	vector<float> res_scores;

	// iterate to obtain result bounding boxes
	while (order.size() > 0) {
		int max_index = order.back();

		// extract result bounding box
		res_boxes.push_back(boxes[max_index]);
		res_scores.push_back(scores[max_index]);

		// compute the coordinates of the intersection regions (of the res_box and all other boxes)
		vector<float> x1, x2, y1, y2, z1, z2;
		for (size_t i = 0; i < order.size() - 1; i++) {
			x1.push_back(front_bottom_left_x[max_index] > front_bottom_left_x[order[i]] ? front_bottom_left_x[max_index] : front_bottom_left_x[order[i]]);
			x2.push_back(back_top_right_x[max_index] < back_top_right_x[order[i]] ? back_top_right_x[max_index] : back_top_right_x[order[i]]);

			y1.push_back(front_bottom_left_y[max_index] > front_bottom_left_y[order[i]] ? front_bottom_left_y[max_index] : front_bottom_left_y[order[i]]);
			y2.push_back(back_top_right_y[max_index] < back_top_right_y[order[i]] ? back_top_right_y[max_index] : back_top_right_y[order[i]]);

			z1.push_back(front_bottom_left_z[max_index] > front_bottom_left_z[order[i]] ? front_bottom_left_z[max_index] : front_bottom_left_z[order[i]]);
			z2.push_back(back_top_right_z[max_index] < back_top_right_z[order[i]] ? back_top_right_z[max_index] : back_top_right_z[order[i]]);

			//printf("x1, y1, z1: %f, %f, %f    ", x1[i], y1[i], z1[i]);
			//printf("x2, y2, z2: %f, %f, %f\n", x2[i], y2[i], z2[i]);
		}
		// [x1, y1, z1] is the front_bottom_left point of the intersection region
		// [x2, y2, z2] is the back_top_right point of the intersection region

		// compute the volume of intersection region
		vector<float> intersection_volume;
		for (size_t i = 0; i < order.size() - 1; i++) {
			intersection_volume.push_back((0 > (x2[i] - x1[i]) ? 0 : (x2[i] - x1[i]))* // width
				(0 > (y2[i] - y1[i]) ? 0 : (y2[i] - y1[i]))* // height
				(0 > (z2[i] - z1[i]) ? 0 : (z2[i] - z1[i])) // depth
			);
		}

		// compute the volume ratio between intersection region and the union of the two bounding boxes
		vector<float> ratio;
		for (size_t i = 0; i < order.size() - 1; i++) {
			float current_ratio = intersection_volume[i] / (volumes[max_index] + volumes[order[i]] - intersection_volume[i]);
			//printf("ratio: %f", current_ratio);
			ratio.push_back(current_ratio);
		}

		// delete the bounding boxes with a higher intersection ratio than iou_threshold
		vector<int> rest_index;
		for (size_t i = 0; i < ratio.size(); i++) {
			if (ratio[i] < iou_threshold)
				rest_index.push_back(i);
		}
		vector<int> temp_order;
		for (size_t i = 0; i < rest_index.size(); i++) {
			temp_order.push_back(order[rest_index[i]]);
		}
		//printf("rest_index size: %d", rest_index.size());
		order.clear();
		order = temp_order;
	}
	
	res.res_box = res_boxes;
	res.res_score = res_scores;

	return res;
}

PYBIND11_MODULE(nms_cpp, m) {
	m.doc() = "implementation of NMS algorithm in 3D application";
	py::class_<bb_score>(m, "bb_score")
		.def_readwrite("res_boxes", &bb_score::res_box)
		.def_readwrite("res_scores", &bb_score::res_score);

	m.def("nms_3d", &nms_3d, py::return_value_policy::reference);
}
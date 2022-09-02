#pragma warning(disable: 4819)

#include <seeta/FaceDetector.h>
#include <seeta/FaceLandmarker.h>

#include <seeta/Struct_cv.h>
#include <seeta/Struct.h>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <string.h>
#include <array>
#include <map>
#include <iostream>
#include <fstream>

//int test_image(seeta::FaceDetector &FD, seeta::FaceLandmarker &FL) {
//	std::string image_path = "1.jpg";
//	std::cout << "Loading image: " << image_path << std::endl;
//	auto frame = cv::imread(image_path);
//	seeta::cv::ImageData simage = frame;
//
//	if (simage.empty()) {
//		std::cerr << "Can not open image: " << image_path << std::endl;
//		return EXIT_FAILURE;
//	}
//
//
//	auto faces = FD.detect(simage);
//
//	for (int i = 0; i < faces.size; ++i) {
//		auto &face = faces.data[i];
//		auto points = FL.mark(simage, face.pos);
//
//		cv::rectangle(frame, cv::Rect(face.pos.x, face.pos.y, face.pos.width, face.pos.height), CV_RGB(128, 128, 255), 3);
//		for (auto &point : points) {
//			cv::circle(frame, cv::Point(point.x, point.y), 3, CV_RGB(128, 255, 128), -1);
//		}
//	}
//
//	auto output_path = image_path + ".pts81.png";
//	cv::imwrite(output_path, frame);
//	std::cerr << "Saving result into: " << output_path << std::endl;
//
//	return EXIT_SUCCESS;
//}

int main() {
    seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
    int id = 0;
    seeta::ModelSetting FD_model( "./model/fd_2_00.dat", device, id );
    seeta::ModelSetting FL_model( "./model/pd_2_00_pts81.dat", device, id );

	seeta::FaceDetector FD(FD_model);
	seeta::FaceLandmarker FL(FL_model);

	FD.set(seeta::FaceDetector::PROPERTY_VIDEO_STABLE, 1);

	// 打开相机📷
	//int camera_id = 0;
	//cv::VideoCapture capture(camera_id);
	//if (!capture.isOpened()) {
	//	std::cerr << "Can not open camera(" << camera_id << "), testing image..." << std::endl;
	//	return test_image(FD, FL);
	//}
	//std::cout << "Open camera(" << camera_id << ")" << std::endl;

	cv::String video_dir_root = "D:\\HR Estimation\\PFFdatabase\\";
	std::string dat_dir_root = "D:\\HR Estimation\\face_landmarks_81p\\";
	std::vector<std::string> scenario{ "DM", "DS", "NM", "NS", "NSE" };

	std::ofstream log_digest; // 运行时间长，记录关键日志信息
	log_digest.open("D:\\HR Estimation\\face_landmark_generation.log", std::ios::out);

	// 数据集01-13循环开始
	for (int data_id = 1; data_id <= 13; ++data_id) {

		cv::String video_no = cv::String(std::to_string(data_id));
		if (data_id < 10)
			video_no = cv::String("0") + video_no;
		cv::String video_dir_pref = 
			video_dir_root + video_no + cv::String("\\") + video_no + cv::String("_");

		std::string dat_no = std::to_string(data_id);
		if (data_id < 10)
			dat_no = "0" + dat_no;
		std::string dat_dir_pref = 
			dat_dir_root + dat_no + "\\" + dat_no + "_";

		// 场景循环开始
		for (auto& sce : scenario) {

			cv::String video_dir = video_dir_pref + cv::String(sce) + cv::String("_f.MOV");
			std::string dat_dir = dat_dir_pref + sce + "\\";

			// 打开视频
			cv::VideoCapture capture;
			capture.open(video_dir);
			/*if (!capture.isOpened()) {
				std::cerr << "Failed to open video file.";
				return EXIT_FAILURE;
			}*/
			if (!capture.isOpened()) {
				std::clog << "Failed to open video file: " + video_dir << std::endl;
				log_digest << "Failed to open video file: " + video_dir << std::endl;
				continue; // 有些数据文件夹的场景不全，需要跳过
			}

			// 获取视频尺寸
			//auto video_width = capture.get(cv::CAP_PROP_FRAME_WIDTH);
			//auto video_height = capture.get(cv::CAP_PROP_FRAME_HEIGHT);

			// 逐帧处理
			int frameCount = 0; // 帧数
			cv::Mat frame;
			while (capture.isOpened()) {

				frameCount++;

				bool bool_grab = capture.grab();
				bool bool_retrieve = capture.retrieve(frame);
				//if (frame.empty()) break;
				if (!bool_grab || !bool_retrieve) break;

				seeta::cv::ImageData simage = frame;
				auto faces = FD.detect(simage);

				for (int i = 0; i < faces.size; ++i) {
					auto& face = faces.data[i];
					auto points = FL.mark(simage, face.pos);

					// 输出数据文件
					std::string dat_dir_final = 
						dat_dir + "landmarks" + std::to_string(frameCount) + ".dat";
					std::ofstream fout;
					fout.open(dat_dir_final, std::ios::out | std::ios::binary);
					for (auto& point : points) {
						int px = int(point.x);
						int py = int(point.y);
						fout.write((char*)&px, sizeof(int));
						fout.write((char*)&py, sizeof(int));
					}
					fout.close();
					std::clog << "Write file " + dat_dir_final << std::endl;

					// 标记图像
					/*cv::rectangle(frame, cv::Rect(face.pos.x, face.pos.y, face.pos.width, face.pos.height), CV_RGB(128, 128, 255), 3);
					for (auto& point : points) {
						cv::circle(frame, cv::Point(int(point.x), int(point.y)), 2, CV_RGB(128, 255, 128), -1);
					}*/
				}

				// 标示视频信息
				/*std::string frame_info = video_dir +
					"    Frame: " + std::to_string(frameCount) +
					"    Time: " + std::to_string(frameCount / 50) + "s";
				cv::putText(frame, frame_info, cv::Point(10, 30),
					cv::FONT_HERSHEY_SIMPLEX, 0.75, CV_RGB(255, 128, 0), 2);*/

				// 显示视频
				//cv::imshow("Frame", frame);
				//auto key = cv::waitKey(1); // 延时并接收键盘；若连续处理速度过快，则无法播放
				//if (key == 27) // 按Esc退出
				//	break;

			}

			log_digest << "Completed landmarks in directory: " + dat_dir << std::endl;

		} // 场景循环结束

	} // 数据集01-13循环结束

	log_digest.close();

	system("PAUSE");
	return EXIT_SUCCESS;
}

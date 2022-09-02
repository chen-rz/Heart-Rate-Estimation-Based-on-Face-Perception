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

int main() {
	seeta::ModelSetting::Device device = seeta::ModelSetting::CPU;
	int id = 0;
	seeta::ModelSetting FD_model("./model/fd_2_00.dat", device, id);
	seeta::ModelSetting FL_model("./model/pd_2_00_pts81.dat", device, id);

	seeta::FaceDetector FD(FD_model);
	seeta::FaceLandmarker FL(FL_model);

	FD.set(seeta::FaceDetector::PROPERTY_VIDEO_STABLE, 1);

	// 打开相机📷
	/*int camera_id = 0;
	cv::VideoCapture capture(camera_id);
	if (!capture.isOpened()) {
		std::cerr << "Could not open camera(" << camera_id << ")" << std::endl;
		return EXIT_FAILURE;
	}
	std::cout << "Opened camera(" << camera_id << ")" << std::endl;*/

	// 设置视频尺寸
	/*capture.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
	capture.set(cv::CAP_PROP_FRAME_HEIGHT, 720);*/

	// 打开视频
	cv::VideoCapture capture;
	capture.open("..\\VideoCapture\\raw_video.MOV");
	if (!capture.isOpened()) {
		std::cerr << "Failed to open video file." << std::endl;
		return EXIT_FAILURE;
	}

	// 文件输出路径
	std::ofstream fout;
	std::string dat_dir = "..\\VideoCapture\\rt_face_landmarks\\";

	// 逐帧处理
	int frameCount = 0; // 帧数
	cv::Mat frame;
	while (capture.isOpened()) {

		frameCount++;

		// 取下一帧
		bool bool_grab = capture.grab();
		bool bool_retrieve = capture.retrieve(frame);
		//if (frame.empty()) break;
		if (!bool_grab || !bool_retrieve) break;

		// 人脸检测
		seeta::cv::ImageData simage = frame;
		auto faces = FD.detect(simage);
		
		// 若没有人脸则报错退出
		if (faces.size == 0) {
			std::cerr << "Error: No face detected. Please keep steady and try again." 
				<< std::endl;
			return EXIT_FAILURE;
		}

		// 只标记第一个人脸
		auto& face = faces.data[0];
		auto points = FL.mark(simage, face.pos);

		// 输出数据文件
		std::string dat_dir_final =
			dat_dir + "landmarks" + std::to_string(frameCount) + ".dat";
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
		cv::rectangle(
			frame,
			cv::Rect(face.pos.x, face.pos.y, face.pos.width, face.pos.height),
			CV_RGB(128, 128, 255), 3
		);
		for (auto& point : points) {
			cv::circle(
				frame,
				cv::Point(int(point.x), int(point.y)),
				2, CV_RGB(128, 255, 128), -1
			);
		}

		// 标示视频信息
		std::string frame_info = "Processing... Frame: " + std::to_string(frameCount);
		cv::putText(frame, frame_info, cv::Point(10, 30),
			cv::FONT_HERSHEY_SIMPLEX, 0.75, CV_RGB(255, 128, 128), 2);

		// 显示视频
		std::string prompt = "Face Landmarks - 81 Points";
		cv::namedWindow(prompt, cv::WINDOW_NORMAL);
		cv::resizeWindow(prompt, cv::Size(960, 540));
		cv::imshow(prompt, frame);
		cv::waitKey(1); // 延时，若连续处理速度过快，则无法播放

	}

	capture.release();
	cv::destroyAllWindows();

	//system("PAUSE");
	return EXIT_SUCCESS;
}

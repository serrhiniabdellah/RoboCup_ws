#ifndef BRAS_AUTOMATIQUE_FINDER_H
#define BRAS_AUTOMATIQUE_FINDER_H

#include <opencv2/opencv.hpp>
#include <vector>
#include <utility>
#include <cv_bridge/cv_bridge.hpp>

std::pair<cv::Point_<int>, cv::Point_<int>> getMinMaxPoints(const std::vector<cv::Point_<int>>& points);
std::pair<cv::Point_<int>, cv::Point_<int>> getMinMaxPointsX(const std::vector<cv::Point_<int>>& points);
std::pair<cv::Point_<int>, cv::Point_<int>> getMinMaxPointsY(const std::vector<cv::Point_<int>>& points);
std::vector<cv::Point_<int>> MoyenneVecteurs(const std::vector<cv::Point_<int>>& vecteur1, const std::vector<cv::Point_<int>>& vecteur2);
std::vector<cv::Point_<int>> Approximation_ligne(cv_bridge::CvImagePtr testimage, std::vector<cv::Point_<int>> Contour, int nombre_decoupage, int iR, int iG, int iB);

#endif // BRAS_AUTOMATIQUE_FINDER_H

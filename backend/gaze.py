from typing import Literal
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark, NormalizedLandmarkList
from numpy import ndarray
from scipy.spatial import distance
import imutils

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

flag = 0

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def sleep_detection(frame: ndarray) -> str:
    global flag
    thresh = 0.10
    frame_check = 20
    
    frame = imutils.resize(frame, width=450)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if not results.multi_face_landmarks:
        return "awake"

    for face_landmarks in results.multi_face_landmarks:
        # MediaPipe eye landmarks indices (left and right eyes)
        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]

        left_eye = []
        right_eye = []
        
        # Extract left eye coordinates
        for idx in left_eye_indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            left_eye.append((x, y))
            
        # Extract right eye coordinates
        for idx in right_eye_indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            right_eye.append((x, y))

        leftEAR = eye_aspect_ratio(left_eye)
        rightEAR = eye_aspect_ratio(right_eye)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < thresh:
            flag += 1

            if flag >= frame_check:
                if ear< thresh:
                    return "sleepy"
                flag = 0
        else:
            flag = 0
            return "forward"

def relative(landmark: NormalizedLandmark, shape: tuple[int, int, int]) -> tuple[int, int]:
    return (int(landmark.x * shape[1]), int(landmark.y * shape[0]))

def relativeT(landmark: NormalizedLandmark, shape: tuple[int, int, int]) -> tuple[int, int, Literal[0]]:
    return (int(landmark.x * shape[1]), int(landmark.y * shape[0]), 0)

def gaze(frame: ndarray, points: NormalizedLandmarkList) -> str:
    """
    The gaze function gets an image and face landmarks from mediapipe framework.
    Returns the gaze direction as a string: 'forward', 'left', or 'right'
    """

    image_points = np.array([
        relative(points.landmark[4], frame.shape),
        relative(points.landmark[152], frame.shape),
        relative(points.landmark[263], frame.shape),
        relative(points.landmark[33], frame.shape),
        relative(points.landmark[287], frame.shape),
        relative(points.landmark[57], frame.shape)
    ], dtype="double")

    image_points1 = np.array([
        relativeT(points.landmark[4], frame.shape),
        relativeT(points.landmark[152], frame.shape),
        relativeT(points.landmark[263], frame.shape),
        relativeT(points.landmark[33], frame.shape),
        relativeT(points.landmark[287], frame.shape),
        relativeT(points.landmark[57], frame.shape)
    ], dtype="double")

    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0, -63.6, -12.5),
        (-43.3, 32.7, -26),
        (43.3, 32.7, -26),
        (-28.9, -28.9, -24.1),
        (28.9, -28.9, -24.1)
    ])

    Eye_ball_center_left = np.array([[29.05], [32.7], [-39.5]])

    focal_length = frame.shape[1]
    center = (frame.shape[1] / 2, frame.shape[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    dist_coeffs = np.zeros((4, 1))
    (success, rotation_vector, translation_vector) = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    left_pupil = relative(points.landmark[468], frame.shape)

    _, transformation, _ = cv2.estimateAffine3D(image_points1, model_points)

    if transformation is not None:
        pupil_world_cord = transformation @ np.array([[left_pupil[0], left_pupil[1], 0, 1]]).T

        S = Eye_ball_center_left + (pupil_world_cord - Eye_ball_center_left) * 10

        (eye_pupil2D, _) = cv2.projectPoints((int(S[0]), int(S[1]), int(S[2])), rotation_vector,
                                             translation_vector, camera_matrix, dist_coeffs)
        (head_pose, _) = cv2.projectPoints((int(pupil_world_cord[0]), int(pupil_world_cord[1]), int(40)),
                                           rotation_vector,
                                           translation_vector, camera_matrix, dist_coeffs)
        gaze = left_pupil + (eye_pupil2D[0][0] - left_pupil) - (head_pose[0][0] - left_pupil)

        point1 = (int(left_pupil[0]), int(left_pupil[1]))
        point2 = (int(gaze[0]), int(gaze[1]))

        point1_arr = np.array([int(left_pupil[0]), int(left_pupil[1])])
        point2_arr = np.array([int(gaze[0]), int(gaze[1])])

        points_diff = point1_arr - point2_arr
        abs_points_diff = abs(points_diff)

        if -10 > points_diff[1]:
            print("looking down")
            return "down"

        elif 10 > points_diff[0] > -40:
            if sleep_detection(frame) == "sleepy":
                print("sleepy")
                return "sleepy"
            print("looking forward")
            return "forward"

        elif points_diff[0] != abs_points_diff[0]:
            print("looking left")
            return "left"

        else:
            print("looking right")
            return "right"
    
    return "unknown"
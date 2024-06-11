import cv2
import numpy as np
from pupil_apriltags import Detector

def main():
    # 打開預設攝像頭
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    # 創建 AprilTag 檢測器
    detector = Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=False)

    while True:
        # 讀取幀
        ret, frame = cap.read()
        if not ret:
            break

        # 轉換為灰度圖像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 檢測 AprilTag
        detections = detector.detect(gray)

        # 檢查是否有檢測到 AprilTag
        if detections:
            # 繪製檢測結果
            for detection in detections:
                # 獲取角點
                pts = np.array(detection.corners, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

                # 顯示 AprilTag ID
                cv2.putText(frame, str(detection.tag_id), (pts[0][0][0], pts[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # 顯示姿態信息
                if detection.pose_R is not None and detection.pose_t is not None:
                    cv2.putText(frame, f"tvec: {detection.pose_t[0]:.2f}, {detection.pose_t[1]:.2f}, {detection.pose_t[2]:.2f}", (pts[0][0][0], pts[0][0][1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, f"rvec: {detection.pose_R[0]:.2f}, {detection.pose_R[1]:.2f}, {detection.pose_R[2]:.2f}", (pts[0][0][0], pts[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 顯示結果
        cv2.imshow('AprilTag Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

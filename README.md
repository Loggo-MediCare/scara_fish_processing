# SCARA Fish Processing System 🐟🤖

本專案結合 **SCARA 機器人手臂**、**電腦視覺 (OpenCV)** 與 **Raspberry Pi GPIO 控制**，  
用於 **魚類/肉類自動加工**，展示智慧食品加工的創新應用。

---

## ✨ 系統架構


flowchart LR
    Camera[📷 Camera - Fish Detection] -->|影像輸入| Vision[Vision System (OpenCV + NumPy)]
    Vision -->|輪廓 + 切割點| Control[Integrated Control System (Python)]
    Control -->|IK + Trajectory| SCARA[🤖 SCARA Robot Arm]
    SCARA -->|GPIO PWM| RPi[Raspberry Pi]
🔧 功能特色

SCARA 機器人控制

正運動學 / 逆運動學 (NumPy)

軌跡規劃 (線性插補 + S 曲線平滑)

GPIO 控制伺服馬達與夾爪

電腦視覺 (魚類加工)

圖像預處理 (灰階、模糊、Canny 邊緣檢測)

魚體輪廓偵測 (RANSAC 擬合)

體積估算與切割點預測

集成控制系統

任務分派 (CuttingTask)

自動執行切割與誤差分析

可擴充至產線自動化

## 📂 專案結構

scara_fish_processing/
│
├── scara_robot.py          # SCARA 機器人運動學與 GPIO 控制
├── fish_vision.py          # 魚類加工影像處理
├── integrated_system.py    # 集成控制系統
├── main.py                 # 主程式入口
├── requirements.txt        # 依賴套件
└── README.md               # 專案說明

## 🚀 安裝與執行
1. 建立環境
git clone git@github.com:RootInnovationTW/scara_fish_processing.git
cd scara_fish_processing
pip install -r requirements.txt

2. 執行主程式
python3 main.py

3. 更新程式到 GitHub
./git_update.sh "update vision module"

📊 未來擴充

 整合 AI 模型 (YOLO/Mask R-CNN) 提升魚體偵測準確率

 增加數位孿生 (Digital Twin) 進行虛擬模擬

 支援 Docker 部署與 CI/CD

 應用於智慧醫療/食品安全檢測

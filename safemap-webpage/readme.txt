----------Installation Guide(for the fontend/backend)----------
前端(frontend)：
1. 安裝最新版本之 Node.js
3. 確定 npm 指令可用 (cmd)
4. cd到前端資料夾(或vscode開啟資料夾)，輸入指令：npm install
5. 新建檔案".env.local"，內部輸入文字內容：
REACT_APP_GOOGLE_MAPS_API_KEY = key
(key-> google api key)
(如何取得api key: https://console.cloud.google.com/google/maps-apis/start?hl=zh-tw)

後端(backend):
1. 建立osmnx之python環境 (以下利用conda建立環境)
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx
(ox為環境名稱可自行更改)
2. conda activate ox 
(也可使用 pip install osmnx, 但可能會缺少部分套件)
3. pip install flask


-------------------------How to Start-------------------------
前端(frontend)：
1. cd到前端資料夾
2. npm start

後端(backend):
1. cd到後端資料夾
2. conda activate ox
3. python app.py

--------------------------------------------------------------
Q: 我很懶不想要輸入指令怎麼辦?
A: 新增一個文字文件並輸入以下內容：
start cmd.exe /C "cd frontend && npm start"
start cmd.exe /C "cd backend && conda activate ox &&python app.py runserver"
將此文字文件之副檔名改為.bat即可雙擊此檔案同時啟動前端與後端。
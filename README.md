python初学者自学项目，所含素材仅用作学习交流

外星人入侵（Alien Invasion）
一款基于 Pygame 的 2D 射击游戏，玩家控制飞船，发射子弹消灭不断移动的外星人。随着关卡提升，游戏速度逐渐加快，考验你的反应能力。

功能特性
外星人群自动移动，到达边缘会下移并反向
子弹与外星人碰撞检测，消灭外星人获得分数
每消灭一群外星人，游戏速度提升，等级增加
生命值系统（可配置生命数）
实时显示得分、等级、剩余飞船数
游戏结束后按 R 键 重新开始
简单易上手，适合 Pygame 初学者学习

运行环境
Python 3.11 或更高版本
Pygame 2.6.1 或更高版本

安装与运行
克隆本仓库到本地：
bash
git clone https://github.com/你的用户名/alien_invasion.git
cd alien_invasion

安装依赖（推荐使用虚拟环境）：
bash
pip install -r requirements.txt
如果没有 requirements.txt，可手动安装 Pygame：
bash
pip install pygame

运行游戏：
bash
python alien_invasion.py

操作说明
按键	功能
← / →	左右移动飞船
↑ / W	向上移动飞船
↓ / S	向下移动飞船
空格	发射子弹
R	游戏结束后重新开始

项目结构
text
alien_invasion/
├── alien_invasion.py    # 主游戏文件
├── images/              # 存放游戏图片（需自备）
│   └── ship.bmp         # 飞船图片
├── README.md            # 本文件
└── .gitignore           # Git 忽略文件

自定义与扩展
修改生命值：在 Settings 类中调整 self.ship_limit。
修改游戏速度：调整 Settings 中的 ship_speed、bullet_speed、alien_speed 等。
替换图片：将 ship.bmp 和 alien.bmp 放入 images/ 文件夹，代码会自动加载。
增加新功能：如增加特殊武器、Boss 战等，欢迎 fork 并提交 PR。

常见问题
Q：运行后窗口一闪而过？
A：检查是否安装了 Pygame，或在命令行中运行查看错误信息。

Q：按 R 键无效？
A：确保游戏窗口处于活动状态，且输入法为英文模式。

Q：没有飞船图片怎么办？
A：你可以用画图工具创建一个简单的彩色矩形，保存为 ship.bmp 放到 images/ 文件夹。

致谢
本项目参考《Python编程：从入门到实践》第12~14章内容实现。

感谢 Pygame 社区提供的优秀库。

注意，素材来自于网路，非商业用途，仅供个人学习使用，若侵权请联系删除。

你可以根据实际仓库信息修改用户名、补充截图等。如有任何问题，欢迎在 Issues 中提出。

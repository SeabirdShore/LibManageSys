文件结构说明：
librarian/reader.yaml：为登陆信息
src：图书管理系统的主要实现文件
authenticator：密码验证系统

操作系统：Ubuntu22.04
前端框架：Tornado（integrated in Streamlit）
后端框架：Streamlit 1.33.0 数据库：MySQL 8.036
编译环境：Anaconda 23.7.4 虚拟环境配置详见 requirements.txt
##################Command of Compiling in Terminal#################
1| conda activate <env_name>
2| cd src
3| streamlit run app.py
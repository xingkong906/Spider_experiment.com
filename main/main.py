from dao.backer import Backer
from dao.project_page import ProjectPage
from dao.Dao import Dao

index = 'https://experiment.com'


def select_project():
    dao = Dao()
    sql = 'SELECT id,url FROM project WHERE "process_status"="false"'
    rs = dao.cursor.execute(sql).fetchall()
    print(len(rs))
    for cell in rs:
        id, url = cell
        page = ProjectPage(id=id, url=index + url)
        page.run()


def select_backer():
    pass


def run():
    pass


if __name__ == '__main__':
    # 项目主程序
    run()
    select_project()

from dao.backer import Backer
from dao.project_page import ProjectPage
from dao.Dao import Dao
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

index = 'https://experiment.com'
root = ' '


def select_project():
    dao = Dao()
    sql = 'SELECT id,url FROM project WHERE "process_status"="false"'
    rs = dao.cursor.execute(sql).fetchall()
    print(len(rs))
    for cell in rs:
        id, url = cell
        print(id)
        page = ProjectPage(id=id, url=index + url)
        page.run()


def select_backer():
    dao = Dao()
    sql = 'SELECT id,username FROM backers WHERE "process_status"="false"'
    rs = dao.cursor.execute(sql).fetchall()
    print(len(rs))
    return rs
    # for cell in rs:
    #     id, username = cell
    #     print(id)
    #     backer = Backer(id=id, url=root + username)
    #     backer.run()


def main(task):
    ids, username = task
    print(ids)
    backer = Backer(id=ids, url=root + username)
    backer.run()
    print(id)


def run(tasks):
    # select_project()
    # select_backer()
    with ThreadPoolExecutor(max_workers=10) as execctor:
        execctor.map(main, tasks, timeout=100)
    print("处理完成")


if __name__ == '__main__':
    # 项目主程序
    # run()
    # select_project()
    tasks = select_backer()
    run(tasks)
    print("已经完成")

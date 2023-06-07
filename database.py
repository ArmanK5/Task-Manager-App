import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-manager-database.db")
        self.cursor = self.con.cursor()
        self.create_task_table()

    # Creating the tasks table
    def create_task_table(self):
        self.cursor.execute("create table if not exists tasks (id integer PRIMARY KEY AUTOINCREMENT ,"
                            " task varchar(50) NOT NULL, due_date varchar(50), "
                            "completed BOOLEAN NOT NULL CHECK (completed IN (0,1)))")
        self.con.commit()

    def create_task(self, task, due_date=None):
        self.cursor.execute("insert into tasks(task, due_date, completed) VALUES(?,?,?)", (task, due_date, 0))
        self.con.commit()

        # Getting last entered item
        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0",
                                           (task,)).fetchall()
        return created_task[-1]

    # Get the tasks
    def get_tasks(self):
        # Grabs all tasks and filters to complete and incompleted
        incompleted_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        completed_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        return completed_tasks, incompleted_tasks

    # Updating tasks
    def mark_task_complete(self, taskid):
        # mark tasks as completed
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ? ", (taskid,))
        self.con.commit()

    def mark_task_incomplete(self, taskid):
        # mark tasks as completed
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ? ", (taskid,))
        self.con.commit()

        # return task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text[0][0]

    # Deleting tasks
    def delete_tasks(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit()

    # close connection
    def db_close(self):
        self.con.close()


import cherrypy
from models import *
from datetime import datetime
import os

class ScholarshipWebApp:

    @cherrypy.expose
    def index(self):
        """Главная страница со списком всех справок"""
        scholarships = Scholarship.select().join(Student).join(Department)

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Система управления справками о стипендиях</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .btn { padding: 8px 16px; margin: 5px; text-decoration: none; 
                       background-color: #007bff; color: white; border-radius: 4px; }
                .btn:hover { background-color: #0056b3; }
                .btn-danger { background-color: #dc3545; }
                .btn-danger:hover { background-color: #c82333; }
                .container { max-width: 1200px; margin: 0 auto; }
                .nav { margin-bottom: 20px; }
                .nav a { margin-right: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Система управления справками о стипендиях</h1>
                
                <div class="nav">
                    <a href="/" class="btn">Главная</a>
                    <a href="/students" class="btn">Студенты</a>
                    <a href="/departments" class="btn">Факультеты</a>
                    <a href="/add_scholarship" class="btn">Добавить справку</a>
                </div>
                
                <h2>Список справок о стипендиях</h2>
                <table>
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Дата</th>
                            <th>Студент</th>
                            <th>Факультет</th>
                            <th>Размер стипендии</th>
                            <th>Куда выдается</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for scholarship in scholarships:
            html += f"""
                        <tr>
                            <td>{scholarship.number}</td>
                            <td>{scholarship.date}</td>
                            <td>{scholarship.student.full_name}</td>
                            <td>{scholarship.student.department.name}</td>
                            <td>{scholarship.amount} руб.</td>
                            <td>{scholarship.destination}</td>
                            <td>
                                <a href="/edit_scholarship/{scholarship.id}" class="btn">Редактировать</a>
                                <a href="/delete_scholarship/{scholarship.id}" class="btn btn-danger" 
                                   onclick="return confirm('Вы уверены?')">Удалить</a>
                            </td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        return html

    @cherrypy.expose
    def students(self):
        """Страница со списком студентов"""
        students = Student.select().join(Department)

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Студенты</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .btn { padding: 8px 16px; margin: 5px; text-decoration: none; 
                       background-color: #007bff; color: white; border-radius: 4px; }
                .btn:hover { background-color: #0056b3; }
                .container { max-width: 1200px; margin: 0 auto; }
                .nav { margin-bottom: 20px; }
                .nav a { margin-right: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Список студентов</h1>
                
                <div class="nav">
                    <a href="/" class="btn">Главная</a>
                    <a href="/students" class="btn">Студенты</a>
                    <a href="/departments" class="btn">Факультеты</a>
                    <a href="/add_student" class="btn">Добавить студента</a>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>ФИО</th>
                            <th>Номер студента</th>
                            <th>Факультет</th>
                            <th>Количество справок</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for student in students:
            scholarship_count = student.scholarships.count()
            html += f"""
                        <tr>
                            <td>{student.id}</td>
                            <td>{student.full_name}</td>
                            <td>{student.student_id}</td>
                            <td>{student.department.name}</td>
                            <td>{scholarship_count}</td>
                            <td>
                                <a href="/edit_student/{student.id}" class="btn">Редактировать</a>
                            </td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        return html

    @cherrypy.expose
    def departments(self):
        """Страница со списком факультетов"""
        departments = Department.select()

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Факультеты</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .btn { padding: 8px 16px; margin: 5px; text-decoration: none; 
                       background-color: #007bff; color: white; border-radius: 4px; }
                .btn:hover { background-color: #0056b3; }
                .container { max-width: 1200px; margin: 0 auto; }
                .nav { margin-bottom: 20px; }
                .nav a { margin-right: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Список факультетов</h1>
                
                <div class="nav">
                    <a href="/" class="btn">Главная</a>
                    <a href="/students" class="btn">Студенты</a>
                    <a href="/departments" class="btn">Факультеты</a>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Название</th>
                            <th>Код</th>
                            <th>Количество студентов</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for dept in departments:
            student_count = dept.students.count()
            html += f"""
                        <tr>
                            <td>{dept.id}</td>
                            <td>{dept.name}</td>
                            <td>{dept.code}</td>
                            <td>{student_count}</td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        return html

    @cherrypy.expose
    def add_scholarship(self, **kwargs):
        """Добавление новой справки"""
        error_msg = ""

        if cherrypy.request.method == 'POST':
            try:
                number = kwargs.get('number')
                date = kwargs.get('date')
                student_id = kwargs.get('student_id')
                amount = kwargs.get('amount')
                destination = kwargs.get('destination')

                if not all([number, date, student_id, amount, destination]):
                    raise ValueError("Все поля должны быть заполнены")

                student = Student.get_by_id(int(student_id))
                Scholarship.create(
                    number=int(number),
                    date=date,
                    student=student,
                    amount=float(amount),
                    destination=destination
                )
                raise cherrypy.HTTPRedirect("/")
            except ValueError as e:
                error_msg = f"Ошибка валидации: {str(e)}"
            except Exception as e:
                if "HTTPRedirect" not in str(type(e)):
                    error_msg = f"Ошибка при добавлении справки: {str(e)}"
                else:
                    raise

        students = Student.select().join(Department)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Добавить справку</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .btn {{ padding: 8px 16px; margin: 5px; text-decoration: none; 
                       background-color: #007bff; color: white; border-radius: 4px; border: none; cursor: pointer; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .form-group {{ margin: 15px 0; }}
                .form-group label {{ display: inline-block; width: 150px; font-weight: bold; }}
                .form-group input, .form-group select {{ padding: 8px; width: 250px; border: 1px solid #ddd; border-radius: 4px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; }}
                .error {{ color: red; margin: 10px 0; padding: 10px; background-color: #f8d7da; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Добавить справку о стипендии</h1>
                
                <div class="nav">
                    <a href="/" class="btn">Главная</a>
                    <a href="/students" class="btn">Студенты</a>
                    <a href="/departments" class="btn">Факультеты</a>
                </div>
                
                {f'<div class="error">{error_msg}</div>' if error_msg else ''}
                
                <form method="post">
                    <div class="form-group">
                        <label for="number">Номер справки:</label>
                        <input type="number" id="number" name="number" required min="1">
                    </div>
                    
                    <div class="form-group">
                        <label for="date">Дата:</label>
                        <input type="date" id="date" name="date" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="student_id">Студент:</label>
                        <select id="student_id" name="student_id" required>
                            <option value="">Выберите студента</option>
        """

        for student in students:
            html += f'<option value="{student.id}">{student.full_name} ({student.department.name})</option>'

        html += """
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="amount">Размер стипендии:</label>
                        <input type="number" step="0.01" id="amount" name="amount" required min="0">
                    </div>
                    
                    <div class="form-group">
                        <label for="destination">Куда выдается:</label>
                        <input type="text" id="destination" name="destination" required maxlength="200">
                    </div>
                    
                    <div class="form-group">
                        <button type="submit" class="btn">Добавить справку</button>
                        <a href="/" class="btn btn-secondary">Отмена</a>
                    </div>
                </form>
            </div>
        </body>
        </html>
        """
        return html

    @cherrypy.expose
    def edit_scholarship(self, scholarship_id, **kwargs):
        """Редактирование справки"""
        error_msg = ""

        try:
            scholarship = Scholarship.get_by_id(int(scholarship_id))
        except:
            raise cherrypy.HTTPError(404, "Справка не найдена")

        if cherrypy.request.method == 'POST':
            try:
                number = kwargs.get('number')
                date = kwargs.get('date')
                student_id = kwargs.get('student_id')
                amount = kwargs.get('amount')
                destination = kwargs.get('destination')

                if not all([number, date, student_id, amount, destination]):
                    raise ValueError("Все поля должны быть заполнены")

                student = Student.get_by_id(int(student_id))
                scholarship.number = int(number)
                scholarship.date = date
                scholarship.student = student
                scholarship.amount = float(amount)
                scholarship.destination = destination
                scholarship.save()

                raise cherrypy.HTTPRedirect("/")
            except ValueError as e:
                error_msg = f"Ошибка валидации: {str(e)}"
            except Exception as e:
                if "HTTPRedirect" not in str(type(e)):
                    error_msg = f"Ошибка при редактировании справки: {str(e)}"
                else:
                    raise

        students = Student.select().join(Department)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Редактирование справки</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .btn {{ padding: 8px 16px; margin: 5px; text-decoration: none; 
                       background-color: #007bff; color: white; border-radius: 4px; border: none; cursor: pointer; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .form-group {{ margin: 15px 0; }}
                .form-group label {{ display: inline-block; width: 150px; font-weight: bold; }}
                .form-group input, .form-group select {{ padding: 8px; width: 250px; border: 1px solid #ddd; border-radius: 4px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; }}
                .error {{ color: red; margin: 10px 0; padding: 10px; background-color: #f8d7da; border-radius: 4px; }}
                .success {{ color: green; margin: 10px 0; padding: 10px; background-color: #d4edda; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Редактирование справки</h1>
                
                <div class="nav">
                    <a href="/" class="btn">Главная</a>
                    <a href="/students" class="btn">Студенты</a>
                    <a href="/departments" class="btn">Факультеты</a>
                </div>
                
                {f'<div class="error">{error_msg}</div>' if error_msg else ''}
                
                <form method="post">
                    <div class="form-group">
                        <label for="number">Номер справки:</label>
                        <input type="number" id="number" name="number" required min="1" value="{scholarship.number}">
                    </div>
                    
                    <div class="form-group">
                        <label for="date">Дата:</label>
                        <input type="date" id="date" name="date" required value="{scholarship.date}">
                    </div>
                    
                    <div class="form-group">
                        <label for="student_id">Студент:</label>
                        <select id="student_id" name="student_id" required>
                            <option value="">Выберите студента</option>
        """

        for student in students:
            html += f'<option value="{student.id}" {"selected" if student.id == scholarship.student.id else ""}>{student.full_name} ({student.department.name})</option>'

        html += """
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="amount">Размер стипендии:</label>
                        <input type="number" step="0.01" id="amount" name="amount" required min="0" value="{scholarship.amount}">
                    </div>
                    
                    <div class="form-group">
                        <label for="destination">Куда выдается:</label>
                        <input type="text" id="destination" name="destination" required maxlength="200" value="{scholarship.destination}">
                    </div>
                    
                    <div class="form-group">
                        <button type="submit" class="btn">Сохранить изменения</button>
                        <a href="/" class="btn btn-secondary">Отмена</a>
                    </div>
                </form>
            </div>
        </body>
        </html>
        """
        return html

    @cherrypy.expose
    def add_student(self, full_name=None, student_id=None, department_id=None):
        """Добавление нового студента"""
        error_msg = ""

        if cherrypy.request.method == 'POST':
            try:
                department = Department.get_by_id(department_id)
                Student.create(
                    full_name=full_name,
                    student_id=student_id,
                    department=department
                )
                raise cherrypy.HTTPRedirect("/students")
            except Exception as e:
                error_msg = f"Ошибка при добавлении студента: {str(e)}"

        departments = Department.select()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Добавить студента</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .btn {{ padding: 8px 16px; margin: 5px; text-decoration: none; 
                       background-color: #007bff; color: white; border-radius: 4px; border: none; cursor: pointer; }}
                .btn:hover {{ background-color: #0056b3; }}
                .form-group {{ margin: 10px 0; }}
                .form-group label {{ display: inline-block; width: 150px; }}
                .form-group input, .form-group select {{ padding: 5px; width: 200px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; }}
                .error {{ color: red; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Добавить студента</h1>
                
                <div class="nav">
                    <a href="/" class="btn">Главная</a>
                    <a href="/students" class="btn">Студенты</a>
                    <a href="/departments" class="btn">Факультеты</a>
                </div>
                
                {f'<div class="error">{error_msg}</div>' if error_msg else ''}
                
                <form method="post">
                    <div class="form-group">
                        <label for="full_name">ФИО:</label>
                        <input type="text" id="full_name" name="full_name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="student_id">Номер студента:</label>
                        <input type="text" id="student_id" name="student_id" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="department_id">Факультет:</label>
                        <select id="department_id" name="department_id" required>
                            <option value="">Выберите факультет</option>
        """

        for dept in departments:
            html += f'<option value="{dept.id}">{dept.name}</option>'

        html += """
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <button type="submit" class="btn">Добавить студента</button>
                        <a href="/students" class="btn" style="background-color: #6c757d;">Отмена</a>
                    </div>
                </form>
            </div>
        </body>
        </html>
        """
        return html
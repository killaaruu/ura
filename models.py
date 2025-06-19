from peewee import *
from datetime import datetime

# Database connection
db = SqliteDatabase('scholarships.db')

class BaseModel(Model):
    class Meta:
        database = db

class Department(BaseModel):
    """Модель для кафедр/факультетов"""
    name = CharField(max_length=100, unique=True)
    code = CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Student(BaseModel):
    """Модель для студентов"""
    full_name = CharField(max_length=200)
    student_id = CharField(max_length=20, unique=True)
    department = ForeignKeyField(Department, backref='students')
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.full_name

class Scholarship(BaseModel):
    """Модель для справок о стипендиях"""
    number = IntegerField(unique=True)
    date = DateField()
    student = ForeignKeyField(Student, backref='scholarships')
    amount = DecimalField(max_digits=10, decimal_places=2)
    destination = CharField(max_length=200)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Справка №{self.number} - {self.student.full_name}"

# Create tables
def create_tables():
    with db:
        db.create_tables([Department, Student, Scholarship])

# Initialize with sample data
def init_sample_data():
    try:
        # Create departments
        dept1, created = Department.get_or_create(
            name="Факультет информационных технологий",
            code="ФИТ"
        )
        dept2, created = Department.get_or_create(
            name="Экономический факультет",
            code="ЭФ"
        )

        # Create students
        student1, created = Student.get_or_create(
            full_name="Иванов Иван Иванович",
            student_id="2021001",
            department=dept1
        )
        student2, created = Student.get_or_create(
            full_name="Петрова Анна Сергеевна",
            student_id="2021002",
            department=dept1
        )
        student3, created = Student.get_or_create(
            full_name="Сидоров Петр Александрович",
            student_id="2021003",
            department=dept2
        )

        # Create scholarships
        Scholarship.get_or_create(
            number=1001,
            date="2024-01-15",
            student=student1,
            amount=2000.00,
            destination="Банк для стипендии"
        )
        Scholarship.get_or_create(
            number=1002,
            date="2024-01-16",
            student=student2,
            amount=2500.00,
            destination="Касса университета"
        )
        Scholarship.get_or_create(
            number=1003,
            date="2024-01-17",
            student=student3,
            amount=1800.00,
            destination="Банковская карта"
        )

    except Exception as e:
        print(f"Error initializing sample data: {e}")

if __name__ == '__main__':
    create_tables()
    init_sample_data()
    print("Database initialized successfully!")
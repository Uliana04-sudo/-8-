from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from .models import (
    AcademicGroup,
    Course,
    Department,
    StudentProfile,
)
from .forms import (
    AcademicGroupForm,
    CourseForm,
    DepartmentForm,
)

def is_methodist(user):
  return user.groups.filter(
        name='Методист'
    ).exists()
@login_required
def profile(request):
    return render(
        request,
        'profile.html',
        {
            'is_methodist': is_methodist(
                request.user
            )
        }
    )

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(
        request,
        'department_list.html',
        {
            'departments': departments,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )
@login_required
def academic_group_list(request):
    groups = AcademicGroup.objects.all()

    return render(
        request,
        'academic_group_list.html',
        {
            'groups': groups,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )
@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление учебной группы',
        }
    )
@login_required
@user_passes_test(is_methodist)
def academic_group_update(request, pk):
    group = get_object_or_404(
        AcademicGroup,
        pk=pk
    )

    if request.method == 'POST':
        form = AcademicGroupForm(
            request.POST,
            instance=group
        )

        if form.is_valid():
            form.save()
            return redirect(
                'academic_group_list'
            )
    else:
        form = AcademicGroupForm(
            instance=group
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение учебной группы',
        }
    )
@login_required
@user_passes_test(is_methodist)
def academic_group_delete(request, pk):
    group = get_object_or_404(
        AcademicGroup,
        pk=pk
    )

    if request.method == 'POST':
        group.delete()
        return redirect(
            'academic_group_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': group,
            'title': 'Удаление учебной группы',
        }
    )

@login_required
@user_passes_test(is_methodist)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление факультета',
        }
    )
@login_required
@user_passes_test(is_methodist)
def department_update(
    request,
    pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == 'POST':
        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():
            form.save()
            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение факультета',
        }
    )
@login_required
@user_passes_test(is_methodist)
def department_delete(
    request,
    pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == 'POST':
        department.delete()
        return redirect(
            'department_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': department,
            'title': 'Удаление факультета',
        }
    )

@login_required
def course_list(request):
    courses = Course.objects.select_related('department').all()

    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )

def is_methodist(user):
    return user.groups.filter(
        name='Методист'
    ).exists()

@login_required
@user_passes_test(is_methodist)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление курса',
        }
    )
@login_required
@user_passes_test(is_methodist)
def course_update(request, pk):
    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == 'POST':
        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():
            form.save()
            return redirect(
                'course_list'
            )
    else:
        form = CourseForm(
            instance=course
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение курса',
        }
    )
@login_required
@user_passes_test(is_methodist)
def course_delete(request, pk):
    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == 'POST':
        course.delete()
        return redirect(
            'course_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': course,
            'title': 'Удаление курса',
        }
    )
@login_required
def dashboard(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')

    courses = Course.objects.all()
    groups = AcademicGroup.objects.all()
    students = StudentProfile.objects.filter(department__isnull=False)

    if department_id:
        courses = courses.filter(department_id=department_id)
        groups = groups.filter(department_id=department_id)
        students = students.filter(department_id=department_id)

    departments_count = (
        departments.filter(id=department_id).count()
        if department_id
        else departments.count()
    )

    courses_count = courses.count()
    groups_count = groups.count()
    users_count = User.objects.count()

    courses_by_department = list(
        courses
        .values('department__name')
        .annotate(total=Count('id'))
    )

    groups_by_department = list(
        groups
        .values('department__name')
        .annotate(total=Count('id'))
    )

    students_by_department = list(
        students
        .values('department__name')
        .annotate(total=Count('id'))
    )

    students_by_group = list(
        students
        .filter(academic_group__isnull=False)
        .values('academic_group__name')
        .annotate(total=Count('id'))
    )

    return render(
        request,
        'dashboard.html',
        context={
            'departments_count': departments_count,
            'courses_count': courses_count,
            'groups_count': groups_count,
            'users_count': users_count,

            'courses_by_department': courses_by_department,
            'groups_by_department': groups_by_department,
            'students_by_department': students_by_department,
            'students_by_group': students_by_group,

            'departments': departments,
            'selected_department': department_id,
        }
    )

@login_required
def courses_dashboard(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')

    courses = Course.objects.all()

    if department_id:
        courses = courses.filter(department_id=department_id)

    students_by_course = list(
        courses
        .values('title')
        .annotate(total=Count('students'))
    )

    return render(
        request,
        'courses_dashboard.html',
        context={
            'students_by_course': students_by_course,
            'departments': departments,
            'selected_department': department_id,
        }
    )

@login_required
def groups_dashboard(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')

    groups = AcademicGroup.objects.all()
    students = StudentProfile.objects.filter(
        academic_group__isnull=False
    )

    if department_id:
        groups = groups.filter(department_id=department_id)
        students = students.filter(department_id=department_id)

    groups_by_department = list(
        groups
        .values('department__name')
        .annotate(total=Count('id'))
    )

    students_by_department = list(
        students
        .filter(department__isnull=False)
        .values('department__name')
        .annotate(total=Count('id'))
    )

    students_by_group = list(
        students
        .values('academic_group__name')
        .annotate(total=Count('id'))
    )

    return render(
        request,
        'groups_dashboard.html',
        context={
            'groups_by_department': groups_by_department,
            'students_by_department': students_by_department,
            'students_by_group': students_by_group,
            'departments': departments,
            'selected_department': department_id,
        }
    )

@login_required
def departments_dashboard(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')

    courses = Course.objects.all()
    students = StudentProfile.objects.filter(
        department__isnull=False
    )

    if department_id:
        courses = courses.filter(department_id=department_id)
        students = students.filter(department_id=department_id)

    students_by_department = list(
        students
        .values('department__name')
        .annotate(total=Count('id'))
    )

    courses_by_department = list(
        courses
        .values('department__name')
        .annotate(total=Count('id'))
    )

    return render(
        request,
        'departments_dashboard.html',
        context={
            'students_by_department': students_by_department,
            'courses_by_department': courses_by_department,
            'departments': departments,
            'selected_department': department_id,
        }
    )

@login_required
def summary_dashboard(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')

    courses = Course.objects.all()

    if department_id:
        courses = courses.filter(department_id=department_id)

    courses_by_department = list(
        courses
        .values('department__name')
        .annotate(total=Count('id'))
    )

    students_by_course = list(
        courses
        .values('title')
        .annotate(total=Count('students'))
    )

    return render(
        request,
        'summary_dashboard.html',
        context={
            'courses_by_department': courses_by_department,
            'students_by_course': students_by_course,
            'departments': departments,
            'selected_department': department_id,
        }
    )

from django.shortcuts import render
from .forms import *
from .models import *
from datetime import datetime
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
import secrets
from django.template import RequestContext
from .generate_docx import *
from docx import Document
import threading
import shutil
import os
import pandas as pd

portal_open_status = True

def application_to_form(application, id = 0):
    return ApplicationForm(initial={
                'phong_gddt': application.phong_gddt,
                'truong_tieu_hoc': application.truong_tieu_hoc,
                'lop': application.lop,
                'ho_va_ten': application.ho_va_ten,
                'gioi_tinh': application.gioi_tinh,
                'ngay_sinh': application.ngay_sinh,
                'noi_sinh': application.noi_sinh,
                'dan_toc': application.dan_toc,
                'noi_thuong_tru_so_nha': application.noi_thuong_tru_so_nha,
                'noi_thuong_tru_to': application.noi_thuong_tru_to,
                'noi_thuong_tru_phuong': application.noi_thuong_tru_phuong,
                'noi_thuong_tru_quan_huyen': application.noi_thuong_tru_quan_huyen,
                'noi_thuong_tru_tinh': application.noi_thuong_tru_tinh,
                'sdt': application.sdt,
                'ma_dinh_danh': application.ma_dinh_danh,
                'khen_thuong_1': application.khen_thuong_1,
                'khen_thuong_2': application.khen_thuong_2,
                'khen_thuong_3': application.khen_thuong_3,
                'khen_thuong_4': application.khen_thuong_4,
                'khen_thuong_5': application.khen_thuong_5,
                'ket_qua_1_toan': application.ket_qua_1_toan,
                'ket_qua_1_tieng_viet': application.ket_qua_1_tieng_viet,
                'ket_qua_2_toan': application.ket_qua_2_toan,
                'ket_qua_2_tieng_viet': application.ket_qua_2_tieng_viet,
                'ket_qua_3_toan': application.ket_qua_3_toan,
                'ket_qua_3_tieng_viet': application.ket_qua_3_tieng_viet,
                'ket_qua_3_tieng_anh': application.ket_qua_3_tieng_anh,
                'ket_qua_4_toan': application.ket_qua_4_toan,
                'ket_qua_4_tieng_viet': application.ket_qua_4_tieng_viet,
                'ket_qua_4_khoa_hoc': application.ket_qua_4_khoa_hoc,
                'ket_qua_4_su_dia': application.ket_qua_4_su_dia,
                'ket_qua_4_tieng_anh': application.ket_qua_4_tieng_anh,
                'ket_qua_5_toan': application.ket_qua_5_toan,
                'ket_qua_5_tieng_viet': application.ket_qua_5_tieng_viet,
                'ket_qua_5_su_dia': application.ket_qua_5_su_dia,
                'ket_qua_5_khoa_hoc': application.ket_qua_5_khoa_hoc,
                'ket_qua_5_tieng_anh': application.ket_qua_5_tieng_anh,
                'ma_hoc_sinh': application.ma_hoc_sinh,
                'ma_ho_so': application.ma_ho_so,
                'id': id
    })

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    if request.user.is_superuser:
        return HttpResponseRedirect("/manage")

    application = Application.objects.filter(user = request.user).first()

    if application:
        return HttpResponseRedirect("/application/" + str(application.id))

    return HttpResponseRedirect("/edit")

def manage_application(request):
    if not request.user.is_superuser:
        return handler404(request)

    search = request.GET['search'] if 'search' in request.GET else ''
    order_by = request.GET['sort_by'] if 'sort_by' in  request.GET and request.GET['sort_by'] else 'ma_ho_so'
    page = int(request.GET['page']) if 'page' in request.GET and request.GET['page'].isdigit() else 1

    search_by_id = Application.objects.none()
    search_by_name = Application.objects.none()
    if search != '':
        search_by_id = Application.objects.filter(ma_ho_so = search)
        search_by_name = Application.objects.filter(ho_va_ten__icontains=search)
    else:
        search_by_name = Application.objects.all()

    print("qwfwefweeqweqwe")
    print(order_by)
    if order_by not in ["ngay_nop", "-tong_diem", "-ngay_nop", "tong_diem", "ma_ho_so", "-ma_ho_so"]:
        return handler404(request)

    applications = (search_by_id | search_by_name).order_by(order_by)[(page - 1) * 100 : page * 100]

    return render(request, "manage.html", {
        'applications':applications,
        'form': SearchForm(request.GET),
        'pages': [p for p in range(max(1, page - 2), max(1, page - 2) + 5)],
        'selected_page': page,
        'prv_page': max(1, page - 1),
        'nxt_page': page + 1
    })

template_name = [
    "send_application.html",
    "send_application.html"
]

def _generate_docx(application):
        os.system(f"cp -rf ./template ./media/docx/{application.ma_ho_so}.docx")
        replacedict = {
            'ma_ho_so': application.ma_ho_so,
            'phong_gddt': application.phong_gddt,
            'truong_tieu_hoc': application.truong_tieu_hoc,
            'lop': application.lop,
            'ho_va_ten': application.ho_va_ten,
            'noi_sinh': application.noi_sinh,
            'dan_toc': application.dan_toc,
            'so_nha': application.noi_thuong_tru_so_nha,
            'tototo': application.noi_thuong_tru_to,
            'phuong': application.noi_thuong_tru_phuong,
            'quan_huyen': application.noi_thuong_tru_quan_huyen,
            'tinh': application.noi_thuong_tru_tinh,
            'sdt': application.sdt,
            'ma_hoc_sinh': application.ma_hoc_sinh,
            'ma_dinh_danh': application.ma_dinh_danh,
            'kt1': application.khen_thuong_1,
            'kt2': application.khen_thuong_2,
            'kt3': application.khen_thuong_3,
            'kt4': application.khen_thuong_4,
            'kt5': application.khen_thuong_5,
            '1to': str(application.ket_qua_1_toan),
            '1tv': str(application.ket_qua_1_tieng_viet),
            '2to': str(application.ket_qua_2_toan),
            '2tv': str(application.ket_qua_2_tieng_viet),
            '3to': str(application.ket_qua_3_toan),
            '3tv': str(application.ket_qua_3_tieng_viet),
            '3ta': str(application.ket_qua_3_tieng_anh),
            '4to': str(application.ket_qua_4_toan),
            '4tv': str(application.ket_qua_4_tieng_viet),
            '4kh': str(application.ket_qua_4_khoa_hoc),
            '4sd': str(application.ket_qua_4_su_dia),
            '4ta': str(application.ket_qua_4_tieng_anh),
            '5to': str(application.ket_qua_5_toan),
            '5tv': str(application.ket_qua_5_tieng_viet),
            '5sd': str(application.ket_qua_5_su_dia),
            '5kh': str(application.ket_qua_5_khoa_hoc),
            '5ta': str(application.ket_qua_5_tieng_anh),
            'tong_diem': str(application.tong_diem),
            'ma_hoc_sinh': application.ma_hoc_sinh,
            'td1': str(application.ket_qua_1_toan + application.ket_qua_1_tieng_viet),
            'td2': str(application.ket_qua_2_toan + application.ket_qua_2_tieng_viet),
            'td3': str(application.ket_qua_3_toan + application.ket_qua_3_tieng_viet + application.ket_qua_3_tieng_anh),
            'td4': str(application.ket_qua_4_toan + application.ket_qua_4_tieng_viet + application.ket_qua_4_tieng_anh + application.ket_qua_4_khoa_hoc + application.ket_qua_4_su_dia),
            'td5': str(application.ket_qua_5_toan + application.ket_qua_5_tieng_viet + application.ket_qua_5_tieng_anh + application.ket_qua_5_khoa_hoc + application.ket_qua_5_su_dia),
        }

        if application.gioi_tinh == "Nam":
            replacedict['g1'] = 'X'
            replacedict['g2'] = ''
        else:
            replacedict['g2'] = 'X'
            replacedict['g1'] = ''

        replacedict['mm'] = application.ngay_sinh.month
        replacedict['dd'] = application.ngay_sinh.day
        replacedict['yyyy'] = application.ngay_sinh.year

        replacedict['mmm'] = datetime.now().month
        replacedict['ddd'] = datetime.now().day

        generate(replacedict, f"./media/docx/{application.ma_ho_so}.docx")

def get_status(request, ma_ho_so):
    application = Application.objects.filter(ma_ho_so = ma_ho_so).first()
    if not application:
        return HttpResponse(False)
    _generate_docx(application)
    application.generated = True
    application.save()
    return HttpResponse(application.generated)

def view_application(request, id, status = 0):
    application = Application.objects.filter(ma_ho_so = id).first()

    if not application:
        return handler404(request)
    
    if not application.generated:
        return render(request, "load_application.html", {
            'application':application.ma_ho_so,
        }) 

    return render(request, "send_application.html", {
        'form': application_to_form(application),
        'user':request.user,
        'done': True,
        'id':id,
        'status': status,
        'application':application,
    }) 

def my_rate(group, request):
    if request.user.is_authenticated:
        return '1000/m'
    return '15/d'

class ApplicationView(View):
    tokens = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def random_id(self):
        return ''.join([secrets.choice(self.tokens) for i in range(4)])

    def get(self, request, id):
        if not request.user.is_superuser and not portal_open_status:
            return render(request, "portal_close.html")

        application = Application.objects.filter(ma_ho_so = id).first()
        if application and not request.user.is_superuser:
            return handler404(request)

        if len(id) == 10:
            if id.isdigit():
                application = Application()
                application.ma_hoc_sinh = id

        if not application:
            return handler404(request)

        return render(request, "send_application.html", {
            'form': application_to_form(application, id),
            'user': request.user,
            'done': False,
            'id': id,
            'application':application,
        })

    

    def post(self, request, id = ""):
        if not request.user.is_superuser and not portal_open_status:
            return HttpResponse(404)

        form = ApplicationForm(request.POST, request.FILES)

        application = Application.objects.filter(ma_ho_so = id).first()

        if application and not request.user.is_superuser:
            return handler404(request)

        if len(id) == 10:
            if id.isdigit():
                application = Application()

        if (not application):
            return handler404(request)

        if form.is_valid():
            form = form.cleaned_data
            
            application.phong_gddt = form['phong_gddt']
            application.truong_tieu_hoc = form['truong_tieu_hoc']
            application.lop = form['lop']
            application.ho_va_ten = form['ho_va_ten'].upper()
            application.gioi_tinh = form['gioi_tinh']
            application.ngay_sinh = form['ngay_sinh']
            application.noi_sinh = form['noi_sinh']
            application.dan_toc = form['dan_toc']
            application.noi_thuong_tru_so_nha = form['noi_thuong_tru_so_nha']
            application.noi_thuong_tru_to = form['noi_thuong_tru_to']
            application.noi_thuong_tru_phuong = form['noi_thuong_tru_phuong']
            application.noi_thuong_tru_quan_huyen = form['noi_thuong_tru_quan_huyen']
            application.noi_thuong_tru_tinh = form['noi_thuong_tru_tinh']
            application.sdt = form['sdt']
            application.ma_hoc_sinh = form['ma_hoc_sinh']
            application.ma_dinh_danh = form['ma_dinh_danh']
            application.khen_thuong_1 = form['khen_thuong_1']
            application.khen_thuong_2 = form['khen_thuong_2']
            application.khen_thuong_3 = form['khen_thuong_3']
            application.khen_thuong_4 = form['khen_thuong_4']
            application.khen_thuong_5 = form['khen_thuong_5']
            application.ket_qua_1_toan = form['ket_qua_1_toan']
            application.ket_qua_1_tieng_viet = form['ket_qua_1_tieng_viet']
            application.ket_qua_2_toan = form['ket_qua_2_toan']
            application.ket_qua_2_tieng_viet = form['ket_qua_2_tieng_viet']
            application.ket_qua_3_toan = form['ket_qua_3_toan']
            application.ket_qua_3_tieng_viet = form['ket_qua_3_tieng_viet']
            application.ket_qua_3_tieng_anh = form['ket_qua_3_tieng_anh']
            application.ket_qua_4_toan = form['ket_qua_4_toan']
            application.ket_qua_4_tieng_viet = form['ket_qua_4_tieng_viet']
            application.ket_qua_4_khoa_hoc = form['ket_qua_4_khoa_hoc']
            application.ket_qua_4_su_dia = form['ket_qua_4_su_dia']
            application.ket_qua_4_tieng_anh = form['ket_qua_4_tieng_anh']
            application.ket_qua_5_toan = form['ket_qua_5_toan']
            application.ket_qua_5_tieng_viet = form['ket_qua_5_tieng_viet']
            application.ket_qua_5_su_dia = form['ket_qua_5_su_dia']
            application.ket_qua_5_khoa_hoc = form['ket_qua_5_khoa_hoc']
            application.ket_qua_5_tieng_anh = form['ket_qua_5_tieng_anh']

            application.tong_diem = application.ket_qua_1_toan \
                                    +application.ket_qua_1_tieng_viet \
                                    +application.ket_qua_2_toan \
                                    +application.ket_qua_2_tieng_viet \
                                    +application.ket_qua_3_toan \
                                    +application.ket_qua_3_tieng_viet \
                                    +application.ket_qua_3_tieng_anh \
                                    +application.ket_qua_4_toan \
                                    +application.ket_qua_4_tieng_viet \
                                    +application.ket_qua_4_khoa_hoc \
                                    +application.ket_qua_4_su_dia \
                                    +application.ket_qua_4_tieng_anh \
                                    +application.ket_qua_5_toan \
                                    +application.ket_qua_5_tieng_viet \
                                    +application.ket_qua_5_su_dia \
                                    +application.ket_qua_5_khoa_hoc \
                                    +application.ket_qua_5_tieng_anh
            

            application.save()
            application.ma_ho_so = (str(application.pk).zfill(4) + '-' + self.random_id()) if len(id) == 10 else id
            application.save()

            if request.user.is_superuser:
                _generate_docx(application)

            return HttpResponseRedirect("/application/"+str(application.ma_ho_so)+"/1")

        return render(request, "send_application.html", {
            'form': form,
            'done':False,
            'id':id,
            'application':application,
        })

class StudentIDView(View):
    def get(self, request):
        if not request.user.is_superuser and not portal_open_status:
            return render(request, "portal_close.html")

        return render(request, 'student_id.html', {
            'form': StudentIDForm()
        })

    def post(self, request):
        form = StudentIDForm(request.POST)

        if form.is_valid():
            ma_hoc_sinh = form.cleaned_data['ma_hoc_sinh']

            return HttpResponseRedirect(f"/edit/{ma_hoc_sinh}")

        return render(request, 'student_id.html', {
            'form': form
        })

class SearchApplicationView(View):
    def get(self, request):
        return render(request, 'search.html', {
            'form': ApplicationSearchForm()
        })

    def post(self, request):
        form = ApplicationSearchForm(request.POST)
        if form.is_valid():
            ma_ho_so = form.cleaned_data['ma_ho_so']
            applications =  Application.objects.filter(ma_hoc_sinh = ma_ho_so) |  Application.objects.filter(ma_ho_so = ma_ho_so)
            return render(request, 'search.html', {
                'applications': applications
            })

        return render(request, 'search.html', {
            'form': form
        })

class PrintView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return handler404(request)
        return render(request, 'print_application.html', {})

    def post(self, request):
        print("123")
        if not request.user.is_superuser:
            return handler404(request)


        shutil.make_archive("./media/tatcahoso", 'zip', './media/docx')
        return HttpResponseRedirect("./media/tatcahoso.zip")

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response

def export_to_excel(request):
    # Retrieve data from your table
    table_data = Application.objects.all()  # Replace `YourTableModel` with your actual table model

    column_names = {
        'id': 'STT',
        'ma_ho_so': 'Mã hồ sơ',
        'phong_gddt': 'Phòng GDDT',
        'truong_tieu_hoc': 'Trường tiểu học',
        'lop': 'Lớp',
        'ho_va_ten': 'Họ và tên',
        'gioi_tinh': 'Giới tính',
        'ngay_sinh': 'Ngày tháng năm sinh',
        'noi_sinh': 'Nơi sinh',
        'dan_toc': 'Dân tộc',
        'noi_thuong_tru_so_nha': 'Số nhà (ngõ/ngách)',
        'noi_thuong_tru_to': 'Tổ (thôn/khu phố)',
        'noi_thuong_tru_phuong': 'Phường (xã/thị trấn)',
        'noi_thuong_tru_quan_huyen': 'Quận (huyện)',
        'noi_thuong_tru_tinh': 'Tỉnh (TP)',
        'sdt': 'Số điện thoại',
        'ma_hoc_sinh': 'Mã học sinh',
        'ma_dinh_danh': 'Mã định danh',
        'khen_thuong_1': 'Danh hiệu lớp 1',
        'khen_thuong_2': 'Danh hiệu lớp 2',
        'khen_thuong_3': 'Danh hiệu lớp 3',
        'khen_thuong_4': 'Danh hiệu lớp 4',
        'khen_thuong_5': 'Danh hiệu lớp 5',
        'ket_qua_1_toan': 'Toán Lớp 1',
        'ket_qua_1_tieng_viet': 'Tiếng Việt Lớp 1',
        'ket_qua_2_toan': 'Toán Lớp 2',
        'ket_qua_2_tieng_viet': 'Tiếng Việt Lớp 2',
        'ket_qua_3_toan': 'Toán Lớp 3',
        'ket_qua_3_tieng_viet': 'Tiếng Việt Lớp 3',
        'ket_qua_3_tieng_anh': 'Tiếng Anh Lớp 3',
        'ket_qua_4_toan': 'Toán Lớp 4',
        'ket_qua_4_tieng_viet': 'Tiếng Việt Lớp 4',
        'ket_qua_4_khoa_hoc': 'Khoa học Lớp 4',
        'ket_qua_4_su_dia': 'Lịch sử và Địa lí Lớp 4',
        'ket_qua_4_tieng_anh': 'Tiếng Anh Lớp 4',
        'ket_qua_5_toan': 'Toán Lớp 5',
        'ket_qua_5_tieng_viet': 'Tiếng Việt Lớp 5',
        'ket_qua_5_khoa_hoc': 'Khoa học Lớp 5',
        'ket_qua_5_su_dia': 'Lịch sử và Địa lí Lớp 5',
        'ket_qua_5_tieng_anh': 'Tiếng Anh Lớp 5',
        'tong_diem': 'Tổng điểm'
    }

    # Create a pandas DataFrame from the table data
    table_data = Application.objects.all()  # Replace `YourTableModel` with your actual table model

    # Create a pandas DataFrame from the table data
    df = pd.DataFrame(list(table_data.values()))  # Convert queryset to a list of dictionaries

    # Rename the DataFrame columns based on the column names mapping
    df = df.rename(columns=column_names)

    # Create a response object with the appropriate content type for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to the response as an Excel file
    df.to_excel(response, index=False)

    return response

def toggle_portal_status(request):
    global portal_open_status
    if not request.user.is_superuser:
        return handler404(request)
    
    portal_open_status = not portal_open_status

    return HttpResponse(200)
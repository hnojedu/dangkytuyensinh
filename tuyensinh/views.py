from django.shortcuts import render
from .forms import *
from .models import *
from datetime import datetime
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
import secrets
from django.template import RequestContext
from .generate_docx import *
from docxcompose.composer import Composer
from docx import Document
import shutil

import os

def application_to_form(application, id = 0):
    return ApplicationForm(initial={
                'anh_3x4': application.anh_3x4,
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
    order_by = request.GET['sort_by'] if 'sort_by' in  request.GET and request.GET['sort_by'] else 'ngay_nop'
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
    if order_by not in ["ngay_nop", "-tong_diem", "-ngay_nop", "tong_diem"]:
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

def view_application(request, id, status = 0):
    application = Application.objects.filter(ma_ho_so = id).first()

    if not application:
        return handler404(request)

    return render(request, template_name[request.user.is_superuser], {
        'form': application_to_form(application),
        'user':request.user,
        'done': True,
        'id':id,
        'status': status,
        'application':application
    }) 

class ApplicationView(View):
    tokens = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def random_id(self):
        result = None
        while not result and Application.objects.filter(ma_ho_so = result).exists():
            result = ''.join([secrets.choice(self.tokens) for i in range(8)])

        return result

    def get(self, request, id):
        print(id)
        if len(id) != 8 and len(id) != 10:
            return handler404(request)

        application = Application.objects.filter(ma_ho_so = id).first()

        if len(id) == 10:
            if not id.isdigit():
                return handler404(request)
            application = Application()
            application.ma_hoc_sinh = id
            print(application.ma_hoc_sinh)

        if not application:
            return handler404(request)

        return render(request, template_name[request.user.is_superuser], {
            'form': application_to_form(application, id),
            'user': request.user,
            'done': False,
            'id': id,
            'application':application,
        })

    def _generate_docx(self, ma_ho_so, application):
        os.system(f"cp -rf ./media/docx/template ./media/docx/{ma_ho_so}.docx")
        replacedict = {
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

        generate(replacedict, f"./media/docx/{ma_ho_so}.docx")

    def post(self, request, id = ""):
        form = ApplicationForm(request.POST, request.FILES)

        if len(id) != 8 and len(id) != 10:
            return handler404(request)

        application = Application.objects.filter(ma_ho_so = id).first()

        if len(id) == 10:
            if not id.isdigit():
                return handler404(request)
            application = Application()

        if (len(id) == 8 and not request.user.is_superuser) or (not application):
            return handler404(request)

        if form.is_valid():
            form = form.cleaned_data

            image = form['anh_3x4']
            if image:
                image._name = secrets.token_urlsafe(8) + "." + image.name.split('.')[-1]
                application.anh_3x4 = image

            application.ma_ho_so = self.random_id() if len(id) == 10 else id
            application.phong_gddt = form['phong_gddt']
            application.truong_tieu_hoc = form['truong_tieu_hoc']
            application.lop = form['lop']
            application.ho_va_ten = form['ho_va_ten']
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

            self._generate_docx(application.ma_ho_so, application)
            application.save()

            return HttpResponseRedirect("/application/"+str(application.ma_ho_so)+"/1")

        return render(request, "send_application.html", {
            'form': form,
            'done':False,
            'id':id,
            'application':application,
        })

class StudentIDView(View):
    def get(self, request):
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

            return HttpResponseRedirect(f"/application/{ma_ho_so}")

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
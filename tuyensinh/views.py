from django.shortcuts import render
from .forms import *
from .models import *
from datetime import datetime
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
import pandas
from django.template import RequestContext
import secrets

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

def manage_application(request, page = 1):
    if not request.user.is_superuser:
        return handler404(request)

    search = request.GET['search'] if 'search' in request.GET else ''
    order_by = request.GET['sort_by'] if 'sort_by' in  request.GET else 'ngay_nop'

    search_by_id = Application.objects.none()
    search_by_name = Application.objects.none()

    if search != '':
        if search.isdigit():
            search_by_id = Application.objects.filter(id = int(search))
        else:
            search_by_name = Application.objects.filter(ho_va_ten__icontains=search)
    else:
        search_by_name = Application.objects.all()

    if order_by not in ["ngay_nop", "-tong_diem"]:
        return handler404(request)

    applications = (search_by_id | search_by_name).order_by(order_by)[(page - 1) * 100 : 100]

    return render(request, "manage.html", {
        'applications':applications,
        'form': SearchForm(request.GET),
    })

template_name = [
    "send_application.html",
    "send_application_admin.html"
]

def view_application(request, id):
    application = Application.objects.filter(id = id).first()
    if not application:
        print(404)
        return handler404(request)

    if not request.user.is_superuser and application.user != request.user:
        return handler404(request)

    print('weqwe')

    return render(request, template_name[request.user.is_superuser], {
        'form': application_to_form(application),
        'user':request.user,
        'done': True,
        'id':id,
        'application':application
    }) 

class ApplicationView(View):
    template_name = [
        "send_application.html",
        "send_application_admin.html"
    ]
        
    def is_available(self, request, id):
        if not id:
            return Application(user=request.user)

        application = Application.objects.filter(id = id).first()

        if not request.user.is_authenticated:
            return None

        if not application:
            return None

        if application.user != request.user and not request.user.is_superuser:
            return None

        return application


    def get(self, request, id = 0):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("login")

        if not id and request.user.is_superuser:
            return handler404(request)

        application = self.is_available(request, id)

        if not application:
            return handler404(request)

        print(template_name[request.user.is_superuser])
        print("herer")
        return render(request, template_name[request.user.is_superuser], {
            'form': application_to_form(application, id),
            'user': request.user,
            'done': False,
            'id': id,
            'application':application,
        })

    def post(self, request, id = 0):
        form = ApplicationForm(request.POST, request.FILES)

        application = self.is_available(request, id)

        print(application)

        if not application:
            return handler404(request)

        if form.is_valid():
            form = form.cleaned_data

            form_id = form['id']
            if form_id != id:
                return handler404(request)
            
            #???
            try:
                application.user
            except:
                application.user = request.user

            image = form['anh_3x4']
            if image:
                image._name = secrets.token_urlsafe(8) + "." + image.name.split('.')[-1]
                application.anh_3x4 = image
            
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

            return HttpResponseRedirect("/application/"+str(application.id))

        return render(request, template_name[request.user.is_superuser], {
            'form': form,
            'done':False,
            'user':request.user,
            'id':id,
            'application':application,
        })


class UploadUserView(View):
    def get(self, request):
        return render(request, 'upload.html', {
            'form': FileForm()
        })

    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = request.FILES['user']
            fs = FileSystemStorage(location='')
            filename = fs.save(user.name, user)
            user_excel = pandas.read_excel(user.name, sheet_name=0)
            
            username = user_excel['Username'].tolist()
            password = user_excel['Password'].tolist()

            for i in range(0, len(username)):
                User.objects.create_user(username = username[i], password = password[i])

        return render(request, 'upload.html', {
            'form': FileForm()
        })

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response
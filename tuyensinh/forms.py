from django import forms
from django.contrib.auth.forms import User
from django.contrib.postgres.forms import SimpleArrayField
from django.conf import settings
from .models import Application

def file_size(value): # add this to some file where you can import it from
    limit = 1024 * 1024
    if value.size > limit:
        raise forms.ValidationError('Ảnh không được vượt quá 1 Megabyte.')

class DateInput(forms.DateInput):
    input_type = 'date'

class ApplicationForm(forms.Form):
    class Meta:
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }

    KHEN_THUONG = (
        ("K", "K"),
        ("HTT", "HTT"),
        ("HTXS", "HTXS"),
    )
    GIOI_TINH = (
        ("Nam", "Nam"),
        ("Nữ", "Nữ"),
    )

    phong_gddt = forms.CharField(max_length = 255)
    truong_tieu_hoc = forms.CharField(max_length = 255)
    lop = forms.CharField(max_length = 255)
    ho_va_ten = forms.CharField(max_length = 255)
    gioi_tinh = forms.CharField(widget=forms.Select(choices=GIOI_TINH), max_length = 3)
    ngay_sinh = forms.DateTimeField(widget=DateInput(format=('%Y-%m-%d'),attrs={'type': 'date'}),input_formats=['%d-%m-%Y'],required=True)
    noi_sinh = forms.CharField(max_length = 255)
    dan_toc = forms.CharField(max_length = 255)

    noi_thuong_tru_so_nha = forms.CharField(max_length = 255)
    noi_thuong_tru_to = forms.CharField(max_length = 255)
    noi_thuong_tru_phuong = forms.CharField(max_length = 255)
    noi_thuong_tru_quan_huyen = forms.CharField(max_length = 255)
    noi_thuong_tru_tinh = forms.CharField(max_length = 255)

    sdt = forms.CharField(max_length = 20)
    ma_dinh_danh = forms.CharField(max_length = 12)
    ma_hoc_sinh = forms.CharField(max_length = 10, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    ma_ho_so = forms.CharField(required=False)

    khen_thuong_1 = forms.CharField(widget=forms.Select(choices=KHEN_THUONG))
    khen_thuong_2 = forms.CharField(widget=forms.Select(choices=KHEN_THUONG))
    khen_thuong_3 = forms.CharField(widget=forms.Select(choices=KHEN_THUONG))
    khen_thuong_4 = forms.CharField(widget=forms.Select(choices=KHEN_THUONG))
    khen_thuong_5 = forms.CharField(widget=forms.Select(choices=KHEN_THUONG))
    
    ket_qua_1_toan = forms.FloatField()
    ket_qua_1_tieng_viet = forms.FloatField()
    
    ket_qua_2_toan = forms.FloatField()
    ket_qua_2_tieng_viet = forms.FloatField()

    ket_qua_3_toan = forms.FloatField()
    ket_qua_3_tieng_viet = forms.FloatField()
    ket_qua_3_tieng_anh = forms.FloatField()

    ket_qua_4_toan = forms.FloatField()
    ket_qua_4_tieng_viet = forms.FloatField()
    ket_qua_4_khoa_hoc = forms.FloatField()
    ket_qua_4_su_dia= forms.FloatField()
    ket_qua_4_tieng_anh = forms.FloatField()

    ket_qua_5_toan = forms.FloatField()
    ket_qua_5_tieng_viet = forms.FloatField()
    ket_qua_5_su_dia    = forms.FloatField()
    ket_qua_5_khoa_hoc = forms.FloatField()
   
    ket_qua_5_tieng_anh = forms.FloatField()
    
    anh_3x4 = forms.ImageField(required = False,widget=forms.FileInput(attrs=({'onchange':'loadFile(event)'})))

    def clean_sdt(self):
        sdt = self.cleaned_data['sdt']

        if len(sdt) < 10 or len(sdt) > 11:
            raise forms.ValidationError("Số điện thoại không hợp lệ.")

        if sdt[0] != '0':
            raise forms.ValidationError("Số điện thoại không hợp lệ.")

        return sdt

    def clean_ma_hoc_sinh(self):
        ma_hoc_sinh = self.cleaned_data['ma_hoc_sinh']

        if len(ma_hoc_sinh) != 10 or not ma_hoc_sinh.isdigit():
            raise forms.ValidationError("Mã học sinh không hợp lệ.")
        
        return ma_hoc_sinh

    def clean_ma_dinh_danh(self):
        ma_dinh_danh = self.cleaned_data['ma_dinh_danh']

        if len(ma_dinh_danh) != 12:
            raise forms.ValidationError("Mã định danh không hợp lệ.")

        return ma_dinh_danh

    def valid_score(self, s):
        return 0 <= s <= 10

    def clean(self):
        cleaned_data = super().clean()

        ket_qua_1_toan = cleaned_data.get('ket_qua_1_toan')
        ket_qua_1_tieng_viet = cleaned_data.get('ket_qua_1_tieng_viet')
        ket_qua_2_toan = cleaned_data.get('ket_qua_2_toan')
        ket_qua_2_tieng_viet = cleaned_data.get('ket_qua_2_tieng_viet')
        ket_qua_3_toan = cleaned_data.get('ket_qua_3_toan')
        ket_qua_3_tieng_viet = cleaned_data.get('ket_qua_3_tieng_viet')
        ket_qua_3_tieng_anh = cleaned_data.get('ket_qua_3_tieng_anh')
        ket_qua_4_toan = cleaned_data.get('ket_qua_4_toan')
        ket_qua_4_tieng_viet = cleaned_data.get('ket_qua_4_tieng_viet')
        ket_qua_4_khoa_hoc = cleaned_data.get('ket_qua_4_khoa_hoc')
        ket_qua_4_su_dia = cleaned_data.get('ket_qua_4_su_dia')
        ket_qua_4_tieng_anh = cleaned_data.get('ket_qua_4_tieng_anh')
        ket_qua_5_toan = cleaned_data.get('ket_qua_5_toan')
        ket_qua_5_tieng_viet = cleaned_data.get('ket_qua_5_tieng_viet')
        ket_qua_5_su_dia = cleaned_data.get('ket_qua_5_su_dia')
        ket_qua_5_khoa_hoc = cleaned_data.get('ket_qua_5_khoa_hoc')
        ket_qua_5_tieng_anh = cleaned_data.get('ket_qua_5_tieng_anh')

        anh_3x4 = cleaned_data.get('anh_3x4')
        ma_ho_so = cleaned_data.get('ma_ho_so')

        if not anh_3x4 and not Application.objects.filter(ma_ho_so = ma_ho_so).exists():
            raise forms.ValidationError("Bạn chưa tải ảnh lên.")
        

        if not (self.valid_score(ket_qua_1_toan) \
            and self.valid_score(ket_qua_1_tieng_viet) \
            and self.valid_score(ket_qua_2_toan) \
            and self.valid_score(ket_qua_2_tieng_viet) \
            and self.valid_score(ket_qua_3_toan) \
            and self.valid_score(ket_qua_3_tieng_viet) \
            and self.valid_score(ket_qua_3_tieng_anh) \
            and self.valid_score(ket_qua_4_toan) \
            and self.valid_score(ket_qua_4_tieng_viet) \
            and self.valid_score(ket_qua_4_khoa_hoc) \
            and self.valid_score(ket_qua_4_su_dia) \
            and self.valid_score(ket_qua_4_tieng_anh) \
            and self.valid_score(ket_qua_5_toan) \
            and self.valid_score(ket_qua_5_tieng_viet) \
            and self.valid_score(ket_qua_5_su_dia) \
            and self.valid_score(ket_qua_5_khoa_hoc) \
            and self.valid_score(ket_qua_5_tieng_anh)):
            raise forms.ValidationError("Điểm phải nằm trong khoảng 0.0 đến 10.0.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'block w-full text-gray-900 border rounded sm:text-xs focus:ring-blue-500 focus:border-blue-500 light:bg-gray-700 light:border-gray-600 light:placeholder-gray-400 light:text-white light:focus:ring-blue-500 light:focus:border-blue-500'
            visible.field.widget.attrs['placeholder'] = " "
            #visible.field.widget.attrs['class'] = "cleanslate"
class SearchForm(forms.Form):
    SAP_XEP = (
        ("ngay_nop", "Ngày nộp"),
        ("-tong_diem", "Tổng điểm"),
    )
    

    search = forms.CharField(label='Tìm kiếm', max_length = 64, required = False,widget=forms.TextInput(attrs={
        'class': 'block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 light:bg-gray-700 light:border-gray-600 light:placeholder-gray-400 light:text-white light:focus:ring-blue-500 light:focus:border-blue-500',
        'placeholder': 'Tìm theo tên hoặc mã hồ sơ'
    }))
    sort_by = forms.CharField(label='Sắp xếp', required=False)
    page = forms.CharField(required=False)

class FileForm(forms.Form):
    user = forms.FileField(
        label='Select a file',
    )

class StudentIDForm(forms.Form):
    ma_hoc_sinh = forms.CharField(max_length = 10)

    def clean_ma_hoc_sinh(self):
        ma_hoc_sinh = self.cleaned_data['ma_hoc_sinh']
        if len(ma_hoc_sinh) != 10 or not ma_hoc_sinh.isdigit():
            raise forms.ValidationError("Mã học sinh không hợp lệ.")
        
        return ma_hoc_sinh

class ApplicationSearchForm(forms.Form):
    ma_ho_so = forms.CharField(max_length = 10)

    def clean_ma_ho_so(self):
        ma_ho_so = self.cleaned_data['ma_ho_so']
        print(ma_ho_so)
        if not Application.objects.filter(ma_ho_so = ma_ho_so).exists():
            raise forms.ValidationError("Mã hồ sơ không tồn tại.")
        
        return ma_ho_so
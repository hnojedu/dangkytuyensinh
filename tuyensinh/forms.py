from django import forms
from django.contrib.auth.forms import User
from django.contrib.postgres.forms import SimpleArrayField
from django.conf import settings

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
    id = forms.IntegerField(widget=forms.HiddenInput())

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
    

    def clean_sdt(self):
        sdt = self.cleaned_data['sdt']

        if len(sdt) < 10 or len(sdt) > 11:
            raise forms.ValidationError("Số điện thoại không hợp lệ.")

        if sdt[0] != '0':
            raise forms.ValidationError("Số điện thoại không hợp lệ.")

        return sdt

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

class SearchForm(forms.Form):
    SAP_XEP = (
        ("ngay_nop", "Ngày nộp"),
        ("-tong_diem", "Tổng điểm"),
    )

    search = forms.CharField(label='Tìm kiếm', max_length = 64, required = False)
    sort_by = forms.CharField(label='Sắp xếp', widget=forms.Select(choices=SAP_XEP))

class FileForm(forms.Form):
    user = forms.FileField(
        label='Select a file',
    )

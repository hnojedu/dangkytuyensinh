from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Application(models.Model):
    KHEN_THUONG = (
        ("K", "Không"),
        ("HTT", "Hoàn thành tốt"),
        ("HTXS", "Hoàn thành xuất sắc"),
    )

    GIOI_TINH = (
        ("Nam", "Nam"),
        ("Nữ", "Nữ")
    )
    
    class Meta:
        indexes = [
            models.Index(fields = ['ma_ho_so'])
        ]

    ma_ho_so = models.CharField(null = True)

    # Thong tin ca nhan
    id = models.AutoField(primary_key = True)

    phong_gddt = models.CharField(max_length = 255)
    truong_tieu_hoc = models.CharField(max_length = 255)
    lop = models.CharField(max_length = 255)
    ho_va_ten = models.CharField(max_length = 255)
    gioi_tinh = models.CharField(choices = GIOI_TINH, max_length = 3)

    ngay_sinh = models.DateField(auto_now = False)
    noi_sinh = models.CharField(max_length = 255)
    dan_toc = models.CharField(max_length = 255)

    noi_thuong_tru_so_nha = models.CharField(max_length = 255)
    noi_thuong_tru_to = models.CharField(max_length = 255)
    noi_thuong_tru_phuong = models.CharField(max_length = 255)
    noi_thuong_tru_quan_huyen = models.CharField(max_length = 255)
    noi_thuong_tru_tinh = models.CharField(max_length = 255)

    sdt = models.CharField(max_length = 20)

    ma_dinh_danh = models.CharField(max_length = 12)
    ma_hoc_sinh = models.CharField(max_length = 10,null=True)

    # Thong tin so tuyen

    
    khen_thuong_1 = models.CharField(max_length = 4,null=True)
    khen_thuong_2 = models.CharField(max_length = 4,null=True)
    khen_thuong_3 = models.CharField(max_length = 4,null=True)
    khen_thuong_4 = models.CharField(max_length = 4,null=True)
    khen_thuong_5 = models.CharField(max_length = 4,null=True)
    
    ket_qua_1_toan = models.FloatField(null = True)
    ket_qua_1_tieng_viet = models.FloatField(null=True)
    
    ket_qua_2_toan = models.FloatField(null=True)
    ket_qua_2_tieng_viet = models.FloatField(null=True)

    ket_qua_3_toan = models.FloatField(null=True)
    ket_qua_3_tieng_viet = models.FloatField(null=True)
    ket_qua_3_tieng_anh = models.FloatField(null=True)

    ket_qua_4_toan = models.FloatField(null=True)
    ket_qua_4_tieng_viet = models.FloatField(null=True)
    ket_qua_4_khoa_hoc = models.FloatField(null=True)
    ket_qua_4_su_dia= models.FloatField(null=True)
    ket_qua_4_tieng_anh = models.FloatField(null=True)

    ket_qua_5_toan = models.FloatField(null=True)
    ket_qua_5_tieng_viet = models.FloatField(null=True)
    ket_qua_5_su_dia    = models.FloatField(null=True)
    ket_qua_5_khoa_hoc = models.FloatField(null=True)
   
    ket_qua_5_tieng_anh = models.FloatField(null=True)

    tong_diem = models.FloatField(null = True)

    ngay_nop = models.DateField(auto_now_add = True, null = True)
    anh_3x4 = models.ImageField(upload_to="anh_3x4",null=True)
# from django.contrib import admin

# from crop_home.models import Recomendation, Production

# @admin.register(Recomendation)
# class PersonAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Production)
# class CourseAdmin(admin.ModelAdmin):
#     pass


from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Production
from .models import Recomendation
from django import forms
from .models import Production
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('Division_Name','District_Name','Crop_Year','Season','Crop','Area','Production')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        print('[INFO] Uploading CSV file')
        if request.method == "POST":
            print('[INFO] Uploading CSV file IF condition')
            csv_file = request.FILES["csv_upload"]
            print(f'[INFO] csv file got')
            if not csv_file.name.endswith('.csv'):
                print('[INFO] Uploading file is not a CSV file')
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            print(f'[INFO] after spliting csv_data ')
            Production.objects.all().delete()
            print(f'[INFO] after deleting all data')
            print(f'[INFO] Start Inserting New Data')
            for x in csv_data:
                fields = x.split(",")
                if fields[0] != '' and fields[1] != '' and fields[2] != '' and fields[3] != '' and fields[4] != '' and fields[5] != '' and fields[6] != '':
                    if fields[0] == '':
                        fields[0] = 'Dhaka'
                    if fields[1] == '':
                        fields[1] = 'Dhaka'
                    if fields[2] == '':
                        fields[2] = '2012'
                    if fields[3] == '':
                        fields[3] = 'Rabi'
                    if fields[4] == '':
                        fields[4] = 'Rice'
                    if fields[5] == '':
                        fields[5] = '100'
                    if fields[6] == '':
                        fields[6] = '100'
                    created = Production.objects.update_or_create(
                        Division_Name = fields[0],
                        District_Name = fields[1],
                        Crop_Year = fields[2],
                        Season = fields[3],
                        Crop = fields[4],
                        Area = fields[5],
                        Production = fields[6]
                        )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        print(f'[INFO] Successfully Inserted New Data of Production')
        return render(request, "admin/csv_upload.html", data)

admin.site.register(Production, ProductionAdmin)


class RecomendationAdmin(admin.ModelAdmin):
    list_display = ('N','P','K','temperature','humidity','ph','rainfall','label')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        print('[INFO] Uploading CSV file')
        if request.method == "POST":
            print('[INFO] Uploading CSV file IF condition')
            csv_file = request.FILES["csv_upload"]
            print(f'[INFO] csv file got')
            if not csv_file.name.endswith('.csv'):
                print('[INFO] Uploading file is not a CSV file')
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            print(f'[INFO] after spliting csv_data ')
            Recomendation.objects.all().delete()
            print(f'[INFO] after deleting all data')
            print(f'[INFO] Start Inserting New Data')
            for x in csv_data:
                fields = x.split(",")
                if fields[0] != '' and fields[1] != '' and fields[2] != '' and fields[3] != '' and fields[4] != '' and fields[5] != '' and fields[6] != '' and fields[7] != '':
                    if fields[0] == '':
                        fields[0] = '70'
                    if fields[1] == '':
                        fields[1] = '45'
                    if fields[2] == '':
                        fields[2] = '38'
                    if fields[3] == '':
                        fields[3] = '74.36794079'
                    if fields[4] == '':
                        fields[4] = '6.334610249'
                    if fields[5] == '':
                        fields[5] = '166.2549307'
                    if fields[6] == '':
                        fields[6] = 'B.Aman'
                    created = Recomendation.objects.update_or_create(
                        N = fields[0],
                        P = fields[1],
                        K = fields[2],
                        temperature = fields[3],
                        humidity = fields[4],
                        ph = fields[5],
                        rainfall = fields[6],
                        label = fields[7]
                        )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        print(f'[INFO] Successfully Inserted New Data of Recomendation')
        return render(request, "admin/csv_upload.html", data)

admin.site.register(Recomendation, RecomendationAdmin)


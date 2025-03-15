import json
from django.http import JsonResponse
from django.shortcuts import render
import snp_manager
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'index.html')

def graph(request):
    if request.method == "POST" and request.FILES.getlist("files"):
        files = request.FILES.getlist("files")
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        paths = []
        for file_instance in files:
            file_name = fs.save(file_instance.name, file_instance)
            paths.append([fs.path(file_name)])
        data = snp_manager.filegroup(snp_manager.parsepaths(paths))
        snp_data = {}
        context = {}
        for snp_instance in data.snps:
            snp_json = {}
            for attr in list(snp_instance.__dict__.keys()):
                snp_json[attr] = str(getattr(snp_instance, attr))
            snp_data[getattr(snp_instance, "rsid")] = snp_json
        context["snp_data"] = snp_data
        context["headings"] = data.atts
        fs.delete(file_name)
        return render(request, "graph.html", context)
    elif request.method == "POST" and request.FILES.get("file"):
        # temporarily save the file
        file = request.FILES["file"]
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        file_name = fs.save(file.name, file)
        data = snp_manager.filegroup(snp_manager.parsepaths([fs.path(file_name)]))
        snp_data = {}
        context = {}
        for snp_instance in data.snps:
            snp_json = {}
            for attr in list(snp_instance.__dict__.keys()):
                snp_json[attr] = str(getattr(snp_instance, attr))
            snp_data[getattr(snp_instance, "rsid")] = snp_json
        context["snp_data"] = snp_data
        context["headings"] = data.atts
        fs.delete(file_name)
        return render(request, "graph.html", context)
    else:
        return render(request, "index.html")
